"""Offline copy fixture and meaningful integrity failures."""
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import subprocess
import sys
import unittest
from unittest import mock

from scripts.check_template import CHANNELS, LIMIT, check

ROOT = Path(__file__).resolve().parents[1]


def copy_template(destination):
    for name in ('README.md', 'AGENTS.md', 'AGENTS.local.md', 'docs', '.github',
                 '.project-template', '.engineering-kit', 'scripts', 'tests',
                 '.editorconfig', '.gitignore', 'LICENSE'):
        source = ROOT / name
        target = destination / name
        if source.is_dir():
            shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__'))
        else:
            shutil.copy2(source, target)


class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        copy_template(self.root)

    def test_new_project_and_local_rules(self):
        self.assertEqual(check(self.root), [])
        (self.root / 'AGENTS.local.md').write_text('Native gates: strict local test\n')
        (self.root / 'docs/ARCHITECTURE.md').write_text('Chosen native design\n')
        self.assertEqual(check(self.root), [])

    def test_creation_retains_license_outside_managed_channels(self):
        self.assertEqual((self.root / 'LICENSE').read_bytes(), (ROOT / 'LICENSE').read_bytes())
        from scripts.check_template import ADMIN_FILES, KIT_FILES
        self.assertNotIn('LICENSE', ADMIN_FILES | KIT_FILES)
        (self.root / 'LICENSE').unlink()
        self.assertTrue(any('broken link LICENSE' in error for error in check(self.root)))

    def test_drift_missing_link_and_symlink(self):
        (self.root / 'AGENTS.md').write_text('modified')
        self.assertIn('managed drift: AGENTS.md', check(self.root))
        (self.root / 'docs/INDEX.md').write_text('[missing](absent.md)\n')
        self.assertTrue(any('broken link' in p for p in check(self.root)))
        (self.root / 'AGENTS.md').unlink()
        (self.root / 'AGENTS.md').symlink_to(self.root / 'README.md')
        self.assertTrue(any('unsafe managed path' in p for p in check(self.root)))


    @contextmanager
    def changed(self, name, data):
        path = self.root / name
        before = path.read_bytes()
        path.write_bytes(data)
        try:
            yield
        finally:
            path.write_bytes(before)

    def assert_rejected(self, name, value):
        with self.changed(name, json.dumps(value).encode()):
            self.assertTrue(check(self.root), name)

    def test_lock_schema_fields_types_and_paths(self):
        for lock_name, _, channel in CHANNELS:
            valid = json.loads((self.root / lock_name).read_text())
            mutations = [None, [], {}, {**valid, 'unexpected': True}]
            for key in valid:
                mutations.append({k: v for k, v in valid.items() if k != key})
            for key, values in (
                ('format', [True, '1', 0, 3]),
                ('upstream', [None, [], 'main', 'a' * 39, 'A' * 40]),
                ('profile', [None, [], 'unknown', 'minimal' if channel == 'admin' else 'administrative']),
                ('files', [None, [], {}, {'../outside': 'a' * 64}]),
            ):
                mutations.extend({**valid, key: value} for value in values)
            if channel == 'admin':
                mutations += [{**valid, 'owner': 'untrusted/other'},
                              {**valid, 'publication': 'public'}]
            else:
                mutations += [{**valid, 'owner': 'untrusted/other'},
                              {**valid, 'publication': 'public'}]
            for name in ('../AGENTS.md', '/AGENTS.md', 'docs/../AGENTS.md',
                         'AGENTS.local.md', '.github/workflows/native.yml'):
                mutations.append({**valid, 'files': {**valid['files'], name: 'a' * 64}})
            first = next(iter(valid['files']))
            for value in (None, [], 'z' * 64, 'a' * 63):
                mutations.append({**valid, 'files': {**valid['files'], first: value}})
            for index, value in enumerate(mutations):
                with self.subTest(channel=channel, mutation=index):
                    self.assert_rejected(lock_name, value)

    def test_bundle_structure_content_hashes_and_divergence(self):
        for _, bundle_name, channel in CHANNELS:
            valid = json.loads((self.root / bundle_name).read_text())
            first = next(iter(valid['contents']))
            mutations = [None, [], {}, {**valid, 'extra': True},
                         {**valid, 'contents': []}, {**valid, 'contents': {}},
                         {**valid, 'manifest': None}]
            for value in (None, [], 'CORRUPTED', chr(0xd800)):
                mutations.append({**valid, 'contents': {**valid['contents'], first: value}})
            mutations += [
                {**valid, 'contents': {**valid['contents'], '../outside': 'bad'}},
                {**valid, 'manifest': {**valid['manifest'], 'upstream': 'b' * 40}},
                {**valid, 'manifest': {**valid['manifest'], 'format': True}},
                {**valid, 'manifest': {**valid['manifest'], 'files': {
                    **valid['manifest']['files'], first: 'a' * 64}}},
            ]
            if channel == 'admin':
                mutations += [{**valid, 'manifest': {**valid['manifest'], 'owner': 'other'}},
                              {**valid, 'manifest': {**valid['manifest'], 'publication': 'public'}}]
            # A self-consistent retained artifact still must match the installed lock.
            divergent = json.loads(json.dumps(valid))
            divergent['contents'][first] += 'changed'
            divergent['manifest']['files'][first] = hashlib.sha256(
                divergent['contents'][first].encode()).hexdigest()
            mutations.append(divergent)
            for index, value in enumerate(mutations):
                with self.subTest(channel=channel, mutation=index):
                    self.assert_rejected(bundle_name, value)
            for bad in (b'CORRUPTED', b'{', b'\xff'):
                with self.subTest(channel=channel, raw=bad):
                    with self.changed(bundle_name, bad):
                        self.assertTrue(check(self.root))

    def test_kit_pin_and_tooling_publication(self):
        name = '.project-template/tooling.json'
        valid = json.loads((self.root / name).read_text())
        for key, value in (('kit_baseline', 'c' * 40), ('publication', 'public'),
                           ('admin_sync_implementation', 'main'), ('format', True)):
            with self.subTest(field=key):
                self.assert_rejected(name, {**valid, key: value})
        lock_name, bundle_name, _ = CHANNELS[1]
        lock = json.loads((self.root / lock_name).read_text())
        bundle = json.loads((self.root / bundle_name).read_text())
        lock['upstream'] = bundle['manifest']['upstream'] = 'c' * 40
        with self.changed(lock_name, json.dumps(lock).encode()):
            self.assert_rejected(bundle_name, bundle)

    def test_admin_source_pin_is_not_packaging_head(self):
        lock_name, bundle_name, _ = CHANNELS[0]
        lock = json.loads((self.root / lock_name).read_text())
        bundle = json.loads((self.root / bundle_name).read_text())
        lock['upstream'] = bundle['manifest']['upstream'] = 'd' * 40
        with self.changed(lock_name, json.dumps(lock).encode()):
            with self.changed(bundle_name, json.dumps(bundle).encode()):
                self.assertEqual(check(self.root), [])

    def test_lock_bundle_symlinks_and_missing_artifacts(self):
        names = [name for pair in CHANNELS for name in pair[:2]]
        for name in names:
            with self.subTest(path=name):
                path = self.root / name
                before = path.read_bytes()
                path.unlink()
                self.assertTrue(check(self.root))
                equivalent = self.root / 'equivalent.json'
                equivalent.write_bytes(before)
                path.symlink_to(equivalent)
                self.assertTrue(any('symlink refused' in e for e in check(self.root)))
                path.unlink()
                path.symlink_to(self.root / 'absent')
                self.assertTrue(check(self.root))
                path.unlink()
                path.write_bytes(before)
                equivalent.unlink()
        directory = self.root / '.engineering-kit/bundles'
        saved = directory.with_name('saved-bundles')
        directory.rename(saved)
        directory.symlink_to(saved, target_is_directory=True)
        self.assertTrue(any('symlink refused' in e for e in check(self.root)))

    def test_bounded_json_duplicates_and_controlled_cli_failure(self):
        names = [name for pair in CHANNELS for name in pair[:2]]
        for name in names:
            for payload in (b'[' * 10000 + b']' * 10000, b' ' * (LIMIT + 1),
                            b'{"format":1,"format":1}', b'NaN'):
                with self.subTest(path=name, size=len(payload)):
                    with self.changed(name, payload):
                        self.assertTrue(check(self.root))
        with self.changed(names[0], b'[' * 10000 + b']' * 10000):
            result = subprocess.run(
                [sys.executable, '-B', str(ROOT / 'scripts/check_template.py'),
                 '--root', str(self.root)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('JSON nesting exceeds limit', result.stdout)
            self.assertNotIn('Traceback', result.stdout + result.stderr)
        with mock.patch('scripts.check_template.json.loads', side_effect=RecursionError):
            self.assertTrue(check(self.root))

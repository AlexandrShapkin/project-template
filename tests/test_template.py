"""Offline copy fixture and meaningful integrity failures."""
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts.check_template import check

ROOT = Path(__file__).resolve().parents[1]


def copy_template(destination):
    for name in ('README.md', 'AGENTS.md', 'AGENTS.local.md', 'docs', '.github',
                 '.project-template', '.engineering-kit', 'scripts', 'tests',
                 '.editorconfig', '.gitignore'):
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

    def test_drift_missing_link_and_symlink(self):
        (self.root / 'AGENTS.md').write_text('modified')
        self.assertIn('managed drift: AGENTS.md', check(self.root))
        (self.root / 'docs/INDEX.md').write_text('[missing](absent.md)\n')
        self.assertTrue(any('broken link' in p for p in check(self.root)))
        (self.root / 'AGENTS.md').unlink()
        (self.root / 'AGENTS.md').symlink_to(self.root / 'README.md')
        self.assertTrue(any('unsafe managed path' in p for p in check(self.root)))

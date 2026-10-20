"""Policy discovery, taxonomy integrity and read-only GitHub triage regressions."""
import json
import subprocess
import unittest
from unittest import mock

from scripts.check_github_metadata import audit, get
from scripts.check_template import check_policy
from tests import test_template


# Keep the fixture reusable without running its unrelated tests twice.
class GovernanceTests(unittest.TestCase):
    setUp = test_template.TemplateTests.setUp
    changed = test_template.TemplateTests.changed

    def test_canonical_contract_inherited_by_new_project(self):
        check_policy(self.root)
        interface = (self.root / '.github/DEVELOPMENT_INTERFACE.md').read_text()
        for requirement in (
            'independent immutable `vMAJOR.MINOR.PATCH`',
            'breaking changes require\na MINOR increment',
            'Full commit SHA and\nartifact SHA-256 remain authoritative',
            'GitHub Release matching the same immutable tag',
            'Non-distributable repositories record N/A with reason',
            'Every published GitHub Release requires',
            'prior limitation, motivation, resulting',
            'no mandatory exhaustive changelog',
            'Never delete active Draft work, uncommitted changes, unknown resources',
            'priority, owner, affected subsystem, impact and actionable',
            'Exactly one `priority:P0` through `priority:P3`',
            'Assign Milestones only for confirmed versions',
            'both upstreams',
        ):
            self.assertIn(requirement, interface)
        # The retained distribution must expose the identical policy to consumers.
        bundle = json.loads((self.root / '.project-template/bundles/initial.json').read_text())
        self.assertEqual(bundle['contents']['.github/DEVELOPMENT_INTERFACE.md'], interface)

    def test_policy_discovery_cannot_be_bypassed_by_rehashing(self):
        for heading in ('## Release contract', '### Distribution',
                        '### Narrative release notes',
                        '## Workspace hygiene and technical debt', '## GitHub governance'):
            path = self.root / '.github/DEVELOPMENT_INTERFACE.md'
            with self.changed(str(path.relative_to(self.root)), path.read_bytes().replace(heading.encode(), b'')):
                with self.assertRaisesRegex(ValueError, 'missing canonical policy'):
                    check_policy(self.root)  # independent of lock hash validation
        for name, reference in [('AGENTS.md', '.github/DEVELOPMENT_INTERFACE.md'),
                                ('AGENTS.md', 'AGENTS.local.md'),
                                ('docs/WORKFLOW.md', '../.github/DEVELOPMENT_INTERFACE.md')]:
            with self.changed(name, (self.root / name).read_bytes().replace(reference.encode(), b'absent')):
                with self.assertRaisesRegex(ValueError, 'missing policy entrypoint'):
                    check_policy(self.root)

    def test_taxonomy_rejects_missing_duplicate_and_unusable_definitions(self):
        name = '.github/labels.json'
        value = json.loads((self.root / name).read_text())
        for labels in ([], value['labels'][1:], value['labels'] * 2,
                       [{**value['labels'][0], 'color': 'grey'}] + value['labels'][1:],
                       [{**value['labels'][0], 'description': ''}] + value['labels'][1:]):
            with self.changed(name, json.dumps({**value, 'labels': labels}).encode()):
                with self.assertRaises(ValueError):
                    check_policy(self.root)

    def test_live_report_detects_drift_and_active_classification_only(self):
        taxonomy = json.loads((self.root / '.github/labels.json').read_text())
        labels = taxonomy['labels']
        active = dict(number=6, state='open', labels=[{'name': n} for n in
                      ('priority:P1', 'type:maintenance', 'area:automation', 'stage:release')])
        closed = dict(number=1, state='closed', labels=[])
        self.assertEqual(audit(taxonomy, labels, [active, closed]), [])
        self.assertTrue(audit(taxonomy, labels[1:], [active]))
        for names in ([], ['priority:P1', 'priority:P2', 'type:maintenance', 'area:automation'],
                      ['priority:urgent', 'type:maintenance', 'area:automation'],
                      ['priority:P1', 'type:maintenance', 'area:automation', 'stage:invented']):
            invalid = {**active, 'labels': [{'name': n} for n in names]}
            self.assertTrue(audit(taxonomy, labels, [invalid]))

    def test_metadata_transport_is_paginated_get_only(self):
        with mock.patch('scripts.check_github_metadata.subprocess.run') as run:
            run.return_value = subprocess.CompletedProcess([], 0, '[[{"number":1}],[{"number":2}]]')
            self.assertEqual(get('owner/repo', 'issues?state=all'), [{'number': 1}, {'number': 2}])
            self.assertEqual(run.call_args.args[0], [
                'gh', 'api', '--method', 'GET', '--paginate', '--slurp',
                'repos/owner/repo/issues?state=all'])

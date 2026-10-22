"""Entrypoint safety independently of consistent lock/bundle rehashing."""
import json
import unittest

from scripts.check_template import ADMIN_FILES, KIT_FILES, check_policy
from scripts.measure_instruction_context import section
from tests import test_template


class ProgressiveDisclosureTests(unittest.TestCase):
    setUp = test_template.TemplateTests.setUp
    changed = test_template.TemplateTests.changed

    def test_missing_entry_invariants_and_routes_fail_closed(self):
        clauses = ('Always read [AGENTS.local.md]', 'remote main and active PRs',
                   'Search open/closed Issues', 'No standing merge authority',
                   'every mandatory local native/platform/security gate',
                   'independent technical acceptance', 'refresh exact-head CI evidence',
                   'Never delete uncommitted work, test evidence',
                   'Never expose secrets or user data', '**Task lifecycle**',
                   '**Release contract**', '**GitHub governance**',
                   '**Workspace hygiene and technical debt**')
        original = (self.root / 'AGENTS.md').read_text()
        for clause in clauses:
            with self.subTest(clause=clause), self.changed(
                    'AGENTS.md', original.replace(clause, 'OMITTED').encode()):
                with self.assertRaises(ValueError):
                    check_policy(self.root)

    def test_lifecycle_requirements_unchanged_and_channel_ownership_preserved(self):
        old = json.loads((self.root / '.project-template/bundles/pre-progressive-disclosure.json').read_text())
        interface = (self.root / '.github/DEVELOPMENT_INTERFACE.md').read_text()
        self.assertEqual(interface.replace('## Task lifecycle\n\n', '', 1),
                         old['contents']['.github/DEVELOPMENT_INTERFACE.md'])
        current = json.loads((self.root / '.project-template/bundles/initial.json').read_text())
        self.assertEqual(set(current['contents']), ADMIN_FILES)
        self.assertEqual(current['contents']['AGENTS.md'], (self.root / 'AGENTS.md').read_text())
        self.assertFalse({'AGENTS.local.md', 'docs/INDEX.md'} & (ADMIN_FILES | KIT_FILES))
        for heading in ('Task lifecycle', 'Release contract',
                        'Workspace hygiene and technical debt', 'GitHub governance'):
            self.assertTrue(section(interface, heading).startswith('## ' + heading))
        with self.assertRaises(ValueError):
            section(interface, 'Absent')

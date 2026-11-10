import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("checker", Path(__file__).resolve().parents[1] / "scripts/check_template.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class TemplateTests(unittest.TestCase):
    def test_missing_scaffold_is_rejected(self):
        with tempfile.TemporaryDirectory() as path:
            with self.assertRaisesRegex(ValueError, "Missing scaffold"):
                checker.check(Path(path))

    def test_project_instructions_must_be_discoverable(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            for name in checker.REQUIRED:
                (root / name).write_text("placeholder")
            with self.assertRaisesRegex(ValueError, "discover"):
                checker.check(root)
            (root / "AGENTS.md").write_text("Read AGENTS.local.md")
            checker.check(root)

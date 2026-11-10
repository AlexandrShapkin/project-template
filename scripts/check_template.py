"""Check the small reusable scaffold; no managed synchronization."""
from pathlib import Path

REQUIRED = ("README.md", "AGENTS.md", "AGENTS.local.md", "LICENSE", ".editorconfig", ".gitignore")

def check(root):
    missing = [name for name in REQUIRED if not (root / name).is_file()]
    if missing:
        raise ValueError("Missing scaffold files: " + ", ".join(missing))
    if "AGENTS.local.md" not in (root / "AGENTS.md").read_text():
        raise ValueError("Common instructions must discover project instructions")

if __name__ == "__main__":
    check(Path(__file__).resolve().parents[1])
    print("Template scaffold OK")

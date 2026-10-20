"""Offline integrity/link checks only. No synchronization or native execution."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def check(root):
    root = Path(root).absolute()
    errors = []
    for lock_name in ('.project-template/lock.json', '.engineering-kit/lock.json'):
        try:
            lock = json.loads((root / lock_name).read_text())
            if not re.fullmatch('[0-9a-f]{40}', lock['upstream']):
                raise ValueError('full upstream SHA required')
            for name, expected in lock['files'].items():
                path = root / name
                if (Path(name).is_absolute() or '..' in Path(name).parts
                        or any(p.is_symlink() for p in (path, *path.parents))):
                    raise ValueError('unsafe managed path')
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                if actual != expected:
                    errors.append('managed drift: ' + name)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f'{lock_name}: {exc}')
    # Historical Kit reference documents intentionally retain old source links.
    paths = [root / n for n in ('README.md', 'AGENTS.md', 'AGENTS.local.md',
                                '.project-template/OWNERSHIP.md')]
    paths += list((root / 'docs').rglob('*.md'))
    paths += list((root / '.github').rglob('*.md'))
    for path in paths:
        try:
            content = path.read_text()
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
                if '://' in target or target.startswith(('#', 'mailto:')):
                    continue
                target = target.split('#')[0]
                if target and not (path.parent / target).exists():
                    errors.append(f'{path.relative_to(root)}: broken link {target}')
        except OSError as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    problems = check(args.root)
    print('\n'.join(problems) if problems else 'PASS: administrative integrity and relative links')
    raise SystemExit(bool(problems))

"""Offline integrity/link checks only. No synchronization or native execution."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat


# Validate this template's distribution, not arbitrary Kit sync inputs. All writes,
# planning, adoption and migration remain exclusively in Engineering Kit.
LIMIT = 1024 * 1024
MAX_DEPTH = 64
ADMIN_FILES = frozenset((
    'AGENTS.md', '.github/DEVELOPMENT_INTERFACE.md',
    '.github/ISSUE_TEMPLATE/task.yml', '.github/pull_request_template.md',
    'docs/WORKFLOW.md', '.project-template/OWNERSHIP.md',
))
KIT_FILES = frozenset((
    '.engineering-kit/PROFILE.md', '.engineering-kit/contract/AGENT_COMMON.md',
    '.engineering-kit/contract/DEVELOPMENT_INTERFACE.md',
    '.engineering-kit/skills/ek-context/SKILL.md',
    '.engineering-kit/skills/ek-verify/SKILL.md',
    '.engineering-kit/skills/ek-pr-closeout/SKILL.md',
))
CHANNELS = (
    ('.project-template/lock.json', '.project-template/bundles/initial.json', 'admin'),
    ('.engineering-kit/lock.json', '.engineering-kit/bundles/baseline.json', 'kit'),
)


def read_file(path):
    """Bounded regular-file reads; refuse symlinks including ancestor paths."""
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('unsafe managed path: symlink refused')
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK), 'rb') as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError('regular file required')
        data = stream.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError('file exceeds 1 MiB limit')
    return data


def read_json(path):
    text = read_file(path).decode('utf-8')
    depth = 0
    quoted = escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in '{[':
            depth += 1
            if depth > MAX_DEPTH:
                raise ValueError('JSON nesting exceeds limit')
        elif char in '}]':
            depth -= 1

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError('invalid JSON constant')

    try:
        return json.loads(text, object_pairs_hook=unique, parse_constant=invalid_constant)
    except RecursionError as exc:
        raise ValueError('JSON nesting exceeds parser limit') from exc


def full_sha(value, length=40):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{%d}' % length, value)


def check_policy(root):
    """Check discoverability even when a drifted bundle was rehashed consistently."""
    interface = read_file(root / '.github/DEVELOPMENT_INTERFACE.md').decode('utf-8')
    for heading in ('## Release contract', '### Distribution',
                    '### Narrative release notes',
                    '## Workspace hygiene and technical debt', '### Artifact lifecycle',
                    '## GitHub governance'):
        if heading not in interface:
            raise ValueError('missing canonical policy section: ' + heading)
    for clause in (
        'Prefer Git branches over duplicate repository clones',
        'task isolation justifies them', 'Reuse trusted installed toolchains',
        'Rust, Go or Python runtimes', 'owner/task, retention reason and cleanup conditions',
        'approximate disk usage', 'without owner approval',
        'no unique evidence or', 'active dependencies',
        'Expiry triggers', 'Stronger project protections remain binding',
    ):
        if clause not in interface:
            raise ValueError('missing artifact lifecycle requirement: ' + clause)
    closeout = read_file(root / '.github/pull_request_template.md').decode('utf-8')
    for field in ('temporary paths', 'approximate disk usage', 'deletion safety',
                  'purpose, owner/task, retention reason, cleanup conditions'):
        if field not in closeout:
            raise ValueError('missing artifact closeout field: ' + field)
    for name, reference in (('AGENTS.md', '.github/DEVELOPMENT_INTERFACE.md'),
                            ('AGENTS.md', 'AGENTS.local.md'),
                            ('docs/WORKFLOW.md', '../.github/DEVELOPMENT_INTERFACE.md')):
        if reference not in read_file(root / name).decode('utf-8'):
            raise ValueError('missing policy entrypoint: ' + name + ' -> ' + reference)
    taxonomy = read_json(root / '.github/labels.json')
    priorities = [f'priority:P{n}' for n in range(4)]
    if (not isinstance(taxonomy, dict) or taxonomy.get('schema_version') != 1
            or taxonomy.get('priority_order') != priorities
            or not isinstance(taxonomy.get('labels'), list)):
        raise ValueError('invalid label taxonomy')
    names = set()
    for label in taxonomy['labels']:
        if (not isinstance(label, dict) or set(label) != {'name', 'color', 'description'}
                or not isinstance(label['name'], str)
                or not re.fullmatch(r'(priority|type|area|stage):[A-Za-z0-9_-]+', label['name'])
                or label['name'] in names or not isinstance(label['color'], str)
                or not re.fullmatch('[0-9A-Fa-f]{6}', label['color'])
                or not isinstance(label['description'], str) or not label['description'].strip()):
            raise ValueError('invalid or duplicate label definition')
        names.add(label['name'])
    if (not set(priorities) <= names
            or any(not any(n.startswith(prefix) for n in names)
                   for prefix in ('type:', 'area:', 'stage:'))):
        raise ValueError('missing label classification family')


def manifest(value, channel):
    fields = {'format', 'upstream', 'profile', 'files'}
    if channel == 'admin':
        fields |= {'owner', 'publication'}
    if (not isinstance(value, dict) or set(value) != fields
            or type(value['format']) is not int
            or value['format'] != (2 if channel == 'admin' else 1)
            or not full_sha(value['upstream'])
            or not isinstance(value['profile'], str)
            or value['profile'] not in (('administrative',) if channel == 'admin' else
                                       ('minimal', 'backend', 'infrastructure', 'research'))
            or not isinstance(value['files'], dict)
            or set(value['files']) != (ADMIN_FILES if channel == 'admin' else KIT_FILES)
            or not all(full_sha(v, 64) for v in value['files'].values())):
        raise ValueError('invalid lock/bundle manifest schema, pins or managed paths')
    if channel == 'admin' and (value['owner'] != 'AlexandrShapkin/project-template'
                               or value['publication'] != 'private'):
        raise ValueError('invalid administrative owner/publication')
    # Kit format 1 intentionally has no owner/publication fields. Its private
    # distribution and pinned baseline are recorded separately in tooling.json.
    return value


def check(root):
    root = Path(root).absolute()
    errors = []
    try:
        check_policy(root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f'policy: {exc}')
    tooling = None
    try:
        tooling = read_json(root / '.project-template/tooling.json')
        if (not isinstance(tooling, dict) or type(tooling.get('format')) is not int
                or tooling['format'] != 1 or tooling.get('publication') != 'private'
                or not full_sha(tooling.get('kit_baseline'))
                or not full_sha(tooling.get('admin_sync_implementation'))):
            raise ValueError('invalid tooling version pins/publication')
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        errors.append(f'.project-template/tooling.json: {exc}')
        tooling = None
    for lock_name, bundle_name, channel in CHANNELS:
        lock = None
        try:
            lock = manifest(read_json(root / lock_name), channel)
            if channel == 'kit' and tooling and lock['upstream'] != tooling['kit_baseline']:
                raise ValueError('Kit upstream differs from pinned tooling baseline')
            for name, expected in lock['files'].items():
                if hashlib.sha256(read_file(root / name)).hexdigest() != expected:
                    errors.append('managed drift: ' + name)
        except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
            errors.append(f'{lock_name}: {exc}')
        try:
            bundle = read_json(root / bundle_name)
            if not isinstance(bundle, dict) or set(bundle) != {'manifest', 'contents'}:
                raise ValueError('invalid bundle structure')
            retained = manifest(bundle['manifest'], channel)
            contents = bundle['contents']
            if not isinstance(contents, dict) or set(contents) != set(retained['files']):
                raise ValueError('bundle content file set mismatch')
            for name, content in contents.items():
                if (not isinstance(content, str)
                        or hashlib.sha256(content.encode('utf-8')).hexdigest() != retained['files'][name]):
                    raise ValueError('invalid bundle content/hash: ' + name)
            if retained != lock:
                raise ValueError('retained bundle manifest differs from installed lock')
        except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
            errors.append(f'{bundle_name}: {exc}')
    # Historical Kit reference documents intentionally retain old source links.
    paths = [root / n for n in ('README.md', 'AGENTS.md', 'AGENTS.local.md',
                                '.project-template/OWNERSHIP.md')]
    paths += list((root / 'docs').rglob('*.md'))
    paths += list((root / '.github').rglob('*.md'))
    for path in paths:
        try:
            content = read_file(path).decode('utf-8')
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
                if '://' in target or target.startswith(('#', 'mailto:')):
                    continue
                target = target.split('#')[0]
                if target and not (path.parent / target).exists():
                    errors.append(f'{path.relative_to(root)}: broken link {target}')
        except (OSError, ValueError) as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    problems = check(args.root)
    print('\n'.join(problems) if problems else 'PASS: administrative integrity and relative links')
    raise SystemExit(bool(problems))

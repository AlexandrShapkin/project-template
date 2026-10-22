"""Offline UTF-8 instruction-byte accounting, not tokenizer or runtime profiling.

Baseline is immutable pre-change Git source. Counts unique files and selected
section bytes once per scenario; excludes shared task source/tool output. Section
reads model targeted retrieval, not a claim that an agent actually used this much.
"""
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'a3ee63ac8fd32d787438a5cee14f69db7c384ef7'
INTERFACE = '.github/DEVELOPMENT_INTERFACE.md'
ENTRY = ['AGENTS.md', 'AGENTS.local.md']
BASE_FILES = ENTRY + [INTERFACE, 'docs/INDEX.md', 'docs/PROJECT.md', 'docs/ARCHITECTURE.md']


def section(text, heading):
    match = re.search(r'^## ' + re.escape(heading) + r'\n', text, re.M)
    if not match:
        raise ValueError('missing measurement section: ' + heading)
    end = re.search(r'^## ', text[match.end():], re.M)
    return text[match.start():match.end() + end.start() if end else len(text)]


def measure():
    def old(name):
        return subprocess.check_output(['git', '-C', str(ROOT), 'show', BASE + ':' + name])
    def new(name):
        return (ROOT / name).read_bytes()
    interface = new(INTERFACE).decode()
    result = []
    scenarios = {
        'documentation preparation': (['Task lifecycle'], []),
        'bugfix preparation': (['Task lifecycle'], ['docs/ARCHITECTURE.md']),
        'security preparation': (['Task lifecycle'], ['docs/SECURITY.md']),
        'PR handoff (also all change-task closeouts)': (
            ['Task lifecycle', 'GitHub governance', 'Workspace hygiene and technical debt'],
            ['.github/pull_request_template.md', '.github/ISSUE_TEMPLATE/task.yml']),
        'release preparation and handoff': (
            ['Task lifecycle', 'GitHub governance', 'Workspace hygiene and technical debt', 'Release contract'],
            ['docs/RELEASING.md', '.github/pull_request_template.md', '.github/ISSUE_TEMPLATE/task.yml']),
    }
    for name, (sections, extra) in scenarios.items():
        baseline = set(BASE_FILES + extra)
        selected = set(ENTRY + extra)
        after = sum(len(new(f)) for f in selected)
        after += sum(len(section(interface, s).encode()) for s in sections)
        before = sum(len(old(f)) for f in baseline)
        result.append(dict(scenario=name, before_bytes=before, after_bytes=after,
                           saved_bytes=before-after, before_files=len(baseline),
                           after_files=len(selected | {INTERFACE}),
                           section_reads=len(sections)))
    return result


if __name__ == '__main__':
    print(json.dumps(measure(), indent=2))

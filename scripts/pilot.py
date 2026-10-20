"""Offline end-to-end exercise using a separately reviewed local Kit checkout."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tests.test_template import copy_template  # noqa: E402


def pilot(kit):
    tooling = json.loads((ROOT / '.project-template/tooling.json').read_text())
    head = subprocess.check_output(['git', '-C', str(kit), 'rev-parse', 'HEAD']).decode().strip()
    if head != tooling['admin_sync_implementation']:
        raise ValueError('Kit checkout must match pinned admin implementation')
    dirty = subprocess.check_output(['git', '-C', str(kit), 'status', '--porcelain',
                                     '--untracked-files=no'])
    if dirty:
        raise ValueError('Kit tracked files must be clean')
    sys.path.insert(0, str(kit))
    from engineering_kit.sync import export, plan, write, SyncError, LOCK, ADMIN_LOCK

    def apply(root, bundle, channel):
        p, _ = plan(root, bundle, channel)
        write(root, bundle, [c['path'] for c in p['changes']], p['plan_sha256'], channel)
        assert not plan(root, bundle, channel)[0]['changes']

    def refused(call):
        try:
            call()
        except SyncError:
            return
        raise AssertionError('unsafe action was accepted')

    with tempfile.TemporaryDirectory(prefix='project-template-pilot-') as temp:
        base = Path(temp)
        consumer = base / 'consumer'
        consumer.mkdir()
        copy_template(consumer)
        def git(root, *args):
            return subprocess.check_output(['git', '-C', str(root), *args]).decode().strip()
        def commit(root, message):
            git(root, 'add', '.')
            git(root, '-c', 'user.name=Offline Pilot', '-c',
                'user.email=pilot@example.invalid', '-c', 'core.hooksPath=/dev/null',
                'commit', '-qm', message)
            return git(root, 'rev-parse', 'HEAD')
        git(consumer, 'init', '-q')
        commit(consumer, 'Offline adoption')
        old = consumer / '.project-template/bundles/initial.json'
        assert not plan(consumer, old, 'admin')[0]['changes']
        kit_bundle = consumer / '.engineering-kit/bundles/baseline.json'
        assert not plan(consumer, kit_bundle)[0]['changes']
        (consumer / 'AGENTS.local.md').write_text('Mandatory native gate: keep\n')
        native = consumer / '.github/workflows/native.yml'
        native.write_text('# project-specific gate fixture\n')
        commit(consumer, 'Project-local choices')
        draft = base / 'active-draft'
        git(consumer, 'worktree', 'add', '-q', '-b', 'active-draft', str(draft))
        evidence = draft / 'unique-evidence.txt'
        evidence.write_text('Active Draft evidence; preserve uncommitted work\n')
        draft_status = git(draft, 'status', '--porcelain')
        local_project = (consumer / 'docs/PROJECT.md').read_bytes()
        source = base / 'upstream'
        source.mkdir()
        copy_template(source)
        git(source, 'init', '-q')
        commit(source, 'Canonical source fixture')
        interface = source / '.github/DEVELOPMENT_INTERFACE.md'
        interface.write_text(interface.read_text() + '\nPilot reviewed lifecycle clarification.\n')
        revision = commit(source, 'One central lifecycle change')
        bundle = base / 'next.json'
        exported = export(source, revision, 'administrative', bundle, 'admin')
        assert exported['publication'] == 'private'
        assert exported['upstream'] == revision
        kit_before = (consumer / LOCK).read_bytes()
        p, _ = plan(consumer, bundle, 'admin')
        assert {c['path'] for c in p['changes']} == {
            '.github/DEVELOPMENT_INTERFACE.md', ADMIN_LOCK}
        refused(lambda: write(consumer, bundle, [ADMIN_LOCK], p['plan_sha256'], 'admin'))
        apply(consumer, bundle, 'admin')
        assert (consumer / LOCK).read_bytes() == kit_before
        commit(consumer, 'Proposed consumer update, no remote writes')
        backend = base / 'backend.json'
        export(kit, tooling['kit_baseline'], 'backend', backend)
        admin_before = (consumer / ADMIN_LOCK).read_bytes()
        apply(consumer, backend, 'kit')
        assert (consumer / ADMIN_LOCK).read_bytes() == admin_before
        apply(consumer, kit_bundle, 'kit')
        target = consumer / '.github/DEVELOPMENT_INTERFACE.md'
        reviewed = target.read_bytes()
        target.write_text('local conflict')
        refused(lambda: plan(consumer, old, 'admin'))
        target.unlink()
        refused(lambda: plan(consumer, old, 'admin'))
        target.symlink_to(base / 'absent')
        refused(lambda: plan(consumer, old, 'admin'))
        target.unlink()
        target.write_bytes(reviewed)  # fixture-only restore of known bytes
        apply(consumer, old, 'admin')
        assert (consumer / 'AGENTS.local.md').read_text() == 'Mandatory native gate: keep\n'
        assert native.read_text() == '# project-specific gate fixture\n'
        assert (consumer / 'docs/PROJECT.md').read_bytes() == local_project
        assert evidence.read_text() == 'Active Draft evidence; preserve uncommitted work\n'
        assert git(draft, 'status', '--porcelain') == draft_status
        assert 'active-draft' in git(consumer, 'worktree', 'list', '--porcelain')
        assert (consumer / LOCK).read_bytes() == kit_before
        commit(consumer, 'Reviewed rollback fixture')
        from scripts.check_template import check
        assert check(consumer) == []
        print('PASS: offline creation, exact-source central update, idempotence, separate Kit')
        print('upgrade/rollback, native/local preservation, conflict/missing/symlink refusal,')
        print('partial permission refusal, administrative rollback and private classification.')
        print('Disposable Git fixtures removed by TemporaryDirectory; no remote operations.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kit', type=Path, required=True)
    pilot(parser.parse_args().kit.absolute())

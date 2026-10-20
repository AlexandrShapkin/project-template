# Creation, controlled updates and rollback

## Trust and versions

There are two independent channels: `.project-template/lock.json` records the
full reviewed template source SHA and SHA-256 of managed admin files;
`.engineering-kit/lock.json` records the separate installed Kit SHA/profile/hashes.
`.project-template/tooling.json` pins the proposed admin-capable Kit implementation
separately from the accepted baseline. Kit PR #10 is a dependency, not accepted
main. Review it independently before real adoption. Do not claim these Draft
sources have independent acceptance.

Use a trusted local Kit checkout at the full implementation SHA from tooling.json;
verify `git -C "$KIT" rev-parse HEAD` before executing it. In the examples KIT is
that absolute checkout; TEMPLATE is a trusted local project-template checkout,
TEMPLATE_SHA is a full reviewed commit and CONSUMER is an existing absolute path.
No network fetch, dependency installation or global configuration is implicit.
Use Python 3.11+, POSIX and Git. Read the Kit's docs/SYNC.md for trust/failure limits.

Both upstreams/distributions are private. Before copying into any public consumer,
STOP: obtain separate publication authorization or a reviewed public-safe bundle.
Neither hashes nor an offline export establish a license or redistribution rights.

## New project (offline equivalent of Use this template)

Choose a full template commit containing both locks and retained bundles. Review
its provenance, classification and file list first. Use a new private local path;
never copy over an existing repository. No GitHub repository is created here.

```sh
mkdir "$CONSUMER"
git -C "$TEMPLATE" archive "$TEMPLATE_SHA" | tar -x -C "$CONSUMER"
git -C "$CONSUMER" init
python3 -B "$CONSUMER/scripts/check_template.py" --root "$CONSUMER"
python3 -B "$KIT/scripts/ek.py" sync plan --channel admin --root "$CONSUMER" \
  --bundle "$CONSUMER/.project-template/bundles/initial.json"
python3 -B "$KIT/scripts/ek.py" sync plan --root "$CONSUMER" \
  --bundle "$CONSUMER/.engineering-kit/bundles/baseline.json"
# Both plans must be empty before any project customization.
```

The admin lock references the source commit of its managed files; a later packaging
commit adds the lock and bundle. This avoids a self-referential SHA. Source hashes
must match the reviewed source; the lock need not equal the packaging HEAD.

Complete docs/PROJECT.md, README, AGENTS.local.md and native CI. Local/scaffold
files can change freely; keep managed lifecycle files byte-identical. Product
checks remain UNVERIFIED until selected and run. Commit the initial snapshot and
record the full source/package SHAs for review. GitHub template availability
(`is_template`) is not assumed; this task does not change repository settings.

## One upstream change → one consumer proposal

1. Change the canonical interface in project-template, review its PR, and obtain
   the resulting accepted full source SHA. Do not edit Kit legacy contracts too.
2. From a trusted local template checkout export into a NEW retained bundle:

   ```sh
   python3 -B "$KIT/scripts/ek.py" bundle --channel admin --source "$TEMPLATE" \
     --revision "$TEMPLATE_SHA" --profile administrative --output /tmp/admin-next.json
   ```

3. Inventory the consumer's branch, full HEAD, status, worktrees and open PRs.
   Create a bounded update branch from a verified base and preserve the clean
   pre-update commit/bundles for rollback. Run read-only plan:

   ```sh
   python3 -B "$KIT/scripts/ek.py" sync plan --channel admin --root "$CONSUMER" \
     --bundle /tmp/admin-next.json
   ```

4. Review bundle owner/full SHA/private classification, file hashes and actual
   content diff against the consumer. `plan` returns path/action metadata and a
   digest, not a unified text diff: inspect `contents` in the JSON against the
   named current files without applying it. Approve every create/update/delete.
   Write only with that digest and one literal `--allow PATH` for EACH changed
   path, including `.project-template/lock.json`; no directory/glob permissions:

   ```sh
   python3 -B "$KIT/scripts/ek.py" sync write --channel admin --root "$CONSUMER" \
     --bundle /tmp/admin-next.json --plan-sha256 REVIEWED_DIGEST \
     --allow .github/DEVELOPMENT_INTERFACE.md --allow .project-template/lock.json
   # Example applies only when exactly those two paths change.
   ```

5. Preserve the previous retained bundle separately for rollback, then copy the
   reviewed new bundle to `.project-template/bundles/initial.json`. Despite its
   historical filename, this is the current installed admin bundle. Its manifest
   must equal the installed administrative lock. For a Kit update, likewise
   preserve the old bundle, replace `.engineering-kit/bundles/baseline.json` with
   the reviewed installed bundle and update `kit_baseline` in tooling.json to
   the installed full Kit SHA. This metadata/artifact maintenance is explicit,
   reviewed file work; only Kit performs managed-file/lock synchronization.
   Inspect `git diff`, run template integrity and all consumer native gates,
   and repeat plan (empty).
   Commit files and lock together. Create a Draft PR with old/new SHAs, complete
   diff, test evidence, publication classification and rollback. CI must match
   the exact HEAD; independent review and owner merge authorization are required.
   No automatic push/main write/merge, repository administration or rollout.

For an independent Kit profile/version update export `bundle --profile PROFILE`
without `--channel admin`, then use the same plan/write protocol on the Kit
channel. Preserve the administrative lock. Profiles: minimal, backend,
infrastructure, research. The retained baseline bundle remains available for
rollback; choosing a profile does not choose native commands or activate skills.

## Conflicts and existing repositories

Edited/missing managed files, collisions on first adoption, unsafe paths,
symlinks and checksum/lock errors fail closed before writes. Preserve the edits;
do not delete the lock, reset user work or force-adopt. Move genuine local rules
into AGENTS.local.md in a separately reviewed migration, restore the verified
managed version only with explicit review, then replan. Initial adoption into an
existing repo with AGENTS.md requires an explicit reviewed migration of that
file; it is not an overwrite feature. See the ownership map for legacy migration.
Scaffold improvements (architecture/security/testing docs) are manual proposals,
never automatic replacement of project decisions.

## Rollback / interruption

Export or retain the OLD bundle. Plan and explicitly write it with fresh digest
and all changed paths; review deletion operations too. Commit rollback as a new
consumer PR and rerun native gates. Restore the corresponding retained current
bundle too (and the tooling Kit pin for a Kit rollback), keeping the superseded
bundle separately. No history rewrite or automatic reset.
The engine is atomic per file, not across files; keep a quiescent trusted checkout.
If I/O fails halfway, preserve evidence and restore only affected managed files
AND lock from the verified pre-update Git snapshot/backup after checking for
local work, then replan. Never auto-clean unknown data or delete locks to recover.

## Reproduction

Run template checks plus the Kit suite. The optional integration pilot uses the
pinned local Kit checkout, performs no network operations and creates only
TemporaryDirectory fixtures:

```sh
python3 -B scripts/check_template.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/pilot.py --kit "$KIT"
```

The pilot copies this template into a disposable Git repository, exports exact
source commits, updates one canonical lifecycle file, preserves local/native CI,
checks separate Kit upgrades, rejects drift/symlinks/partial permissions and
rolls back. This is offline adoption evidence, not public distribution or native
application verification. Report results in the review handoff.

# Author verification handoff

Owning requirements: Engineering Kit Issues #7 and #9. Author checks are not
independent ChatGPT acceptance. Both PRs must remain Draft pending review.

## Revisions

- Accepted Kit baseline / installed minimal profile:
  `f808af695c7787fb68f332d8ff1214fb2100f9b5`.
- Proposed admin implementation, [Kit PR #10](https://github.com/AlexandrShapkin/codex-engineering-kit/pull/10):
  `21cf2914cb0a1c904ca8c783a36723786373b600`.
- Administrative managed-file source:
  `adfc75e686f7853a13618ee5858a775000f0a396`.
- Template packaging HEAD: use the full current PR HEAD; the lock intentionally
  points to the prior exact source commit to avoid a circular commit hash.

The Kit baseline bundle was exported from the exact Git commit, reviewed through
sync plan and explicitly installed with all seven allowed paths. The administrative
bundle was exported from the source commit, planned and explicitly installed with
all seven allowed paths into a fresh staging directory. Its installed managed
bytes were compared with the source template before packaging the generated lock
and retained bundle. This is initial canonical packaging, not collision bypass
for an existing consumer. Existing consumers must use the documented migration.

## Commands and results

- `python3 -B scripts/check_template.py`: PASS, managed hashes and relative links.
- `python3 -B -m unittest discover -s tests -v`: PASS, 8 template tests with
  offline creation/local edits, strict lock/bundle schema and pin validation,
  content/hash/manifest consistency, symlink/missing/unsafe-path cases, bounded
  JSON/duplicate-key rejection and controlled CLI failure without traceback.
- `python3 -B scripts/pilot.py --kit /tmp/project-template-kit`: PASS, real
  disposable Git repositories, exact-commit export, one upstream lifecycle
  update, consumer commit, rollback commit, idempotence, separate Kit profile
  upgrade/rollback, preservation of local/native fixtures, drift/missing/symlink
  and incomplete-permission refusals. All fixture paths are TemporaryDirectory.
- Both Kit and admin `sync plan` on installed retained bundles: PASS, empty changes.
- Kit `python3 -B -m unittest discover -s tests -q`: PASS, 45 tests.
- Kit `python3 -B scripts/check_contract.py --self-check`: PASS; frozen legacy
  contract bytes remain compatible.
- `git diff --check`: PASS in both repositories.
- [Kit exact-head CI](https://github.com/AlexandrShapkin/codex-engineering-kit/actions/runs/39443688341):
  success at `21cf2914cb0a1c904ca8c783a36723786373b600`, Python 3.11/3.12/3.13.
  Template exact-head CI is reported in its PR; its job is explicitly administrative.

## Limits and cleanup

No native application exists; product tests/platform/security gates remain
UNVERIFIED until owner selection. Public redistribution is blocked by policy;
these offline mechanisms cannot inspect remote visibility or authenticate a
publisher. Both repos remain private. No license is selected. No deployment,
merge, main write, global settings change, runtime activation, RDC or RelayForge
runtime was performed. GitHub is_template remains false: the offline-copy
acceptance path was used, with no repository-settings change.

Writes are atomic per file, not transactional across files; recovery requires a
verified snapshot and a quiescent trusted POSIX filesystem. Locks do not prove
source acceptance. Kit PR #10 is a separately reviewed dependency; the baseline
alone cannot update administrative files. Scaffold/local documentation remains
consumer-owned and receives only manual reviewed proposals.

Temporary pilot and unittest fixtures were removed by their context managers.
The own Kit checkout `/tmp/project-template-kit` and both open PR branches are
retained for independent review. No user branch, worktree or data was deleted.

## PR #1 review corrections

P2: integrity checks now read both retained bundles and both installed locks,
validate channel-specific schemas and exact distribution file sets, verify UTF-8
contents/SHA-256, and require retained manifests to equal installed locks. The
Kit format-1 manifest intentionally has no owner/publication fields; unknown
fields are rejected, while private distribution and the full Kit pin are checked
through tooling.json. Administrative owner/private classification are mandatory.
No packaging HEAD comparison is made; the source/package split remains valid.

P3: all artifact reads are limited to 1 MiB and regular non-symlink paths, JSON
nesting is limited to 64, duplicate keys/nonstandard constants are rejected, and
parser RecursionError is reported as a validation failure. Negative tests cover
a 10,000-level JSON input and exercise the CLI's nonzero exit without traceback.
This is a read-only distribution checker, not a second synchronization engine.
Kit #10 is unchanged. Updated exact-head CI evidence is recorded in PR #1.

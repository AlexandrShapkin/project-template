# Author verification handoff

Owning requirements: Engineering Kit Issues #7 and #9; release follow-up:
[template Issue #2](https://github.com/AlexandrShapkin/project-template/issues/2).
Kit PR #10 and template PR #1 received independent technical acceptance and were
merged by the owner. Author checks below are separate evidence. The Issue #2
follow-up remains subject to its own Draft PR review and owner merge authority.

## Revisions

- Accepted Kit baseline / installed minimal profile:
  `f808af695c7787fb68f332d8ff1214fb2100f9b5`.
- Accepted admin implementation, [Kit PR #10](https://github.com/AlexandrShapkin/codex-engineering-kit/pull/10):
  `21cf2914cb0a1c904ca8c783a36723786373b600`.
- Administrative managed-file source:
  `adfc75e686f7853a13618ee5858a775000f0a396`.
- Accepted template merge: `ad15dfe1b12405517b639f8ba85067f21a8fb62c` (PR #1).
- Accepted Kit merge: `e647d9d535eb9b55f2a6df55c2bf5e4b9a47957d` (PR #10).
- The source pins above remain unchanged. Packaging and merge commits differ from
  managed source commits by design, avoiding a circular commit hash.

The Kit baseline bundle was exported from the exact Git commit, reviewed through
sync plan and explicitly installed with all seven allowed paths. The administrative
bundle was exported from the source commit, planned and explicitly installed with
all seven allowed paths into a fresh staging directory. Its installed managed
bytes were compared with the source template before packaging the generated lock
and retained bundle. This is initial canonical packaging, not collision bypass
for an existing consumer. Existing consumers must use the documented migration.

## Original implementation checks (PR #1 / Kit #10)

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
runtime was performed by these authoring tasks. The original PR #1 used offline
copy fixtures. The owner subsequently enabled GitHub Template repository; read-only
metadata verification on 2026-10-20 confirms `is_template=true`, `private=true`.

Writes are atomic per file, not transactional across files; recovery requires a
verified snapshot and a quiescent trusted POSIX filesystem. Locks do not prove
source acceptance. Kit PR #10 is an accepted dependency; the installed baseline
alone cannot update administrative files. Scaffold/local documentation remains
consumer-owned and receives only manual reviewed proposals.

Temporary pilot and unittest fixtures were removed by their context managers.
The own Kit checkout `/tmp/project-template-kit` was retained as review evidence;
PR #1 and Kit #10 are now merged. No user branch, worktree or data was deleted.

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

## Issue #2 release follow-up

On 2026-10-20, GitHub metadata confirmed the owner-enabled source repository is
private and `is_template=true`. This follow-up changes tooling status to
`accepted` and corrects stale acceptance/activation documentation only. All
reviewed SHA pins, hash-managed normative files and both bundles/locks are
unchanged; no Kit changes, re-export or synchronization writes are involved.
Acceptance refers to merged PR #1 and Kit #10, not automatic acceptance of this
follow-up or future consumer changes.

A genuine private GitHub Template generation was performed with the authorized
`gh repo create --private --template AlexandrShapkin/project-template` operation:

- [Private smoke repository](https://github.com/AlexandrShapkin/project-template-smoke-issue-2-20261020).
- Initial generated HEAD: `f51bc86b1512fca1ff9b5e0e898cf64fa3977cdd`.
- Source main: `ad15dfe1b12405517b639f8ba85067f21a8fb62c`.
- GitHub metadata: `private=true`; `template_repository.full_name` is
  `AlexandrShapkin/project-template`, itself private and enabled as a template.
- Generated tree `43521e6baa0b1c54bc60b56cc95237bfcd0a7810` equals the source
  main tree. Both retained bundles/locks were also compared byte-for-byte.
- From the generated checkout: `python3 -B scripts/check_template.py` PASS;
  `python3 -B -m unittest discover -s tests -v` PASS, 8 tests. This checks agent
  instructions/relative links, installed hashes, pins and retained artifacts.
- [Generated-repository exact-head CI](https://github.com/AlexandrShapkin/project-template-smoke-issue-2-20261020/actions/runs/39451523247)
  SUCCESS at the generated HEAD, Python 3.11/3.12/3.13.

This smoke test exercises GitHub Template creation from the already accepted
main; the release-status follow-up is checked separately on its Draft PR HEAD.
The generated repository naturally retains main's pre-follow-up status text;
no consumer update or remote write was made after generation. Its private remote
and clean local checkout `/tmp/project-template-smoke-issue-2-20261020` are retained
for independent review; remote deletion is not authorized. Temporary unit fixtures
are removed by their context managers. No visibility/settings changes, public
redistribution, deployment, merge or runtime operation was performed. Product-native
verification remains UNVERIFIED until a project chooses and runs its native gates.

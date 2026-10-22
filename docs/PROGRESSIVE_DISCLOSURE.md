# Progressive-disclosure audit and review handoff

Owning task: [Template #14](https://github.com/AlexandrShapkin/project-template/issues/14).
This is evidence and a rollout proposal, not a second policy or execution grant.
Baseline inspected 2026-10-23; canonical base is
`a3ee63ac8fd32d787438a5cee14f69db7c384ef7`. No consumer files changed.

## Classification and requirement-preservation matrix

| Requirements / source | Class | Enforcement / destination |
| --- | --- | --- |
| Identity, full SHA, status/worktrees, verified base, owning Issue, scope/plan | Always-on | Root entrypoint; local identity rules remain mandatory |
| User precedence, stronger local rules, no inferred authority, conflict handling | Always-on | Root; interface remains authoritative; stop dependent work only |
| Preserve work/contracts, meaningful behavior tests, complete diff, native/platform/security checks, truthful evidence | Always-on | Root and unchanged Task lifecycle; no CI changes |
| Draft, exact-head CI refresh, independent acceptance vs formal approval vs merge authority | Always-on | Root; Task lifecycle and PR template before handoff |
| Merge/deploy/publish/credentials/admin boundaries; no RDC/RelayForge runtime; secrets/data | Always-on | Root plus all stronger local prohibitions |
| Cleanup prohibitions and evidence retention; closeout inventory | Always-on | Root; full hygiene section before environments, cleanup or closeout |
| Detailed task lifecycle | Task-conditional | Before any implementation/documentation change; new section heading only |
| Issue/PR labels, milestones, historical metadata and administration safeguards | Task-conditional | GitHub governance + existing templates before relevant operation |
| Immutable SemVer, distribution, narrative notes, approval/provenance/rollback | Task-conditional | Entire Release contract and local release policy before release work |
| Temporary environments, runtime copies, hygiene/debt details | Task-conditional | Entire Workspace hygiene section including Artifact lifecycle |
| Security boundaries and migrations | Task-conditional | Local security docs; ownership/upgrade procedure; combine applicable triggers |
| Local native gates, product invariants, protected PRs, execution limits | Always-on | AGENTS.local.md still mandatory; no consumer trimming in this PR |
| Index, architecture, ADRs, project scaffolds | Navigation/reference, conditional when affected | Select relevant docs; preserve any stricter local mandatory reads |
| Frozen Kit contracts | Reference-only | Never activate as a second administrative policy; no snapshot edits |
| Kit technical skills | Conditional reference | Opt-in when justified; no installation, dependency or framework added |
| Ownership, locks, source mappings, retained artifacts and publication classification | Conditional contract | Existing upgrade procedure and Kit engine; no managed path/schema expansion |

The complete lifecycle body is byte-preserved, with only `## Task lifecycle`
inserted; a regression enforces this against the retained pre-change bundle.
Root summaries intentionally overlap high-risk lifecycle clauses so conditional
loading cannot defer their application. This is deliberate safety duplication,
not a claimed elimination of all repeated semantics. Local Template edits only
make placeholder project/architecture context conditional; every local gate and
publication/rights constraint remains intact. The index becomes navigation.

## Six-repository inventory

All six roots were 791 bytes and identical (SHA-256
`f2bd56969e314ae5f89c8fad4a5bb3e00efc6c7f2170523e9b06da81e1b7cb69`).
All six interfaces were 12,615 bytes and identical (SHA-256
`ef358ea6728bd90cf79029257eecce1712e17027b900cabb1ca4342d4c85e3ae`).
Remote GitHub main and local main/HEAD agreed at inventory time:

| Repository | Full main SHA | Existing worktrees before this task | Open PRs |
| --- | --- | --- | --- |
| project-template | a3ee63ac8fd32d787438a5cee14f69db7c384ef7 | 1 | none |
| codex-engineering-kit | 749f8b1024759958a79f132abf210cdd0a173529 | 5 | none |
| codex-smart | ff9416bab4108ff47c7fb303283ae58f5f1cb837 | 2 | #125, #164, #172–175 |
| rustcraft | 053773150f2e34d11d60e8046c0465d2644d7696 | 1 | none |
| assistant-hub | 0f701089de89f77c5fe37d6b573e451eba7bf36a | 3 | #53, #54 |
| relayforge | 53e388493c61530f666348324798eac80992a800 | 4 | #64, #66, #76, #88 |

All launch checkouts were clean; no existing worktree or PR was altered. Kit's
four old detached worktree entries were prunable according to Git; this is not
a deletion decision. Actual paths/state must be re-inventoried before rollout.
Open/closed Issues were inspected (all Template records; latest 100 per other
repository). No distinct progressive-disclosure owner was found in that inventory;
older consumer history needs a focused search before any new consumer Issue.
Closed lifecycle records Template #12, Kit #20, Smart #179, Rustcraft #41,
Hub #64 and Relayforge #94 provide history, not authorization to reopen or merge.
Kit #8 already owns consumer propagation mechanics; reuse that work.

## Duplication and conflicts

- Mandatory full interface/index reads in all roots duplicate the interface's
  bounded-context intent. Template local also demanded placeholder PROJECT and
  ARCHITECTURE; remove that unconditional read only here.
- Consumer local preludes currently say to read the interface first. Those stronger
  reads remain effective until separately reviewed local migrations; copying the
  new root alone cannot deliver the modeled savings there.
- Kit `ek-context` still says to read the pinned contract, despite root instructions
  making legacy contracts provenance-only. Review this conditional skill's active
  references in Kit; do not rewrite accepted frozen snapshots or silently execute
  the skill. `ek-verify` and `ek-pr-closeout` repeat useful safety/evidence rules
  and grant no execution authority; retain their technical responsibilities.
- Rustcraft documentation-maintenance and stage-execution already support bounded
  context and canonical workflow; keep their generated-doc/registry ownership,
  stage authorization and Ubuntu/Windows evidence rules. Other domain skills are
  outside this navigation-only change and remain available under their triggers.
- Smart local standing delegation and interface no-standing-merge wording require
  explicit authority reconciliation at review; this PR neither expands delegation
  nor resolves the PR #125 ban by inference. #164 must not be activated; preserve
  #170/#176 references and every existing branch even if absent from open PRs.
- Hub local work-loop duplicates shared workflow but includes public-tree checks,
  localhost/data/executor restrictions and explicit owner boundaries. Retain until
  clause-by-clause separate review. Relayforge local cleanup repeats shared text
  but accompanies stricter live/build boundaries; do not remove by text similarity.

## Context comparison

Reproduce with `python3 -B scripts/measure_instruction_context.py`. Counts are
UTF-8 bytes and distinct files selected by explicit task scenarios, not tokens,
model latency, actual tool call counts or successful end-to-end task trials.
Baseline reads the old root/interface/index/local and locally required PROJECT
and ARCHITECTURE from the exact base commit. After reads new root/local and
selected interface sections. Common task source is excluded; scenario-specific
architecture/security/release docs and templates are included on both sides.
One selected file may require multiple section reads; cache avoids recounting.

| Scenario | Before bytes | After bytes | Saved bytes | Distinct files before → after | Interface section reads after |
| --- | ---: | ---: | ---: | --- | ---: |
| Documentation preparation | 16,985 | 8,133 | 8,852 | 6 → 3 | 1 |
| Bugfix preparation | 16,985 | 8,477 | 8,508 | 6 → 4 | 1 |
| Security preparation | 17,628 | 8,776 | 8,852 | 7 → 4 | 1 |
| PR handoff / change-task closeout | 19,682 | 16,317 | 3,365 | 8 → 5 | 3 |
| Release preparation and handoff | 24,685 | 25,026 | -341 | 9 → 6 | 4 |

Preparation rows stop before Issue/PR creation and closeout; all change tasks
must subsequently load governance and hygiene before those actions. An existing
owning Issue is assumed during preparation. For mixed tasks take the union of
required context, including extra local reads. This audit itself necessarily
loads the full interface and many documents; it is not the small-doc scenario.
Release work grows slightly because it needs almost the entire interface plus
the longer invariant summary. No token savings were measured or claimed.

Exact repeated nonblank whole lines across the six active Template context files
(root, local, interface, index, PROJECT, ARCHITECTURE) were zero before and after;
this crude metric does not measure semantic duplication. Across repositories,
five redundant physical copies of the old root/interface total 67,030 bytes;
those managed copies are intentionally retained for offline enforcement, not
removed. Only unconditional loading is reduced. Consumer savings remain
UNVERIFIED until their local context commands and mandatory reads are evaluated.

## Ordered rollout and acceptance gates

1. **Template #14:** independently review this Draft, preservation matrix, exact
   final-head administrative CI and native-gate applicability. Owner-authorized
   merge accepts the canonical source. Retain old bundle and review source/package
   SHAs separately; immutable pin must resolve to the managed bytes. Do not roll
   out a merely proposed source. Release/milestone N/A: no release requested.
2. **Engineering Kit:** after Template acceptance, bounded adoption PR using the
   existing administrative channel, independently selected trusted Kit SHA and
   the accepted Template source. Review `ek-context` references and checker
   assumptions; preserve frozen contracts. Run `check_contract.py --self-check`,
   complete unittest suite and exact-head CI. Add source-update negative/rollback
   cases only if engine behavior changes; do not add a new propagation engine.
3. **Codex Smart:** separate reviewed source-update proposal from fresh verified
   main, under existing Kit #8 coordination and a reused/focused owning Issue.
   Keep identical accepted root, reconcile mandatory local full-interface reads
   explicitly, retain `just context`, documentation registry/ADRs, `just docs-check`,
   `just check`, applicable cached `just security`, exact-head CI/Security and
   independent ACCEPT. Preserve read-only doctor and protected PR/branch rules.
4. **Rustcraft:** same accepted root/source adapter, separate PR. Preserve launch
   checkout identity, stage/reference-study and registry gates, `just codex-context`,
   product/API invariants, `just ci`, exact-head Ubuntu AND Windows CI, independent
   review and cleanup protections. Do not install tools or touch proprietary assets.
5. **Assistant Hub:** separate PR; keep local product/data restrictions, no hidden
   dispatch/provider activation, runtime isolation and all Python/doctor/public-tree
   plus Node syntax/tests gates. Preserve #53/#54 work and exact-head review/CI.
6. **Relayforge:** separate PR; keep development-without-RDC/security precedence,
   isolated explicit CARGO_TARGET_DIR for every local Cargo command, no legacy
   target/release/live runtime, no service/device/grant changes. Hosted CI preferred;
   unavailable/unauthorized release-build or live evidence stays UNVERIFIED.
   Preserve #64/#66/#76/#88, runtime-artifact/recovery and human-local acceptance.

Steps 3–6 depend on canonical acceptance and independently accepted Kit mechanism;
none changes consumer files in this task. Refresh all baselines/PR inventories.
Existing public source.json records are not bundle locks: use reviewed
`source-update plan/write`, full SHAs, installed/old-source checks, fresh digest
and each literal path permission. Preserve license notices, other channel and
local files; explicitly review changed governance record-test hashes. Manual
local/index improvements are separate owned diffs, never added managed paths.
Require empty replan, full diff, native/security CI at exact HEAD and independent
acceptance per repository. No automatic merge/deploy/release or settings mutation.
Rollback uses retained old source/bundle with fresh plan and reviewed PR, never
reset, force-adoption or deletion of evidence. Re-measure each consumer before
claiming savings; all root copies must equal accepted Template bytes after rollout.

## Evidence and retention

Validation: PASS `python3 -B scripts/check_template.py`; PASS 17 unittests;
PASS `git diff --check`; PASS pinned Kit offline pilot (creation, idempotence,
separate channels/rollback, local/native/Draft evidence preservation, drift,
missing/symlink/partial-permission refusal). No dependencies installed.
Canonical managed source is `51e2fb06aed0245096a5b7bacbc937a3eca488d2`;
packaging uses the existing pinned Kit bundle exporter and an immutable source
pin, not the packaging commit. Existing CI runs the checker and full suite on
Python 3.11/3.12/3.13; remote results must be checked at final PR HEAD.

Template integrity and unittests are administrative, not product CI. Product
native toolchain remains UNVERIFIED as before. Negative tests remove always-on
clauses/routes independently of rehashed manifests and prove lifecycle byte
preservation, unchanged managed paths and bundle/root agreement. Existing tests
cover links, drift, unsafe paths, schemas, pins and local-rule freedom.

Retain `/tmp/project-template-progressive` (this task's branch/worktree and Draft
review evidence) until accepted/closed and provenance reviewed. No prior artifacts,
branches, worktrees or caches deleted. The detached pinned Kit pilot checkout `/tmp/progressive-kit-pinned` is test-only
at `21cf2914cb0a1c904ca8c783a36723786373b600`; no Kit source edits. Measured
usage before packaging was 376 KiB (Template worktree) and 184 KiB (Kit checkout).
Retain both for review reproducibility; deletion is deferred until Draft closure
and a fresh ownership/dirty/dependency inventory. Scratch `/tmp/progressive-*`
JSON/body files and `/tmp/implement_progressive.py` are this task's audit/packaging
evidence, retained with the same purpose and decision; do not wildcard-delete.
No new product debt; existing TODO(owner) native-toolchain placeholders remain
explicitly UNVERIFIED. Independent review and merge authority remain pending.

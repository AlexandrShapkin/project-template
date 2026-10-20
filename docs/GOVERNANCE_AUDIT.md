# Issues #6/#7 audit and bounded handoff

Audit date: 2026-10-21. Template base:
`a99f391a7b0deedc1388c51f6d7d8e0e9958c45d`.
Kit accepted main verified via GitHub:
`61a5fde6d146b83add3eaedda2a7d959f924e340`.
No open PRs existed in either upstream. Kit PR #14 is merged, despite older Issue
text calling it Draft. Template's `private=true`, `is_template=true` were verified;
its remote tag inventory was empty, so `v0.1.0` was unused at audit time.
This is preparation, not release qualification or public-history clearance.

## Inventory and actual metadata operations

Read all states with paginated GitHub Issues/PR, label and Milestone GETs.
Before this Draft, Template had 7 Issue/PR records (active Issues #4/#6/#7);
Kit had 15 (active Issues #8/#11/#13/#15). All seven active Issues already had
exactly one priority and suitable type/area/stage. Closed records had incomplete
historical classification; they were intentionally preserved. Both upstreams had
zero Milestones in all states. Stage/milestone rationale is in [the map](ROADMAP.md).

Compared the accepted consumer `rustcraft` `.github/labels.json` (read-only):
retained all 13 shared priority/type/area definitions and their colors/descriptions.
Added four documented upstream stage values; legacy consumer aliases remain
consumer-specific. No consumer metadata or source was modified.

Authorized non-destructive normalization applied to BOTH upstreams:

| Repository | Existing definitions repaired (color/description) | Canonical definitions added | Result |
| --- | --- | --- | --- |
| Template | priority:P1; area:automation/docs; type:maintenance/documentation; stage:distribution/release | Remaining 10 canonical labels | 17 canonical + 10 historical/default labels |
| Kit | priority:P1; area:automation/security; type:maintenance/security; stage:distribution/release/rollout | Remaining 9 canonical labels | 17 canonical + 10 historical/default labels |

Actual operations were only label POSTs and color/description PATCHes. No labels
were renamed/deleted, no existing Issue/PR assignments/bodies were rewritten, and
no milestone, Project, repository setting or permission changed. The new Template
Draft receives priority:P1, type:maintenance, area:automation and stage:release.
The read-only `scripts/check_github_metadata.py --repo OWNER/REPO` report verified
both upstreams' actual definitions and active classifications. It reports all-state
counts and active milestone assignments; stage relevance and milestone N/A remain
human review against the map, not a guessed automated milestone scheduler.

Separate approval would be needed for destructive label operations, historical
reclassification, Project/settings changes or new confirmed milestone creation.
No such operation is needed now. The declarative taxonomy is scaffold outside
the existing six managed paths; Kit #15 must manually adopt it at the reviewed
Template source, preserving documented extensions and native checks.

## Verification limits and remaining coordination

Managed bytes require a new administrative source/package pair, not a change to
wire formats, owners or the independent Kit pins. The original admin source
`adfc75e686f7853a13618ee5858a775000f0a396` and retained artifact remain recoverable
in base history. The private format-2 admin lock/bundle is refreshed using the
already pinned Kit implementation; installed Kit baseline/tooling/format-1 bundle
remain unchanged. No SemVer tag, Release or public format-3 artifact is created.

An actual `codex exec` read-only, ephemeral instruction fixture was attempted with
root AGENTS.md directing a read of AGENTS.local.md and a unique proof marker.
The CLI exited 1 during initialization with filesystem/permission failure;
no marker response was obtained. Actual CLI discovery/compliance is therefore
BLOCKED, not inferred from offline tests. The fixture was removed automatically.
[Official instruction guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
distinguishes discovered AGENTS instructions from agent-directed file reads;
our tests prove explicit references and inherited bytes, not model compliance.
Repeat the isolated probe in a working CLI environment before consumer rollout.

Remaining existing follow-ups (owner: AlexandrShapkin; priority P1):

- [Kit #15](https://github.com/AlexandrShapkin/codex-engineering-kit/issues/15):
  adopt the accepted Template interface/taxonomy via a separate Draft; replace
  legacy policy activation, add Kit's local stage map and pass Kit native CI.
  Until then Kit source still points to its legacy contract; metadata alone does
  not complete inheritance. Kit source is deliberately untouched here.
- [Kit #8](https://github.com/AlexandrShapkin/codex-engineering-kit/issues/8):
  per-consumer Draft migrations, preserve native rules/active work/evidence,
  repeat CLI discovery and obtain exact-head native CI and independent acceptance.
- Template #4/#6 and Kit #11/#13 retain publication/history/rights/license and
  exact-byte package qualification. No public-readiness or native-product PASS
  follows from this administrative PR. Existing stronger restrictions remain.

No new workaround, dependency, disabled test or bypassed gate is introduced.
Shared policy duplication is avoided; unresolved upstream adoption is explicitly
tracked above. Independent ChatGPT review and owner merge authority remain pending.

## Cleanup inventory

Retained: this task's branch and future Draft PR for review; original local
`fix/issue-2-release-status` branch and existing `/tmp/project-template-kit`
checkout plus `/tmp/project-template-smoke-issue-2-20261020` evidence. The Kit
checkout's untracked `.code-graph/` is pre-existing/unknown and untouched.
No task-created persistent worktree or build output is required. Unittest,
CLI-probe and integration-pilot fixtures use bounded TemporaryDirectory cleanup;
the pilot's synthetic active Draft/evidence is confined to its own fixture.
No user branch/worktree, remote resource or historical artifact was deleted;
no reclaimed disk space is claimed. Review retained legacy resources separately
only after ownership, references and recoverability are established.

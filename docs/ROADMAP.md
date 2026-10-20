# Upstream stage map (project-owned)

This navigates existing Issues; acceptance lives in those Issues and their PRs.
Shared rules and taxonomy belong to the [interface](../.github/DEVELOPMENT_INTERFACE.md).
Kit adoption is coordinated through [Kit #15](https://github.com/AlexandrShapkin/codex-engineering-kit/issues/15);
this map is a handoff for its local map, not a change to Kit source.

| Stage ID | Goal | Dependencies | Owning Issues (Template / Kit) | Completion evidence |
| --- | --- | --- | --- | --- |
| foundation | Accepted source and independent offline channels | None | Template #2 (closed); Kit #1, #3, #5, #7, #9 (closed) | Template PRs #1/#3 and Kit PRs #2/#4/#6/#10 merged; historical labels unchanged |
| distribution | Reviewed publication boundaries | foundation | Template #4; Kit #11 | Template #5 and Kit #12 merged; public/license authorization remains separate |
| release | Independent release qualification and shared governance | foundation; distribution before publication | Template #6/#7; Kit #13/#15 | This Draft supplies policy; exact-head CI and independent review required; Kit #14 merged at accepted main |
| rollout | Preserve native rules while adopting reviewed pins | accepted release/governance source and private distribution review | Kit #8 | Separate consumer Draft PRs, native CI and independent acceptance per repository |

Issue links use each upstream's GitHub inventory, not a second backlog.
No Milestones exist in either upstream at the 2026-10-21 audit. Deliberate N/A:
`v0.1.0` is proposed, not a confirmed publication target, and these policy changes
do not establish a dated release/deliverable. Do not create placeholder milestones.
An owner-confirmed deliverable may acquire a matching milestone through an
explicitly authorized metadata update; keep its stage and Issue scope aligned.

Template local release applicability: administrative bundles are usable distribution
and therefore applicable for a significant release, consistent with accepted Kit
release preparation at `61a5fde6d146b83add3eaedda2a7d959f924e340`.
The candidate is an administrative JSON bundle, plus SHA256SUMS and provenance,
for the existing Python 3.11+/POSIX offline Kit workflow; no executable or native
binary is applicable because Template has no runtime. Public-safe packaging,
license and exact-byte publication approval remain BLOCKED under Template #4/#6
and Kit #11. Private format-2 bundles are never public fallback assets. Artifact
names, final hashes and exact-code/platform verification must be reviewed before
release; no unsupported platform or reproducible-build claim is made here.

Template's public compatibility surface is the managed administrative interface,
six managed paths, Task/PR forms, lock/bundle schemas and migration behavior.
The proposed first compatibility range is `>=0.1.0,<0.2.0` for compatible patches;
no release is declared by this proposal. A breaking `0.x` change increments MINOR
with migration/rollback evidence. Wire format integers remain independent.

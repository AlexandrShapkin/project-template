# Template v0.1.0 release candidate

Owning Issue: [#6](https://github.com/AlexandrShapkin/project-template/issues/6).
The shared normative release contract is already implemented in
[the managed interface](../.github/DEVELOPMENT_INTERFACE.md), adopted by Kit and
all four consumers. Kit #8 is CLOSED. This preparation does not repeat that rollout.
Kit owns export/update mechanisms; Template owns administrative policy.

Accepted source baseline: `8f964eda3f530d41f78e776a2087d0b33e570358`.
Kit's independent accepted baseline is
`8f2008dfcfa27ca1e4b4b754baecec29a22e86a0`. Both are PUBLIC/MIT; prior private-source,
unselected-license and pending rollout statements in historical audits are
superseded by accepted publication/migration closeout. Preserve that evidence;
review fresh complete reachable source/history and GitHub surface deltas before
publication. A source license does not approve generated asset bytes.

The full reviewed PR head identifies this candidate in its handoff. A different
accepted merge target needs its own exact-head checks. No `v0.1.0` tag or Release
exists because this document proposes one. Template and Kit versions advance
independently; full source SHAs and per-file/artifact SHA-256 remain authoritative.
Tags must be annotated and immutable; never reuse or move a published tag.

## Compatibility and artifact matrix

The public interface is the six managed administrative paths, lifecycle/local
extension contract, Task/PR forms, ownership, bundle/lock formats and migration
behavior. Compatible first-series patches support `>=0.1.0,<0.2.0`. A breaking
`0.x` change needs a MINOR increment and migration guidance; wire format integers
are independent. Kit pins and Template pins remain separate.

| Asset | Platform / use | Qualification |
| --- | --- | --- |
| `template-v0.1.0-administrative.public-safe.json` | Python 3.11+ / POSIX; six-file administrative format-3 bundle | Exact source-byte review, full independent source/generator/review pins and approved artifact digest. |
| `SHA256SUMS` | Hashes of all approved deliverables and provenance | Verify actual bytes; a downloaded checksum is not publisher authentication. |
| `PROVENANCE.md` and MIT notice | Full source/build/generator/review evidence and attribution | Review exact sidecar bytes; MIT notice remains outside the six managed paths. |

This is usable administrative distribution, not a native executable. There is no
placeholder binary or installer. Private format-2 bundles remain private evidence,
never public fallback assets. No generated artifact is distributed by this PR.

## Qualification and release decision

Run `python3 -B scripts/check_template.py` and the complete native unittest suite.
Require exact-head Python 3.11/3.12/3.13 hosted CI, independent technical ACCEPT,
canonical ownership/MIT/history and fresh GitHub exposure review. Verify all tag
and Release inventories including drafts and candidate ancestry on accepted main.
Check every required file against its canonical Git blob; generate reviewed
candidate bundles twice privately and compare all hashes and sidecars. Exercise
Kit and Template update/idempotence/rollback in disposable repositories with
native/local files and active evidence preserved. Template integrity CI is not
consumer product or platform verification.

Use Kit's existing read-only `scripts/check_release.py --project template` with
actual exact-head native CI evidence. Its private staging mode always returns
`publication_authorized=false`; it is neither a GitHub attestor nor an owner
approval store. Do not manufacture public classification to bypass qualification.

Finalize [narrative notes](RELEASE_NOTES_v0.1.0.md), compatibility and limitations.
**Pending separate owner action:** approve Template v0.1.0's exact full target,
annotation, notes, canonical destination and every named asset digest after
accepted checks/review. Kit v0.1.0 needs its own distinct approval. No tag, Release,
upload, visibility change, automatic merge or deployment is authorized here.
Check annotated object ID, peeled source and downloaded hashes again after any
separately approved release; never overwrite a published tag/asset.

## Rollback and limits

Retain the prior accepted source snapshot, both independent records/bundles and
MIT notices. Revert this preparation normally. For consumer updates restore only
the affected channel through a reviewed revert or fresh plan/write against its
retained older full revision; run native checks/CI again. Conflicts and partial
writes require snapshot recovery/replanning, never forced reset or deleted locks.
Preserve AGENTS.local.md, native CI, product/security rules and unrelated work.

Sync is POSIX and requires a quiescent checkout; per-file replacement is not a
multi-file transaction. SHA-256 is consistency evidence, not source authority.
Real Codex automatic instruction compliance is not established. Existing explicit
local-rule reads, native gates and owner authority remain mandatory.

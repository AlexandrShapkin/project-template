# Public distribution proposal (private staging)

Owning coordination: Engineering Kit Issue #11. This document grants no
publication authority and changes no accepted bundle, tooling pin or private
classification. The canonical administrative lifecycle remains in this repository;
Engineering Kit owns generation, validation and the single sync plan/write engine.
No Template updater or generator is introduced.

The proposed delivery is two independently versioned, immutable JSON release
artifacts generated from exact reviewed Git commits. Canonical repositories remain
private. A distribution repository, if separately authorized, stores generated
release output only: never editable policy or a copy of the private checkout.
Per-consumer delivery uses separate reviewed Draft PRs with both source SHAs and
native exact-head gates. No public repository or release is authorized yet.

The six administrative files are AGENTS.md, .github/DEVELOPMENT_INTERFACE.md,
.github/ISSUE_TEMPLATE/task.yml, .github/pull_request_template.md,
docs/WORKFLOW.md and .project-template/OWNERSHIP.md. The private baseline is
0a53f56dba841675b3203a76e33594fee1a73b9f. Kit's private Issue #11 inventory records
all twelve channel hashes, links, metadata and content classifications. Its
candidate protocol is proposed in Kit's dedicated Draft PR; accepted tooling.json
continues to require the existing private implementation. Do not invoke new flags
on the accepted older pin or replace this pin before independent acceptance.

PUBLIC-SAFE is a content classification, never a license, signature, source
acceptance or owner publication grant. Named bytes require separate owner review
and authorization of the full artifact SHA-256, chosen license, provenance
metadata (including owner/repository names and commit IDs), delivery destination
and release creation. Review input and generated hashes do not prove identity.
Neither publication=public nor relabeling a format-2 manifest is supported.
Private default and its strict checker remain unchanged.

Resolve these blockers in canonical sources and independent review before release:

- No redistribution license or publication approval has been selected.
- Review historical product references in both channels; frozen Kit v0.1 policy
  must not be silently rewritten or activated as a second administrative source.
- OWNERSHIP.md currently states both distributions remain private. A future
  explicitly reviewed source revision must describe any approved exception.
- AGENTS.md requires consumer docs/INDEX.md and AGENTS.local.md; WORKFLOW.md also
  requires UPGRADING.md and PROJECT.md. These are outside the six managed files.
  Review consumer-owned prerequisites separately; do not implicitly add them to
  the public payload or fetch them from a private URL.
- Existing AGENTS.md or development interface is a hard initial collision.
  Migration requires its own reviewed transformation preserving local rules,
  native CI and product stage/architecture docs; never remove a lock to bypass it.

For RustCraft, preserve just status, just codex-context, full just ci and actual
Ubuntu/Windows workflows. A disposable fixture demonstrates collision and byte
preservation only, not Rust build success or consumer acceptance. RustCraft PR #36
is excluded. After pipeline review and separate owner authorization, prepare a
bounded migration Draft PR; no current consumer writes are authorized.

For update or rollback, retain the independently reviewed old/new channel
artifacts. Use only Kit sync plan, inspect changes, then sync write with the exact
plan digest and every exact path permission. New public protocol adoption from a
private lock requires a separate reviewed migration; no implicit conversion.
A partial I/O failure requires restoring a verified pre-update snapshot before
replanning. Native product CI, independent review, owner merge and live proof
remain separate gates.

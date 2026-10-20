# Project setup checklist (project-owned)

- [ ] TODO(owner): name, purpose, intended users, scope and non-goals; replace README.
- [ ] TODO(owner): maintainers, review owner and security contact.
- [ ] TODO(owner): select Kit profile: minimal (undecided toolchain), backend
  (API/data), infrastructure (drift/rollback), research (methods/data provenance).
  Profiles install reference files, not dependencies or execution authority.
- [ ] TODO(owner): native language/toolchain, format/lint/type/test/build commands,
  supported platforms and security gates in AGENTS.local.md and TESTING.md.
- [ ] TODO(owner): replace template-only CI with real native CI; preserve stronger
  gates. Configure branch protection only under separate explicit authorization.
- [ ] TODO(owner): architecture, data boundaries, secret injection and rollback.
- [ ] Consumer adoption: decide this product's visibility, rights and license.
  The template source is MIT; retain its notice. Upstream source visibility
  does not reclassify private bundles or authorize consumer publication.
- [ ] TODO(owner): record reviewed upstream SHAs and retained bundles per UPGRADING.

Template upstream stage navigation and current release applicability:
[roadmap](ROADMAP.md). Replace this project-owned map on adoption; keep canonical
rules in the development interface and native/product choices here.

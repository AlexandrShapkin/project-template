# Project Template v0.1.0 — release candidate, unpublished

Template separates the shared engineering lifecycle from project-owned commands
and product decisions. This first proposed version gives maintainers a named
administrative source and bundle they can review independently of Engineering
Kit's technical references and each product's own version.

- Shared instructions require exact-head native CI, independent review and
  explicit owner merge/release authority. Green checks do not authorize deployment.
- Release policy calls for independent immutable versions, narrative notes,
  project-specific usable artifacts and SHA-pinned provenance. Non-distributable
  milestones may document N/A; placeholder binaries are not required.
- GitHub Issues remain the live task queue. Local rules retain stronger native,
  security and platform requirements; cleanup preserves active work and evidence.

The proposed deliverable is the six-file administrative format-3 bundle with
SHA-256 sums, full source/generator/review provenance and MIT notice. There is
no native runtime or installer. See [qualification](RELEASING.md) for exact gates.
Source is PUBLIC/MIT; no tag, Release or generated asset is published here.
The PR/Issue handoff records the exact candidate SHA and CI/review evidence;
final named asset hashes and separate owner release approval remain required.

Compatible first-series patches support `>=0.1.0,<0.2.0`; breaking `0.x` changes
require a MINOR increment and migration guidance. Adoption uses Python 3.11+ on
POSIX with a quiescent checkout. Template integrity tests are not product tests.
Private legacy bundles are not public fallback assets; hashes do not authenticate
a publisher. Automatic model instruction compliance is not claimed.

Review each consumer update separately. Keep local rules, native CI and the
previous source record/bundle. Roll back only the affected channel using a
reviewed revert or retained older revision plan; resolve collisions explicitly.
Published tags/assets are immutable; corrections need a separately approved patch.

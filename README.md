# project-template

Private, source-only starter for a consistent reviewed development process.
No application framework, runtime, deployment, credentials or license is chosen.

After **Use this template**, replace this title/purpose and complete
[project choices](docs/PROJECT.md). Keep [AGENTS.local.md](AGENTS.local.md) for
native commands and specialized rules. The single shared lifecycle starts at
[AGENTS.md](AGENTS.md) and the [development interface](.github/DEVELOPMENT_INTERFACE.md).
Documentation starts at [docs/INDEX.md](docs/INDEX.md).

Quick start: create a private repository through an owner-authorized template
operation or use the [offline creation procedure](docs/UPGRADING.md). Run
`python3 -B scripts/check_template.py` and
`python3 -B -m unittest discover -s tests -v` with Python 3.11+ on POSIX.
These validate administration only. Select and configure actual native CI before
claiming product verification. The owner enabled GitHub Template repository;
`is_template=true` and private visibility were verified on 2026-10-20.
Use **Use this template → Create a new repository** and select **Private**.

Shared administration is versioned by full template source SHA and hashes in
`.project-template/lock.json`; Kit is pinned independently in
`.engineering-kit/lock.json`. Read [ownership](.project-template/OWNERSHIP.md) and
[controlled updates](docs/UPGRADING.md). GitHub's initial copy alone is not the
update mechanism. No second sync engine is included here.

The retained Engineering Kit baseline is
`f808af695c7787fb68f332d8ff1214fb2100f9b5`. Its historical contracts/skills are
labelled reference/provenance, not automatically activated instructions.
The admin channel implementation was independently accepted and merged in
[Kit PR #10](https://github.com/AlexandrShapkin/codex-engineering-kit/pull/10);
the template was accepted and merged in
[template PR #1](https://github.com/AlexandrShapkin/project-template/pull/1).
The reviewed source SHAs remain pinned intentionally; acceptance does not repin
bundles to merge commits or authorize consumer updates, merges or publication.
See [release verification](docs/VERIFICATION.md) for evidence and limitations.

# Testing (project-owned)

TODO(owner): list actual format, lint, type, unit, integration, build, platform
and security commands with prerequisites and expected outputs. Link them from
AGENTS.local.md and native CI. Product verification is UNVERIFIED until selected.

The template's `python3 -B scripts/check_template.py` checks source links and
managed hashes; its unittest suite checks offline template adoption. These are
administrative checks, not tests of a future product. Kit's suite separately
checks synchronization safety. Never report these as native application CI.

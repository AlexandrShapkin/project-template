# Project-owned agent rules

This file is never synchronized. Add specialized constraints here; do not copy
shared lifecycle text. Read docs/PROJECT.md and docs/ARCHITECTURE.md for context.

- Native toolchain, commands and platform/security gates: TODO(owner), UNVERIFIED.
- This template repository checks: `python3 -B scripts/check_template.py` and
  `python3 -B -m unittest discover -s tests -v`. Replace these with actual native
  gates when adopting; retain template integrity checks while consuming updates.
- Deployment and publication: not authorized. No license has been selected.
- Preserve stronger user/product constraints and user data.

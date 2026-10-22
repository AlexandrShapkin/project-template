# Project-owned agent rules

This file is never synchronized. Add specialized constraints here; do not copy
shared lifecycle text. Read docs/PROJECT.md and docs/ARCHITECTURE.md when
project setup or architecture is relevant.

- Native toolchain, commands and platform/security gates: TODO(owner), UNVERIFIED.
- This template repository checks: `python3 -B scripts/check_template.py` and
  `python3 -B -m unittest discover -s tests -v`. Replace these with actual native
  gates when adopting; retain template integrity checks while consuming updates.
- MIT LICENSE covers owner-controlled template source; retain its notice on adoption.
- Source visibility is owner-authorized after safety/rights checks and independent review/approved merge. Tags, Releases, public bundle uploads and deployment remain separate.
- Preserve stronger user/product constraints and user data.

# Project Template

A lightweight repository starting point for different languages and products.
Copy or use this template, rename the project and customize the small scaffold.

- AGENTS.md holds common agent guidance; AGENTS.local.md holds project constraints.
- docs/PROJECT.md, ARCHITECTURE.md and TESTING.md are optional starting points.
- .github contains basic Issue/PR forms and template integrity CI.
- .editorconfig and .gitignore provide essential development defaults.

Choose your own source layout, native tooling and CI. Replace placeholders and
add the checks appropriate to your product. No application architecture, mandatory
stage lifecycle, managed synchronization or Engineering Kit dependency is imposed.
Engineering Kit independently provides optional development utilities.

Run `python3 -B scripts/check_template.py` and
`python3 -B -m unittest discover -s tests -v` to check the scaffold itself.
These checks do not replace product or security tests in adopted repositories.
Retired governance and synchronization implementation remains in Git history.
Licensed under MIT; see LICENSE and docs/SOURCE_RIGHTS.md.

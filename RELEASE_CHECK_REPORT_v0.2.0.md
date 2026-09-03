# pifira 0.2.0 release-candidate check report

Checked: 2026-09-03 (Asia/Seoul)

This candidate was prepared from public `main` commit
`06f1ea361eb00db86f4d0e7100ad3e298eca1265`. No commit, tag, GitHub release,
PyPI upload, or Zenodo deposit was made during preparation.

## Candidate scope

- Retains the public 0.1.0 LPG inverse-analysis API.
- Adds the `pifira.lh2` namespace for rigid-rotor ortho/para thermodynamics,
  a domain-guarded published natural-conversion correlation, and explicitly
  bounded nozzle comparators.
- Does not package source publications, experimental files, digitized traces,
  derived validation tables, or manuscript-specific audit outputs.
- Lists persistent identifiers, official acquisition locations, evidence use,
  and claim limits in `VALIDATION_SOURCES.md`.

## Completed checks

| Check | Result |
|---|---|
| Package/unit tests in the release virtual environment | PASS, 20/20 |
| Wheel installation and import in a clean virtual environment | PASS |
| Package and module version agreement | PASS, 0.2.0 |
| `twine check` for wheel and sdist | PASS |
| CFF 1.2 schema validation with `cffconvert` | PASS |
| `.zenodo.json` JSON syntax | PASS |
| GitHub Actions workflow YAML syntax | PASS |
| Distribution third-party-data policy audit | PASS for wheel and sdist |
| Git whitespace/error check | PASS; Windows line-ending notices only |

The release workflow repeats the tests, package build, `twine` metadata check,
and distribution data-policy audit before requesting a short-lived PyPI token.
The ordinary test workflow checks Python 3.10, 3.11, 3.12, and 3.13.

## Candidate artifacts

| File | SHA-256 |
|---|---|
| `pifira-0.2.0-py3-none-any.whl` | `970096b12bb7d56d6bebd436d59227c25231e31fd1a9b6178a899e8315eadec6` |
| `pifira-0.2.0.tar.gz` | `51e8cde9ae232610c41b3e24dde0d581d7b3d78ae0d34b6ba79f4dcd4eeb24ca` |

These hashes identify the locally built candidate only. Rebuilding after any
source or packaging change will legitimately produce new hashes; record the
new values before publication.

## Publication gate

Before publishing `v0.2.0`, confirm that GitHub Actions passes on the exact
commit selected for the tag, that the PyPI Trusted Publisher is restricted to
the `pypi` environment and `publish.yml`, and that the Zenodo GitHub switch is
enabled for `lyullee/pifira`. Follow `DEPLOY.md` in order.


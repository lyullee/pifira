# Changelog

All notable changes to `pifira` are recorded here.

## 0.2.0 - release candidate

### Added

- Evidence-gated LH2 rigid-rotor ortho-para thermodynamics.
- Milenko/Petitpas natural-conversion correlation with strict published-domain
  checks enabled by default.
- Ideal-gas and CoolProp HEOS fixed-nozzle comparators.
- Validation-source registry containing original DOI/official-source links,
  evidence boundaries and selected source fingerprints, but no third-party
  data.
- Distribution audit that blocks common validation-data and document formats
  from wheel and source archives.
- Current GitHub, Zenodo and PyPI release instructions.

### Changed

- Corrected damaged mathematical symbols and page ranges in the README.
- Raised the declared minimum Python version to 3.10. Version 0.1.0 used
  Python 3.10 union syntax while incorrectly declaring Python 3.9 support.
- Expanded CI to Python 3.10-3.13 and added build/archive verification.
- Updated citation and Zenodo metadata for the broader scope.

### Unchanged boundaries

- No experimental or validation data are distributed.
- The LH2 API is not a certified PSV sizing model and does not infer missing
  commercial-valve geometry, lift or capacity.

## 0.1.0 - 2026-08-29

- Initial public release of the LPG pressure-rise and radiative-area toolkit.
- Archived version DOI: <https://doi.org/10.5281/zenodo.22162093>.

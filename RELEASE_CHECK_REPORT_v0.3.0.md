# pifira 0.3.0 release-candidate check report

Checked: 2026-09-04 (Asia/Seoul)

## Outcome

The `0.3.0` candidate passed its release checks and was published on
2026-09-04. GitHub tag `v0.3.0` resolves to commit
`00c61233d754ca0b5257899e7ffe2938f0204736`.

## Scope of the release

- Existing LPG and `0.2.0` LH2 APIs remain available.
- New state-point and pathwise para-composition thresholds are public.
- A one-sided composition-allowance feasibility check is public.
- A transparent equilibrium-direction path ledger and saturation crossover
  calculation are public.
- The API does not calculate, certify or reduce pressure-relief-device
  capacity.

## Reproducibility and numerical checks

- Python: 3.13.9 (Anaconda distribution)
- Test result: **26 passed**
- Version declarations: `pyproject.toml`, `pifira.__version__`,
  `CITATION.cff` and `.zenodo.json` all report `0.3.0`.
- The public API was independently compared with the authoritative manuscript
  audit JSON at 50 psia. Absolute differences were zero for:
  - state-point para threshold;
  - full-path para threshold from 20.3 K;
  - 99.7%-para initial adverse inventory;
  - 99.7%-para target signed heat; and
  - saturation crossover pressure.
- A wheel-installed smoke test returned `pifira.__version__ == "0.3.0"` and
  `-5.219330 kJ kg-1` for the 99.7%-para target-state ledger value.

## Built artifacts

Artifacts are in `release_dist/v0.3.0/`.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `pifira-0.3.0-py3-none-any.whl` | 21,589 | `c0403e51f39d8dca97cae2fd402e63f407d0fd27815c353396782d337ebeb632` |
| `pifira-0.3.0.tar.gz` | 35,511 | `ff6c25bd419dd7545441a40e789ef41fb1393a48289bdbeee67778cd93f717c0` |

- `twine check`: **PASS** for both artifacts.
- Distribution-policy audit: **PASS** for both artifacts.
- Wheel member count: 14; sdist member count: 41.
- Forbidden data/document/media/archive files: 0.
- Private-reproduction bundle references or contents: 0.

## Third-party-data boundary

No experimental files, source publications, digitized traces, derived
validation tables, manuscript figures, or reproduction archives are included
in the Git candidate, wheel, or source archive. Public documentation lists
original sources and claim boundaries only.

A separate local-only archive was created outside the Git repository:

`06_논문화/JLPPI_OP_PSV/PIFIRA_JLPPI_REPRODUCTION_PRIVATE_DO_NOT_UPLOAD_2026-09-04.zip`

- Archive size: 2,414,664,256 bytes
- ZIP entries: 271
- Manifest-controlled inputs: 80 (2,326.35 MiB)
- Missing manifest inputs: 0
- SHA-256 mismatches: 0
- ZIP CRC test: PASS
- Public-release-repository entries inside the private archive: 0
- Archive SHA-256:
  `3fbd328f3917ca51b4138f32dd545d4040e2ec16bc01eaa8ba9ddc33a02c1e34`

The private archive contains third-party material and must not be uploaded to
GitHub, Zenodo, PyPI or a public journal supplement.

## Post-release verification

- GitHub release: <https://github.com/lyullee/pifira/releases/tag/v0.3.0>
- GitHub tests workflow: PASS on Python 3.10, 3.11, 3.12 and 3.13.
- GitHub publish workflow: PASS.
- PyPI: <https://pypi.org/project/pifira/0.3.0/>
- Clean installation from the PyPI Simple Index: PASS.
- Installed pathwise threshold at 50 psia: `99.79505843112076%` para.
- PyPI wheel SHA-256:
  `66d53e8301aec0d4381e0d791188e62794f0b4a7fa438310bd0871b627cf8ea4`
- PyPI sdist SHA-256:
  `265e9b42822f18f63c2b2686a46fcd4d5c248aa9b2421043f3fbf935606f8eb0`
- Zenodo version DOI: <https://doi.org/10.5281/zenodo.22291661>
- Zenodo concept DOI: <https://doi.org/10.5281/zenodo.22162092>

The version DOI can now replace `<VERSION_DOI>` in the manuscript availability
statement. No public release contains the private reproduction archive.

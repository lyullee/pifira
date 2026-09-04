# Validation-source registry

Updated 2026-09-04 for the `pifira` 0.3.0 release candidate.

## Distribution policy

This repository records provenance only. It does **not** distribute any
third-party source document, spreadsheet, presentation, image, raw record,
digitized trace, or derived validation table. A DOI or URL in this file is a
pointer to the original provider; it does not grant a new licence or override
the provider's terms.

Users who repeat a study-specific comparison should:

1. obtain the material from the original location below;
2. record the download date, source version and licence or access terms;
3. calculate a SHA-256 fingerprint of the acquired file;
4. store it under a local `validation-data/` directory, which is ignored by
   this repository; and
5. describe any transcription or graph digitization as source-derived rather
   than raw experimental data.

The hashes listed below identify exact source copies reviewed during the
associated study. They are provenance fingerprints, not redistributed files.

## Ortho-para hydrogen evidence

| ID | Original source | Quantity used | Admission boundary | Reviewed SHA-256 |
|---|---|---|---|---|
| OP-1 | G. Petitpas et al., *Int. J. Hydrogen Energy* 39 (2014) 6533-6547, [doi:10.1016/j.ijhydene.2014.01.205](https://doi.org/10.1016/j.ijhydene.2014.01.205) | Rigid-rotor equations, printed Milenko rate law, Raman histories | Some history points are graph-derived; successful cases do not establish universal reverse-conversion validity | `3087f2d34d6a94141f5404edc2ccd33218ac0718c0c4b7ce4d4aea8d73b7c9ed` |
| OP-2 | Y.Y. Milenko et al., *J. Low Temp. Phys.* 107 (1997) 77-92, [doi:10.1007/BF02396837](https://doi.org/10.1007/BF02396837) | Primary natural-conversion correlation and original fitted domain | Do not extrapolate beyond the documented phase, temperature, density or composition domain | not assigned |
| OP-3 | G.M. Sellner et al., *PRX Energy* 5 (2026) 013010, [doi:10.1103/lf6d-nnr8](https://doi.org/10.1103/lf6d-nnr8) | Independent natural o-to-p rate measurements | Apparatus-transfer check only; no universal correction factor | `6e99ffc106cf06ce941eea20773f1e3684d551472f7fb527e92500b1134f9810` |

## LH2 tank and thermal-boundary evidence

| ID | Original source | Quantity used | Admission boundary | Reviewed SHA-256 |
|---|---|---|---|---|
| TK-1 | O. Kartuzova et al., NASA NTRS 20240016283, [official NTRS record](https://ntrs.nasa.gov/citations/20240016283); N.T. Van Dresar et al., NASA TM-105411, [official NTRS record](https://ntrs.nasa.gov/citations/19920009200) | K-Site pressure-rise conditions, temperature locations and heat distribution | Cross-condition tank challenge; current quantitative tank gate remains closed | `2801c5695f2253d69d0f0be41b65fa9febf8f83ff01004b63642602f59fdef6d` (2025 paper); `91775f3185f280847c5fc27cc086517cc7d8fd8db32d5bfd5deda0a79f109e78` (TM-105411) |
| TK-2 | J.C. Aydelott, NASA TN D-3742 (1967), [official NTRS record](https://ntrs.nasa.gov/citations/19670009809) | 21 pressure-rise tests and 17 energy partitions | Establishes heat-location sensitivity; no coefficient transfer to another tank | `ad30620fc98cddf90410a9b7f1f8325540dd5ac80fc2a500b793df26f5069efe` |
| TK-3 | J.C. Aydelott, NASA TN D-3256 (1966), [official NTRS record](https://ntrs.nasa.gov/citations/19660007756) | Constant-pressure outflow and no-flow heat checks | Forward challenge only; not PSV validation | `d1157d05913d042ba8b2b36137bb41468dc6b6a6cd57b8dd046fbc31f81bd322` |
| TK-4 | J.C. Aydelott and C.M. Spuckler, NASA TN D-5263 (1969), [official NTRS record](https://ntrs.nasa.gov/citations/19690018242) | Vented-tank pressure, temperatures and released mass | Manual vent tests without valve lift; mass/energy challenge only | `101dadd887f14a2542fc739df09bd21ea7642e28bb550c30836d2c7d5ced4419` |
| TK-5 | C. Wan et al., CEC/ICMC 2025 C1Or4C-07, [official Indico record and presentation](https://indico.cern.ch/event/1431974/contributions/6396821/) | Four passive pressure histories and seven synchronized temperatures in a 500 L horizontal LH2 tank | Graph-derived source/EOS consistency check; no fitted horizontal-tank validation | `0fc36ce43d011ba6ca55c559dce02d46ca49d87dcc50928e7c48601be6647c7f` |
| TK-6 | C. Wan et al., *Int. J. Hydrogen Energy* 152 (2025) 149399, [doi:10.1016/j.ijhydene.2025.05.029](https://doi.org/10.1016/j.ijhydene.2025.05.029); related design article, [doi:10.1016/j.ijrefrig.2024.10.037](https://doi.org/10.1016/j.ijrefrig.2024.10.037) | Geometry, instrumentation and supplementary LH2 temperature/level evidence | The design article's self-pressurization tests use LN2; do not relabel them as hydrogen validation | `79bcfbabcd69cbcd6325238f356c152895e0e64fde4dc18a632379150213351f` (design article) |
| TK-7 | K. Tani et al., ICHS 2019 ID172, [official HySafe paper](https://hysafe.info/uploads/papers/2019/172.pdf) | 30 m3 LH2 depressurization pressure, temperature and vent-mass evidence | Manually operated vent; registered as a future large-scale challenge | `bc264f5296b1f9a9e0524a0d074ed2c06faa7e723b99094b31a98c9dadf8721e` |

## Fixed-nozzle hydrogen datasets

| ID | Original source | Quantity used | Admission boundary |
|---|---|---|---|
| NZ-1 | T. Jordan et al., PRESLHY E3.1 part A, KIT dataset [doi:10.35097/1187](https://doi.org/10.35097/1187) | 22 warm and 22 cold fixed-nozzle blowdowns | Supports a 300 K to 80 K cold-gas outlet-model transfer only; not LH2 or a reclosable PSV |
| NZ-2 | A. Friedrich et al., PRESLHY E3.1 part B, KIT dataset [doi:10.35097/1317](https://doi.org/10.35097/1317) | Five nominally 290 K fixed-nozzle blowdowns | Warm-gas implementation check only |

The deposited KIT directories and internal filenames should be preserved
exactly. They are large third-party datasets and are deliberately absent from
GitHub, Zenodo and PyPI.

## Valve and relief-device evidence

| ID | Original source | Quantity used | Admission boundary | Reviewed SHA-256 |
|---|---|---|---|---|
| RV-1 | Y.M. Seo et al., *Results in Engineering* 28 (2025) 107328, [doi:10.1016/j.rineng.2025.107328](https://doi.org/10.1016/j.rineng.2025.107328) | HV-SV-02 opening/reseat pressure cycles and valve-inlet temperature | No public orifice, lift or open-state mass-flow history; no capacity inference | source article retained by original provider |
| RV-2 | M. Carolan et al., DOT/FRA/ORD-24/20 (2024), [official ROSA-P record](https://rosap.ntl.bts.gov/view/dot/73150) | Cryogenic PRV pressure, flow, density and repeated operation | LN2 system without measured disk lift; not hydrogen capacity | `8d43cf7cc35fa57dc0f28dbbfbd8b2c3bac666a20359c289fa0f94ce96d8dc68` |
| RV-3 | W. Elmayyah and W. Dempster, *Proc. IMechE Part E* 227 (2013) 42-55, [doi:10.1177/0954408912453407](https://doi.org/10.1177/0954408912453407), [institutional record](https://strathprints.strath.ac.uk/42272/) | Nine warm-air fixed-lift mass-flow points | Supports geometry-aware lift-to-area interpretation only; no cryogenic or commercial-valve transfer | `59cdf635a37a88cc186f09cb91ebc505128d5536244f3542e4c0b23b13582bf4` |
| RV-4 | HEROSE Types 06012 and 06440 manufacturer datasheets, available from the [manufacturer download centre](https://www.herose.com/en/downloads/) | Published orifice areas, coefficients and standard-air ratings | Unit and implementation check; manufacturer rating is not independent measured LH2 capacity | source-version hashes retained in the study audit |
| RV-5 | NASA low-leakage relief-valve campaigns, [2022 NTRS record](https://ntrs.nasa.gov/citations/20220007253) and [2023 NTRS record](https://ntrs.nasa.gov/citations/20230017263) | Cryogenic cracking, reseat, cycling and post-closure leakage | Piloted valve and gaseous test media; leakage is not open-valve capacity | source-version hashes retained in the study audit |
| RV-6 | National Board NB-18 listing, [official live directory](https://buscenter.nationalboard.org/TestLab/nb-18) | Mt.H manufacturer/design-level certified K entries | Separate SC 32/SP 32 designs cannot be assigned to HV-SV-02 | live record; record the access date |

## Claim boundary retained with the source registry

The source inventory supports the directly observed Petitpas full-scale
dormancy benefit, bounded statements about published OP kinetics,
heat-location sensitivity, cold-gas fixed-nozzle transfer,
commercial-valve traceability, and cryogenic opening/reseat behavior. It does
not support:

- an HV-SV-02 orifice, lift law, discharge coefficient or open-state flow;
- certified two-phase LH2 relief capacity;
- a universal OP kinetic relation or generally transferable LH2 tank model;
- a quantitatively validated coupled tank-PSV transient or a generic
  standards-capacity reduction factor; or
- replacement of ISO/API/ASME/KGS procedures or manufacturer certification.

The missing synchronized LH2 pressure-temperature-lift-mass-flow dataset is an
explicit evidence gap when cycling, chatter or partial-opening dynamics are
the intended claim; it is not a parameter to be filled by assumption. A
scenario relief-demand calculation may instead remain separate from the
certified device-capacity and installation checks.

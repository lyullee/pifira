# pifira 0.2.0

Version 0.2.0 retains the complete 0.1.0 LPG inverse-analysis API and adds a
separate `pifira.lh2` namespace for evidence-gated research utilities.

Highlights:

- parity-resolved rigid-rotor ortho-para equilibrium and conversion energy;
- the published Milenko/Petitpas rate expression with strict domain guards;
- ideal-gas and CoolProp HEOS fixed-nozzle comparators;
- explicit warnings against treating component checks as coupled LH2 PSV
  validation or certified capacity;
- a source-only validation registry; and
- automated release-archive checks that reject third-party data and document
  formats.

This release intentionally excludes all source PDFs, spreadsheets,
presentations, figure images, digitized traces and derived validation tables.
Obtain third-party material from the original links in
`VALIDATION_SOURCES.md` and keep it outside version control.

Compatibility note: the minimum supported Python version is now 3.10. The
public 0.1.0 code already used syntax introduced in Python 3.10 despite its
metadata declaring Python 3.9.

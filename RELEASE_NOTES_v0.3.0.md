# pifira 0.3.0

Version 0.3.0 adds the composition and equilibrium-path screens used by the
LH2 ortho--para credit framework while retaining the complete LPG and 0.2.0
LH2 APIs.

Highlights:

- separate state-point and full-path para-fraction thresholds;
- a one-sided measurement-allowance feasibility check;
- a transparent 99.7%-para equilibrium-path energy ledger;
- crossover temperature and saturated-pressure calculation;
- a data-free example reproducing the 50 psia paper landmarks; and
- explicit separation of thermodynamic screening, experiment-specific
  dormancy credit and standards-facing device-capacity decisions.

At 50 psia, the default 20.3 K calculation gives 98.9565% para for the
state-point sign boundary and 99.7951% para for the full-path non-heating
criterion. A 99.7%-para batch has +0.667 kJ/kg initial adverse inventory,
crosses sign near 134.6 kPa(abs), and reaches -5.219 kJ/kg at 50 psia.

These quantities are equilibrium-direction thermodynamic potentials. Realized
heat requires a qualified kinetic and system path. This release does not
calculate, certify or reduce pressure-relief-device capacity.

No experimental data, source documents, digitized traces, derived validation
tables or manuscript outputs are included. Original sources and claim limits
remain listed in `VALIDATION_SOURCES.md`.

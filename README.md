# pifira

[![PyPI](https://img.shields.io/pypi/v/pifira)](https://pypi.org/project/pifira/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22162092.svg)](https://doi.org/10.5281/zenodo.22162092)
[![tests](https://github.com/lyullee/pifira/actions/workflows/tests.yml/badge.svg)](https://github.com/lyullee/pifira/actions/workflows/tests.yml)

**P**ressure-based **I**nverse **F**ire-heat-flux and **R**adiative-**A**rea
analysis, with evidence-gated liquid-hydrogen utilities.

`pifira` is a research toolkit for two related process-safety workflows:

1. estimating heat input and effective flame-contact area from pressure and
   wall-temperature histories of pressurized LPG tanks; and
2. evaluating traceable liquid-hydrogen (LH2) ortho-para thermodynamics,
   state-point and pathwise composition screens, published Milenko/Petitpas
   kinetics, and a CoolProp HEOS nozzle closure.

> **No experimental or validation data are distributed in the repository,
> source archive, or wheel.** The validation material belongs to its original
> publishers and depositors. [`VALIDATION_SOURCES.md`](https://github.com/lyullee/pifira/blob/main/VALIDATION_SOURCES.md)
> identifies the original DOI or official download page, the evidence used,
> and the limits of each comparison.

## Installation

```bash
python -m pip install pifira
```

Python 3.10 or newer is required. Plotting support is optional:

```bash
python -m pip install "pifira[plot]"
```

## LPG inverse-analysis example

```python
import pifira

tank = pifira.TankSpec(
    volume=0.619,
    fluid="HEOS::Propane[0.95]&n-Butane[0.05]",
    fill=0.70,
)

heat_W = pifira.heat_input(
    P1_bar=10.83,
    P2_bar=16.30,
    dt=544.5,
    tank=tank,
)

arc = pifira.effective_arc(
    angles_deg=[0, 90, 180, -90],
    T_wall_C=[271, 49, 39, 46],
    T_amb_C=35.0,
)["arc_deg"]

height = pifira.effective_height(flame_height_m=0.767, liquid_height_m=0.885)
area = pifira.effective_area(diameter_m=0.75, arc_deg=arc, height_m=height)
print(pifira.heat_flux(heat_W, area), "kW/m2")
```

The pressure-rise calculation uses a closed-vessel interval before relief
venting. The internal energy is evaluated with CoolProp while total mass and
vessel volume remain fixed. The effective circumferential width is obtained
from a Gaussian fit to the radiative driving force
`T_wall^4 - T_ambient^4`.

## LH2 evidence-gated example

```python
from pifira.lh2 import MilenkoCorrelation, RigidRotorSpinThermo

thermo = RigidRotorSpinThermo()
print(thermo.equilibrium_ortho(20.3))
print(thermo.conversion_energy_J_per_kg(20.3))

kinetics = MilenkoCorrelation()
k = kinetics.forward_rate_per_s(
    temperature_K=20.3,
    density_kg_m3=70.0,
    phase="liquid",
)
print(k, "1/s")
```

The LH2 functions enforce the reported temperature, density, phase and
composition domains by default. They do not constitute a certified relief
valve sizing method. In particular, the package does not infer a discharge
coefficient, effective area, lift law or two-phase capacity for a commercial
PSV from pressure cycling alone.

### State-point and full-path OP criteria

The state at relief and the complete warming path are deliberately separate
claims. The following data-free calculation reproduces the 50 psia landmarks
used in the associated method paper:

```python
from pifira.lh2 import (
    apply_para_composition_allowance,
    equilibrium_path_ledger,
    required_para_fraction_for_nonheating,
    required_para_fraction_for_pathwise_nonheating,
)

pressure_Pa = 50.0 * 6894.757293168
state_point = required_para_fraction_for_nonheating(pressure_Pa)
full_path = required_para_fraction_for_pathwise_nonheating(
    pressure_Pa, initial_temperature_K=20.3
)
adjusted, feasible = apply_para_composition_allowance(full_path, 0.1)
ledger = equilibrium_path_ledger(0.003, pressure_Pa)  # 99.7% para

print(100 * state_point)  # 98.9565% para at the relief state
print(100 * full_path)    # 99.7951% para over the declared path
print(100 * adjusted, feasible)
print(ledger["crossover_pressure_kPa_abs"])  # 134.6 kPa(abs)
```

The ledger is an equilibrium-direction accounting result. It neither predicts
realized conversion heat without a kinetic path nor authorizes a reduction in
standards-required or certified relief capacity. See
[`examples/lh2_pathwise_credit.py`](examples/lh2_pathwise_credit.py).

## Public API

| Area | Public objects |
|---|---|
| LPG pressure rise | `TankSpec`, `internal_energy`, `liquid_height`, `heat_input`, `heat_input_series` |
| Effective area | `radiative_driving_force`, `effective_arc`, `effective_height`, `effective_area`, `heat_flux` |
| Representative values | `heat_input_weighted_mean`, `simple_mean`, `coverage_fraction`, `normalized_flux`, `pressurization_number`, `orientation_factor` |
| File input | `load_pressure_csv`, `load_temperature_csv` |
| LH2 spin thermodynamics | `pifira.lh2.RigidRotorSpinThermo` |
| LH2 composition credit screens | `required_para_fraction_for_nonheating`, `required_para_fraction_for_pathwise_nonheating`, `apply_para_composition_allowance`, `equilibrium_path_ledger` |
| LH2 published kinetics | `pifira.lh2.MilenkoCorrelation`, `pifira.lh2.CorrelationDomainError` |
| LH2 nozzle utility | `pifira.lh2.HEOSNozzleLookup`, `pifira.lh2.heos_nozzle_lookup` |

## Validation-data policy

Only source metadata and acquisition instructions are versioned. The project
does not redistribute source PDFs, spreadsheets, presentation files, figure
rasters, digitized traces, or derived validation tables. Users who reproduce a
comparison must obtain the material from the original source, comply with its
terms, and keep it outside version control. See
[`VALIDATION_SOURCES.md`](https://github.com/lyullee/pifira/blob/main/VALIDATION_SOURCES.md).

Package releases are checked automatically for common third-party data and
document formats before PyPI publication.

## Scope and safety

`pifira` is research software. It is not an ISO 21013, API 520/521, ASME or
KGS design implementation, and it must not replace certified sizing,
manufacturer capacity data, or engineering review. A successful numerical
reproduction means that the code regenerated a reported result; it does not by
itself establish physical validation or fitness for safety-critical use.

## Citation and release history

Use [`CITATION.cff`](https://github.com/lyullee/pifira/blob/main/CITATION.cff)
and cite the archived Zenodo release. Version 0.3.0 is archived at
[doi:10.5281/zenodo.22291661](https://doi.org/10.5281/zenodo.22291661). The
badge above uses the concept DOI, which resolves to the newest archived
version. Changes are listed in
[`CHANGELOG.md`](https://github.com/lyullee/pifira/blob/main/CHANGELOG.md).

## License

The software is released under the
[MIT License](https://github.com/lyullee/pifira/blob/main/LICENSE). Third-party source
material is not covered by that license and is not included.

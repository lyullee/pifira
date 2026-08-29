# pifira

**P**ressure-based **I**nverse **F**ire-heat-flux and **R**adiative-**A**rea analysis

A data-agnostic Python toolkit for estimating **fire heat input** and
**effective flame-contact area** for pressurized LPG tanks under **localized
(non-engulfing) flame exposure**.

pifira combines the **closed-vessel pressure-rise method** (heat input from a
measured pressure history) with a **radiative (T?? weighted angular-temperature
inversion** (effective fire-contact area from surface temperatures), and
provides a **dimensionless framework** that unifies localized and
full-engulfment exposure across tank sizes, fill levels and orientations.

> **No experimental data are bundled with this package.** All routines operate
> on user-supplied arrays. See [Data sources](#data-sources) for how to obtain
> the public validation datasets.

---

## Why

Most published fire-engulfment work assumes *uniform, full engulfment* of
*horizontal* tanks. Small **vertical** LPG tanks under *localized* flame
exposure are under-studied, and standards (API 521, KGS) do not cover heat-input
estimation for this case. pifira addresses this by inverting a measured
pressure rise for heat input and a measured angular temperature distribution
for the effective contact area ??without assuming full engulfment.

## Installation

```bash
pip install pifira
```

Dependencies: `numpy`, `scipy`, `pandas`, `CoolProp`. Optional plotting extras:

```bash
pip install "pifira[plot]"
```

## Quick start

```python
import numpy as np
import pifira

# 1. Define the tank (volume, fluid, fill fraction)
tank = pifira.TankSpec(
    volume=0.619,
    fluid="HEOS::Propane[0.95]&n-Butane[0.05]",
    fill=0.70,
)

# 2. Heat input from a pressure history (bring your own arrays)
#    t [s], P [bar gauge], closed-vessel window before PRV opens
Q_W = pifira.heat_input(P1_bar=10.83, P2_bar=16.30, dt=544.5, tank=tank)
print(Q_W / 1000, "kW")

# 3. Effective contact area from angular wall temperatures
#    flame centre at 0 deg; off-flame points at +/-90, 180
res = pifira.effective_arc(
    angles_deg=[0, 90, 180, -90],
    T_wall_C=[271, 49, 39, 46],   # period-averaged wall temps
    T_amb_C=35.0,
)
arc_deg = res["arc_deg"]          # area-preserving equivalent width

h_eff = pifira.effective_height(flame_height_m=0.767, liquid_height_m=0.885)
A_eff = pifira.effective_area(diameter_m=0.75, arc_deg=arc_deg, height_m=h_eff)

# 4. Heat flux
print(pifira.heat_flux(Q_W, A_eff), "kW/m^2")
```

A full time-varying workflow (moving-window heat input, per-instant effective
arc, heat-input-weighted representative value) is in
[`examples/analyze_localized.py`](examples/analyze_localized.py).

## Public API

| Area | Functions |
|---|---|
| Heat input (pressure-rise) | `TankSpec`, `internal_energy`, `liquid_height`, `heat_input`, `heat_input_series` |
| Effective area (inversion) | `radiative_driving_force`, `effective_arc`, `effective_height`, `effective_area`, `heat_flux` |
| Representative value | `heat_input_weighted_mean`, `simple_mean` |
| Dimensionless framework | `coverage_fraction` (?), `normalized_flux` (q\*), `pressurization_number` (?), `orientation_factor` (Ω) |
| I/O | `load_pressure_csv`, `load_temperature_csv` |

## Method summary

1. **Closed-vessel pressure-rise.** Before pressure-relief venting, incident
   heat converts entirely into the contents' internal-energy rise:
   `Q = dU/dt = d/dt(m_L u_L + m_V u_V)`. Mass and volume are fixed; the
   liquid/vapour split is re-flashed at each pressure (CoolProp).

2. **Radiative (T?? angular inversion.** Radiative flux scales with
   `T_wall????T_amb?? (Stefan-Boltzmann). Angular wall temperatures are fit
   with a Gaussian; the area-preserving equivalent width `??2?)·?` gives the
   effective arc.

3. **Axial intersection.** Effective height = min(flame contact height, wetted
   liquid height). Vapour-space wall is excluded.

4. **Representative value.** Heat-input-weighted mean `Σ(q·Q)/ΣQ`, since fire
   safety is governed by high-heat-input instants.

5. **Dimensionless framework.** ? (coverage), q\* (normalized flux), ?
   (pressurization), Ω (orientation) unify localized/full and vertical/horizontal.

## Data sources

pifira ships **no data**. The public datasets used to validate the method in
the associated study are available from their original publications:

- **Moodie, K., Billinge, K., Cutler, D.P. (1988).** *Fire Engulfment of LPG
  Storage Tanks.* IChemE Symposium Series No. 93, pp. 87??06. Institution of
  Chemical Engineers. ??pressure history (Fig. 5) and initial conditions /
  heat fluxes (Tables 1??). Obtain from IChemE or a library.

- **Birk, A.M., Poirier, D., Davison, C. (2006).** *On the thermal rupture of
  1.9 m³ propane pressure vessels with defects in their thermal protection
  system.* Journal of Loss Prevention in the Process Industries **19**(6),
  582??97. https://doi.org/10.1016/j.jlp.2006.02.002 ??pressure (Fig. 8) and
  lading-temperature stratification (Fig. 10) for the 25% partial-engulfment
  test. Obtain from the publisher.

To reproduce the validation, digitize the relevant figures from the original
papers and pass the values to the pifira API. Digitized values are **not**
redistributed here.

Experimental data from the authors' own fire tests are **not** included and are
reported separately.

## Citing

If you use pifira, please cite it via [`CITATION.cff`](CITATION.cff) and the
archived release DOI (Zenodo). See the repository release page for the DOI.

## License

MIT ??see [LICENSE](LICENSE).

## Author

Woo-gui-yeon Lee, Korea Gas Safety Corporation (KGS), AI Safety Research Team
([ORCID 0009-0008-8976-5363](https://orcid.org/0009-0008-8976-5363)).

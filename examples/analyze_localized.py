#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: full localized-exposure heat-flux workflow with pifira.

This reproduces the time-varying analysis:
  moving-window heat input  x  per-instant radiative-weighted effective arc
  x  axial intersection  ->  heat-input-weighted representative flux.

No data are bundled. Provide your own pressure/temperature CSVs via the
command line:

    python analyze_localized.py PRESSURE.csv TEMPERATURE.csv

Pressure CSV : columns [idx, datetime, seconds, pressure_bar]
Temperature  : columns [idx, datetime, seconds, CH1..CH10]
              with the flame-facing sensors identified by *temperature*
              (hottest = flame side), not by any label.

Sensor angular layout used here (edit to match your rig):
    0 deg   = flame centre   (hottest circumferential sensor)
   +90 deg  = top   (12 o'clock)
   180 deg  = rear  (opposite the flame)
   -90 deg  = bottom (6 o'clock)     <-- note: bottom, not a side sensor
"""

import sys
import numpy as np

import pifira


# ----- rig-specific configuration (edit for your setup) -------------------
DIAMETER_M = 0.75
VOLUME_M3 = 0.619
FLUID = "HEOS::Propane[0.95]&n-Butane[0.05]"
FILL = 0.70
CYL_LENGTH_M = 1.150

T_START, T_END = 205.5, 750.0        # closed-vessel window [s]
T_AMB_C = 35.0
FLAME_HEIGHT_M = CYL_LENGTH_M * (2 / 3)   # observed flame contact height

# circumferential angle -> channel name (assign from your rig geometry)
CIRC = {0: "CH3", 90: "CH1", 180: "CH7", -90: "CH5"}


def main(pressure_csv, temperature_csv):
    A_sec = np.pi / 4 * DIAMETER_M**2
    V_head = np.pi / 24 * DIAMETER_M**3

    t_p, P = pifira.load_pressure_csv(pressure_csv)
    t_t, dft = pifira.load_temperature_csv(temperature_csv)

    tank = pifira.TankSpec(volume=VOLUME_M3, fluid=FLUID, fill=FILL)
    m_tot = tank.initial_mass(P[np.searchsorted(t_p, T_START)])

    _, Q = pifira.heat_input_series(t_p, P, tank, window=60, m_tot=m_tot)

    i0, i1 = np.searchsorted(t_p, T_START), np.searchsorted(t_p, T_END)
    ql, Ql, widths = [], [], []
    for i in range(i0, i1, 4):
        Qi = Q[i]
        if not np.isfinite(Qi):
            continue
        idx = np.searchsorted(t_t, t_p[i])
        angles = list(CIRC.keys())
        temps = [dft[CIRC[a]].iloc[idx] for a in angles]
        try:
            arc = pifira.effective_arc(angles, temps, T_amb_C=T_AMB_C)["arc_deg"]
        except Exception:
            continue
        h_liq = pifira.liquid_height(P[i], m_tot, tank, A_sec, V_head)
        h_eff = pifira.effective_height(FLAME_HEIGHT_M, h_liq)
        A = pifira.effective_area(DIAMETER_M, arc, h_eff)
        ql.append(pifira.heat_flux(Qi, A))
        Ql.append(Qi)
        widths.append(arc)

    q_rep = pifira.heat_input_weighted_mean(ql, Ql)
    print(f"total mass         : {m_tot:.1f} kg")
    print(f"effective arc (var): {min(widths):.0f}-{max(widths):.0f} deg "
          f"(mean {np.mean(widths):.0f})")
    print(f"heat-input weighted: {q_rep:.1f} kW/m^2   <- representative")
    print(f"simple mean        : {pifira.simple_mean(ql):.1f} kW/m^2")
    print(f"instantaneous max  : {max(ql):.1f} kW/m^2")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

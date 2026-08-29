"""
pifira.pressure_rise
====================
Closed-vessel pressure-rise method for fire heat-input estimation.

The core physics: for a sealed vessel (constant mass and volume) exposed to
fire before any pressure-relief venting, the incident heat is converted
entirely into the internal-energy rise of the two-phase contents:

    Q = dU/dt = d/dt ( m_L u_L + m_V u_V )

By tracking total mass and internal energy at each pressure and calling a
two-phase equilibrium flash, the heat-input rate Q is recovered from a
measured pressure history alone.

This module is data-agnostic: the caller supplies pressure-time arrays and
tank/fluid parameters. No experimental data are bundled.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

try:
    from CoolProp.CoolProp import PropsSI
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "pifira requires CoolProp. Install with: pip install CoolProp"
    ) from exc


P_ATM_BAR = 1.01325


@dataclass
class TankSpec:
    """Geometry and fluid specification for a pressurized tank.

    Parameters
    ----------
    volume : float
        Internal volume [m^3].
    fluid : str
        CoolProp fluid string, e.g. ``"HEOS::Propane"`` or a mixture like
        ``"HEOS::Propane[0.95]&n-Butane[0.05]"``.
    fill : float
        Initial liquid fill fraction by volume (0-1).
    """

    volume: float
    fluid: str = "HEOS::Propane"
    fill: float = 0.70

    def initial_mass(self, P_bar_gauge: float) -> float:
        """Total contents mass [kg] at a given initial gauge pressure."""
        p = (P_bar_gauge + P_ATM_BAR) * 1e5
        VL = self.fill * self.volume
        VV = (1.0 - self.fill) * self.volume
        rho_L = PropsSI("D", "P", p, "Q", 0, self.fluid)
        rho_V = PropsSI("D", "P", p, "Q", 1, self.fluid)
        return VL * rho_L + VV * rho_V


def internal_energy(P_bar_gauge: float, m_tot: float, tank: TankSpec) -> float:
    """Two-phase internal energy U [J] under closed-vessel constraint.

    The liquid/vapour split is redistributed at each pressure so that total
    mass ``m_tot`` and total volume ``tank.volume`` are conserved.
    """
    p = (P_bar_gauge + P_ATM_BAR) * 1e5
    rho_L = PropsSI("D", "P", p, "Q", 0, tank.fluid)
    rho_V = PropsSI("D", "P", p, "Q", 1, tank.fluid)
    u_L = PropsSI("U", "P", p, "Q", 0, tank.fluid)
    u_V = PropsSI("U", "P", p, "Q", 1, tank.fluid)
    V_L = (m_tot - tank.volume * rho_V) / (rho_L - rho_V)
    return V_L * rho_L * u_L + (tank.volume - V_L) * rho_V * u_V


def liquid_height(P_bar_gauge: float, m_tot: float, tank: TankSpec,
                  cross_section: float, head_volume: float = 0.0) -> float:
    """Dynamic liquid height [m] in the cylindrical section.

    Parameters
    ----------
    cross_section : float
        Horizontal cross-sectional area of the cylinder [m^2].
    head_volume : float
        Volume of the bottom head below the cylinder [m^3] (default 0).
    """
    p = (P_bar_gauge + P_ATM_BAR) * 1e5
    rho_L = PropsSI("D", "P", p, "Q", 0, tank.fluid)
    rho_V = PropsSI("D", "P", p, "Q", 1, tank.fluid)
    V_L = (m_tot - tank.volume * rho_V) / (rho_L - rho_V)
    return max(0.0, (V_L - head_volume) / cross_section)


def heat_input(P1_bar: float, P2_bar: float, dt: float,
               tank: TankSpec, m_tot: float | None = None) -> float:
    """Average heat-input rate Q [W] over a closed-vessel window.

    Q = (U(P2) - U(P1)) / dt, with mass fixed at its initial value.

    Parameters
    ----------
    P1_bar, P2_bar : float
        Gauge pressures at the start and end of the window [bar].
    dt : float
        Duration of the window [s].
    tank : TankSpec
    m_tot : float, optional
        Total mass [kg]. If omitted, computed from ``P1_bar``.
    """
    if m_tot is None:
        m_tot = tank.initial_mass(P1_bar)
    dU = internal_energy(P2_bar, m_tot, tank) - internal_energy(P1_bar, m_tot, tank)
    return dU / dt


def heat_input_series(t: np.ndarray, P_bar: np.ndarray, tank: TankSpec,
                      window: int = 60, m_tot: float | None = None
                      ) -> tuple[np.ndarray, np.ndarray]:
    """Instantaneous heat-input rate Q(t) [W] via a moving-window slope.

    A local linear fit of pressure over +/- ``window`` samples gives dP/dt,
    which is converted to dU/dt through the equation of state.

    Returns
    -------
    t_out, Q_out : np.ndarray
        Times and instantaneous heat-input rates (NaN where the window
        does not fit).
    """
    t = np.asarray(t, float)
    P_bar = np.asarray(P_bar, float)
    if m_tot is None:
        m_tot = tank.initial_mass(P_bar[0])

    Q = np.full(len(P_bar), np.nan)
    for i in range(len(P_bar)):
        if i < window or i + window >= len(P_bar):
            continue
        a, b = np.polyfit(t[i - window:i + window], P_bar[i - window:i + window], 1)
        Pc = a * t[i] + b
        dUdP = (internal_energy(Pc + 0.05, m_tot, tank)
                - internal_energy(Pc - 0.05, m_tot, tank)) / 0.1
        Q[i] = dUdP * a
    return t, Q

"""
pifira.representative
=====================
Representative heat-flux estimators and the dimensionless framework.

For a time-varying heat flux q(t) driven by a time-varying heat input Q(t),
the physically meaningful design value weights instants by how much heat
actually entered the vessel (a heat-input-weighted mean), because fire safety
is governed by the high-heat-input instants.

The dimensionless framework expresses localized-exposure heat flux in a form
independent of tank size, fill level and orientation.
"""

from __future__ import annotations

import numpy as np

Q_ENGULF_DEFAULT = 100.0  # reference full-engulfment heat flux [kW/m^2]


def heat_input_weighted_mean(q, Q):
    """Heat-input-weighted mean flux: sum(q*Q) / sum(Q).

    Parameters
    ----------
    q : array-like
        Instantaneous heat flux [kW/m^2].
    Q : array-like
        Instantaneous heat-input rate [W] (weights).
    """
    q = np.asarray(q, float)
    Q = np.asarray(Q, float)
    mask = np.isfinite(q) & np.isfinite(Q)
    return float(np.sum(q[mask] * Q[mask]) / np.sum(Q[mask]))


def simple_mean(q):
    """Plain time-average of instantaneous flux [kW/m^2]."""
    q = np.asarray(q, float)
    return float(np.nanmean(q))


# --------------------------------------------------------------------------
# Dimensionless framework
# --------------------------------------------------------------------------
def coverage_fraction(A_eff, A_wetted):
    """phi = A_eff / A_wetted  (fire coverage fraction; 1 = full engulfment)."""
    return A_eff / A_wetted


def normalized_flux(q_local, q_engulf=Q_ENGULF_DEFAULT):
    """q* = q_local / q_engulf (dimensionless heat flux)."""
    return q_local / q_engulf


def pressurization_number(dPdt, volume, Q_engulf_W):
    """Pi = (dP/dt * V) / Q_engulf (dimensionless pressurization rate)."""
    return (dPdt * volume) / Q_engulf_W


def orientation_factor(liquid_height_m, diameter_m):
    """Omega = h_liq / D (orientation factor; vertical > 1, horizontal < 1)."""
    return liquid_height_m / diameter_m

"""
pifira.effective_area
=====================
Inverse estimation of the effective fire-contact area from surface-temperature
measurements under localized (non-engulfing) flame exposure.

Two directions are treated independently:

* Circumferential -- wall temperatures at several angular positions are
  weighted by their radiative driving force (Stefan-Boltzmann, T^4) and fit
  with a Gaussian. The area-preserving equivalent width sqrt(2*pi)*sigma gives
  the effective arc.
* Axial -- the flame-contact height intersected with the wetted (liquid) part
  of the wall; vapour-space wall above the liquid level is excluded because it
  contributes negligibly to pressurization.

The effective contact area is the product of the effective arc length and the
effective height. All routines are data-agnostic.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit

KELVIN = 273.15


def _gaussian(theta, amp, sigma):
    return amp * np.exp(-theta**2 / (2.0 * sigma**2))


def radiative_driving_force(T_wall_C, T_amb_C=35.0):
    """Radiative driving force (T_wall^4 - T_amb^4) with temperatures in degC.

    Returns the value in K^4. This is the physically correct weight for a
    radiation-dominated fire, rather than the plain temperature rise.
    """
    return (np.asarray(T_wall_C) + KELVIN) ** 4 - (T_amb_C + KELVIN) ** 4


def effective_arc(angles_deg, T_wall_C, T_amb_C=35.0, sigma0=40.0):
    """Effective circumferential arc [deg] from angular wall temperatures.

    Parameters
    ----------
    angles_deg : array-like
        Circumferential angles of the sensors [deg], flame centre at 0.
        Include the flame-facing point (0 deg) and off-flame points
        (e.g. +/-90, 180). At least three distinct angles are needed.
    T_wall_C : array-like
        Wall temperatures at those angles [degC] (period-averaged or
        instantaneous).
    T_amb_C : float
        Ambient temperature [degC].
    sigma0 : float
        Initial guess for the Gaussian standard deviation [deg].

    Returns
    -------
    dict with keys:
        ``sigma`` : fitted standard deviation [deg]
        ``arc_deg`` : area-preserving equivalent width sqrt(2*pi)*sigma [deg]
        ``fwhm_deg`` : full width at half maximum 2.355*sigma [deg]
    """
    ang = np.asarray(angles_deg, float)
    drive = radiative_driving_force(T_wall_C, T_amb_C)
    if np.max(drive) <= 0:
        raise ValueError("Non-positive radiative driving force; check inputs.")
    popt, _ = curve_fit(_gaussian, ang, drive,
                        p0=[float(np.max(drive)), sigma0], maxfev=10000)
    sigma = abs(popt[1])
    return {
        "sigma": sigma,
        "arc_deg": np.sqrt(2.0 * np.pi) * sigma,
        "fwhm_deg": 2.355 * sigma,
    }


def effective_height(flame_height_m, liquid_height_m):
    """Effective axial height [m] = min(flame contact, wetted liquid).

    Vapour-space wall above the liquid level is excluded.
    """
    return min(flame_height_m, liquid_height_m)


def effective_area(diameter_m, arc_deg, height_m):
    """Effective fire-contact area [m^2].

    A_eff = pi * D * (arc/360) * height
    """
    arc_length = np.pi * diameter_m * (arc_deg / 360.0)
    return arc_length * height_m


def heat_flux(Q_W, area_m2):
    """Heat flux [kW/m^2] from heat-input rate [W] and area [m^2]."""
    return Q_W / area_m2 / 1000.0

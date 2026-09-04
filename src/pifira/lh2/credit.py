"""Thermodynamic admission screens for ortho--para credit in LH2 studies.

The functions in this module distinguish a sign test at one saturated state
from a non-heating guarantee over a declared saturated path.  They return
equilibrium-direction potentials only.  Realized heat, pressure response,
dormancy and relief demand additionally depend on kinetics and system boundary
conditions.

Nothing in this module calculates or reduces certified pressure-relief-device
capacity.  Device capacity and installation remain separate standard- and
manufacturer-governed checks.
"""

from __future__ import annotations

from typing import Any

import CoolProp.CoolProp as CP
import numpy as np
from scipy.optimize import brentq

from .spin import RigidRotorSpinThermo


DEFAULT_FLUID = "ParaHydrogen"
DEFAULT_FILL_TEMPERATURE_K = 20.3


def _positive_finite(value: float, name: str) -> float:
    value = float(value)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return value


def saturation_state(
    pressure_Pa: float,
    fluid: str = DEFAULT_FLUID,
) -> tuple[float, float]:
    """Return saturation temperature and latent enthalpy at ``pressure_Pa``.

    Returns
    -------
    temperature_K, latent_enthalpy_J_per_kg
        CoolProp HEOS saturation properties for the selected fluid.
    """
    pressure_Pa = _positive_finite(pressure_Pa, "pressure_Pa")
    temperature_K = float(CP.PropsSI("T", "P", pressure_Pa, "Q", 0, fluid))
    h_liquid = float(CP.PropsSI("Hmass", "P", pressure_Pa, "Q", 0, fluid))
    h_vapor = float(CP.PropsSI("Hmass", "P", pressure_Pa, "Q", 1, fluid))
    return temperature_K, h_vapor - h_liquid


def required_para_fraction_for_nonheating(
    pressure_Pa: float,
    thermo: RigidRotorSpinThermo | None = None,
    fluid: str = DEFAULT_FLUID,
) -> float:
    """Return the para-fraction threshold for a sign test at one state.

    At the specified saturated state, equilibration releases heat when the
    actual ortho fraction exceeds the equilibrium fraction and absorbs heat
    when it is lower.  This threshold does not guarantee the same direction at
    earlier states on a warming path.
    """
    thermo = RigidRotorSpinThermo() if thermo is None else thermo
    temperature_K, _ = saturation_state(pressure_Pa, fluid)
    return 1.0 - float(thermo.equilibrium_ortho(temperature_K))


def required_para_fraction_for_pathwise_nonheating(
    pressure_Pa: float,
    initial_temperature_K: float = DEFAULT_FILL_TEMPERATURE_K,
    thermo: RigidRotorSpinThermo | None = None,
    fluid: str = DEFAULT_FLUID,
    grid_points: int = 801,
) -> float:
    """Return a conservative para threshold over a saturated path.

    The returned value is one minus the minimum equilibrium ortho fraction
    encountered between ``initial_temperature_K`` and the saturated relief
    state.  A batch ortho upper bound no larger than that minimum has no
    exothermic equilibrium direction anywhere on the declared path.
    """
    thermo = RigidRotorSpinThermo() if thermo is None else thermo
    initial_temperature_K = _positive_finite(
        initial_temperature_K, "initial_temperature_K"
    )
    grid_points = int(grid_points)
    if grid_points < 2:
        raise ValueError("grid_points must be at least two")
    relief_temperature_K, _ = saturation_state(pressure_Pa, fluid)
    temperatures_K = np.linspace(
        initial_temperature_K, relief_temperature_K, grid_points
    )
    equilibrium_ortho = np.asarray(
        thermo.equilibrium_ortho(temperatures_K), dtype=float
    )
    return 1.0 - float(np.min(equilibrium_ortho))


def apply_para_composition_allowance(
    required_para_fraction: float,
    allowance_percentage_points: float,
) -> tuple[float, bool]:
    """Add a one-sided absolute composition allowance.

    The allowance is supplied in para percentage points, not as a relative
    percentage.  The result is ``(adjusted_fraction, physically_feasible)``.
    Values above one are returned rather than clipped so infeasibility remains
    visible to the caller.
    """
    required = float(required_para_fraction)
    allowance = float(allowance_percentage_points)
    if not np.isfinite(required) or not 0.0 <= required <= 1.0:
        raise ValueError("required_para_fraction must be within [0, 1]")
    if not np.isfinite(allowance) or allowance < 0.0:
        raise ValueError("allowance_percentage_points must be finite and nonnegative")
    adjusted = required + allowance / 100.0
    return adjusted, adjusted <= 1.0


def signed_equilibrium_heat_J_per_kg(
    ortho_fraction: float,
    pressure_Pa: float,
    thermo: RigidRotorSpinThermo | None = None,
    fluid: str = DEFAULT_FLUID,
) -> float:
    """Return heat released (+) or absorbed (-) upon state equilibration."""
    thermo = RigidRotorSpinThermo() if thermo is None else thermo
    ortho_fraction = float(ortho_fraction)
    if not np.isfinite(ortho_fraction) or not 0.0 <= ortho_fraction <= 1.0:
        raise ValueError("ortho_fraction must be finite and within [0, 1]")
    temperature_K, _ = saturation_state(pressure_Pa, fluid)
    equilibrium_ortho = float(thermo.equilibrium_ortho(temperature_K))
    conversion_energy = float(
        thermo.conversion_energy_J_per_kg(temperature_K)
    )
    return (ortho_fraction - equilibrium_ortho) * conversion_energy


def crossover_saturation_state(
    ortho_fraction: float,
    thermo: RigidRotorSpinThermo | None = None,
    fluid: str = DEFAULT_FLUID,
) -> tuple[float, float] | None:
    """Return ``(temperature_K, pressure_Pa)`` where equilibrium equals a batch.

    ``None`` is returned when no crossing exists over the subcritical
    saturation range or when the fraction is exactly zero or one.
    """
    thermo = RigidRotorSpinThermo() if thermo is None else thermo
    ortho_fraction = float(ortho_fraction)
    if not np.isfinite(ortho_fraction) or not 0.0 <= ortho_fraction <= 1.0:
        raise ValueError("ortho_fraction must be finite and within [0, 1]")
    if ortho_fraction in {0.0, 1.0}:
        return None
    triple_K = float(CP.PropsSI("Ttriple", fluid)) + 1.0e-4
    critical_K = float(CP.PropsSI("Tcrit", fluid)) - 1.0e-4
    low = float(thermo.equilibrium_ortho(triple_K)) - ortho_fraction
    high = float(thermo.equilibrium_ortho(critical_K)) - ortho_fraction
    if low * high > 0.0:
        return None
    temperature_K = float(
        brentq(
            lambda value: float(thermo.equilibrium_ortho(value))
            - ortho_fraction,
            triple_K,
            critical_K,
        )
    )
    pressure_Pa = float(CP.PropsSI("P", "T", temperature_K, "Q", 0, fluid))
    return temperature_K, pressure_Pa


def equilibrium_path_ledger(
    ortho_fraction: float,
    pressure_Pa: float,
    initial_temperature_K: float = DEFAULT_FILL_TEMPERATURE_K,
    thermo: RigidRotorSpinThermo | None = None,
    fluid: str = DEFAULT_FLUID,
    grid_points: int = 801,
) -> dict[str, Any]:
    """Return a transparent equilibrium-direction energy ledger.

    The ledger separates initial adverse inventory, reverse-conversion
    capacity created by warming, and the signed contrast at the relief state.
    These are thermodynamic potentials; realized heat requires a kinetic path.
    """
    thermo = RigidRotorSpinThermo() if thermo is None else thermo
    ortho_fraction = float(ortho_fraction)
    if not np.isfinite(ortho_fraction) or not 0.0 <= ortho_fraction <= 1.0:
        raise ValueError("ortho_fraction must be finite and within [0, 1]")
    initial_temperature_K = _positive_finite(
        initial_temperature_K, "initial_temperature_K"
    )
    relief_temperature_K, latent_J_per_kg = saturation_state(
        pressure_Pa, fluid
    )
    initial_equilibrium_ortho = float(
        thermo.equilibrium_ortho(initial_temperature_K)
    )
    relief_equilibrium_ortho = float(
        thermo.equilibrium_ortho(relief_temperature_K)
    )
    initial_conversion_energy = float(
        thermo.conversion_energy_J_per_kg(initial_temperature_K)
    )
    relief_conversion_energy = float(
        thermo.conversion_energy_J_per_kg(relief_temperature_K)
    )
    initial_signed = (
        ortho_fraction - initial_equilibrium_ortho
    ) * initial_conversion_energy
    target_signed = (
        ortho_fraction - relief_equilibrium_ortho
    ) * relief_conversion_energy
    warming_reverse_capacity = max(
        0.0,
        (relief_equilibrium_ortho - initial_equilibrium_ortho)
        * relief_conversion_energy,
    )
    path_para_requirement = required_para_fraction_for_pathwise_nonheating(
        pressure_Pa,
        initial_temperature_K,
        thermo,
        fluid,
        grid_points,
    )
    path_ortho_limit = 1.0 - path_para_requirement
    crossing = crossover_saturation_state(ortho_fraction, thermo, fluid)
    return {
        "initial_temperature_K": initial_temperature_K,
        "relief_pressure_kPa_abs": float(pressure_Pa) / 1000.0,
        "relief_saturation_temperature_K": relief_temperature_K,
        "initial_ortho_fraction": ortho_fraction,
        "initial_equilibrium_ortho_fraction": initial_equilibrium_ortho,
        "relief_equilibrium_ortho_fraction": relief_equilibrium_ortho,
        "initial_adverse_inventory_kJ_per_kg": max(initial_signed, 0.0)
        / 1000.0,
        "warming_reverse_capacity_kJ_per_kg": warming_reverse_capacity
        / 1000.0,
        "target_signed_equilibrium_heat_kJ_per_kg": target_signed / 1000.0,
        "target_sign": (
            "releases heat"
            if target_signed > 0.0
            else "absorbs heat"
            if target_signed < 0.0
            else "neutral"
        ),
        "target_positive_latent_equivalent_percent": 100.0
        * max(target_signed, 0.0)
        / latent_J_per_kg,
        "state_point_nonheating": ortho_fraction
        <= relief_equilibrium_ortho,
        "pathwise_nonheating": ortho_fraction <= path_ortho_limit + 1.0e-15,
        "crossover_temperature_K": None if crossing is None else crossing[0],
        "crossover_pressure_kPa_abs": None
        if crossing is None
        else crossing[1] / 1000.0,
        "qualification": (
            "equilibrium-direction ledger; realized heat requires a kinetic path"
        ),
    }


__all__ = [
    "DEFAULT_FILL_TEMPERATURE_K",
    "DEFAULT_FLUID",
    "apply_para_composition_allowance",
    "crossover_saturation_state",
    "equilibrium_path_ledger",
    "required_para_fraction_for_nonheating",
    "required_para_fraction_for_pathwise_nonheating",
    "saturation_state",
    "signed_equilibrium_heat_J_per_kg",
]

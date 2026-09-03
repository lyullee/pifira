"""One-dimensional hydrogen nozzle comparators.

The HEOS lookup is a homogeneous-equilibrium, isentropic, single-inlet-state
comparator. It is useful for fixed-nozzle model selection; it is not a PSV
capacity certificate and does not represent valve lift, piping losses or
commercial-valve geometry.
"""

from __future__ import annotations

from functools import lru_cache

import CoolProp.CoolProp as CP
import numpy as np


class NozzleDomainError(ValueError):
    """Raised when a nozzle lookup would extrapolate its tabulated domain."""


def ideal_gas_nozzle(
    pressure_Pa: float,
    temperature_K: float,
    back_pressure_Pa: float,
    gas_constant_J_kgK: float,
    gamma: float,
) -> tuple[float, float, float, bool]:
    """Return ideal-gas isentropic nozzle mass flux and throat state.

    The upstream pressure and temperature are treated as stagnation values.
    The returned tuple is ``(mass_flux, throat_pressure, throat_temperature,
    choked)``. Mass flux is in kg/(m2 s).
    """
    values = (
        pressure_Pa,
        temperature_K,
        back_pressure_Pa,
        gas_constant_J_kgK,
        gamma,
    )
    if not np.all(np.isfinite(values)):
        raise ValueError("Finite nozzle inputs required")
    if min(values[:4]) <= 0 or gamma <= 1:
        raise ValueError("Positive nozzle inputs and gamma > 1 required")
    if back_pressure_Pa >= pressure_Pa:
        return 0.0, pressure_Pa, temperature_K, False
    critical_ratio = (2.0 / (gamma + 1.0)) ** (gamma / (gamma - 1.0))
    pressure_ratio = max(back_pressure_Pa / pressure_Pa, critical_ratio)
    factor = 2.0 * gamma / (gamma - 1.0) * (
        pressure_ratio ** (2.0 / gamma)
        - pressure_ratio ** ((gamma + 1.0) / gamma)
    )
    mass_flux = (
        pressure_Pa
        / np.sqrt(gas_constant_J_kgK * temperature_K)
        * np.sqrt(max(0.0, factor))
    )
    return (
        float(mass_flux),
        pressure_Pa * pressure_ratio,
        temperature_K * pressure_ratio ** ((gamma - 1.0) / gamma),
        back_pressure_Pa / pressure_Pa <= critical_ratio,
    )


class HEOSNozzleLookup:
    """Cached mass-flux table parameterized by pressure and vapor superheat.

    The default table covers 0-105 K superheat and upstream pressures from the
    larger of 60 kPa or back pressure through 800 kPa. Evaluation outside that
    domain raises :class:`NozzleDomainError`; values are never silently
    extrapolated.
    """

    def __init__(
        self,
        fluid: str = "ParaHydrogen",
        back_pressure_Pa: float = 101325.0,
        pressure_points: int = 54,
        superheat_points: int = 58,
        downstream_points: int = 56,
    ) -> None:
        if not np.isfinite(back_pressure_Pa) or not 0 < back_pressure_Pa < 8.0e5:
            raise ValueError("back_pressure_Pa must be within (0, 800000) Pa")
        if min(pressure_points, superheat_points, downstream_points) < 4:
            raise ValueError("At least four grid points are required per dimension")
        self.fluid = fluid
        self.back_pressure_Pa = float(back_pressure_Pa)
        self.pressure_Pa = np.linspace(
            max(6.0e4, self.back_pressure_Pa), 8.0e5, pressure_points
        )
        self.superheat_K = np.linspace(0.0, 105.0, superheat_points)
        table_shape = (len(self.superheat_K), len(self.pressure_Pa))
        self.mass_flux_kg_m2_s = np.zeros(table_shape)
        self.throat_pressure_Pa = np.broadcast_to(
            self.pressure_Pa, table_shape
        ).copy()
        self.throat_temperature_K = np.zeros(table_shape)

        for pressure_index, pressure in enumerate(self.pressure_Pa):
            saturation_temperature = CP.PropsSI(
                "T", "P", pressure, "Q", 1, fluid
            )
            for superheat_index, superheat in enumerate(self.superheat_K):
                temperature = saturation_temperature + superheat
                self.throat_temperature_K[
                    superheat_index, pressure_index
                ] = temperature
                if pressure <= self.back_pressure_Pa * (1.0 + 1e-10):
                    continue
                if superheat == 0.0:
                    stagnation_enthalpy = CP.PropsSI(
                        "Hmass", "P", pressure, "Q", 1, fluid
                    )
                    stagnation_entropy = CP.PropsSI(
                        "Smass", "P", pressure, "Q", 1, fluid
                    )
                else:
                    stagnation_enthalpy = CP.PropsSI(
                        "Hmass", "P", pressure, "T", temperature, fluid
                    )
                    stagnation_entropy = CP.PropsSI(
                        "Smass", "P", pressure, "T", temperature, fluid
                    )
                downstream_pressure = np.geomspace(
                    self.back_pressure_Pa,
                    pressure * (1.0 - 1e-8),
                    downstream_points,
                )
                entropy = np.full_like(downstream_pressure, stagnation_entropy)
                density = CP.PropsSI(
                    "Dmass", "P", downstream_pressure, "Smass", entropy, fluid
                )
                enthalpy = CP.PropsSI(
                    "Hmass", "P", downstream_pressure, "Smass", entropy, fluid
                )
                mass_flux = density * np.sqrt(
                    np.maximum(0.0, 2.0 * (stagnation_enthalpy - enthalpy))
                )
                throat_index = int(np.nanargmax(mass_flux))
                self.mass_flux_kg_m2_s[
                    superheat_index, pressure_index
                ] = mass_flux[throat_index]
                self.throat_pressure_Pa[
                    superheat_index, pressure_index
                ] = downstream_pressure[throat_index]
                self.throat_temperature_K[
                    superheat_index, pressure_index
                ] = CP.PropsSI(
                    "T",
                    "P",
                    downstream_pressure[throat_index],
                    "Smass",
                    stagnation_entropy,
                    fluid,
                )

    def _coordinates(self, pressure_Pa: float, temperature_K: float):
        if not np.all(np.isfinite([pressure_Pa, temperature_K])):
            raise ValueError("Finite pressure and temperature required")
        if pressure_Pa <= self.back_pressure_Pa:
            return None
        if not self.pressure_Pa[0] <= pressure_Pa <= self.pressure_Pa[-1]:
            raise NozzleDomainError(
                f"pressure must be within {self.pressure_Pa[0]:g}-"
                f"{self.pressure_Pa[-1]:g} Pa"
            )
        saturation_temperature = CP.PropsSI(
            "T", "P", pressure_Pa, "Q", 1, self.fluid
        )
        superheat = temperature_K - saturation_temperature
        if not self.superheat_K[0] <= superheat <= self.superheat_K[-1]:
            raise NozzleDomainError(
                "upstream state must be saturated vapor or have 0-105 K superheat"
            )
        pressure_index = int(np.searchsorted(self.pressure_Pa, pressure_Pa) - 1)
        superheat_index = int(np.searchsorted(self.superheat_K, superheat) - 1)
        pressure_index = max(0, min(pressure_index, len(self.pressure_Pa) - 2))
        superheat_index = max(
            0, min(superheat_index, len(self.superheat_K) - 2)
        )
        pressure_fraction = (
            (pressure_Pa - self.pressure_Pa[pressure_index])
            / (
                self.pressure_Pa[pressure_index + 1]
                - self.pressure_Pa[pressure_index]
            )
        )
        superheat_fraction = (
            (superheat - self.superheat_K[superheat_index])
            / (
                self.superheat_K[superheat_index + 1]
                - self.superheat_K[superheat_index]
            )
        )
        return (
            pressure_index,
            superheat_index,
            float(pressure_fraction),
            float(superheat_fraction),
        )

    @staticmethod
    def _interpolate(table, coordinates) -> float:
        pressure_index, superheat_index, pressure_fraction, superheat_fraction = (
            coordinates
        )
        return float(
            table[superheat_index, pressure_index]
            * (1.0 - pressure_fraction)
            * (1.0 - superheat_fraction)
            + table[superheat_index, pressure_index + 1]
            * pressure_fraction
            * (1.0 - superheat_fraction)
            + table[superheat_index + 1, pressure_index]
            * (1.0 - pressure_fraction)
            * superheat_fraction
            + table[superheat_index + 1, pressure_index + 1]
            * pressure_fraction
            * superheat_fraction
        )

    def evaluate(
        self, pressure_Pa: float, temperature_K: float
    ) -> tuple[float, float, float, bool]:
        """Return HEOS mass flux, throat pressure, temperature and choke flag."""
        coordinates = self._coordinates(pressure_Pa, temperature_K)
        if coordinates is None:
            return 0.0, pressure_Pa, temperature_K, False
        mass_flux = self._interpolate(self.mass_flux_kg_m2_s, coordinates)
        throat_pressure = self._interpolate(self.throat_pressure_Pa, coordinates)
        throat_temperature = self._interpolate(
            self.throat_temperature_K, coordinates
        )
        return (
            mass_flux,
            throat_pressure,
            throat_temperature,
            throat_pressure > self.back_pressure_Pa * 1.002,
        )


@lru_cache(maxsize=8)
def heos_nozzle_lookup(
    fluid: str = "ParaHydrogen", back_pressure_Pa: float = 101325.0
) -> HEOSNozzleLookup:
    """Return a cached default HEOS lookup for one fluid and back pressure."""
    return HEOSNozzleLookup(fluid, back_pressure_Pa)

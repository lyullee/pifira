"""Evidence-traceable ortho-para hydrogen submodels.

Thermodynamic equilibrium and rotational energies follow the parity-resolved
rigid-rotor partition functions reported by Petitpas et al. (2014). The rate
expression reproduces their transcription of the Milenko et al. correlation.
The primary rate regression used 0.62-0.75 ortho fraction and is not a
validated low-ortho reverse-conversion law.

Separate ParaHydrogen and OrthoHydrogen property calls can use different
energy zeros. Their native enthalpies or internal energies must not be
subtracted unless a common reference has been established explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


class CorrelationDomainError(ValueError):
    """Raised when a published correlation is asked to extrapolate."""


@dataclass(frozen=True)
class RigidRotorSpinThermo:
    """Ideal rigid-rotor spin thermodynamics with parity-resolved levels.

    Parameters
    ----------
    gas_constant_J_kgK:
        Specific gas constant on the hydrogen mass basis.
    gap_J_per_kg:
        J=1 minus J=0 rotational energy difference.
    maximum_J:
        Highest rotational level retained in the partition sums.

    Notes
    -----
    The result is a spectroscopic ideal-rotor contribution. It is not a
    dense-fluid para/ortho mixture equation of state.
    """

    gas_constant_J_kgK: float = 4124.0
    gap_J_per_kg: float = 702000.0
    maximum_J: int = 40

    def __post_init__(self) -> None:
        if not np.isfinite(self.gas_constant_J_kgK) or self.gas_constant_J_kgK <= 0:
            raise ValueError("Positive finite gas constant required")
        if not np.isfinite(self.gap_J_per_kg) or self.gap_J_per_kg <= 0:
            raise ValueError("Positive finite J=1/J=0 gap required")
        if self.maximum_J < 8:
            raise ValueError("maximum_J must retain enough higher rotational levels")

    @property
    def rotational_temperature_K(self) -> float:
        return self.gap_J_per_kg / (2.0 * self.gas_constant_J_kgK)

    def _moments(self, temperature_K, odd: bool):
        temperature_K = np.asarray(temperature_K, dtype=float)
        if np.any(~np.isfinite(temperature_K)) or np.any(temperature_K <= 0):
            raise ValueError("Positive finite temperature required")
        levels_J = np.arange(1 if odd else 0, self.maximum_J + 1, 2, dtype=float)
        level_energy_index = levels_J * (levels_J + 1.0)
        weights = (2.0 * levels_J + 1.0) * np.exp(
            -self.rotational_temperature_K
            * level_energy_index
            / temperature_K[..., None]
        )
        if odd:
            weights *= 3.0
        partition = np.sum(weights, axis=-1)
        mean = np.sum(weights * level_energy_index, axis=-1) / partition
        second = np.sum(weights * level_energy_index**2, axis=-1) / partition
        return partition, mean, second

    def equilibrium_ortho(self, temperature_K):
        """Return equilibrium ortho mole/mass fraction."""
        para_partition = self._moments(temperature_K, odd=False)[0]
        ortho_partition = self._moments(temperature_K, odd=True)[0]
        return ortho_partition / (para_partition + ortho_partition)

    def rotational_energy_J_per_kg(self, temperature_K, species: str):
        """Return rotational energy relative to the para J=0 ground state."""
        if species not in {"para", "ortho"}:
            raise ValueError("species must be 'para' or 'ortho'")
        mean = self._moments(temperature_K, odd=species == "ortho")[1]
        return self.gas_constant_J_kgK * self.rotational_temperature_K * mean

    def rotational_cv_J_per_kgK(self, temperature_K, species: str):
        """Return the temperature derivative of rotational energy."""
        if species not in {"para", "ortho"}:
            raise ValueError("species must be 'para' or 'ortho'")
        temperature_K = np.asarray(temperature_K, dtype=float)
        _, mean, second = self._moments(
            temperature_K, odd=species == "ortho"
        )
        variance = np.maximum(0.0, second - mean**2)
        return (
            self.gas_constant_J_kgK
            * self.rotational_temperature_K**2
            * variance
            / temperature_K**2
        )

    def conversion_energy_J_per_kg(self, temperature_K):
        """Return E_rot,ortho - E_rot,para on a common J=0 reference."""
        return self.rotational_energy_J_per_kg(
            temperature_K, "ortho"
        ) - self.rotational_energy_J_per_kg(temperature_K, "para")

    def d_conversion_energy_dT_J_per_kgK(self, temperature_K):
        """Return the temperature derivative of conversion energy."""
        return self.rotational_cv_J_per_kgK(
            temperature_K, "ortho"
        ) - self.rotational_cv_J_per_kgK(temperature_K, "para")


@dataclass(frozen=True)
class MilenkoCorrelation:
    """Milenko natural-conversion correlation transcribed by Petitpas et al.

    Density is supplied in kg/m3 and converted internally to g/cm3, the unit
    used in the printed correlation. ``strict=True`` enforces the published
    phase, temperature, density and primary-composition domains.
    """

    liquid_temperature_K: tuple[float, float] = (17.0, 32.0)
    gas_temperature_K: tuple[float, float] = (40.0, 120.0)
    maximum_density_kg_m3: float = 92.0
    primary_ortho_fraction_range: tuple[float, float] = (0.62, 0.75)

    def _validate(self, temperature_K, density_kg_m3, phase: str, strict: bool):
        temperature, density = np.broadcast_arrays(
            np.asarray(temperature_K, dtype=float),
            np.asarray(density_kg_m3, dtype=float),
        )
        if np.any(~np.isfinite(temperature)) or np.any(~np.isfinite(density)):
            raise ValueError("Finite temperature and density required")
        if np.any(temperature <= 0) or np.any(density <= 0):
            raise ValueError("Positive temperature and density required")
        if phase not in {"liquid", "gas"}:
            raise ValueError("phase must be 'liquid' or 'gas'")
        if strict:
            lower, upper = (
                self.liquid_temperature_K
                if phase == "liquid"
                else self.gas_temperature_K
            )
            if np.any((temperature < lower) | (temperature > upper)):
                raise CorrelationDomainError(
                    f"Milenko correlation {phase} temperature domain is "
                    f"{lower:g}-{upper:g} K"
                )
            if np.any(density > self.maximum_density_kg_m3):
                raise CorrelationDomainError(
                    "Milenko correlation density exceeds the reported "
                    "92 kg/m3 range"
                )
        return temperature, density

    def forward_rate_per_s(
        self,
        temperature_K,
        density_kg_m3,
        phase: str,
        strict: bool = True,
    ):
        """Return forward ortho-to-para rate constant in s^-1."""
        temperature, density = self._validate(
            temperature_K, density_kg_m3, phase, strict
        )
        density_g_cm3 = density / 1000.0
        rate_in_1e_minus3_per_h = (
            18.2 * temperature**0.56 * density_g_cm3
            + 5.0e4
            * (0.77 + 921.0 * temperature**-2.5)
            * density_g_cm3**3.6
        )
        return rate_in_1e_minus3_per_h * 1.0e-3 / 3600.0

    def ortho_fraction_rate_per_s(
        self,
        ortho_fraction,
        temperature_K,
        density_kg_m3,
        phase: str,
        thermo: RigidRotorSpinThermo | None = None,
        strict: bool = True,
    ):
        """Return dc/dt from Petitpas Eq. (9)."""
        fraction = np.asarray(ortho_fraction, dtype=float)
        if np.any(~np.isfinite(fraction)) or np.any(
            (fraction < 0) | (fraction > 1)
        ):
            raise ValueError("Ortho fraction must be finite and within [0,1]")
        if strict:
            lower, upper = self.primary_ortho_fraction_range
            if np.any((fraction < lower) | (fraction > upper)):
                raise CorrelationDomainError(
                    "Primary Milenko fit used 0.62-0.75 ortho fraction; "
                    "low-ortho reverse conversion requires separate validation"
                )
        thermo = RigidRotorSpinThermo() if thermo is None else thermo
        equilibrium = thermo.equilibrium_ortho(temperature_K)
        rate = self.forward_rate_per_s(
            temperature_K, density_kg_m3, phase, strict
        )
        return (
            -rate
            * fraction
            * (fraction - equilibrium)
            / (1.0 - equilibrium)
        )


def require_common_energy_reference(references_aligned: bool) -> None:
    """Refuse para/ortho EOS energy differencing without aligned references."""
    if references_aligned is not True:
        raise ValueError(
            "Para/Ortho EOS energies cannot be differenced before explicit "
            "common-reference alignment"
        )


PETITPAS_REVERSE_VALIDITY_THRESHOLDS = (
    # density kg/m3, minimum temperature K, minimum ortho fraction
    (14.0, 163.0, 0.275),
    (28.0, 108.0, 0.170),
    (51.3, 90.0, 0.130),
    (61.2, 75.0, 0.040),
)

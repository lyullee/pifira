"""Evidence-gated liquid-hydrogen research utilities.

The subpackage exposes traceable spin-isomer thermodynamics, state-point and
pathwise composition admission screens, the published Milenko/Petitpas
natural-conversion correlation, and one-dimensional nozzle comparators. It is
not a certified pressure-relief sizing implementation.
"""

from .credit import (
    DEFAULT_FILL_TEMPERATURE_K,
    DEFAULT_FLUID,
    apply_para_composition_allowance,
    crossover_saturation_state,
    equilibrium_path_ledger,
    required_para_fraction_for_nonheating,
    required_para_fraction_for_pathwise_nonheating,
    saturation_state,
    signed_equilibrium_heat_J_per_kg,
)
from .nozzle import (
    HEOSNozzleLookup,
    NozzleDomainError,
    heos_nozzle_lookup,
    ideal_gas_nozzle,
)
from .spin import (
    PETITPAS_REVERSE_VALIDITY_THRESHOLDS,
    CorrelationDomainError,
    MilenkoCorrelation,
    RigidRotorSpinThermo,
    require_common_energy_reference,
)

__all__ = [
    "CorrelationDomainError",
    "DEFAULT_FILL_TEMPERATURE_K",
    "DEFAULT_FLUID",
    "HEOSNozzleLookup",
    "MilenkoCorrelation",
    "NozzleDomainError",
    "PETITPAS_REVERSE_VALIDITY_THRESHOLDS",
    "RigidRotorSpinThermo",
    "apply_para_composition_allowance",
    "crossover_saturation_state",
    "equilibrium_path_ledger",
    "heos_nozzle_lookup",
    "ideal_gas_nozzle",
    "required_para_fraction_for_nonheating",
    "required_para_fraction_for_pathwise_nonheating",
    "require_common_energy_reference",
    "saturation_state",
    "signed_equilibrium_heat_J_per_kg",
]

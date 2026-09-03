"""Evidence-gated liquid-hydrogen research utilities.

The subpackage exposes traceable spin-isomer thermodynamics, the published
Milenko/Petitpas natural-conversion correlation, and one-dimensional nozzle
comparators. It is not a certified pressure-relief sizing implementation.
"""

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
    "HEOSNozzleLookup",
    "MilenkoCorrelation",
    "NozzleDomainError",
    "PETITPAS_REVERSE_VALIDITY_THRESHOLDS",
    "RigidRotorSpinThermo",
    "heos_nozzle_lookup",
    "ideal_gas_nozzle",
    "require_common_energy_reference",
]

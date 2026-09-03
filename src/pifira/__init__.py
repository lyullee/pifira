"""
pifira -- Pressure-based Inverse Fire-heat-flux and Radiative-Area analysis
==========================================================================

A data-agnostic toolkit for estimating fire heat input and effective
flame-contact area for pressurized LPG tanks under localized (non-engulfing)
flame exposure, using the closed-vessel pressure-rise method combined with a
radiative (T^4) weighted angular-temperature inversion.

No experimental data are bundled. Supply your own pressure/temperature series;
see the ``examples`` directory and ``VALIDATION_SOURCES.md`` for the analysis
workflow and source provenance.

Public API
----------
Pressure-rise (heat input):
    TankSpec, internal_energy, liquid_height, heat_input, heat_input_series
Effective area (inversion):
    radiative_driving_force, effective_arc, effective_height,
    effective_area, heat_flux
Representative value & dimensionless framework:
    heat_input_weighted_mean, simple_mean, coverage_fraction,
    normalized_flux, pressurization_number, orientation_factor
I/O:
    load_pressure_csv, load_temperature_csv
"""

from .pressure_rise import (
    TankSpec,
    internal_energy,
    liquid_height,
    heat_input,
    heat_input_series,
)
from .effective_area import (
    radiative_driving_force,
    effective_arc,
    effective_height,
    effective_area,
    heat_flux,
)
from .representative import (
    heat_input_weighted_mean,
    simple_mean,
    coverage_fraction,
    normalized_flux,
    pressurization_number,
    orientation_factor,
)
from .io import load_pressure_csv, load_temperature_csv

__version__ = "0.2.0"

__all__ = [
    "TankSpec", "internal_energy", "liquid_height", "heat_input",
    "heat_input_series", "radiative_driving_force", "effective_arc",
    "effective_height", "effective_area", "heat_flux",
    "heat_input_weighted_mean", "simple_mean", "coverage_fraction",
    "normalized_flux", "pressurization_number", "orientation_factor",
    "load_pressure_csv", "load_temperature_csv",
]

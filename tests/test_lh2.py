"""Data-free implementation tests for the LH2 utilities."""

import numpy as np
import pytest
from CoolProp.CoolProp import PropsSI

from pifira.lh2 import (
    CorrelationDomainError,
    HEOSNozzleLookup,
    MilenkoCorrelation,
    NozzleDomainError,
    RigidRotorSpinThermo,
    ideal_gas_nozzle,
    require_common_energy_reference,
)


def test_rigid_rotor_equilibrium_landmarks():
    thermo = RigidRotorSpinThermo()
    fraction = thermo.equilibrium_ortho(np.array([20.3, 80.0, 300.0]))
    assert 0.001 < fraction[0] < 0.005
    assert 0.45 < fraction[1] < 0.55
    assert 0.748 < fraction[2] < 0.7501


def test_conversion_energy_and_analytic_derivative():
    thermo = RigidRotorSpinThermo()
    low, warm = thermo.conversion_energy_J_per_kg(np.array([20.3, 300.0]))
    assert 690000.0 < low < 703000.0
    assert 0.0 < warm < 60000.0
    temperature, delta = 110.0, 1.0e-3
    numeric = (
        thermo.conversion_energy_J_per_kg(temperature + delta)
        - thermo.conversion_energy_J_per_kg(temperature - delta)
    ) / (2.0 * delta)
    analytic = thermo.d_conversion_energy_dT_J_per_kgK(temperature)
    assert analytic == pytest.approx(numeric, rel=2.0e-5)


def test_milenko_units_and_nominal_value():
    correlation = MilenkoCorrelation()
    value = correlation.forward_rate_per_s(20.0, 70.0, "liquid")
    density_g_cm3 = 0.070
    expected = (
        18.2 * 20.0**0.56 * density_g_cm3
        + 5.0e4
        * (0.77 + 921.0 * 20.0**-2.5)
        * density_g_cm3**3.6
    ) * 1.0e-3 / 3600.0
    assert value == pytest.approx(expected, rel=1.0e-14)
    assert 2.0e-6 < value < 5.0e-6


def test_milenko_domains_are_enforced():
    correlation = MilenkoCorrelation()
    with pytest.raises(CorrelationDomainError):
        correlation.forward_rate_per_s(33.0, 70.0, "liquid")
    with pytest.raises(CorrelationDomainError):
        correlation.forward_rate_per_s(39.0, 2.0, "gas")
    with pytest.raises(CorrelationDomainError):
        correlation.forward_rate_per_s(80.0, 93.0, "gas")
    with pytest.raises(CorrelationDomainError, match="0.62-0.75"):
        correlation.ortho_fraction_rate_per_s(
            0.02, 20.0, 70.0, "liquid"
        )


def test_milenko_rate_has_expected_direction():
    correlation = MilenkoCorrelation()
    thermo = RigidRotorSpinThermo()
    equilibrium = float(thermo.equilibrium_ortho(20.0))
    assert correlation.ortho_fraction_rate_per_s(
        equilibrium / 2.0,
        20.0,
        70.0,
        "liquid",
        thermo,
        strict=False,
    ) > 0.0
    assert correlation.ortho_fraction_rate_per_s(
        min(1.0, equilibrium * 2.0),
        20.0,
        70.0,
        "liquid",
        thermo,
        strict=False,
    ) < 0.0


def test_common_reference_guard():
    with pytest.raises(ValueError, match="common-reference"):
        require_common_energy_reference(False)
    require_common_energy_reference(True)


def test_ideal_nozzle_choked_limit():
    pressure, temperature = 300000.0, 30.0
    gas_constant, gamma = 4124.0, 5.0 / 3.0
    flux, throat_pressure, throat_temperature, choked = ideal_gas_nozzle(
        pressure, temperature, 101325.0, gas_constant, gamma
    )
    expected = (
        pressure
        * np.sqrt(gamma / (gas_constant * temperature))
        * (2.0 / (gamma + 1.0))
        ** ((gamma + 1.0) / (2.0 * (gamma - 1.0)))
    )
    assert flux == pytest.approx(expected, rel=1.0e-12)
    assert throat_temperature / temperature == pytest.approx(
        2.0 / (gamma + 1.0)
    )
    assert throat_pressure < pressure
    assert choked


def test_ideal_nozzle_has_no_reverse_flow():
    result = ideal_gas_nozzle(200000.0, 30.0, 200000.0, 4124.0, 1.4)
    assert result == (0.0, 200000.0, 30.0, False)


def test_small_heos_lookup_runs_and_rejects_extrapolation():
    lookup = HEOSNozzleLookup(
        pressure_points=4,
        superheat_points=4,
        downstream_points=8,
    )
    pressure = 300000.0
    saturation = PropsSI("T", "P", pressure, "Q", 1, "ParaHydrogen")
    flux, throat_pressure, throat_temperature, choked = lookup.evaluate(
        pressure, saturation + 20.0
    )
    assert flux > 0.0
    assert lookup.back_pressure_Pa <= throat_pressure < pressure
    assert throat_temperature > 0.0
    assert isinstance(choked, bool)
    with pytest.raises(NozzleDomainError):
        lookup.evaluate(900000.0, saturation + 20.0)

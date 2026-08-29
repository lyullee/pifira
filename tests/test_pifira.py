"""
Tests for pifira. These are data-free: they check physical consistency and
known analytic properties, not any bundled experimental dataset.
"""

import numpy as np
import pytest

import pifira


def test_tankspec_mass_positive():
    tank = pifira.TankSpec(volume=0.619, fluid="HEOS::Propane", fill=0.70)
    m = tank.initial_mass(10.0)
    assert m > 0
    # 70% of 0.619 m^3 of liquid propane is order 200-300 kg
    assert 150 < m < 350


def test_heat_input_positive_for_rising_pressure():
    tank = pifira.TankSpec(volume=0.619, fluid="HEOS::Propane", fill=0.70)
    Q = pifira.heat_input(P1_bar=10.0, P2_bar=15.0, dt=500.0, tank=tank)
    assert Q > 0  # heating raises pressure -> positive heat input


def test_internal_energy_monotonic_in_pressure():
    tank = pifira.TankSpec(volume=0.619, fluid="HEOS::Propane", fill=0.70)
    m = tank.initial_mass(10.0)
    U1 = pifira.internal_energy(10.0, m, tank)
    U2 = pifira.internal_energy(15.0, m, tank)
    assert U2 > U1


def test_radiative_driving_force_t4():
    # doubling absolute temperature raises driving force ~16x (minus ambient)
    d1 = pifira.radiative_driving_force(0.0, T_amb_C=-273.15)   # 273.15 K
    d2 = pifira.radiative_driving_force(273.15, T_amb_C=-273.15)  # 546.3 K
    assert d2 / d1 == pytest.approx(16.0, rel=0.05)


def test_effective_arc_symmetric_gaussian():
    # a symmetric bell centred at 0 should recover a finite equivalent width
    angles = [0, 90, 180, -90]
    temps = [271, 49, 39, 46]
    res = pifira.effective_arc(angles, temps, T_amb_C=35.0)
    assert res["sigma"] > 0
    assert res["arc_deg"] == pytest.approx(np.sqrt(2 * np.pi) * res["sigma"])
    assert res["fwhm_deg"] == pytest.approx(2.355 * res["sigma"])


def test_effective_height_takes_minimum():
    assert pifira.effective_height(0.767, 0.885) == 0.767
    assert pifira.effective_height(1.2, 0.885) == 0.885


def test_effective_area_and_flux():
    A = pifira.effective_area(diameter_m=0.75, arc_deg=90.0, height_m=0.767)
    assert A > 0
    q = pifira.heat_flux(16800.0, A)  # 16.8 kW over A
    assert q > 0


def test_weighted_mean_biases_toward_high_Q():
    q = [30.0, 70.0]
    Q_equal = [1.0, 1.0]
    Q_high = [1.0, 9.0]
    m_eq = pifira.heat_input_weighted_mean(q, Q_equal)
    m_hi = pifira.heat_input_weighted_mean(q, Q_high)
    assert m_eq == pytest.approx(50.0)
    assert m_hi > m_eq  # weighting toward the high-flux instant


def test_dimensionless_definitions():
    assert pifira.coverage_fraction(0.5, 2.0) == 0.25
    assert pifira.normalized_flux(50.0, q_engulf=100.0) == 0.5
    assert pifira.orientation_factor(0.89, 0.75) == pytest.approx(1.187, rel=1e-3)

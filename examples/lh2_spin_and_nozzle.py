"""Data-free LH2 ortho-para and ideal-nozzle demonstration."""

from pifira.lh2 import MilenkoCorrelation, RigidRotorSpinThermo, ideal_gas_nozzle


def main() -> None:
    thermo = RigidRotorSpinThermo()
    correlation = MilenkoCorrelation()

    temperature_K = 20.3
    density_kg_m3 = 70.0
    equilibrium = thermo.equilibrium_ortho(temperature_K)
    energy = thermo.conversion_energy_J_per_kg(temperature_K)
    rate = correlation.forward_rate_per_s(
        temperature_K, density_kg_m3, phase="liquid"
    )

    mass_flux, throat_pressure, throat_temperature, choked = ideal_gas_nozzle(
        pressure_Pa=300000.0,
        temperature_K=30.0,
        back_pressure_Pa=101325.0,
        gas_constant_J_kgK=4124.0,
        gamma=5.0 / 3.0,
    )

    print(f"equilibrium ortho fraction: {equilibrium:.6f}")
    print(f"ortho-para energy gap: {energy / 1000.0:.3f} kJ/kg")
    print(f"published forward rate: {rate:.6e} 1/s")
    print(f"ideal nozzle mass flux: {mass_flux:.3f} kg/(m2 s)")
    print(f"throat pressure: {throat_pressure / 1000.0:.3f} kPa")
    print(f"throat temperature: {throat_temperature:.3f} K")
    print(f"choked: {choked}")


if __name__ == "__main__":
    main()

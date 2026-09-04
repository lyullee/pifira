"""Reproduce the pifira 0.3.0 LH2 composition-screen landmarks."""

from pifira.lh2 import (
    apply_para_composition_allowance,
    equilibrium_path_ledger,
    required_para_fraction_for_nonheating,
    required_para_fraction_for_pathwise_nonheating,
)


pressure_Pa = 50.0 * 6894.757293168

state_point = required_para_fraction_for_nonheating(pressure_Pa)
pathwise = required_para_fraction_for_pathwise_nonheating(pressure_Pa)
adjusted, feasible = apply_para_composition_allowance(pathwise, 0.1)
ledger_99p7 = equilibrium_path_ledger(ortho_fraction=0.003, pressure_Pa=pressure_Pa)

print(f"State-point threshold: {100.0 * state_point:.4f}% para")
print(f"Full-path threshold:  {100.0 * pathwise:.4f}% para")
print(
    f"With +0.1 percentage point allowance: {100.0 * adjusted:.4f}% para "
    f"(feasible={feasible})"
)
print(
    "99.7%-para ledger: "
    f"initial={ledger_99p7['initial_adverse_inventory_kJ_per_kg']:+.3f} kJ/kg, "
    f"crossover={ledger_99p7['crossover_pressure_kPa_abs']:.1f} kPa(abs), "
    f"target={ledger_99p7['target_signed_equilibrium_heat_kJ_per_kg']:+.3f} kJ/kg"
)
print("Qualification:", ledger_99p7["qualification"])

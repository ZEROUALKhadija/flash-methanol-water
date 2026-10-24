from pathlib import Path
import numpy as np

from src.rachford_rice import solve_flash
from src.energy_balance import sensible_heat
from src.plots import plot_process_diagram, plot_binary_diagram

F = 50.0
z = np.array([0.60, 0.40])  # Eau, méthanol
T_initial = 25.0
T_final = 80.0
P_kPa = 101.325


def main():
    root = Path(__file__).resolve().parent
    results_dir = root / "results"
    figures_dir = results_dir / "figures"
    data_dir = results_dir / "data"

    for folder in (results_dir, figures_dir, data_dir):
        folder.mkdir(parents=True, exist_ok=True)

    result = solve_flash(T_final, P_kPa, F, z)
    energy = sensible_heat(F, z, T_initial, T_final)

    output = results_dir / "resultats.txt"

    with output.open("w", encoding="utf-8") as file:
        file.write("FLASH EAU-METHANOL - NRTL\n")
        file.write(f"Debit alimentation : {F:.6f} mol/h\n")
        file.write(f"Temperature : {T_final:.2f} °C\n")
        file.write(f"Pression : {P_kPa:.3f} kPa\n\n")

        file.write(f"Fraction vaporisee : {result['beta']:.8f}\n")
        file.write(f"Fraction liquide : {result['liquid_fraction']:.8f}\n")
        file.write(
            f"Debit liquide : {result['liquid_flow_mol_h']:.8f} mol/h\n"
        )
        file.write(
            f"Debit vapeur : {result['vapor_flow_mol_h']:.8f} mol/h\n\n"
        )

        file.write("Composition liquide [eau, methanol]\n")
        file.write(f"{result['x_liquid']}\n\n")

        file.write("Composition vapeur [eau, methanol]\n")
        file.write(f"{result['y_vapor']}\n\n")

        file.write(f"K [eau, methanol] : {result['K']}\n")
        file.write(f"Iterations : {result['iterations']}\n\n")
        file.write(
            "Puissance sensible estimee : "
            f"{energy['heat_kW']:.8f} kW\n"
        )
        file.write(
            "La puissance est une estimation du chauffage sensible, "
            "pas un bilan enthalpique complet du flash.\n"
        )
        file.write(
            "NRTL utilise ici une correlation publiee et une vapeur ideale. "
            "Verifier les parametres et le modele de vapeur de DWSIM.\n"
        )

    plot_process_diagram(figures_dir / "schema_procede.png")
    plot_binary_diagram(result, figures_dir / "compositions_phases.png")

    print("Calcul termine avec NRTL.")
    print(f"Fraction vaporisee : {result['beta']:.6f}")
    print("Composition liquide [eau, methanol]:", result["x_liquid"])
    print("Composition vapeur [eau, methanol]:", result["y_vapor"])
    print(f"Fichier : {output}")


if __name__ == "__main__":
    main()
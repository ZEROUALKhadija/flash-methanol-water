import numpy as np


def sensible_heat(F_mol_h, z, T_initial, T_final):
    """
    Estimation de la chaleur sensible.
    F_mol_h : débit molaire total en mol/h.
    z : fractions molaires [eau, méthanol].
    T : degrés Celsius.
    """
    if F_mol_h <= 0:
        raise ValueError("Le débit doit être positif.")

    z = np.asarray(z, dtype=float)
    z = z / z.sum()

    # Cp molaires liquides approximatifs en J/(mol.K)
    cp = np.array([75.3, 81.1])

    delta_T = T_final - T_initial
    cp_mix = float(np.dot(z, cp))

    # J/h -> W
    duty_W = F_mol_h * cp_mix * delta_T / 3600

    return {
        "delta_T_C": delta_T,
        "cp_mix_J_mol_K": cp_mix,
        "heat_W": duty_W,
        "heat_kW": duty_W / 1000,
    }

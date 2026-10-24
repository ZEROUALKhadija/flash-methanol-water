import numpy as np
from src.thermodynamics import equilibrium_constants


def rachford_rice_function(beta, z, K):
    return np.sum(z * (K - 1) / (1 + beta * (K - 1)))


def solve_flash(T_C, P_kPa, F, z, tol=1e-9, max_iter=1000):
    z = np.asarray(z, dtype=float)
    z = z / z.sum()

    # Estimation initiale
    x = z.copy()
    beta = 0.5

    for iteration in range(max_iter):
        K = equilibrium_constants(T_C, P_kPa, x)

        f0 = rachford_rice_function(0.0, z, K)
        f1 = rachford_rice_function(1.0, z, K)

        if f0 <= 0:
            beta = 0.0
            x = z.copy()
            y = K * x
            y /= y.sum()
            return _results(F, beta, x, y, K, iteration + 1)

        if f1 >= 0:
            beta = 1.0
            y = z.copy()
            x = y / K
            x /= x.sum()
            return _results(F, beta, x, y, K, iteration + 1)

        low, high = 0.0, 1.0

        for _ in range(100):
            beta = (low + high) / 2
            value = rachford_rice_function(beta, z, K)

            if abs(value) < tol:
                break
            if value > 0:
                low = beta
            else:
                high = beta

        x_new = z / (1 + beta * (K - 1))
        x_new /= x_new.sum()

        if np.max(np.abs(x_new - x)) < tol:
            x = x_new
            break

        x = 0.5 * x + 0.5 * x_new

    K = equilibrium_constants(T_C, P_kPa, x)
    beta = (low + high) / 2
    x = z / (1 + beta * (K - 1))
    y = K * x

    x /= x.sum()
    y /= y.sum()

    return _results(F, beta, x, y, K, iteration + 1)


def _results(F, beta, x, y, K, iterations):
    return {
        "beta": beta,
        "liquid_fraction": 1 - beta,
        "vapor_fraction": beta,
        "x_liquid": x,
        "y_vapor": y,
        "liquid_flow_mol_h": F * (1 - beta),
        "vapor_flow_mol_h": F * beta,
        "K": K,
        "iterations": iterations,
    }

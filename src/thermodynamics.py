import numpy as np

COMPONENTS = ["Eau", "Methanol"]

# Antoine : Psat en mmHg, T en °C
ANTOINE_A = np.array([8.07131, 8.08097])
ANTOINE_B = np.array([1730.63, 1582.271])
ANTOINE_C = np.array([233.426, 239.726])

MMHG_TO_KPA = 0.133322368


def saturation_pressures(T_C):
    return MMHG_TO_KPA * 10 ** (
        ANTOINE_A - ANTOINE_B / (T_C + ANTOINE_C)
    )


def nrtl_activity_coefficients(x, T_K):
    """
    NRTL pour eau (1) / méthanol (2).
    Corrélation publiée :
    tau_12 = -1.5941 + 367.54/T
    tau_21 =  3.1128 - 582.30/T
    alpha_12 = alpha_21 = 0.30
    """
    x = np.asarray(x, dtype=float)
    x = x / x.sum()

    tau = np.array([
        [0.0, -1.5941 + 367.54 / T_K],
        [3.1128 - 582.30 / T_K, 0.0],
    ])
    alpha = np.array([[0.0, 0.30], [0.30, 0.0]])
    G = np.exp(-alpha * tau)

    gamma = np.zeros(2)

    for i in range(2):
        first = sum(
            x[j] * tau[j, i] * G[j, i]
            for j in range(2)
        ) / sum(x[j] * G[j, i] for j in range(2))

        second = 0.0
        for j in range(2):
            denominator = sum(x[k] * G[k, j] for k in range(2))
            inner = sum(
                x[k] * tau[k, j] * G[k, j]
                for k in range(2)
            ) / denominator
            second += x[j] * G[i, j] / denominator * (
                tau[i, j] - inner
            )

        gamma[i] = np.exp(first + second)

    return gamma


def equilibrium_constants(T_C, P_kPa, x):
    """K_i = gamma_i * Psat_i / P, vapeur supposée idéale."""
    T_K = T_C + 273.15
    gamma = nrtl_activity_coefficients(x, T_K)
    Psat = saturation_pressures(T_C)
    return gamma * Psat / P_kPa

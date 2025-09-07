"""
LUFT lattice-collapse criterion utilities for merger-driven central seed formation.

Units: SI (M in kg, r_p in m, v_rel in m/s). Returns dimensionless Q and r_crit in meters.
Adds an optional foam amplification based on fractional density perturbation.
"""

from __future__ import annotations
import numpy as np

HBAR = 1.054_571_817e-34  # J*s
G = 6.674_30e-11          # m^3 kg^-1 s^-2


def foam_factor(delta_rho_over_rho: float = 0.0, beta: float = 1.0) -> float:
    """
    Simple amplification factor for Q due to fractional density perturbation.
    F = (1 + δρ/ρ)^β, with floor at 0 to avoid unphysical negatives.
    """
    return max(0.0, 1.0 + float(delta_rho_over_rho)) ** float(beta)


def compute_Q(
    M: float,
    r_p: float,
    v_rel: float,
    alpha: float,
    m_eq: float,
    Q_c: float = 1.0,
    *,
    delta_rho_over_rho: float = 0.0,
    beta: float = 1.0,
    hbar: float = HBAR,
    GN: float = G,
) -> float:
    """
    Q ≈ (ħ/m_eq) * alpha * (G M) / (r_p v_rel^2) * foam_factor(δ, β)

    Collapse if Q >= Q_c.
    """
    if r_p <= 0 or v_rel <= 0 or m_eq <= 0:
        raise ValueError("r_p, v_rel, and m_eq must be positive")
    base = (hbar / m_eq) * alpha * (GN * M) / (r_p * v_rel**2)
    return base * foam_factor(delta_rho_over_rho, beta)


def critical_pericenter(
    M: float,
    v_rel: float,
    alpha: float,
    m_eq: float,
    Q_c: float = 1.0,
    *,
    delta_rho_over_rho: float = 0.0,
    beta: float = 1.0,
    hbar: float = HBAR,
    GN: float = G,
) -> float:
    """
    r_crit solves Q == Q_c:
    r_crit ≈ (ħ α G M / (m_eq v_rel^2)) * foam_factor(δ, β) / Q_c
    """
    if v_rel <= 0 or m_eq <= 0 or Q_c <= 0:
        raise ValueError("v_rel, m_eq, and Q_c must be positive")
    return (hbar * alpha * GN * M) / (m_eq * Q_c * v_rel**2) * foam_factor(delta_rho_over_rho, beta)


def nucleates(
    M: float,
    r_p: float,
    v_rel: float,
    alpha: float,
    m_eq: float,
    Q_c: float = 1.0,
    *,
    delta_rho_over_rho: float = 0.0,
    beta: float = 1.0,
) -> bool:
    return compute_Q(M, r_p, v_rel, alpha, m_eq, Q_c, delta_rho_over_rho=delta_rho_over_rho, beta=beta) >= Q_c

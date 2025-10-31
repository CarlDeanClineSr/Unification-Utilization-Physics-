"""
Basic unit tests for the collapse module.

Tests verify:
1. plasma_frequency returns expected GHz range values
2. phase_effective_mass is always positive
3. deltaU_from_gamma raises error for invalid gamma > 1 or gamma <= 0
"""

import sys
import os
import pytest
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from collapse import (
    plasma_frequency,
    phase_effective_mass,
    deltaU_from_gamma,
    EJ_from_Ic,
    HBAR,
    E_CHARGE
)


class TestPlasmaFrequency:
    """Test plasma_frequency function."""
    
    def test_returns_ghz_range_for_typical_junction(self):
        """Test that plasma_frequency returns a value in expected GHz range for a known example."""
        # Typical qubit-like junction parameters
        I_c = 1e-6  # 1 μA critical current
        E_J = EJ_from_Ic(I_c)  # Josephson energy
        C = 1e-15  # 1 fF capacitance
        
        f_p = plasma_frequency(E_J, C)
        
        # Convert to GHz for assertion
        f_p_ghz = f_p * 1e-9
        
        # For typical superconducting junctions, plasma frequency should be in GHz range
        # For small C (1 fF) and moderate I_c (1 μA), expect ~100-500 GHz
        assert 10.0 < f_p_ghz < 1000.0, f"Plasma frequency {f_p_ghz:.2f} GHz outside expected range [10, 1000] GHz"
    
    def test_returns_positive_value(self):
        """Test that plasma_frequency always returns a positive value."""
        E_J = 1e-22  # 1e-22 J
        C = 1e-15  # 1 fF
        
        f_p = plasma_frequency(E_J, C)
        
        assert f_p > 0, "Plasma frequency must be positive"
    
    def test_scales_correctly_with_parameters(self):
        """Test that plasma_frequency scales correctly: f_p ∝ sqrt(E_J/C)."""
        E_J_base = 1e-22  # J
        C_base = 1e-15  # F
        
        f_p_base = plasma_frequency(E_J_base, C_base)
        
        # Double E_J should increase f_p by sqrt(2)
        f_p_2x_ej = plasma_frequency(2 * E_J_base, C_base)
        ratio_ej = f_p_2x_ej / f_p_base
        assert abs(ratio_ej - np.sqrt(2)) < 0.01, f"Expected ratio ~{np.sqrt(2):.3f}, got {ratio_ej:.3f}"
        
        # Double C should decrease f_p by sqrt(2)
        f_p_2x_c = plasma_frequency(E_J_base, 2 * C_base)
        ratio_c = f_p_2x_c / f_p_base
        assert abs(ratio_c - 1/np.sqrt(2)) < 0.01, f"Expected ratio ~{1/np.sqrt(2):.3f}, got {ratio_c:.3f}"


class TestPhaseEffectiveMass:
    """Test phase_effective_mass function."""
    
    def test_returns_positive_value(self):
        """Test that phase_effective_mass is always positive."""
        C_values = [1e-15, 1e-14, 1e-13, 1e-12]  # Various capacitances
        
        for C in C_values:
            m_eff = phase_effective_mass(C)
            assert m_eff > 0, f"Phase effective mass must be positive for C={C}, got {m_eff}"
    
    def test_scales_linearly_with_capacitance(self):
        """Test that phase_effective_mass scales linearly with capacitance."""
        C_base = 1e-15  # 1 fF
        m_eff_base = phase_effective_mass(C_base)
        
        # Double capacitance should double effective mass
        m_eff_2x = phase_effective_mass(2 * C_base)
        ratio = m_eff_2x / m_eff_base
        assert abs(ratio - 2.0) < 0.01, f"Expected ratio 2.0, got {ratio:.3f}"
    
    def test_expected_magnitude(self):
        """Test that phase_effective_mass has expected magnitude."""
        C = 1e-15  # 1 fF
        m_eff = phase_effective_mass(C)
        
        # Expected: m_eff = (hbar^2 * C) / 4 ~ 2.78e-83 for C=1e-15
        expected = (HBAR**2 * C) / 4
        assert abs(m_eff - expected) / expected < 0.01, f"Expected {expected:.3e}, got {m_eff:.3e}"


class TestDeltaUFromGamma:
    """Test deltaU_from_gamma function."""
    
    def test_raises_error_for_gamma_greater_than_one(self):
        """Test that deltaU_from_gamma raises ValueError for gamma > 1."""
        with pytest.raises(ValueError, match="gamma must be in range"):
            deltaU_from_gamma(1.5)
        
        with pytest.raises(ValueError, match="gamma must be in range"):
            deltaU_from_gamma(1.0)  # Exactly 1.0 should also fail
    
    def test_raises_error_for_gamma_less_than_or_equal_zero(self):
        """Test that deltaU_from_gamma raises ValueError for gamma <= 0."""
        with pytest.raises(ValueError, match="gamma must be in range"):
            deltaU_from_gamma(0.0)
        
        with pytest.raises(ValueError, match="gamma must be in range"):
            deltaU_from_gamma(-0.5)
    
    def test_valid_gamma_returns_expected_value(self):
        """Test that deltaU_from_gamma returns the input gamma for valid inputs."""
        gamma_values = [0.1, 0.3, 0.5, 0.7, 0.9]
        
        for gamma in gamma_values:
            result = deltaU_from_gamma(gamma)
            assert result == gamma, f"Expected {gamma}, got {result}"
    
    def test_boundary_values(self):
        """Test deltaU_from_gamma near boundaries (but not at them)."""
        # Just above 0
        result_low = deltaU_from_gamma(0.001)
        assert result_low == 0.001
        
        # Just below 1
        result_high = deltaU_from_gamma(0.999)
        assert result_high == 0.999


class TestEJFromIc:
    """Test EJ_from_Ic function."""
    
    def test_returns_positive_value(self):
        """Test that EJ_from_Ic returns positive Josephson energy."""
        I_c_values = [1e-9, 1e-6, 1e-3]  # Various critical currents
        
        for I_c in I_c_values:
            E_J = EJ_from_Ic(I_c)
            assert E_J > 0, f"Josephson energy must be positive for I_c={I_c}, got {E_J}"
    
    def test_scales_linearly_with_critical_current(self):
        """Test that E_J scales linearly with I_c."""
        I_c_base = 1e-6  # 1 μA
        E_J_base = EJ_from_Ic(I_c_base)
        
        # Double critical current should double Josephson energy
        E_J_2x = EJ_from_Ic(2 * I_c_base)
        ratio = E_J_2x / E_J_base
        assert abs(ratio - 2.0) < 0.01, f"Expected ratio 2.0, got {ratio:.3f}"
    
    def test_expected_formula(self):
        """Test that E_J follows expected formula: E_J = (ħ * I_c) / (2e)."""
        I_c = 1e-6  # 1 μA
        E_J = EJ_from_Ic(I_c)
        
        expected = (HBAR * I_c) / (2 * E_CHARGE)
        assert abs(E_J - expected) / expected < 0.01, f"Expected {expected:.3e}, got {E_J:.3e}"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])

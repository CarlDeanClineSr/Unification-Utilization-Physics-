"""
LUFT Lattice-Collapse Mechanism for Central SMBH Nucleation During Mergers

This module implements the Lattice Unification Field Theory (LUFT) framework
for modeling supermassive black hole (SMBH) nucleation during galaxy mergers,
keeping the electromagnetic (EM) portal term χ φ F^2 to enable LHC constraints.

Mathematical Framework:
- Lattice field φ with electromagnetic coupling χ φ F^2
- Collapse criterion based on critical field density
- Merger dynamics with gravitational wave signatures
"""

import numpy as np
import scipy.special as sp
from typing import Dict, Tuple, Optional, Union
from dataclasses import dataclass
import warnings


@dataclass
class LUFTParameters:
    """Parameters for LUFT lattice-collapse mechanism."""
    
    # Lattice field parameters
    phi_0: float = 1e-3  # Background field value (GeV)
    lambda_phi: float = 0.1  # Self-coupling constant
    m_phi: float = 1e-6  # Field mass (GeV)
    
    # EM portal coupling
    chi: float = 1e-9  # EM portal coupling χ φ F^2 (GeV^-1)
    
    # SMBH parameters
    M_bh_seed: float = 1e3  # Seed black hole mass (M_solar)
    alpha_acc: float = 0.1  # Accretion efficiency
    
    # Merger parameters
    merger_timescale: float = 1e8  # Merger timescale (years)
    q_ratio: float = 1.0  # Mass ratio of merging galaxies
    
    # Collapse criterion parameters
    rho_crit: float = 1e15  # Critical density for collapse (GeV/cm^3)
    beta_collapse: float = 2.0  # Collapse exponent


class LUFTCollapseModel:
    """
    LUFT lattice-collapse model for SMBH nucleation.
    
    This class implements the core physics of lattice field collapse
    during galaxy mergers, leading to central SMBH formation.
    """
    
    def __init__(self, params: Optional[LUFTParameters] = None):
        """Initialize LUFT collapse model with given parameters."""
        self.params = params if params is not None else LUFTParameters()
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Validate input parameters for physical consistency."""
        if self.params.phi_0 <= 0:
            raise ValueError("Background field φ_0 must be positive")
        if self.params.chi <= 0:
            raise ValueError("EM portal coupling χ must be positive")
        if self.params.M_bh_seed <= 0:
            raise ValueError("Seed black hole mass must be positive")
        if self.params.rho_crit <= 0:
            raise ValueError("Critical density must be positive")
    
    def field_potential(self, phi: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate lattice field potential V(φ).
        
        V(φ) = (1/2) m_φ^2 φ^2 + (λ_φ/4!) φ^4
        
        Args:
            phi: Field value(s) (GeV)
            
        Returns:
            Potential energy density (GeV^4)
        """
        m_phi2 = self.params.m_phi**2
        lambda_phi = self.params.lambda_phi
        
        return 0.5 * m_phi2 * phi**2 + (lambda_phi / 24.0) * phi**4
    
    def field_density(self, phi: Union[float, np.ndarray], 
                     dphi_dt: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate field energy density.
        
        ρ_φ = (1/2) (∂φ/∂t)^2 + V(φ)
        
        Args:
            phi: Field value(s) (GeV)
            dphi_dt: Time derivative of field (GeV^2)
            
        Returns:
            Energy density (GeV^4)
        """
        kinetic = 0.5 * dphi_dt**2
        potential = self.field_potential(phi)
        return kinetic + potential
    
    def em_portal_coupling(self, phi: Union[float, np.ndarray], 
                          F_mu_nu_sq: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate EM portal interaction term χ φ F^2.
        
        Args:
            phi: Field value(s) (GeV)
            F_mu_nu_sq: Electromagnetic field tensor squared (GeV^4)
            
        Returns:
            Interaction energy density (GeV^4)
        """
        return self.params.chi * phi * F_mu_nu_sq
    
    def collapse_criterion(self, phi: Union[float, np.ndarray], 
                          dphi_dt: Union[float, np.ndarray],
                          F_mu_nu_sq: Union[float, np.ndarray] = 0.0) -> Union[bool, np.ndarray]:
        """
        Evaluate lattice collapse criterion.
        
        Collapse occurs when total energy density exceeds critical threshold:
        ρ_total = ρ_φ + χ φ F^2 > ρ_crit
        
        Args:
            phi: Field value(s) (GeV)
            dphi_dt: Time derivative of field (GeV^2)
            F_mu_nu_sq: EM field tensor squared (GeV^4)
            
        Returns:
            Boolean indicating collapse condition
        """
        rho_field = self.field_density(phi, dphi_dt)
        rho_em = self.em_portal_coupling(phi, F_mu_nu_sq)
        rho_total = rho_field + rho_em
        
        # Enhanced collapse criterion with power law
        collapse_threshold = self.params.rho_crit * (1 + (phi / self.params.phi_0)**self.params.beta_collapse)
        
        return rho_total > collapse_threshold
    
    def merger_field_evolution(self, t: Union[float, np.ndarray], 
                              impact_parameter: float = 1.0) -> Dict[str, Union[float, np.ndarray]]:
        """
        Model field evolution during galaxy merger.
        
        Simple model: φ(t) ∝ exp(-t/τ_merger) * oscillatory_term
        
        Args:
            t: Time array (years)
            impact_parameter: Merger geometry parameter
            
        Returns:
            Dictionary with field evolution and derivatives
        """
        tau = self.params.merger_timescale
        omega = 2 * np.pi / (tau / 10)  # Oscillation frequency
        
        # Exponential decay with oscillations during merger
        envelope = np.exp(-t / tau)
        oscillation = np.cos(omega * t)
        
        phi = self.params.phi_0 * envelope * oscillation * impact_parameter
        dphi_dt = self.params.phi_0 * envelope * (
            -oscillation / tau - omega * np.sin(omega * t)
        ) * impact_parameter
        
        return {
            'phi': phi,
            'dphi_dt': dphi_dt,
            'envelope': envelope,
            'time': t
        }
    
    def smbh_mass_evolution(self, t_collapse: float, 
                           accretion_rate: Optional[float] = None) -> float:
        """
        Calculate SMBH mass evolution after collapse.
        
        M(t) = M_seed * (1 + α_acc * t / t_collapse)
        
        Args:
            t_collapse: Time of lattice collapse (years)
            accretion_rate: Custom accretion rate (M_solar/year)
            
        Returns:
            Final SMBH mass (M_solar)
        """
        if accretion_rate is None:
            # Default Eddington-limited accretion
            accretion_rate = self.params.alpha_acc * self.params.M_bh_seed / t_collapse
        
        M_final = self.params.M_bh_seed * (1 + accretion_rate * t_collapse / self.params.M_bh_seed)
        return M_final
    
    def lhc_constraint_window(self, energy_scale: float = 13e3) -> Dict[str, float]:
        """
        Calculate LHC constraint window for EM portal coupling χ.
        
        The χ φ F^2 term enables direct LHC constraints through
        high-energy electromagnetic processes.
        
        Args:
            energy_scale: LHC collision energy (GeV)
            
        Returns:
            Dictionary with constraint parameters
        """
        # Simplified LHC constraint model
        chi_max = 1 / (energy_scale * self.params.phi_0)  # Perturbativity bound
        chi_min = 1e-12  # Experimental sensitivity limit
        
        return {
            'chi_max': chi_max,
            'chi_min': chi_min,
            'energy_scale': energy_scale,
            'current_chi': self.params.chi,
            'within_bounds': chi_min <= self.params.chi <= chi_max
        }


def create_default_model() -> LUFTCollapseModel:
    """Create LUFT model with default parameters optimized for SMBH formation."""
    default_params = LUFTParameters(
        phi_0=1e-3,      # GeV
        lambda_phi=0.1,   # Dimensionless
        m_phi=1e-6,      # GeV (light field)
        chi=1e-9,        # GeV^-1 (within LHC bounds)
        M_bh_seed=1e3,   # M_solar
        alpha_acc=0.1,    # Eddington fraction
        merger_timescale=1e8,  # years
        q_ratio=1.0,     # Equal mass merger
        rho_crit=1e15,   # GeV/cm^3
        beta_collapse=2.0 # Power law exponent
    )
    return LUFTCollapseModel(default_params)


# Convenience functions for common calculations
def evaluate_collapse_probability(phi_values: np.ndarray, 
                                dphi_dt_values: np.ndarray,
                                model: Optional[LUFTCollapseModel] = None) -> float:
    """
    Calculate probability of lattice collapse for given field configuration.
    
    Args:
        phi_values: Array of field values
        dphi_dt_values: Array of field derivatives
        model: LUFT model instance
        
    Returns:
        Collapse probability (0-1)
    """
    if model is None:
        model = create_default_model()
    
    collapse_mask = model.collapse_criterion(phi_values, dphi_dt_values)
    return np.mean(collapse_mask.astype(float))


def estimate_smbh_formation_time(merger_params: Dict, 
                                model: Optional[LUFTCollapseModel] = None) -> Optional[float]:
    """
    Estimate time to SMBH formation during merger.
    
    Args:
        merger_params: Dictionary with merger parameters
        model: LUFT model instance
        
    Returns:
        Formation time in years, or None if no collapse
    """
    if model is None:
        model = create_default_model()
    
    # Time array for merger evolution
    t_max = merger_params.get('duration', model.params.merger_timescale)
    t_array = np.linspace(0, t_max, 1000)
    
    # Calculate field evolution
    evolution = model.merger_field_evolution(t_array)
    
    # Check for collapse
    collapse_mask = model.collapse_criterion(evolution['phi'], evolution['dphi_dt'])
    
    if np.any(collapse_mask):
        collapse_indices = np.where(collapse_mask)[0]
        return t_array[collapse_indices[0]]
    else:
        return None
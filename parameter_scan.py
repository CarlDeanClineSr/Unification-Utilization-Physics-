"""
Parameter Scanning Utilities for LUFT Lattice-Collapse Model

This module provides tools for parameter space exploration and sensitivity analysis
of the LUFT mechanism with wide priors suitable for initial fits before constraint
narrowing from observational data.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass, asdict
import multiprocessing as mp
from functools import partial
import warnings

from luft_collapse import LUFTCollapseModel, LUFTParameters, evaluate_collapse_probability


@dataclass
class ParameterPrior:
    """Define prior distribution for a parameter."""
    name: str
    distribution: str  # 'uniform', 'log_uniform', 'gaussian'
    min_val: float
    max_val: float
    mean: Optional[float] = None  # For gaussian
    std: Optional[float] = None   # For gaussian


class ParameterScanner:
    """
    Parameter space scanner for LUFT model with wide priors.
    
    Supports various sampling strategies and parallel evaluation
    for efficient exploration of high-dimensional parameter space.
    """
    
    def __init__(self, priors: Optional[Dict[str, ParameterPrior]] = None):
        """
        Initialize parameter scanner with prior definitions.
        
        Args:
            priors: Dictionary of parameter priors, uses defaults if None
        """
        self.priors = priors if priors is not None else self._create_wide_priors()
        self.results = []
        
    def _create_wide_priors(self) -> Dict[str, ParameterPrior]:
        """Create wide priors for initial parameter exploration."""
        return {
            'phi_0': ParameterPrior('phi_0', 'log_uniform', 1e-6, 1e0),  # GeV
            'lambda_phi': ParameterPrior('lambda_phi', 'log_uniform', 1e-3, 1e1),
            'm_phi': ParameterPrior('m_phi', 'log_uniform', 1e-9, 1e-3),  # GeV
            'chi': ParameterPrior('chi', 'log_uniform', 1e-12, 1e-6),  # GeV^-1
            'M_bh_seed': ParameterPrior('M_bh_seed', 'log_uniform', 1e2, 1e6),  # M_solar
            'alpha_acc': ParameterPrior('alpha_acc', 'uniform', 0.01, 1.0),
            'merger_timescale': ParameterPrior('merger_timescale', 'log_uniform', 1e6, 1e10),  # years
            'q_ratio': ParameterPrior('q_ratio', 'uniform', 0.1, 10.0),
            'rho_crit': ParameterPrior('rho_crit', 'log_uniform', 1e12, 1e18),  # GeV/cm^3
            'beta_collapse': ParameterPrior('beta_collapse', 'uniform', 1.0, 5.0)
        }
    
    def sample_parameter(self, prior: ParameterPrior, n_samples: int = 1) -> np.ndarray:
        """
        Sample from parameter prior distribution.
        
        Args:
            prior: Parameter prior specification
            n_samples: Number of samples to generate
            
        Returns:
            Array of parameter samples
        """
        if prior.distribution == 'uniform':
            return np.random.uniform(prior.min_val, prior.max_val, n_samples)
        
        elif prior.distribution == 'log_uniform':
            log_min = np.log10(prior.min_val)
            log_max = np.log10(prior.max_val)
            log_samples = np.random.uniform(log_min, log_max, n_samples)
            return 10**log_samples
        
        elif prior.distribution == 'gaussian':
            if prior.mean is None or prior.std is None:
                raise ValueError("Gaussian prior requires mean and std")
            samples = np.random.normal(prior.mean, prior.std, n_samples)
            # Clip to bounds
            return np.clip(samples, prior.min_val, prior.max_val)
        
        else:
            raise ValueError(f"Unknown distribution: {prior.distribution}")
    
    def generate_parameter_set(self) -> Dict[str, float]:
        """Generate single random parameter set from priors."""
        param_set = {}
        for name, prior in self.priors.items():
            param_set[name] = float(self.sample_parameter(prior, 1)[0])
        return param_set
    
    def latin_hypercube_sample(self, n_samples: int) -> List[Dict[str, float]]:
        """
        Generate Latin Hypercube samples for efficient space filling.
        
        Args:
            n_samples: Number of parameter sets to generate
            
        Returns:
            List of parameter dictionaries
        """
        n_params = len(self.priors)
        param_names = list(self.priors.keys())
        
        # Generate LHS indices
        lhs_indices = np.zeros((n_samples, n_params))
        for i in range(n_params):
            perm = np.random.permutation(n_samples)
            lhs_indices[:, i] = (perm + np.random.uniform(0, 1, n_samples)) / n_samples
        
        # Convert to parameter values
        parameter_sets = []
        for i in range(n_samples):
            param_set = {}
            for j, (name, prior) in enumerate(self.priors.items()):
                # Convert uniform [0,1] to parameter range
                u = lhs_indices[i, j]
                if prior.distribution == 'uniform':
                    value = prior.min_val + u * (prior.max_val - prior.min_val)
                elif prior.distribution == 'log_uniform':
                    log_min = np.log10(prior.min_val)
                    log_max = np.log10(prior.max_val)
                    log_value = log_min + u * (log_max - log_min)
                    value = 10**log_value
                elif prior.distribution == 'gaussian':
                    # Use inverse normal CDF (approximation)
                    from scipy.stats import norm
                    value = norm.ppf(u, loc=prior.mean, scale=prior.std)
                    value = np.clip(value, prior.min_val, prior.max_val)
                else:
                    raise ValueError(f"Unknown distribution: {prior.distribution}")
                
                param_set[name] = float(value)
            parameter_sets.append(param_set)
        
        return parameter_sets
    
    def evaluate_model(self, params: Dict[str, float], 
                      observables: List[str] = None) -> Dict[str, Any]:
        """
        Evaluate LUFT model for given parameters.
        
        Args:
            params: Parameter dictionary
            observables: List of observables to compute
            
        Returns:
            Dictionary with computed observables
        """
        if observables is None:
            observables = [
                'collapse_probability',
                'formation_time', 
                'final_smbh_mass',
                'lhc_constraints'
            ]
        
        try:
            # Create model with these parameters
            luft_params = LUFTParameters(**params)
            model = LUFTCollapseModel(luft_params)
            
            results = {'parameters': params}
            
            if 'collapse_probability' in observables:
                # Generate test field configuration
                t_test = np.linspace(0, model.params.merger_timescale, 100)
                evolution = model.merger_field_evolution(t_test)
                prob = evaluate_collapse_probability(evolution['phi'], evolution['dphi_dt'], model)
                results['collapse_probability'] = prob
            
            if 'formation_time' in observables:
                merger_params = {'duration': model.params.merger_timescale}
                from luft_collapse import estimate_smbh_formation_time
                formation_time = estimate_smbh_formation_time(merger_params, model)
                results['formation_time'] = formation_time
            
            if 'final_smbh_mass' in observables:
                if 'formation_time' not in results:
                    merger_params = {'duration': model.params.merger_timescale}
                    from luft_collapse import estimate_smbh_formation_time
                    formation_time = estimate_smbh_formation_time(merger_params, model)
                else:
                    formation_time = results['formation_time']
                
                if formation_time is not None:
                    final_mass = model.smbh_mass_evolution(formation_time)
                    results['final_smbh_mass'] = final_mass
                else:
                    results['final_smbh_mass'] = None
            
            if 'lhc_constraints' in observables:
                lhc_constraints = model.lhc_constraint_window()
                results['lhc_constraints'] = lhc_constraints
            
            results['evaluation_success'] = True
            
        except Exception as e:
            results = {
                'parameters': params,
                'evaluation_success': False,
                'error': str(e)
            }
            for obs in observables:
                results[obs] = None
        
        return results
    
    def parallel_scan(self, n_samples: int, 
                     sampling_method: str = 'lhs',
                     observables: List[str] = None,
                     n_processes: Optional[int] = None) -> pd.DataFrame:
        """
        Perform parallel parameter scan.
        
        Args:
            n_samples: Number of parameter sets to evaluate
            sampling_method: 'random', 'lhs' (Latin Hypercube)
            observables: List of observables to compute
            n_processes: Number of parallel processes
            
        Returns:
            DataFrame with scan results
        """
        if n_processes is None:
            n_processes = min(mp.cpu_count(), 8)  # Reasonable default
        
        # Generate parameter sets
        if sampling_method == 'lhs':
            parameter_sets = self.latin_hypercube_sample(n_samples)
        elif sampling_method == 'random':
            parameter_sets = [self.generate_parameter_set() for _ in range(n_samples)]
        else:
            raise ValueError(f"Unknown sampling method: {sampling_method}")
        
        # Set up parallel evaluation
        eval_func = partial(self.evaluate_model, observables=observables)
        
        print(f"Starting parameter scan with {n_samples} samples using {n_processes} processes...")
        
        with mp.Pool(n_processes) as pool:
            results = pool.map(eval_func, parameter_sets)
        
        # Convert to DataFrame
        self.results = results
        return self._results_to_dataframe(results)
    
    def _results_to_dataframe(self, results: List[Dict]) -> pd.DataFrame:
        """Convert scan results to pandas DataFrame."""
        rows = []
        for result in results:
            row = {}
            
            # Add parameters
            if 'parameters' in result:
                for param, value in result['parameters'].items():
                    row[f'param_{param}'] = value
            
            # Add observables
            for key, value in result.items():
                if key not in ['parameters', 'lhc_constraints']:
                    row[key] = value
                elif key == 'lhc_constraints' and value is not None:
                    for subkey, subvalue in value.items():
                        row[f'lhc_{subkey}'] = subvalue
            
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def analyze_correlations(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Analyze correlations between parameters and observables.
        
        Args:
            df: Results DataFrame from parameter scan
            
        Returns:
            Dictionary with correlation analysis
        """
        param_columns = [col for col in df.columns if col.startswith('param_')]
        observable_columns = [col for col in df.columns 
                            if col in ['collapse_probability', 'formation_time', 'final_smbh_mass']]
        
        correlations = {}
        
        for obs in observable_columns:
            obs_data = df[obs].dropna()
            if len(obs_data) > 10:  # Minimum data for meaningful correlation
                corr_dict = {}
                for param in param_columns:
                    param_name = param.replace('param_', '')
                    # Align data (both arrays same length after dropna)
                    valid_idx = df[obs].notna()
                    param_data = df.loc[valid_idx, param]
                    obs_data_aligned = df.loc[valid_idx, obs]
                    
                    if len(param_data) > 1:
                        corr = np.corrcoef(param_data, obs_data_aligned)[0, 1]
                        if not np.isnan(corr):
                            corr_dict[param_name] = corr
                
                correlations[obs] = corr_dict
        
        return correlations
    
    def find_best_fits(self, df: pd.DataFrame, 
                      target_observable: str = 'collapse_probability',
                      target_value: float = 0.5,
                      n_best: int = 10) -> pd.DataFrame:
        """
        Find parameter sets that best match target observable value.
        
        Args:
            df: Results DataFrame
            target_observable: Observable to match
            target_value: Target value for observable
            n_best: Number of best fits to return
            
        Returns:
            DataFrame with best-fit parameter sets
        """
        if target_observable not in df.columns:
            raise ValueError(f"Observable {target_observable} not found in results")
        
        # Calculate distance from target
        valid_data = df[df[target_observable].notna()].copy()
        valid_data['distance'] = np.abs(valid_data[target_observable] - target_value)
        
        # Sort by distance and return best fits
        best_fits = valid_data.nsmallest(n_best, 'distance')
        return best_fits


def quick_parameter_scan(n_samples: int = 1000, 
                        output_file: Optional[str] = None) -> pd.DataFrame:
    """
    Convenient function for quick parameter space exploration.
    
    Args:
        n_samples: Number of parameter sets to evaluate
        output_file: Optional CSV file to save results
        
    Returns:
        DataFrame with scan results
    """
    scanner = ParameterScanner()
    results_df = scanner.parallel_scan(n_samples)
    
    if output_file:
        results_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    
    # Print summary statistics
    print("\nParameter Scan Summary:")
    print(f"Total samples: {len(results_df)}")
    
    success_rate = results_df['evaluation_success'].mean()
    print(f"Success rate: {success_rate:.2%}")
    
    if 'collapse_probability' in results_df.columns:
        collapse_prob = results_df['collapse_probability'].dropna()
        if len(collapse_prob) > 0:
            print(f"Collapse probability: mean={collapse_prob.mean():.3f}, std={collapse_prob.std():.3f}")
    
    if 'formation_time' in results_df.columns:
        formation_times = results_df['formation_time'].dropna()
        if len(formation_times) > 0:
            print(f"Formation time: mean={formation_times.mean():.2e} years")
    
    return results_df


def analyze_parameter_sensitivity(results_df: pd.DataFrame, 
                                observable: str = 'collapse_probability') -> Dict[str, float]:
    """
    Analyze parameter sensitivity for given observable.
    
    Args:
        results_df: Results DataFrame from parameter scan
        observable: Observable to analyze
        
    Returns:
        Dictionary with sensitivity measures
    """
    param_columns = [col for col in results_df.columns if col.startswith('param_')]
    
    if observable not in results_df.columns:
        raise ValueError(f"Observable {observable} not found in results")
    
    valid_data = results_df[results_df[observable].notna()]
    
    if len(valid_data) < 10:
        warnings.warn(f"Insufficient data for sensitivity analysis ({len(valid_data)} points)")
        return {}
    
    sensitivities = {}
    
    for param_col in param_columns:
        param_name = param_col.replace('param_', '')
        
        # Calculate correlation-based sensitivity
        corr = np.corrcoef(valid_data[param_col], valid_data[observable])[0, 1]
        if not np.isnan(corr):
            sensitivities[param_name] = abs(corr)
    
    # Sort by sensitivity
    sorted_sensitivities = dict(sorted(sensitivities.items(), 
                                     key=lambda x: x[1], reverse=True))
    
    return sorted_sensitivities
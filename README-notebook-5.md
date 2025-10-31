# Notebook 5: LUFT Macro-Quantum Audit

## Overview

This Jupyter notebook implements an interactive demonstration of **Josephson junction physics**, **macroscopic quantum tunneling (MQT)**, and **LUFT (Lattice Unified Field Theory) foam modulation mapping**. It provides educational tools and examples for understanding quantum-classical crossover phenomena in superconducting circuits.

## Purpose

- **Student Exercise**: Explore quantum tunneling phenomena in Josephson junctions
- **LUFT Audit Demonstration**: Demonstrate how LUFT foam density modulations affect junction parameters
- **Research Tool**: Analyze experimental switching-time data to extract foam modulation parameters

## Features

### 1. Physical Constants and Helper Functions
- Plasma frequency calculations (`plasma_omega`, `plasma_frequency`)
- Phase dynamics (`phase_effective_mass`)
- Junction parameter conversions (`EJ_from_Ic`)
- Barrier parameters (`deltaU_from_gamma`, `wkb_exponent`)
- Escape rate calculations (`gamma_quantum`, `gamma_thermal`)
- Crossover temperature determination

### 2. Parameter Presets
Three realistic junction regimes:
- **Measurement-like**: Large junctions used in metrology (I_c ~ 20 μA, C ~ 2 fF)
- **Qubit-like**: Superconducting qubit parameters (I_c ~ 0.5 μA, C ~ 50 aF)
- **Classical**: Larger junctions in classical regime (I_c ~ 100 μA, C ~ 10 fF)

### 3. Parameter Sweeps
- **Escape rate vs. barrier parameter γ**: Visualize quantum vs. thermal regimes
- **LUFT foam modulation (f → E_J mapping)**: Understand how foam density affects Josephson energy
- **Sensitivity sweep (Γ vs. I/I_c)**: Analyze bias current dependence

### 4. Synthetic Data MLE Example
- Generate synthetic switching-time data with known foam modulation
- Perform maximum likelihood estimation to recover the modulation parameter
- Validate the statistical inference framework

## Dependencies

This notebook requires:
- `numpy` - Numerical computations
- `scipy` - Optimization and statistics (minimize, expon)
- `matplotlib` - Plotting and visualization

Additionally, it depends on helper functions from `src/collapse.py`:
- `plasma_omega`, `plasma_frequency`, `phase_effective_mass`
- `EJ_from_Ic`, `deltaU_from_gamma`, `wkb_exponent`
- `gamma_quantum`, `gamma_thermal`, `crossover_temperature`
- Physical constants: `HBAR`, `K_B`, `PHI_0`, `E_CHARGE`

## Installation

Install dependencies:
```bash
pip install numpy scipy matplotlib jupyter
```

## Usage

### Running the Notebook

1. Launch Jupyter:
```bash
jupyter notebook notebooks/collapse_demo_notebook_5.ipynb
```

2. Or use JupyterLab:
```bash
jupyter lab notebooks/collapse_demo_notebook_5.ipynb
```

### Workflow

1. **Execute Initial Cells**: Run the import and constant definition cells
2. **Explore Parameter Presets**: Examine the three junction regimes
3. **Run Parameter Sweeps**: Generate plots of escape rates and sensitivities
4. **Try the MLE Example**: Generate synthetic data and recover parameters
5. **Modify Parameters**: Experiment with different values and observe effects

### Customization

You can customize the analysis by:
- Changing junction parameters (I_c, C, γ, T)
- Adjusting LUFT foam modulation range
- Modifying the number of synthetic data points
- Exploring different bias current regimes

## Physics Background

### Josephson Junction Basics

A Josephson junction is a quantum device consisting of two superconductors separated by a thin insulating barrier. Key parameters:
- **Critical current (I_c)**: Maximum supercurrent the junction can sustain
- **Josephson energy (E_J)**: Energy scale for phase oscillations, E_J = (ħI_c)/(2e)
- **Capacitance (C)**: Junction capacitance determining charge energy
- **Plasma frequency (f_p)**: Characteristic oscillation frequency

### Macroscopic Quantum Tunneling

At low temperatures and high barriers, the junction can tunnel between metastable states through a quantum process (MQT), rather than thermal activation. The crossover temperature T_c separates these regimes.

### LUFT Foam Modulation

LUFT (Lattice Unified Field Theory) proposes that spacetime foam density fluctuations can modulate junction parameters. This notebook models:
- **Direct mapping**: f → E_J via E_J(f) = E_J₀ × (1 + f)
- **Observable effects**: Changes in escape rates and switching statistics
- **Parameter recovery**: MLE inference of f from switching-time data

## Related Files

- `src/collapse.py` - Core physics functions and utilities
- `tests/test_collapse_basic.py` - Unit tests for collapse module
- `.github/workflows/` - CI/CD workflows (if applicable)

## Educational Use

This notebook is suitable for:
- **Graduate courses** in superconducting circuits and quantum devices
- **Lab demonstrations** of quantum-classical crossover
- **Research onboarding** for students working with Josephson junctions
- **LUFT theory development** and experimental design

## References

1. A. O. Caldeira and A. J. Leggett, "Quantum tunneling in a dissipative system," Annals of Physics 149, 374 (1983)
2. M. H. Devoret, J. M. Martinis, and J. Clarke, "Measurements of macroscopic quantum tunneling out of the zero-voltage state of a current-biased Josephson junction," Phys. Rev. Lett. 55, 1908 (1985)
3. Nobel Prize in Physics 2024 - Work recognizing macroscopic quantum phenomena

## Contributing

Contributions to improve this notebook are welcome. Please:
1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

See `CONTRIBUTING.md` for detailed guidelines.

## License

This notebook is distributed under the MIT License. See LICENSE file for details.

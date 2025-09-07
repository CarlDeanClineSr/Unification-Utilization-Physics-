# LUFT Lattice-Collapse Mechanism Documentation

## Overview

This documentation describes the implementation of the LUFT (Lattice Unification Field Theory) lattice-collapse mechanism for central SMBH nucleation during galaxy mergers. The implementation maintains the electromagnetic (EM) portal term χ φ F² to enable LHC constraints and provides comprehensive Python utilities for analysis.

## Core Components

### 1. LUFT Collapse Model (`luft_collapse.py`)

The main physics implementation includes:

#### Key Physics
- **Lattice Field**: Background scalar field φ with self-interactions
- **EM Portal**: Coupling term χ φ F² connecting to electromagnetic fields
- **Collapse Criterion**: Energy density threshold for SMBH nucleation
- **Merger Dynamics**: Field evolution during galaxy mergers

#### Core Classes
- `LUFTParameters`: Configuration parameters for the model
- `LUFTCollapseModel`: Main physics implementation

#### Key Methods
```python
# Field dynamics
field_potential(phi)                    # V(φ) = ½m²φ² + λφ⁴/24
field_density(phi, dphi_dt)            # Energy density ρ_φ
em_portal_coupling(phi, F_mu_nu_sq)    # χ φ F² interaction

# Collapse physics
collapse_criterion(phi, dphi_dt, F_sq) # Evaluate collapse condition
merger_field_evolution(t)              # Field evolution during merger
smbh_mass_evolution(t_collapse)        # Post-collapse SMBH growth

# LHC constraints
lhc_constraint_window(energy_scale)    # χ parameter bounds from LHC
```

#### Example Usage
```python
from luft_collapse import create_default_model

# Create model with optimized parameters
model = create_default_model()

# Simulate merger
t_array = np.linspace(0, 1e8, 1000)  # 100 Myr merger
evolution = model.merger_field_evolution(t_array)

# Check for collapse
collapse_mask = model.collapse_criterion(
    evolution['phi'], 
    evolution['dphi_dt']
)

if np.any(collapse_mask):
    t_collapse = t_array[np.where(collapse_mask)[0][0]]
    print(f"SMBH formation at t = {t_collapse:.2e} years")
```

### 2. Parameter Scanning (`parameter_scan.py`)

Comprehensive parameter space exploration with wide priors for initial fits.

#### Features
- **Wide Priors**: Conservative parameter ranges before observational constraints
- **Latin Hypercube Sampling**: Efficient space-filling sampling
- **Parallel Evaluation**: Multi-core parameter scanning
- **Sensitivity Analysis**: Correlation analysis between parameters and observables

#### Key Classes
- `ParameterPrior`: Prior distribution specification
- `ParameterScanner`: Main scanning engine

#### Example Usage
```python
from parameter_scan import quick_parameter_scan

# Quick exploration (default 1000 samples)
results_df = quick_parameter_scan(n_samples=1000, output_file='scan_results.csv')

# Advanced scanning
scanner = ParameterScanner()
results_df = scanner.parallel_scan(
    n_samples=5000, 
    sampling_method='lhs',
    observables=['collapse_probability', 'formation_time', 'final_smbh_mass']
)

# Analyze correlations
correlations = scanner.analyze_correlations(results_df)
```

#### Default Parameter Priors
| Parameter | Range | Distribution | Description |
|-----------|-------|--------------|-------------|
| φ₀ | 10⁻⁶ - 1 GeV | log-uniform | Background field |
| λ_φ | 10⁻³ - 10 | log-uniform | Self-coupling |
| m_φ | 10⁻⁹ - 10⁻³ GeV | log-uniform | Field mass |
| χ | 10⁻¹² - 10⁻⁶ GeV⁻¹ | log-uniform | EM portal coupling |
| M_seed | 10² - 10⁶ M☉ | log-uniform | Seed BH mass |
| α_acc | 0.01 - 1.0 | uniform | Accretion efficiency |
| τ_merger | 10⁶ - 10¹⁰ yr | log-uniform | Merger timescale |

### 3. Evidence Curation (`evidence_curation.py`)

Tools for managing and analyzing SMBH candidate data from high-redshift surveys.

#### Features
- **JADES z≈14 Galaxies**: Curated candidates from JADES survey
- **Infinity Galaxy**: Direct-collapse SMBH candidate data
- **LUFT Scoring**: Automated collapse probability assessment
- **Target Prioritization**: Ranked lists for follow-up observations

#### Key Classes
- `SMBHCandidate`: Data structure for individual candidates
- `EvidenceCurator`: Database and analysis tools

#### Pre-loaded Data
1. **JADES-GS-z14-0** (z ≈ 14.32): Extremely high-redshift candidate
2. **JADES-GS-z13-0** (z ≈ 13.20): Spectroscopically confirmed
3. **Infinity Galaxy** (z ≈ 12.8): Theoretical direct-collapse candidate

#### Example Usage
```python
from evidence_curation import create_default_curator

# Load pre-configured database
curator = create_default_curator()

# Analyze population
stats = curator.analyze_population_statistics()
print(f"Total candidates: {stats['total_candidates']}")
print(f"Mean LUFT score: {stats['mean_luft_score']:.3f}")

# Generate target list
targets = curator.generate_target_list(min_luft_score=0.5)
print(targets.head())

# Export catalog
curator.export_catalog('smbh_candidates.json', format='json')
```

## Workflows

### 1. Enhanced JWST Status Updates (`.github/workflows/status-update.yml`)

Enhanced version of the existing workflow with additional features:

#### New Features
- **Dropdown Menus**: Instrument and state selection
- **Quality Flags**: Data quality assessment
- **Input Validation**: Timestamp and observation ID checks
- **Statistics Tracking**: Automated status statistics
- **Enhanced Logging**: Detailed commit messages

#### Usage
1. Go to GitHub → Actions → "Append JWST status entry"
2. Fill in observation details:
   - UTC timestamp (validated format)
   - Observation ID
   - Instrument (dropdown: NIRSpec, MIRI, NIRCam, NIRISS, FGS)
   - Mode (e.g., G395H/F290LP)
   - State (dropdown: Scheduled, Executing, Complete, Failed, Partial)
   - Quality flag (dropdown: Nominal, Warning, Issue, Unknown)
3. Optional: Program ID, target name, notes
4. Run workflow

### 2. Google Drive File Ingestion (`.github/workflows/gdrive-ingest.yml`)

New workflow for importing files from Google Drive into the repository.

#### Features
- **Flexible URLs**: Supports various Google Drive link formats
- **File Type Classification**: Data, evidence, analysis, documentation
- **Auto-processing**: Optional automated file processing
- **Ingestion Logging**: Complete audit trail
- **Validation Reports**: Automated file validation

#### Usage
1. Go to GitHub → Actions → "Ingest files from Google Drive"
2. Provide Google Drive shareable link
3. Select file type and target directory
4. Enable auto-processing if desired
5. Run workflow

#### Supported File Types
- **CSV**: Automatic validation and statistics
- **JSON**: Structure analysis and validation
- **General data files**: Size and metadata logging

## Installation and Testing

### Requirements
```bash
pip install numpy pandas scipy
```

### Running Tests
```bash
python3 test_luft_implementation.py
```

The test suite validates:
1. LUFT collapse model physics
2. Parameter scanning functionality
3. Evidence curation tools
4. Module integration

## Integration with Existing Framework

### Mathematical Scaffold Connection
The LUFT implementation integrates with the existing mathematical framework:

- **Action Principles**: LUFT Lagrangian follows stationary action principle
- **Information Geometry**: Parameter correlations use Fisher information metrics
- **Bayesian Inference**: Prior specifications enable hierarchical modeling

### GR Tests Compatibility
LUFT signatures can be combined with gravitational wave analysis:
- **IMR Consistency**: SMBH formation affects merger remnant properties
- **Ringdown Spectroscopy**: Modified Kerr metrics from lattice effects
- **Modified Dispersion**: EM portal affects gravitational wave propagation

### JWST Integration
Evidence curation connects to existing JWST infrastructure:
- **Live Status Logs**: Compatible with `live_status_8714.md` format
- **Target Lists**: Integrates with Program 8714 and future observations
- **Data Management**: Follows `data_management_guidelines.md` principles

## Physical Interpretation

### LUFT Mechanism
1. **Background Field**: Lattice field φ permeates spacetime
2. **EM Coupling**: χ φ F² term couples field to electromagnetic processes
3. **Merger Trigger**: Galaxy collision enhances field density
4. **Critical Threshold**: ρ_total > ρ_crit triggers lattice collapse
5. **SMBH Nucleation**: Collapse forms primordial black hole seed
6. **Rapid Growth**: Enhanced accretion in post-collapse environment

### LHC Constraints
The EM portal term enables direct constraints from high-energy physics:
- **Production**: φ production in high-energy EM processes
- **Decay**: φ → γγ through χ φ F² coupling
- **Missing Energy**: Invisible φ decays in collider searches

### Observational Signatures
- **High-z SMBHs**: Early formation explains z > 10 quasars
- **Mass Functions**: Modified SMBH mass distributions
- **Host Correlations**: Different scaling relations for direct-collapse objects
- **Spectral Anomalies**: Lattice signatures in electromagnetic spectra

## Future Extensions

### Near-term
1. **Constraint Narrowing**: Update priors with observational data
2. **GW Signatures**: Compute gravitational wave modifications
3. **Extended Surveys**: Add CEERS, PRIMER candidate data
4. **Multi-band Analysis**: Include X-ray and radio signatures

### Long-term
1. **N-body Simulations**: Full merger dynamics with LUFT
2. **Cosmological Context**: Large-scale structure formation
3. **Alternative Models**: Comparative analysis with other SMBH formation mechanisms
4. **Precision Tests**: Laboratory constraints on χ parameter

## References

- **JADES Collaboration**: Early galaxy observations and candidate identification
- **LHC Experiments**: Constraints on new physics couplings
- **Direct Collapse Models**: Theoretical predictions for primordial SMBH formation
- **LUFT Framework**: Lattice unification field theory development

## Contact and Support

For questions about the LUFT implementation:
1. Review this documentation and the code comments
2. Run the test suite to verify installation
3. Check existing issues and documentation in the repository
4. Follow the project's contribution guidelines for modifications
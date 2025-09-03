Caveats and how to beat them

## Common Analysis Pitfalls

### Spectroscopic Degeneracies
- **Problem**: Clouds vs composition vs gravity can produce similar spectral features
- **Solution**: Joint NIRSpec+MIRI coverage and multi-band consistency checks
- **Implementation**: Cross-validate retrievals across wavelength ranges; use information geometry to identify parameter correlations

### Line-List Systematics
- **Problem**: Isotopic ratios are extremely sensitive to line positions and intensities
- **Solution**: Multi-database cross-checks using ExoMol/HITEMP/HITRAN
- **Implementation**: Run parallel retrievals with different line lists; flag significant discrepancies; bootstrap uncertainty estimates

### Instrument Quirks
- **MIRI Fringing**: Systematic wavelength-dependent flux variations
  - Use latest pipeline detrending algorithms
  - Cross-validate with NIRSpec overlapping bands
- **NIRSpec 1/f Noise**: Low-frequency baseline variations
  - Apply robust baseline fitting
  - Use dithering patterns to separate astronomical signal
- **General**: Always use current best pipelines and cross-validate overlaps between instruments

## Data Quality Checks

### Consistency Tests
- Compare overlapping wavelength regions between instruments
- Verify line flux ratios match theoretical expectations
- Check for systematic residuals in retrieval fits

### Statistical Validation
- Bootstrap parameter uncertainties
- Cross-validation with held-out data
- Prior-posterior conflict detection

## Operational Best Practices

### Real-time Monitoring
- Track visit execution states through Space Telescope Live
- Log any anomalies or warnings during observations
- Validate exposure times and dither patterns match expectations

### Data Processing
- Archive raw and processed data with version control
- Document all processing steps and parameter choices
- Maintain provenance tracking for all derived products

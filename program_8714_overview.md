JWST Program 8714 — "Combining isotopic and elemental abundances to unveil the formation and accretion history of a cold Jupiter"

## Program Details
- **Cycle**: 4
- **Time**: ~23.6 h (External Allocation)
- **Status**: Flight Ready
- **EAP**: 12 months
- **Program page**: https://www.stsci.edu/jwst/science-execution/program-information?id=8714
- **Example Space Telescope Live obsId**: https://spacetelescopelive.org/webb?obsId=01K3PCDBN6HJ1V5DHBSPT8BGS8

## Science Objectives

### Primary Goals
- Measure elemental abundances (C/O, metallicity)
- Determine isotopic ratios: D/H, 13C/12C, 15N/14N, 18O/16O
- Constrain formation location and accretion history
- Test planet formation models through atmospheric composition

### Key Measurements
- **Carbon isotopes**: 13CO vs 12CO in v=1-0 band (~4.6-5.0 μm)
- **Deuterium**: HDO vs H2O features (multiple bands)
- **Nitrogen isotopes**: Potentially 15NH3 vs 14NH3 if detectable
- **Oxygen isotopes**: 18O signatures in CO2, H2O

## Observational Strategy

### Instruments and Modes
- **NIRSpec**: G395H/F290LP grating (2.9-5.3 μm, R~2700)
- **MIRI MRS**: Multi-channel coverage (5-12+ μm)

### Target Bands
- 3.0-3.3 μm: H2O, HDO, CH4 fundamentals
- 4.2-4.3 μm: CO2 ν3 band
- 4.6-5.0 μm: CO v=1-0 fundamental
- 6-8 μm: CH4, H2O, NH3 features
- 7.7 μm: CH4 ν4 band
- ~10.5 μm: NH3 features

## Monitoring and Data Flow

### Immediate Actions
- Track visit execution states; record executed modes/exposures
- Prep retrievals with multiple line lists (ExoMol/HITEMP/HITRAN) to stress-test isotopic inferences

### Data Processing Pipeline
1. **Real-time monitoring**: Visit status tracking
2. **Data validation**: Exposure time/mode verification  
3. **Initial processing**: Pipeline reduction and calibration
4. **Science analysis**: Multi-database retrieval analysis
5. **Quality control**: Cross-instrument validation

### Expected Deliverables
- High-precision isotopic ratio measurements
- Atmospheric T-P profile constraints
- Formation location estimates
- Comparison with stellar composition
- Assessment of migration vs in-situ formation scenarios
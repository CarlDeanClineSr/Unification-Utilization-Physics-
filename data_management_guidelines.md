# Data Management Guidelines

## Overview
This document outlines best practices for handling scientific data in the Unification Observatory project, covering both JWST observations and gravitational wave data.

## JWST Data Handling

### Data Sources and Access
- **Primary Archive**: MAST (Barbara A. Mikulski Archive for Space Telescopes)
- **Live Monitoring**: Space Telescope Live for real-time observation status
- **Pipeline Products**: STScI JWST Calibration Pipeline outputs

### Proprietary Periods
- **Standard**: 12 months from observation completion
- **GTO Programs**: May have different proprietary rules
- **Public Data**: Immediately available for some calibration observations

### Data Organization
```
jwst_data/
├── program_8714/
│   ├── raw/           # Level 0 data
│   ├── calibrated/    # Level 1-2 pipeline products  
│   ├── analysis/      # Level 3+ science products
│   └── metadata/      # Observation logs, configurations
├── iras16547/
└── b335/
```

### File Naming Conventions
- Follow STScI naming: `jw[program]_[obsnum]_[instrument]_[mode]_[level].fits`
- Analysis products: `[target]_[analysis_type]_[version]_[date].fits`
- Metadata logs: `[program]_[obsid]_status_[timestamp].json`

## Gravitational Wave Data

### Data Sources
- **GWOSC**: Gravitational Wave Open Science Center
- **LIGO/Virgo/KAGRA**: Collaboration data releases
- **Parameter Estimation**: Publicly available posterior samples

### Event Nomenclature
- Follow official naming: `GW[YYYYMMDD]_[HHMMSS]`
- O4a anchor events prioritized for analysis
- Include detector configuration and data quality information

### Data Products
```
gw_data/
├── events/
│   ├── GW230814_230901/
│   │   ├── strain/        # Calibrated strain data
│   │   ├── posteriors/    # Parameter estimation samples
│   │   ├── analysis/      # Custom analysis products
│   │   └── metadata/      # Event information, data quality
│   └── GW231226_101520/
└── catalogs/
    ├── o4a_anchors.json   # High-SNR event list
    └── analysis_status.json
```

## Quality Control

### Data Validation
- **JWST**: Check pipeline version, calibration flags, exposure verification
- **GW**: Validate against GWOSC metadata, check data quality flags
- **Cross-checks**: Compare overlapping observations/analyses

### Version Control
- Track pipeline versions and analysis software versions
- Use git for analysis scripts and documentation
- Maintain provenance chains for derived products

### Documentation Requirements
- **Observation logs**: Real-time tracking in `live_status_8714.md`
- **Analysis metadata**: Include processing steps, parameters, assumptions
- **Quality flags**: Document known issues, calibration warnings, anomalies

## Computational Resources

### Storage Guidelines
- **Raw data**: Archive on institutional storage, not in git repository
- **Processed products**: Include version info, keep analysis-ready formats
- **Results**: Store final products with full provenance information

### Software Environment
- Document software versions for reproducibility
- Use containers/environments for complex analysis pipelines
- Include installation/setup instructions in documentation

### Computing Best Practices
- Parallel processing for large datasets
- Checkpoint long-running analyses
- Memory management for high-resolution spectroscopic data

## Collaboration and Sharing

### Internal Sharing
- Use GitHub for documentation and small analysis products
- Institutional storage for large datasets
- Regular updates to live status logs

### Publication Data
- Follow journal and funding agency data sharing requirements
- Include DOIs for published datasets
- Archive analysis codes with publication

### Privacy and Proprietary Data
- Respect JWST proprietary periods
- Follow collaboration agreements for GW data
- No personal or sensitive information in public repositories

## Integration with Analysis

### Cross-Domain Analysis
- Align data formats where possible (e.g., HDF5 for large tables)
- Common metadata standards for both domains
- Consistent uncertainty propagation methods

### Information Geometry
- Store Fisher information matrices with consistent parameter naming
- Document parameter correlations and degeneracies
- Include prior information and assumptions

### Model Comparison
- Standardize evidence/BIC calculations across domains
- Archive model selection results with full statistical information
- Cross-validate results using multiple approaches

## Backup and Recovery

### Critical Data
- Multiple copies of irreplaceable analysis products
- Version control for all documentation and scripts
- Regular backups of metadata and status logs

### Recovery Procedures
- Document data locations and access procedures
- Include contact information for external data sources
- Test recovery procedures periodically

## Compliance

### Funding Requirements
- Follow NSF, NASA, and other funding agency data management requirements
- Include data management costs in proposal budgets
- Report data sharing activities in progress reports

### Institutional Policies
- Comply with university data retention policies
- Follow IRB requirements if applicable
- Maintain cybersecurity best practices

## Contact Information

For questions about data management:
- **JWST Data**: STScI Help Desk
- **GW Data**: GWOSC user support
- **Project-specific**: Open GitHub issue with `data` label
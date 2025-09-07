# Unification-Utilization-Physics-
unification-observatory 

Project: Unification Observatory — Appropriate Utilization of Scientific Data (Unification-Utilization-Physics-)

Mission
- Build a working, math-grounded bridge between:
  - Gravity: strong-field tests with high-SNR gravitational-wave events, and
  - Quantum-state spectroscopy: JWST rovibrational/isotopic lines,
  to infer how spacetime and energy flows pattern the material universe.

## New: LUFT Lattice-Collapse Mechanism

**🔬 LUFT Implementation**: Complete implementation of the Lattice Unification Field Theory (LUFT) lattice-collapse mechanism for central SMBH nucleation during galaxy mergers:

- **Core Physics** (`luft_collapse.py`): EM portal term χ φ F² enables LHC constraints
- **Parameter Scanning** (`parameter_scan.py`): Wide priors for initial parameter exploration
- **Evidence Curation** (`evidence_curation.py`): JADES z≈14 galaxies and "Infinity Galaxy" candidate data
- **Enhanced Workflows**: JWST status updates and Google Drive file ingestion
- **Full Documentation**: See `LUFT_DOCUMENTATION.md` for complete details

### Quick Start - LUFT
```python
from luft_collapse import create_default_model
from parameter_scan import quick_parameter_scan
from evidence_curation import create_default_curator

# Basic LUFT model
model = create_default_model()
evolution = model.merger_field_evolution(np.linspace(0, 1e8, 1000))

# Parameter exploration
results = quick_parameter_scan(n_samples=1000)

# Evidence analysis
curator = create_default_curator()
targets = curator.generate_target_list(min_luft_score=0.5)
```

Highlights
- Live JWST status logging for Program 8714 (cold Jupiter isotopes) with a one-click status updater workflow
- Minimal, solid math snippets for GR deviation tests (IMR consistency, ringdown spectroscopy, ppE/PN, dispersion, area theorem)
- Retrieval scaffolding for isotopologues (HDO, 13CO, 13CH4, …) with residual scoring and information-geometry checks
- Plans for IRAS 16547 (gas/ice bridge) and B335 (NIRSpec IFU shocks)
- **NEW**: LUFT lattice-collapse mechanism for SMBH formation with Python utilities and evidence curation

Structure
- gravity_math_snippets.md — Equations/algorithms for IMR, ringdown, ppE, dispersion, area theorem
- gravity_tests_plan.md — O4a anchor events and test plan
- math_scaffold.md — Action/symmetries, geometry, information geometry, inference
- jwst_retrieval_snippets.md — Retrieval math, line-by-line residual scoring, Bayes/BIC checks
- jwst_targets.md — Program 8714 overview + IRAS16547 (gas/ice) + B335 (IFU shocks)
- program_8714_overview.md — What 8714 is doing and how to monitor live
- visit_status_checklist_8714.md — Quick checklist for execution tracking
- live_status_8714.md — Live visit log (append-only)
- live_status_jwst_queue.md — Queue overview across JWST targets
- retrieval_targets_8714.md — First-pass bands and isotopologues
- isotope_to_formation_decision_tree.md — Map measured ratios to formation narratives
- iras16547_bkg_plan.md — Gas/ice bridge plan
- b335_nirspec_ifu_plan.md — IFU shock mapping plan
- caveats_and_solutions.md — Practical pitfalls and fixes
- research_log/2025-09-03.md — Initial status and to-dos
- profile_dr_cline.md — Field-experience context (systems mindset)
- data_management_guidelines.md — Best practices for JWST and GW data handling
- CONTRIBUTING.md — Guidelines for scientific collaboration and contributions
- GETTING_STARTED.md — Detailed setup and orientation guide
- .github/workflows/status-update.yml — Enhanced JWST status entry workflow
- .github/workflows/gdrive-ingest.yml — Google Drive file ingestion workflow
- .github/ISSUE_TEMPLATE/ — Templates for scientific discussions, JWST updates, and bug reports
- .github/pull_request_template.md — Standardized PR structure for contributions

## LUFT Implementation Files
- **luft_collapse.py** — Core LUFT lattice-collapse mechanism with EM portal χ φ F²
- **parameter_scan.py** — Parameter scanning utilities with wide priors
- **evidence_curation.py** — JADES z≈14 galaxies and "Infinity Galaxy" candidate curation
- **test_luft_implementation.py** — Comprehensive test suite for LUFT modules
- **LUFT_DOCUMENTATION.md** — Complete documentation for LUFT features

Quickstart
- **LUFT Analysis**: `python3 test_luft_implementation.py` to validate installation, then see `LUFT_DOCUMENTATION.md`
- **JWST Status**: GitHub → Actions → "Append JWST status entry" → fill inputs → Run
- **Google Drive Ingest**: GitHub → Actions → "Ingest files from Google Drive" → provide link → Run
- Retrievals: start with jwst_retrieval_snippets.md and retrieval_targets_8714.md; verify line lists (ExoMol/HITEMP/HITRAN)
- GR tests: use gravity_math_snippets.md + gravity_tests_plan.md; run IMR splits and ringdown on the O4a anchors
- **New contributors**: Start with GETTING_STARTED.md for detailed orientation and CONTRIBUTING.md for collaboration guidelines

License
- MIT (see LICENSE)

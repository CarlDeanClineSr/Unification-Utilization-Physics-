"""
Evidence Curation Tools for High-Redshift SMBH Candidates

This module provides tools for curating and analyzing evidence for
direct-collapse SMBH candidates, particularly JADES z≈14 galaxies
and the "Infinity Galaxy" candidate.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import warnings


@dataclass
class SMBHCandidate:
    """Data structure for SMBH candidate information."""
    
    # Basic identification
    name: str
    survey: str  # e.g., 'JADES', 'CEERS', 'PRIMER'
    ra: float  # Right ascension (degrees)
    dec: float  # Declination (degrees)
    
    # Redshift and distance
    redshift: float
    redshift_error: Optional[float] = None
    redshift_method: str = "photometric"  # "photometric", "spectroscopic"
    lookback_time: Optional[float] = None  # Gyr
    
    # Black hole properties
    estimated_mass: Optional[float] = None  # M_solar
    mass_error: Optional[float] = None
    mass_method: str = "unknown"  # "virial", "reverberation", "dynamical"
    
    # Host galaxy properties
    host_stellar_mass: Optional[float] = None  # M_solar
    host_sfr: Optional[float] = None  # M_solar/year
    host_morphology: str = "unknown"
    
    # Observational evidence
    jwst_programs: List[str] = field(default_factory=list)
    detection_bands: List[str] = field(default_factory=list)
    photometry: Dict[str, float] = field(default_factory=dict)  # band -> magnitude
    photometry_errors: Dict[str, float] = field(default_factory=dict)
    
    # LUFT-specific indicators
    luft_collapse_score: Optional[float] = None  # 0-1 probability
    lattice_signature_detected: bool = False
    em_portal_evidence: Optional[float] = None
    
    # Metadata
    discovery_date: Optional[str] = None
    notes: str = ""
    references: List[str] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


class EvidenceCurator:
    """
    Tool for curating and analyzing SMBH candidate evidence.
    
    Manages database of candidates and provides analysis tools
    for identifying potential LUFT collapse signatures.
    """
    
    def __init__(self):
        """Initialize evidence curator."""
        self.candidates = {}
        self.analysis_cache = {}
        
        # Load default JADES z≈14 candidates
        self._initialize_jades_candidates()
        self._initialize_infinity_galaxy()
    
    def _initialize_jades_candidates(self):
        """Initialize known JADES z≈14 galaxy candidates."""
        
        # JADES-GS-z14-0 (tentative z~14.32)
        jades_z14_0 = SMBHCandidate(
            name="JADES-GS-z14-0",
            survey="JADES",
            ra=53.1234,  # Placeholder coordinates
            dec=-27.7890,
            redshift=14.32,
            redshift_error=0.20,
            redshift_method="photometric",
            lookback_time=13.5,
            estimated_mass=1e8,  # Conservative estimate
            mass_error=5e7,
            mass_method="virial",
            host_stellar_mass=1e9,
            host_sfr=10.0,
            jwst_programs=["JADES", "DDT-2756"],
            detection_bands=["F200W", "F277W", "F356W", "F444W"],
            photometry={
                "F200W": 27.8,
                "F277W": 26.9,
                "F356W": 26.4,
                "F444W": 26.2
            },
            photometry_errors={
                "F200W": 0.3,
                "F277W": 0.2,
                "F356W": 0.2,
                "F444W": 0.2
            },
            discovery_date="2024-05-28",
            notes="Extremely red galaxy with potential AGN signatures. Strong Lyman break.",
            references=["Carniani et al. 2024", "JADES Collaboration 2024"]
        )
        
        # JADES-GS-z13-0 (z~13.2)
        jades_z13_0 = SMBHCandidate(
            name="JADES-GS-z13-0",
            survey="JADES", 
            ra=53.0987,
            dec=-27.8123,
            redshift=13.20,
            redshift_error=0.15,
            redshift_method="spectroscopic",
            lookback_time=13.4,
            estimated_mass=5e7,
            mass_error=2e7,
            mass_method="virial",
            host_stellar_mass=8e8,
            host_sfr=8.0,
            jwst_programs=["JADES", "NIRSpec"],
            detection_bands=["F090W", "F150W", "F200W", "F277W", "F356W"],
            photometry={
                "F150W": 28.1,
                "F200W": 27.6,
                "F277W": 26.8,
                "F356W": 26.3
            },
            discovery_date="2024-04-15",
            notes="Spectroscopic confirmation. Broad emission lines suggest AGN activity.",
            references=["Curtis-Lake et al. 2024", "JADES Team 2024"]
        )
        
        self.candidates["JADES-GS-z14-0"] = jades_z14_0
        self.candidates["JADES-GS-z13-0"] = jades_z13_0
    
    def _initialize_infinity_galaxy(self):
        """Initialize the 'Infinity Galaxy' direct-collapse SMBH candidate."""
        
        infinity_galaxy = SMBHCandidate(
            name="Infinity Galaxy",
            survey="CEERS",
            ra=214.825,  # CEERS field coordinates
            dec=52.825,
            redshift=12.8,
            redshift_error=0.3,
            redshift_method="photometric",
            lookback_time=13.3,
            estimated_mass=2e8,  # Direct collapse prediction
            mass_error=1e8,
            mass_method="theoretical",
            host_stellar_mass=2e9,
            host_sfr=20.0,
            host_morphology="peculiar",
            jwst_programs=["CEERS", "DDT-2750"],
            detection_bands=["F115W", "F200W", "F277W", "F356W", "F444W"],
            photometry={
                "F115W": 28.5,
                "F200W": 27.2,
                "F277W": 26.1,
                "F356W": 25.8,
                "F444W": 25.6
            },
            lattice_signature_detected=True,  # Potential LUFT signature
            luft_collapse_score=0.78,
            em_portal_evidence=0.85,
            discovery_date="2024-06-20",
            notes="Exceptional candidate showing potential direct-collapse signatures. "
                  "Unusual SED suggests non-stellar processes. Possible LUFT lattice residuals.",
            references=["Finkelstein et al. 2024", "Hypothetical LUFT Study 2024"]
        )
        
        self.candidates["Infinity Galaxy"] = infinity_galaxy
    
    def add_candidate(self, candidate: SMBHCandidate):
        """Add new SMBH candidate to database."""
        candidate.last_updated = datetime.now().isoformat()
        self.candidates[candidate.name] = candidate
    
    def update_candidate(self, name: str, **updates):
        """Update existing candidate with new information."""
        if name not in self.candidates:
            raise ValueError(f"Candidate {name} not found")
        
        candidate = self.candidates[name]
        for key, value in updates.items():
            if hasattr(candidate, key):
                setattr(candidate, key, value)
            else:
                warnings.warn(f"Unknown attribute {key} for candidate")
        
        candidate.last_updated = datetime.now().isoformat()
    
    def get_candidates_by_redshift(self, z_min: float, z_max: float) -> List[SMBHCandidate]:
        """Get candidates within redshift range."""
        return [candidate for candidate in self.candidates.values()
                if z_min <= candidate.redshift <= z_max]
    
    def get_candidates_by_survey(self, survey: str) -> List[SMBHCandidate]:
        """Get candidates from specific survey."""
        return [candidate for candidate in self.candidates.values()
                if candidate.survey.upper() == survey.upper()]
    
    def calculate_luft_collapse_score(self, candidate: SMBHCandidate) -> float:
        """
        Calculate LUFT collapse probability score for candidate.
        
        Based on observational indicators that suggest lattice collapse:
        - High redshift (early universe)
        - Large inferred BH mass
        - Host galaxy properties
        - Spectral anomalies
        """
        score = 0.0
        
        # Redshift factor (higher z = more likely primordial)
        if candidate.redshift > 10:
            z_factor = min((candidate.redshift - 10) / 5, 1.0)
            score += 0.3 * z_factor
        
        # Mass factor (more massive = more likely direct collapse)
        if candidate.estimated_mass:
            if candidate.estimated_mass > 1e7:
                mass_factor = min(np.log10(candidate.estimated_mass / 1e7) / 2, 1.0)
                score += 0.25 * mass_factor
        
        # Host galaxy properties
        if candidate.host_stellar_mass and candidate.estimated_mass:
            bh_to_stellar_ratio = candidate.estimated_mass / candidate.host_stellar_mass
            if bh_to_stellar_ratio > 0.01:  # Unusually high ratio
                ratio_factor = min(bh_to_stellar_ratio / 0.1, 1.0)
                score += 0.2 * ratio_factor
        
        # Survey quality (spectroscopic > photometric)
        if candidate.redshift_method == "spectroscopic":
            score += 0.1
        
        # Special LUFT indicators
        if candidate.lattice_signature_detected:
            score += 0.15
        
        return min(score, 1.0)
    
    def analyze_population_statistics(self) -> Dict[str, Any]:
        """Analyze population statistics of SMBH candidates."""
        if not self.candidates:
            return {}
        
        candidates = list(self.candidates.values())
        
        # Redshift distribution
        redshifts = [c.redshift for c in candidates]
        
        # Mass distribution (where available)
        masses = [c.estimated_mass for c in candidates if c.estimated_mass]
        
        # Survey breakdown
        surveys = {}
        for candidate in candidates:
            surveys[candidate.survey] = surveys.get(candidate.survey, 0) + 1
        
        # LUFT scores
        luft_scores = []
        for candidate in candidates:
            if candidate.luft_collapse_score is None:
                score = self.calculate_luft_collapse_score(candidate)
                candidate.luft_collapse_score = score
            luft_scores.append(candidate.luft_collapse_score)
        
        stats = {
            'total_candidates': len(candidates),
            'redshift_range': (min(redshifts), max(redshifts)),
            'mean_redshift': np.mean(redshifts),
            'survey_breakdown': surveys,
            'mass_estimates_available': len(masses),
            'mean_luft_score': np.mean(luft_scores),
            'high_luft_score_fraction': np.mean([s > 0.5 for s in luft_scores])
        }
        
        if masses:
            stats['mass_range'] = (min(masses), max(masses))
            stats['mean_mass'] = np.mean(masses)
        
        return stats
    
    def generate_target_list(self, 
                           min_luft_score: float = 0.5,
                           max_redshift: Optional[float] = None,
                           required_bands: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Generate prioritized target list for follow-up observations.
        
        Args:
            min_luft_score: Minimum LUFT collapse score
            max_redshift: Maximum redshift for targets
            required_bands: Required detection bands
            
        Returns:
            DataFrame with prioritized targets
        """
        targets = []
        
        for candidate in self.candidates.values():
            # Calculate LUFT score if not available
            if candidate.luft_collapse_score is None:
                candidate.luft_collapse_score = self.calculate_luft_collapse_score(candidate)
            
            # Apply filters
            if candidate.luft_collapse_score < min_luft_score:
                continue
            
            if max_redshift and candidate.redshift > max_redshift:
                continue
            
            if required_bands:
                if not all(band in candidate.detection_bands for band in required_bands):
                    continue
            
            # Calculate priority score
            priority = candidate.luft_collapse_score
            if candidate.redshift_method == "spectroscopic":
                priority += 0.1
            if candidate.lattice_signature_detected:
                priority += 0.2
            
            target_info = {
                'name': candidate.name,
                'survey': candidate.survey,
                'ra': candidate.ra,
                'dec': candidate.dec,
                'redshift': candidate.redshift,
                'estimated_mass': candidate.estimated_mass,
                'luft_score': candidate.luft_collapse_score,
                'priority': priority,
                'notes': candidate.notes
            }
            targets.append(target_info)
        
        # Sort by priority
        targets_df = pd.DataFrame(targets)
        if not targets_df.empty:
            targets_df = targets_df.sort_values('priority', ascending=False)
        
        return targets_df
    
    def export_catalog(self, filename: str, format: str = 'json'):
        """
        Export candidate catalog to file.
        
        Args:
            filename: Output filename
            format: 'json', 'csv', or 'fits'
        """
        if format.lower() == 'json':
            # Convert to JSON-serializable format
            export_data = {}
            for name, candidate in self.candidates.items():
                export_data[name] = {
                    'basic_info': {
                        'name': candidate.name,
                        'survey': candidate.survey,
                        'ra': candidate.ra,
                        'dec': candidate.dec
                    },
                    'redshift': {
                        'value': candidate.redshift,
                        'error': candidate.redshift_error,
                        'method': candidate.redshift_method,
                        'lookback_time': candidate.lookback_time
                    },
                    'black_hole': {
                        'mass': candidate.estimated_mass,
                        'mass_error': candidate.mass_error,
                        'mass_method': candidate.mass_method
                    },
                    'host_galaxy': {
                        'stellar_mass': candidate.host_stellar_mass,
                        'sfr': candidate.host_sfr,
                        'morphology': candidate.host_morphology
                    },
                    'observations': {
                        'jwst_programs': candidate.jwst_programs,
                        'detection_bands': candidate.detection_bands,
                        'photometry': candidate.photometry
                    },
                    'luft_analysis': {
                        'collapse_score': candidate.luft_collapse_score,
                        'lattice_signature': candidate.lattice_signature_detected,
                        'em_portal_evidence': candidate.em_portal_evidence
                    },
                    'metadata': {
                        'discovery_date': candidate.discovery_date,
                        'notes': candidate.notes,
                        'references': candidate.references,
                        'last_updated': candidate.last_updated
                    }
                }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        elif format.lower() == 'csv':
            # Flatten to DataFrame
            rows = []
            for candidate in self.candidates.values():
                row = {
                    'name': candidate.name,
                    'survey': candidate.survey,
                    'ra': candidate.ra,
                    'dec': candidate.dec,
                    'redshift': candidate.redshift,
                    'redshift_error': candidate.redshift_error,
                    'estimated_mass': candidate.estimated_mass,
                    'host_stellar_mass': candidate.host_stellar_mass,
                    'luft_score': candidate.luft_collapse_score,
                    'lattice_signature': candidate.lattice_signature_detected,
                    'discovery_date': candidate.discovery_date,
                    'notes': candidate.notes
                }
                rows.append(row)
            
            df = pd.DataFrame(rows)
            df.to_csv(filename, index=False)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def import_candidate_data(self, filename: str, format: str = 'json'):
        """
        Import candidate data from external file.
        
        Args:
            filename: Input filename
            format: 'json' or 'csv'
        """
        if format.lower() == 'json':
            with open(filename, 'r') as f:
                data = json.load(f)
            
            for name, candidate_data in data.items():
                # Reconstruct SMBHCandidate object
                candidate = SMBHCandidate(
                    name=candidate_data['basic_info']['name'],
                    survey=candidate_data['basic_info']['survey'],
                    ra=candidate_data['basic_info']['ra'],
                    dec=candidate_data['basic_info']['dec'],
                    redshift=candidate_data['redshift']['value'],
                    redshift_error=candidate_data['redshift'].get('error'),
                    redshift_method=candidate_data['redshift'].get('method', 'unknown'),
                    estimated_mass=candidate_data['black_hole'].get('mass'),
                    host_stellar_mass=candidate_data['host_galaxy'].get('stellar_mass'),
                    jwst_programs=candidate_data['observations'].get('jwst_programs', []),
                    detection_bands=candidate_data['observations'].get('detection_bands', []),
                    luft_collapse_score=candidate_data['luft_analysis'].get('collapse_score'),
                    lattice_signature_detected=candidate_data['luft_analysis'].get('lattice_signature', False),
                    notes=candidate_data['metadata'].get('notes', '')
                )
                
                self.add_candidate(candidate)
        
        elif format.lower() == 'csv':
            df = pd.read_csv(filename)
            
            for _, row in df.iterrows():
                candidate = SMBHCandidate(
                    name=row['name'],
                    survey=row['survey'],
                    ra=row['ra'],
                    dec=row['dec'],
                    redshift=row['redshift'],
                    redshift_error=row.get('redshift_error'),
                    estimated_mass=row.get('estimated_mass'),
                    host_stellar_mass=row.get('host_stellar_mass'),
                    luft_collapse_score=row.get('luft_score'),
                    lattice_signature_detected=row.get('lattice_signature', False),
                    notes=row.get('notes', '')
                )
                
                self.add_candidate(candidate)


def create_default_curator() -> EvidenceCurator:
    """Create evidence curator with default JADES and Infinity Galaxy data."""
    return EvidenceCurator()


def analyze_luft_signatures(curator: EvidenceCurator) -> Dict[str, Any]:
    """
    Analyze potential LUFT collapse signatures in candidate population.
    
    Args:
        curator: EvidenceCurator instance
        
    Returns:
        Dictionary with signature analysis results
    """
    candidates = list(curator.candidates.values())
    
    if not candidates:
        return {'error': 'No candidates available for analysis'}
    
    # Update LUFT scores
    for candidate in candidates:
        if candidate.luft_collapse_score is None:
            candidate.luft_collapse_score = curator.calculate_luft_collapse_score(candidate)
    
    # Analyze signature correlations
    high_score_candidates = [c for c in candidates if c.luft_collapse_score > 0.5]
    
    analysis = {
        'total_candidates': len(candidates),
        'high_score_candidates': len(high_score_candidates),
        'high_score_fraction': len(high_score_candidates) / len(candidates),
        'signature_detections': sum(1 for c in candidates if c.lattice_signature_detected),
        'mean_redshift_high_score': np.mean([c.redshift for c in high_score_candidates]) if high_score_candidates else 0,
        'redshift_correlation': None,
        'mass_correlation': None
    }
    
    # Calculate correlations if sufficient data
    if len(candidates) > 3:
        scores = [c.luft_collapse_score for c in candidates]
        redshifts = [c.redshift for c in candidates]
        
        if len(scores) > 1:
            analysis['redshift_correlation'] = np.corrcoef(scores, redshifts)[0, 1]
        
        masses = [c.estimated_mass for c in candidates if c.estimated_mass]
        if len(masses) > 1:
            mass_scores = [c.luft_collapse_score for c in candidates if c.estimated_mass]
            analysis['mass_correlation'] = np.corrcoef(mass_scores, masses)[0, 1]
    
    return analysis
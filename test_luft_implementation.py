#!/usr/bin/env python3
"""
Test script for LUFT lattice-collapse implementation.

This script performs basic functionality tests of the LUFT modules
to ensure they work correctly before integration.
"""

import sys
import os
import numpy as np
import traceback

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_luft_collapse():
    """Test basic LUFT collapse model functionality."""
    print("Testing LUFT collapse model...")
    
    try:
        from luft_collapse import create_default_model, evaluate_collapse_probability
        
        # Create default model
        model = create_default_model()
        print(f"✓ Created default model with φ_0 = {model.params.phi_0} GeV")
        
        # Test field potential calculation
        phi_test = np.array([1e-4, 1e-3, 1e-2])
        potential = model.field_potential(phi_test)
        print(f"✓ Field potential calculation: {potential}")
        
        # Test collapse criterion
        phi_values = np.linspace(1e-4, 1e-2, 10)
        dphi_dt_values = np.linspace(1e-6, 1e-4, 10)
        
        collapse_results = model.collapse_criterion(phi_values, dphi_dt_values)
        print(f"✓ Collapse criterion: {np.sum(collapse_results)} / {len(collapse_results)} points trigger collapse")
        
        # Test merger evolution
        t_array = np.linspace(0, 1e7, 50)  # Shorter time for test
        evolution = model.merger_field_evolution(t_array)
        print(f"✓ Merger evolution computed for {len(t_array)} time steps")
        
        # Test probability calculation
        prob = evaluate_collapse_probability(evolution['phi'], evolution['dphi_dt'], model)
        print(f"✓ Collapse probability: {prob:.3f}")
        
        # Test LHC constraints
        lhc_constraints = model.lhc_constraint_window()
        print(f"✓ LHC constraints: χ ∈ [{lhc_constraints['chi_min']:.2e}, {lhc_constraints['chi_max']:.2e}]")
        
        return True
        
    except Exception as e:
        print(f"✗ LUFT collapse test failed: {e}")
        traceback.print_exc()
        return False


def test_parameter_scan():
    """Test parameter scanning utilities."""
    print("\nTesting parameter scanner...")
    
    try:
        from parameter_scan import ParameterScanner, quick_parameter_scan
        
        # Create scanner with default priors
        scanner = ParameterScanner()
        print(f"✓ Created scanner with {len(scanner.priors)} parameters")
        
        # Test parameter sampling
        for name, prior in list(scanner.priors.items())[:3]:  # Test first 3
            samples = scanner.sample_parameter(prior, 5)
            print(f"✓ Sampled {name}: [{samples.min():.2e}, {samples.max():.2e}]")
        
        # Test parameter set generation
        param_set = scanner.generate_parameter_set()
        print(f"✓ Generated parameter set with {len(param_set)} parameters")
        
        # Test LHS sampling (small sample for speed)
        lhs_samples = scanner.latin_hypercube_sample(5)
        print(f"✓ Generated {len(lhs_samples)} LHS samples")
        
        # Test single model evaluation
        result = scanner.evaluate_model(param_set)
        print(f"✓ Model evaluation: success = {result.get('evaluation_success', False)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Parameter scan test failed: {e}")
        traceback.print_exc()
        return False


def test_evidence_curation():
    """Test evidence curation tools."""
    print("\nTesting evidence curation...")
    
    try:
        from evidence_curation import create_default_curator, analyze_luft_signatures
        
        # Create curator with default data
        curator = create_default_curator()
        print(f"✓ Created curator with {len(curator.candidates)} candidates")
        
        # Test candidate access
        jades_candidates = curator.get_candidates_by_survey("JADES")
        print(f"✓ Found {len(jades_candidates)} JADES candidates")
        
        # Test redshift filtering
        high_z_candidates = curator.get_candidates_by_redshift(12.0, 15.0)
        print(f"✓ Found {len(high_z_candidates)} high-z candidates")
        
        # Test LUFT score calculation
        for name, candidate in curator.candidates.items():
            score = curator.calculate_luft_collapse_score(candidate)
            print(f"✓ {name}: LUFT score = {score:.3f}")
        
        # Test population analysis
        stats = curator.analyze_population_statistics()
        print(f"✓ Population stats: {stats.get('total_candidates', 0)} candidates, z̄ = {stats.get('mean_redshift', 0):.1f}")
        
        # Test target list generation
        targets = curator.generate_target_list(min_luft_score=0.3)
        print(f"✓ Generated target list with {len(targets)} entries")
        
        # Test signature analysis
        signature_analysis = analyze_luft_signatures(curator)
        print(f"✓ Signature analysis: {signature_analysis.get('high_score_candidates', 0)} high-score candidates")
        
        return True
        
    except Exception as e:
        print(f"✗ Evidence curation test failed: {e}")
        traceback.print_exc()
        return False


def test_integration():
    """Test integration between modules."""
    print("\nTesting module integration...")
    
    try:
        from luft_collapse import create_default_model
        from parameter_scan import ParameterScanner
        from evidence_curation import create_default_curator
        
        # Test parameter scan with LUFT model
        scanner = ParameterScanner()
        param_set = scanner.generate_parameter_set()
        
        # Evaluate with custom observables
        result = scanner.evaluate_model(param_set, observables=['collapse_probability', 'lhc_constraints'])
        
        if result['evaluation_success']:
            prob = result.get('collapse_probability', 0)
            lhc = result.get('lhc_constraints', {})
            print(f"✓ Integrated evaluation: P_collapse = {prob:.3f}, LHC valid = {lhc.get('within_bounds', False)}")
        else:
            print(f"✗ Integrated evaluation failed: {result.get('error', 'Unknown error')}")
            return False
        
        # Test evidence curator with LUFT scores
        curator = create_default_curator()
        
        # Update candidates with theoretical LUFT predictions
        model = create_default_model()
        for name, candidate in curator.candidates.items():
            # Simulate LUFT analysis
            if candidate.redshift > 13:
                candidate.luft_collapse_score = 0.8
                candidate.lattice_signature_detected = True
            
        updated_stats = curator.analyze_population_statistics()
        print(f"✓ Updated curator stats: {updated_stats.get('high_luft_score_fraction', 0):.2f} high-score fraction")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("LUFT Lattice-Collapse Implementation Test Suite")
    print("=" * 60)
    
    tests = [
        test_luft_collapse,
        test_parameter_scan,
        test_evidence_curation,
        test_integration
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test_func.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_func, result) in enumerate(zip(tests, results)):
        status = "PASS" if result else "FAIL"
        print(f"{i+1}. {test_func.__name__:<25} [{status}]")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! LUFT implementation is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
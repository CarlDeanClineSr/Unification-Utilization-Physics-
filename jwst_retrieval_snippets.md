JWST retrieval and residual-scoring snippets

1) Forward model and likelihood
- Data d(λ_i), uncertainties σ_i; model m(λ; θ)
- θ = {T–P, Z, C/O, g, clouds, broadening, isotopic ratios}
- ln L(θ) = −1/2 Σ_i [ (d_i − m_i(θ))^2 / σ_i^2 + ln(2π σ_i^2) ]

2) Isotopologue matched filter
- Templates t_iso(λ): 13CO, HDO, 13CH4, 13CO2…
- SNR: S = (d•t/σ^2)/√(t•t/σ^2); scan small Doppler shifts; evaluate significance via off-band control/permutation

3) Line-by-line residual scoring
- r_i = (d_i − m_i)/σ_i
- Aggregate around iso-only lines: mean R, local χ^2 T; bootstrap vs null

4) Information geometry
- Fisher: F_{mn} = Σ_i (1/σ_i^2) (∂m_i/∂θ_m)(∂m_i/∂θ_n)
- Large κ(F) → add bands (e.g., CH4 3.3 μm and ~7.7 μm), include MIRI features

5) Model comparison (BIC)
- ΔBIC = (k_2 − k_1) ln N − 2 (ln L_2^max − ln L_1^max)
- Decide to free isotopic ratios vs fixed stellar values

Quality controls
- Cross-line-list validation (ExoMol/HITEMP/HITRAN)
- Overlap checks across bands for same species
- Nuisance params: MIRI fringing amplitude, NIRSpec 1/f baselines

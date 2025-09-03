Gravity test snippets — equations and minimal algorithms

1) IMR consistency test
- Goal: check agreement between inspiral-only and post-inspiral-only remnant estimates (M_f, a_f).
- Define: δM_f = M_f^(I) − M_f^(P),  δa_f = a_f^(I) − a_f^(P)
- Joint score: z^2 = δ^T Σ^{-1} δ with δ = (δM_f, δa_f)
- Algorithm:
  1) Split data at f_split near ISCO
  2) Infer (M_f, a_f) from each half via NR fits
  3) Monte Carlo δ and z distribution; z ≲ O(1) consistent with GR

2) Ringdown spectroscopy (Kerr QNMs)
- Single-mode model: h(t) = A e^{−t/τ_220} cos(2π f_220 t + φ), t ≥ t0
- Deviations: f_220 → f_220^GR(1+δf_220), τ_220 → τ_220^GR(1+δτ_220)
- Hierarchical combo across events: δ ~ N(μ, σ^2); test μ ≈ 0

3) ppE/PN inspiral phase deviations
- Phase: Ψ(f) = Ψ_GR(f) + β u^b, u = (π M f)^{1/3}, b ∈ {−7 (−1PN), −5 (0PN), −3 (1PN), …}
- Strategy: fit β for selected b; report posteriors and catalog-combined bounds

4) Modified dispersion / massive graviton
- Generic: E^2 = p^2 c^2 + A p^α c^α ⇒ ΔΨ(f) ∝ A f^{α−1} D_α(z)
- Massive graviton (α = 0, A = m_g^2 c^4):
  ΔΨ_mg(f) = − π D_mg(z) / [ (1+z) λ_g^2 f ], with λ_g = h/(m_g c)
- Combine events by multiplying likelihoods; quote m_g upper bounds

5) Area theorem / horizon absorption
- A_f = 8π M_f^2 [1 + √(1 − a_f^2)],  ΔA = A_f − (A_1 + A_2) ≥ 0
- Compute P(ΔA < 0) from samples

Diagnostics and guardrails
- Residuals: structureless in time/frequency; no correlated leftovers
- f_split stability: vary and recheck z
- Prior–posterior tension: monitor KL divergence

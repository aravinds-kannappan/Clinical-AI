# Consent-constrained clinical AI

Can a healthcare AI monitoring pipeline remain useful while sensitive data flows, errors and consequential decisions are subject to explicit consent and effective human oversight?

This repository studies that question with **40,336 public PhysioNet/CinC 2019 patients**, three validation-tuned predictors, patient-specific consent simulations, mathematical risk/workload certificates and review-process simulations.

**Result:** better discrimination did not make the tested first-alert policies satisfy the declared incident-risk target. Consent and review-path constraints are auditable in the modeled system; their coexistence with effective clinical oversight is **not demonstrated**. This is a negative result for a specific policy family, not a general impossibility theorem.

- [NeurIPS-style paper (PDF)](paper.pdf) · [LaTeX source](paper.tex)
- [Live interactive results, equations and discussion](https://consent-clinical-ai.vercel.app)
- [Full-release report](results/revision/REPORT.md) · [Direct research conclusion](DISCUSSION.md)
- [Mathematics](MATHEMATICS.md) · [Methods](METHODS.md) · [Data card](DATA_CARD.md)

## What the revision found

Across seeds 11, 29 and 47, mean pre-onset AUROC was 0.794 for boosting at hospital A and 0.752 for the GRU at hospital B. Every local first-alert calibration grid was excluded at conditional missed risk alpha=0.05, including at one review per patient. This confidence claim is per frozen model/grid, not simultaneous across every fitted model and seed.

A first alert before the specified six-hour warning window consumes the only review and is a miss under the strict incident endpoint. Lowering a threshold can therefore make this loss worse. The paper proves the counterexample, characterizes population feasibility and applies simultaneous exact-binomial bounds to certify feasibility, grid infeasibility or insufficient evidence. The general confidence machinery is attributed to existing risk-control work.

The validation-selected boosting policy at hospital A had mean challenge utility 0.332 and 0.193 reviews per patient, yet strict incident missed risk 0.960. Challenge utility credits a broader warning window and a persistent positive condition state. **Positive utility is not evidence that the first-review timing target was met.**

The paper includes all-seed patient-bootstrap intervals, local hospital-B calibration, repeated calibration draws, consent opt-out/revocation, 500 random graphs and 972 corrected reviewer-queue scenarios. Actual clinician behavior, privacy/security of a deployed system and patient benefit were not measured. Full credentialed MIMIC-IV was not available.

## Reproduce

Install Python 3.13 and [uv](https://docs.astral.sh/uv/), then run:

```bash
bash run_all.sh
```

The default stage is `revision`. This installs locked dependencies, runs 23 tests, acquires/verifies the public data, fits all models and generates the revision plus policy audit. No GPU, paid service or dataset approval is required for these public inputs. It uses a separate local `.venv`; do not share an environment between concurrent checkouts.

Set `CONSENT_DATA_ROOT` and `CONSENT_RESULTS_DIR` to relocate inputs and outputs. A clean run trains every model. Exact original source archives and the hash-verified partial-run resume are described in [reproducibility/README.md](reproducibility/README.md).

To regenerate paper tables and the figure from saved results:

```bash
uv run --locked python scripts/build_paper_results.py
uv run --locked python figs/incident_frontier.py
tectonic paper.tex
```

The figure script reads the versioned `figs/frontiers.csv` snapshot; replace it from `results/revision/frontiers.csv` when deliberately producing a new analysis. The paper uses the official NeurIPS 2026 style in preprint mode. It is a research draft, not an accepted or submitted NeurIPS paper. Author: Aravind Kannappan.

## Evidence map

| File | What it records |
|---|---|
| `results/revision/metrics.csv` | All model/site/seed discrimination estimates and bootstrap intervals |
| `results/revision/frontiers.csv` | Frozen-grid first and repeated alert risk/workload/utility |
| `results/revision/certificates.csv` | Joint certificate outcomes and calibration support |
| `results/revision/consent.csv` | Simulated heterogeneous opt-out and revocation |
| `results/revision/calibration_draw_summary.csv` | Calibration-subset stability; no certified rule in these draws |
| `results/revision-audit/selected_policies.csv` | Validation-selected policies with exact pointwise test-risk intervals |
| `results/revision-audit/queues.csv` | Corrected reviewer simulation; use this for false-action counts |
| `results/revision/graph_ensemble.csv` | 500 random DAG checks |
| `results/revision/provenance.json` | Exact main-run configuration, commit and resumed-input hashes |

The original `results/revision/queues.csv` is retained for provenance. Its false-action classification included incident-ineligible positive patients; it is superseded by the policy audit. Main predictor, incident-loss and certificate results are unaffected.

## Code map

- `revision_data.py`, `revision_models.py`: causal features, patient splits and tuned models.
- `joint_risk.py`: incident loss and simultaneous finite-grid certificates.
- `revision_evaluation.py`: challenge utility, bootstrap and calibration analysis.
- `revision_stress.py`: consent, graph and reviewer simulations.
- `revision_audit.py`: frozen-score operating-policy audit and uncertainty.
- `graph.py`: patient/purpose masks, revocation and review-path checks.
- `tests/`: mathematical counterexamples, certificate boundaries and leakage checks.

These modules live in `consent_ai/`. Model files are supplied as outputs from this repository; only load serialized models from sources you trust.

## Public data and archived studies

The full PhysioNet/CinC 2019 A/B release is included as `data/raw/sepsis-public/sepsis-public-full.zip` with selection and checksum manifests. Original source: Reyna et al., [version 1.0.0](https://physionet.org/content/challenge-2019/1.0.0/), **CC BY 4.0**. Dataset licenses continue to apply. The official challenge evaluator retains its BSD license.

The earlier 6,000-patient hourly-loss study is in `results/sepsis/`. The sparse MIMIC-IV demo and five-participant movement analyses are historical supplementary results in `results/`; they do not support the revised primary conclusion. MIMIC demo data retain their ODbL terms; UP-Fall derivatives retain their CC BY 4.0 terms. No access agreement is accepted by the code.

## Website

The Next.js application in `website/` is deployed on [Vercel](https://consent-clinical-ai.vercel.app). It renders equations with KaTeX and allows hospital, seed, metric and consent-scenario selection.

```bash
cd website
npm ci
npm run dev
```

`npm run build` refreshes the measured-data snapshot when repository outputs are present; isolated Vercel builds use the committed snapshot. Active standalone HTML reports have been retired.

# Benchmarking AI Under Consent Constraints

Can a sepsis prediction system retain useful performance when patients restrict its inputs? This benchmark study compares full-input reference AI with the same AI under explicit, simulated information-access restrictions.

The public cohort contains **40,336 PhysioNet/CinC 2019 patients**. Three supervised model families, three split seeds, two hospitals and eight permission conditions are evaluated with matched patients, fixed fitted models and fixed validation-selected alert thresholds. Restrictions affect inference-time inputs and derived state; the models were trained using full public inputs.

**Main finding:** similar AUROC can conceal worse alert behavior. At hospital B, removing labs from the GRU changes mean AUROC from 0.752 to 0.745, but increases missed-incident risk by 11.2 percentage points at its fixed hourly threshold while reducing reviews by 1.42 per patient. At 30% independent denial per feature group, mean AUROC falls by 0.019–0.051 across model/hospital combinations. These are three-seed averages, not evidence of clinical equivalence.

- [Two-column paper (PDF)](paper.pdf) · [LaTeX source](paper.tex)
- [Live paper and interactive results](https://consent-clinical-ai.vercel.app)
- [Benchmark protocol](BENCHMARK.md) · [Paired experiment report](results/consent-comparison/REPORT.md)
- [Methods](METHODS.md) · [Mathematics and proofs](MATHEMATICS.md) · [Interpretation](DISCUSSION.md) · [Data card](DATA_CARD.md)

## What the benchmark measures

The primary comparison separates changes in input permissions from changes in the decision threshold. It reports paired discrimination, incident misses, review burden, utility and information-availability proxies. Permission assignment is simulated; the experiment does not collect consent, measure privacy leakage, or decide which performance loss patients should accept.

A secondary evaluation studies the first-alert policy. Every tested local calibration grid is excluded at the 5% conditional missed-risk target, even with one review per patient. An early first alert can consume the review before the strict warning window. Positive challenge utility evaluates a different endpoint and does not repair this failure. The exclusion is per frozen model/grid, not a general impossibility result.

The mathematical contribution makes the estimands and assumptions explicit: a paired bounded-loss criterion, first-alert feasibility characterization and simultaneous finite-grid confidence bounds. The concentration machinery is classical. The empirical contribution is the benchmark design and failure analysis, not a new predictor. Actual human oversight, clinical benefit, training consent and retraining under restricted features remain unmeasured.

## Reproduce

Install Python 3.13 and [uv](https://docs.astral.sh/uv/), then run:

```bash
bash run_all.sh
```

The default stage is `revision`. This installs locked dependencies, runs 26 tests, acquires/verifies the public data, fits all models and generates the full revision, policy audit and paired consent comparison. No GPU, paid service or dataset approval is required for these public inputs. It uses a separate local `.venv`; do not share an environment between concurrent checkouts.

Set `CONSENT_DATA_ROOT` and `CONSENT_RESULTS_DIR` to relocate inputs and outputs. A clean run trains every model. Exact original source archives and the hash-verified partial-run resume are described in [reproducibility/README.md](reproducibility/README.md).

To regenerate paper tables and figures from saved results:

```bash
uv run --locked python scripts/build_paper_results.py
uv run --locked python figs/research_figures.py
uv run --locked python scripts/build_consent_tables.py
uv run --locked python figs/paired_consent_figures.py
tectonic figs/paired_design.tex
tectonic paper.tex
```

The figure script reads versioned snapshots in `figs/`: `frontiers.csv` and `consent.csv` from `results/revision/`, and `selected_policies.csv` from `results/revision-audit/`. Replace them only when deliberately producing a new analysis. The original table generator updates four tables without overwriting manuscript prose. The paired generator adds the complete AUROC table; paired figures read `paired_discrimination.csv` and `paired_policies.csv`, copied from `results/consent-comparison/`. The paper contains seven vector figures.

The paper uses a two-column, 10-point research layout with full-width vector figures, detailed methods, theorem statements and appendix proofs, and 24 references. Sections, equations and captions are unnumbered, with author–year citations. This layout follows the author’s preference; it is not the official single-column NeurIPS submission template. It is a research draft, not an accepted or submitted NeurIPS paper. Author: Aravind Kannappan.

`cohort_statistics.json` records cohort and incident-eligibility counts. Recreate it with `uv run --locked python scripts/cohort_summary.py --archive data/raw/sepsis-public/sepsis-public-full.zip --output cohort_statistics.json`.

## Evidence map

| File | What it records |
|---|---|
| `results/consent-comparison/discrimination.csv` | Primary paired ranking/probability metrics and pointwise uncertainty |
| `results/consent-comparison/policies.csv` | Primary paired fixed-policy outcomes and uncertainty |
| `results/consent-comparison/provenance.json` | Frozen comparison settings and parent model/prediction hashes |
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
- `consent_comparison.py`: matched permission interventions, paired bootstrap differences and score-reproduction checks.
- `revision_audit.py`: frozen-score operating-policy audit and uncertainty.
- `graph.py`: patient/purpose masks, revocation and review-path checks.
- `tests/`: mathematical counterexamples, certificate boundaries and leakage checks.

These modules live in `consent_ai/`. Model files are supplied as outputs from this repository; only load serialized models from sources you trust.

## Public data and archived studies

The full PhysioNet/CinC 2019 A/B release is included as `data/raw/sepsis-public/sepsis-public-full.zip` with selection and checksum manifests. Original source: Reyna et al., [version 1.0.0](https://physionet.org/content/challenge-2019/1.0.0/), **CC BY 4.0**. Dataset licenses continue to apply. The official challenge evaluator retains its BSD license.

The earlier 6,000-patient hourly-loss study is in `results/sepsis/`. The sparse MIMIC-IV demo and five-participant movement analyses are historical supplementary results in `results/`; they do not support the revised primary conclusion. MIMIC demo data retain their ODbL terms; UP-Fall derivatives retain their CC BY 4.0 terms. No access agreement is accepted by the code.

## Website

The Next.js application in `website/` is deployed on [Vercel](https://consent-clinical-ai.vercel.app). It renders equations with KaTeX and presents the paper as a reading experience with vector figures, author–year references and interactive hospital, seed and permission-condition comparisons.

```bash
cd website
npm ci
npm run dev
```

`npm run build` refreshes the measured-data snapshot when repository outputs are present; isolated Vercel builds use the committed snapshot. Active standalone HTML reports have been retired.

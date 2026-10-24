# Open-cohort follow-up: consent, statistical risk and review demand

**REAL OPEN DATA + CONSTRUCTED POLICY. No clinical validation or patient-benefit claim.**
This follow-up retains the original MIMIC-demo experiment and adds a larger approval-free cohort because that endpoint contained only two positive patients. It does not change the earlier endpoint or select a model on test results.

## Cohort and task
A uniform, label-blind sample of 3,000 patients per public hospital was drawn from the complete PhysioNet/CinC 2019 listings using seed 20261023. Files are pinned by source ETags/MD5 and SHA256. The sample is a bounded evaluation, not the full 40,336-patient release.
- Hospital A: 3000 patients, 116980 observed hourly rows, 262 positive patients and 2514 positive rows.
- Hospital B: 3000 patients, 113779 observed hourly rows, 173 positive patients and 1630 positive rows.
The outcome is the provided early-warning SepsisLabel at each hour. Labels were already shifted six hours early by the dataset authors; we do not shift them again. They include hours after the first positive label, so this is not an incident-only or strictly pre-onset forecasting evaluation.
Use current/past rows only. Features are forward-filled values, cumulative means and observed counts. Absolute dates and laboratory storage times are unavailable; no exact calendar holdout or store-time availability guarantee is asserted. Hospital A supplies training/calibration/internal test (60/20/20%), while all sampled B patients are held out externally.

## Discrimination and probability quality
Fixed C=1 logistic regressions compare metadata, full EHR and experimental feature restrictions. Brier is a proper probability score, not a standalone calibration measure; reliability-bin data are reported separately. The following are three-seed means. Seed-11 patient-cluster 95% bootstrap intervals and paired effects are linked separately.
- Hospital A, consent_no_labs: AUROC 0.7116; average precision 0.0824; Brier 0.0225.
- Hospital A, consent_no_vitals: AUROC 0.7172; average precision 0.0847; Brier 0.0254.
- Hospital A, full_ehr: AUROC 0.7143; average precision 0.0881; Brier 0.0266.
- Hospital A, metadata: AUROC 0.7023; average precision 0.0876; Brier 0.0228.
- Hospital B, consent_no_labs: AUROC 0.6205; average precision 0.0568; Brier 0.0144.
- Hospital B, consent_no_vitals: AUROC 0.6445; average precision 0.0558; Brier 0.0389.
- Hospital B, full_ehr: AUROC 0.6452; average precision 0.0554; Brier 0.0377.
- Hospital B, metadata: AUROC 0.6076; average precision 0.0504; Brier 0.0142.

See `intervals.csv`, `paired_effects.csv`, `reliability.csv`, `subgroups.csv`, `splits.json` and `predictions.csv.gz`. Intervals use 500 whole-patient resamples, with identical resampling for paired differences. No selection or tuning used hospital B.

## The important distinction: which risk is controlled?
**Base patient loss:** L_i = missed positive windows / max(1, number of positive windows); zero for no positive windows. B=1, alpha=.05. **Unconditional CRC** calibrates on all calibration patients. **Positive-patient CRC** calibrates on the subset with any positive window; its guarantee additionally requires exchangeability conditional on positive-patient status. Both frozen rules apply to every test patient.
**Assumptions for every CRC number below:** Frozen predictor and loss; exchangeable calibration/future patient loss functions; bounded B=1, non-increasing right-continuous loss in lambda; terminal all-alert loss=0; no post-calibration alert suppression. Expectation over calibration and new patient, not a per-patient/subgroup guarantee. Shifted populations have no asserted guarantee. The positive-conditioned rule uses conditional patient exchangeability. No guarantee is asserted for hospital B or missingness shift.
The finite-sample rule is lambda_hat = inf{lambda: (n R_hat(lambda)+1)/(n+1) ≤ .05}, with an all-alert terminal fallback. Counts and thresholds for every fit are in `calibration.csv`. Expected risk is not a guarantee for an individual or fixed realized calibration sample.
- Seed 11, hospital A, crc_unconditional, n=600, B=1, alpha=.05: patient-average missed loss 0.0468; positive-patient conditional missed loss 0.5014; hourly sensitivity 0.4944; review fraction 0.2054; false alerts per 24 observed patient-hours 4.66. Assumptions and the distinct estimands are as defined immediately above; hospital B is a shift test.
- Seed 11, hospital B, crc_unconditional, n=600, B=1, alpha=.05: patient-average missed loss 0.0379; positive-patient conditional missed loss 0.6569; hourly sensitivity 0.3528; review fraction 0.1270; false alerts per 24 observed patient-hours 2.93. Assumptions and the distinct estimands are as defined immediately above; hospital B is a shift test.
- Seed 11, hospital A, crc_positive_conditional, n=60, B=1, alpha=.05: patient-average missed loss 0.0039; positive-patient conditional missed loss 0.0413; hourly sensitivity 0.9574; review fraction 0.9269; false alerts per 24 observed patient-hours 21.72. Assumptions and the distinct estimands are as defined immediately above; hospital B is a shift test.
- Seed 11, hospital B, crc_positive_conditional, n=60, B=1, alpha=.05: patient-average missed loss 0.0151; positive-patient conditional missed loss 0.2625; hourly sensitivity 0.7466; review fraction 0.6476; false alerts per 24 observed patient-hours 15.29. Assumptions and the distinct estimands are as defined immediately above; hospital B is a shift test.
If non-positive patients have zero loss, unconditional risk equals positive-patient prevalence multiplied by conditional missed loss. A small unconditional risk can therefore coexist with high conditional misses. This is a mathematical limitation of the chosen estimand, not a failure of the CRC theorem.

## Capacity and the research hypotheses
`capacity.csv` evaluates the estimated hourly alert fraction against K=2/5/10/20/40/60 and simulated opportunity rates 5/15/30/60 per hour. These are scenario parameters, not observed nursing workloads. The earlier `../queue_sweep.csv` additionally measures burstiness, waiting, overflow and completed reviews. No post-calibration alert suppression is permitted while retaining the original guarantee.
**H1:** supported for the constructed graph: exact checks expose review bypasses, unsafe storage paths and cached-derivative reuse. Multi-source provenance now includes both EHR and video parents; revoking either blocks merged derivatives. This does not validate an actual hospital network.
**H2:** partially testable here: compare predictive quality of permitted feature sets and the risk/workload consequence of explicit loss definitions. Structural privacy constraints can preserve ephemeral alerts, but useful clinical performance and feasible human review are not established by ROC or CRC alone.
**H3:** the system graph supplies auditable reachability/cut information absent from predictive accuracy. The separate five-participant skeleton ablation remains too small to establish general predictive graph superiority. No provider-graph survival effect is claimed.

## Limits
This is a sample of a retrospective benchmark, with simulated consent and capacity. It does not establish clinical effectiveness, voluntary consent, reviewer competence, reconstructed-data privacy, model unlearning, or prospective benefit. The benchmark labels can reflect existing sepsis; sparse hourly measurements and unavailable acquisition/store timing constrain causal availability claims. Subgroup analyses are descriptive and not multiplicity-adjusted. Confidence intervals quantify patient resampling within a sample, not all data/label/model uncertainty.

## Reproduce
The single `run_all.sh` entry point uses the pinned protocol and sample manifest. `python -m consent_ai.run --stage all` regenerates both the initial public/demo evaluation and this follow-up; `--stage sepsis` regenerates this stage. All figures are PDF/SVG/PNG and every analytical table is CSV.
Primary source: [PhysioNet/CinC 2019 v1.0.0](https://physionet.org/content/challenge-2019/1.0.0/), Reyna et al., DOI 10.13026/v64v-d857, CC BY 4.0. Statistical source: [Conformal Risk Control, Eq. 4 and Theorem 1](https://www.alphaxiv.org/pdf/2208.02814?page=2).

## Provenance
```json
{
  "run_id": "1470edde-bcb7-48f9-88ec-d52684a41a05",
  "commit": "e32e8be7a7639a8a866bdd474a4c1194c01b703a",
  "python": "3.13.5",
  "configuration": {
    "dataset": "PhysioNet/CinC 2019 v1.0.0 public hospital systems A and B",
    "sampling_seed": 20261023,
    "patients_per_site": 3000,
    "sampling": "Uniform without replacement from complete S3 file listings; no labels inspected for inclusion",
    "prediction_time": "Each observed ICU hour t",
    "outcome": "Provided SepsisLabel at t, already shifted six hours early by the dataset authors",
    "prediction_horizon": "Use published early-warning target unchanged; includes hours after the first positive label; not incident-only forecasting",
    "availability": "Only rows 0 through t; forward-fill and cumulative summaries; no backward fill. Store timestamps unavailable.",
    "seeds": [
      11,
      29,
      47
    ],
    "split": "A: 60% train, 20% calibration, 20% internal test; all B patients external-site test",
    "temporal_holdout": "Not identifiable: absolute admission dates are absent; test causal feature invariance instead",
    "models": [
      "metadata",
      "full_ehr",
      "consent_no_labs",
      "consent_no_vitals"
    ],
    "regularization_C": 1,
    "alpha": 0.05,
    "crc_estimands": [
      "unconditional patient missed-positive-window fraction",
      "positive-patient conditional missed-positive-window fraction"
    ],
    "positive_conditioning": "Use only positive calibration patients for the second rule; apply that threshold to all test patients. Conditional exchangeability required.",
    "bootstrap_replicates": 500,
    "bootstrap_seed": 2026,
    "interval_models": "seed 11, all models and both test sites; 500 paired patient-cluster resamples",
    "workload": "Hourly alerts with no cooldown. Count false alerts per 24 observed patient-hours separately from simulated nurse opportunity rates."
  },
  "scope": "EHR + consent/oversight primary; skeletons secondary; no clinical validation",
  "stage": "sepsis"
}
```

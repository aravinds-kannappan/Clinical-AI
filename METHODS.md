# Methods

The revised primary study uses all **40,336 public PhysioNet/CinC 2019 patients** (20,336 hospital A; 20,000 hospital B; 1,552,210 hourly rows). The data manifest records source URLs, ETags and SHA256 checksums. The full public archive is supplied under its original CC BY 4.0 terms. No credentialed MIMIC-IV experiment is claimed.

## Splits and prediction

Seeds 11, 29 and 47 independently split A into 55% training, 15% validation, 15% calibration and 15% test. B reserves 25% for local calibration and 75% for a frozen external test. The resulting test sets overlap across seeds; seed averages are descriptive, not three independent cohorts.

Causal features use available current/last values, expanding means and observation counts. Preprocessing fits only training rows. Training and primary discrimination exclude rows from inferred onset onward. Logistic regression tunes C in {0.1, 1} and unweighted/balanced classes. Histogram gradient boosting tests three leaf/regularization/class-weight settings with 120 iterations, learning rate 0.08 and training-only removal of constant/all-missing columns. The unidirectional GRU tests hidden sizes 32 and 64, six epochs each, Adam learning rate 0.001, batch size 64, clipped gradients and positive-weighted BCE. Validation average precision selects configurations and epochs. The complete settings are in code and tuning JSON files.

## Incident endpoint and review count

The first positive SepsisLabel already precedes inferred onset by six hours. The eligible incident window is [first positive label, first positive label + 6), with onset required inside the observed stay and the first positive label strictly after admission. Initial-positive and right-censored-onset patients are excluded from conditional incident risk but remain in workload. This is a retrospective benchmark definition.

The first-alert policy emits at most one review per patient. A review before the valid warning window consumes that review and is a missed incident under this endpoint. A repeated-alert comparison emits a review at each above-threshold hour; its incident loss counts any alert in the window. Reviews are counted before inferred onset for positive patients and over the full observed stay for negative patients. This outcome-defined stopping time is not itself a deployable operational stopping rule.

Thresholds are 51 validation-score quantiles plus all-alert/no-alert endpoints, deduplicated. No test curve selects a threshold. The headline frontier is descriptive. A separate audit chooses the threshold maximizing validation challenge utility for each policy and evaluates it on both test sites.

The official challenge utility uses full-stay predicted condition states. For one-review policies, that state stays positive after the first crossing. It is intentionally distinct from the strict incident endpoint and review count. The official BSD-licensed evaluator is pinned and checked against the vectorized implementation.

## Statistical analysis

All seeds have 500 whole-patient bootstrap replicates for AUROC and Brier intervals. The fixed validation-selected policy audit gives pointwise exact 95% binomial intervals for conditional incident risk. These are separate from the joint calibration certificate.

The latter uses exact binomial bounds with tail delta/(4M), alpha=0.05 and delta=0.05; budgets are 0.1, 0.25, 0.5, 0.75 and 1 review per patient. It returns certified, grid infeasible or undetermined. Each confidence statement applies to one frozen model/grid. Four prespecified overlapping demographic groups divide delta by four. Local A and B calibration are distinguished from unguaranteed A-to-B transport.

For each available positive calibration size in {25, 50, 100, 200, 400}, 200 subsets are sampled without replacement from the same calibration pool. Overlapping draws diagnose stability, not independent coverage trials. A fitted domain classifier supplies clipped importance ratios only for an exploratory repeated-alert comparison; exact weighted guarantees are not asserted.

## Consent and oversight

Each patient independently denies labs and vitals with probabilities 0, 0.1, 0.3 or 0.5 per group. A separate hour-12 revocation intervention removes denied historical summaries and resets recurrent state. Models remain frozen. Thresholds are recalibrated on A under each consent scenario. If no certificate exists, the clearly labeled empirical fallback is used for descriptive costs. Real consent preferences are not observed.

FCFS queues use the sepsis score trajectories and a validation-selected first-alert threshold. Arrivals are 0.5/1/2 patients per hour; service times 2/5/10 minutes; reviewer sensitivity 0.8/0.9/1 and specificity 0.9/0.99. Sensitivity is multiplied by max(0.5, 1-0.05 times waiting hours). A successful action requires a timely alert, correct review and completion before inferred onset. False actions in the corrected audit count only patients with no positive sepsis label. These parameters are sensitivity assumptions; published provider response times do not identify active review duration.

Five hundred random DAGs with 50–300 nodes supplement the original constructed graph. Structural path checks do not establish effective human oversight. No clinicians or new patients participated.

## Reproducibility

`bash run_all.sh` reproduces the full revision and selected-policy audit using locked dependencies. The release defaults to a fresh run; exact original source snapshots preserve the completed run and its hash-verified partial-run resume. The original revision's `queues.csv` is retained for provenance; use `results/revision-audit/queues.csv` for corrected false-action counts. See `reproducibility/README.md` for the run lineage.

The initial 6,000-patient hourly-loss study, sparse MIMIC demo and five-subject movement track are historical supplementary results, excluded from the revised primary conclusion.

# Benchmark protocol

## Scientific question

How does full-input AI compare with consent-constrained AI? The current evaluation uses frozen sepsis predictors as a concrete test case; it does not establish disease-independent effects. The primary endpoint is a paired difference under a specified access intervention. The benchmark does not define a single ethics score or an accepted clinical non-inferiority margin.

## Dataset and splits

Use the full public PhysioNet/CinC 2019 A/B release and the versioned patient-level split assignments. Fit on hospital A training patients; tune with A validation patients. A calibration and test populations are held apart. B has 5,000 calibration and 15,000 test patients. Seeds 11, 29 and 47 repeat the split protocol; their patient populations overlap. Never use test outcomes to tune a model, threshold or permission intervention.

## Reference baselines

Logistic regression, gradient boosting and GRU use the same 108 causal summaries. Published models are trained with full public inputs. Full-input predictions are recomputed and checked against saved arrays before the comparison. This isolates inference-time access changes and does not establish consent compliance of training.

## Permission interventions

Eight frozen conditions: full input; independent lab/vital denial probability 0.1, 0.3 or 0.5 at admission; complete lab denial; complete vital denial; denial of both physiological groups (metadata retained); independent per-group revocation probability 0.3 beginning at hour 12. Patient-specific seeded masks are shared across model families. A 30% per-group probability does not mean exactly 30% of patients deny any input.

Denied values and running means are made unavailable and observation counts are cleared. Revocation clears denied history. The GRU reset clears the whole recurrent state, including mixed permitted context. Test outcome labels remain available only to the evaluator. These are simulated permissions, not observed choices.

## Fixed-policy comparison

Reuse each model/seed's original validation-utility threshold separately for first-only and repeated-hourly policies. Keep that threshold unchanged across permission scenarios. The strict incident endpoint requires an alert in the six hours before inferred onset. For first-only review, an earlier alert consumes the review and is a miss. The repeated-hourly policy checks for any in-window alert and counts each above-threshold hour as a review. Workload ends at the retrospectively defined monitoring limit, so this is a benchmark endpoint rather than a deployable stopping rule.

## Reporting contract

Release every model/site/seed/scenario result, not only favorable comparisons. Report pre-onset AUROC, average precision and Brier score; incident missed risk; reviews per patient; normalized challenge utility; and false reviews per nonsepsis patient. Report restricted-minus-reference differences. AUROC/Brier differences use 200 paired patient bootstrap replicates; policy differences use 500. Intervals are pointwise, conditional on fitted models, splits and mask assignments. Seed ranges are descriptive and are not confidence intervals. Current average-precision contrasts are point estimates only.

Report both permitted physiological source-hours and retained originally finite last-value feature cells. Neither is a privacy-leakage measure. Record model, prediction, configuration and source hashes. Full-data labels, identity of sites and retrospective onset definitions remain benchmark assumptions.

## Adding models

A new entry should use the same patient assignments, causal feature cutoff, intervention definitions and outcome estimands. Fit/tune only on designated training/validation data; freeze before testing. Report the full comparison matrix and paired uncertainty. Models trained with simulated masks or source-specific inputs belong in an explicitly labeled training-adapted track, distinct from the current frozen full-input baselines. New thresholds selected on restricted validation data are also a separate policy-adaptation intervention; do not merge their effects into the fixed-policy contrast.

## Claims supported

The release supports reproducible comparisons of simulated permission interventions, model sensitivity and the discrepancy between ranking and operating behavior. It does not prove ethical acceptability, real privacy/security, real consent validity, clinical non-inferiority, effective clinician oversight or causal patient benefit. A broader benchmark would require additional clinical tasks, stronger adapted baselines and preferably participant-grounded permission scenarios.

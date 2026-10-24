# Paired sepsis AI evaluation under consent restrictions

The completed comparison reuses nine frozen supervised predictors and identical held-out patients, labels and validation-selected thresholds. It varies inference-time access to laboratory and vital-sign information. Eight conditions, three models, three seeds and two hospitals produce 144 discrimination rows and 288 policy rows.

The primary finding is that similar ranking performance does not guarantee similar alert behavior. At hospital B, removing labs from the GRU changes mean AUROC from 0.752 to 0.745, but increases conditional missed-incident risk from 0.534 to 0.646 at the fixed repeated-hourly threshold. Reviews decrease from 4.172 to 2.756 per patient. The three seed-specific missed-risk increases are 10.1, 10.2 and 13.3 percentage points, with each pointwise paired interval excluding zero.

At independent per-group denial probability 0.3, mean AUROC falls by 0.019–0.051 across the six model/hospital combinations. All non-reference conditions reduce mean AUROC within each model/hospital combination. Individual contrasts have different uncertainty: for GRU/B without labs, two of the three AUROC intervals include zero. That is not evidence of equivalence.

Restrictions can increase workload. Removing labs from hospital-A boosting reduces missed risk by 4.5 percentage points but adds 2.51 reviews per patient and reduces normalized challenge utility by 0.034. A favorable change in one metric does not establish retained usefulness overall.

## Interpretation

This is a sepsis benchmark study of inference-time information access. All predictors were trained on the original full public feature set. It does not evaluate training permission, retraining, unlearning, weak supervision, observed patient preferences, ethical acceptability, or clinical outcomes. Independent permission draws are a controlled simulation, not an estimate of how patients consent in practice. Clearing a GRU state also removes mixed permitted historical context.

Full-input scores were recomputed and matched to the original stored scores within an absolute tolerance of 2e-6. Comparison intervals use the same patient bootstrap multiplicities in both branches: 200 replicates for AUROC/Brier differences and 500 for policy differences. Intervals are pointwise and conditional on fitted models, splits and permission assignments. The three seeds overlap in patient membership. No clinically justified non-inferiority margin was specified.

## Evidence and reproduction

- `discrimination.csv`: AUROC, average precision, Brier score, paired AUROC/Brier intervals and input-availability proxies.
- `policies.csv`: fixed thresholds, incident risk, reviews per patient, challenge utility and false reviews, with paired differences and intervals.
- `patient-effects-*.npz`: paired patient contributions and denominators for checking policy estimates; these are derived public-benchmark records.
- `provenance.json`: frozen configuration, predictor hashes and parent-prediction hashes.
- `summary.json`: complete row counts and descriptive across-seed means.
- `figures/`: vector figures, measured CSV snapshots, generating scripts and style helper.

Source commit: b270a1cbd39109646334a1aca517b3a60f4f4e49. Run: 42f07f68-d91c-4994-93ac-ed30e8085d18. End-to-end runtime 9m10s; comparison stage 508 seconds. All 26 implementation checks passed. These checks support implementation correctness; mathematical arguments are proved in the paper.

The source archive and full reproduction instructions are in `reproducibility/`. The default published pipeline runs full model fitting, the fixed-policy audit, then this paired comparison. The comparison-only stage expects the fitted models and feature cache from the full stage.

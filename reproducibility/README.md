# Exact source and result lineage

The active source defaults to a fresh full-release run followed by the policy audit and paired consent comparison. It removes the original resume requirement and includes the corrected false-action eligibility. It preserves the measured predictor and policy definitions.

| Stage | Run | Source commit | Time |
|---|---|---|---|
| Initial public-data study | d6aca6bc-ab52-4799-85ca-396c5ee6fede | 1fc848a | 16m47s |
| 6,000-patient hourly study | 1470edde-bcb7-48f9-88ec-d52684a41a05 | e32e8be | 5m02s |
| Full-release partial run | 163e8467-10cb-4f72-9a87-ec36769e4ef6 | 6e1b8ea9 | 2m40s |
| Full-release completion | d2efff2d-0525-47d7-ba94-879667d6b795 | fbfaff0d | 9m03s |
| Paired consent comparison | 42f07f68-d91c-4994-93ac-ed30e8085d18 | b270a1cb | 9m10s |
| Frozen-policy/reviewer audit | a5b85a5f-3001-4207-9b7d-31902ad8f4c0 | 652de9e8 | 1m20s |

The partial run completed logistic seed 11, then failed on boosting binning of constant/all-missing features. The completion run added training-only constant-feature removal and hash-verified the completed logistic outputs. The exact resume inputs are in `results/revision-initial-partial/`; source snapshots preserve their hashes. A fresh active-source run trains logistic again.

`source-full-revision.tar.gz` and `source-policy-audit.tar.gz` are immutable Git archives of those runs. They contain no private proposal, prompt, progress notes or credentials. Original baseline/hourly source archives are also retained.

To replay the original full-revision snapshot, extract its archive into a separate directory, set CONSENT_DATA_ROOT to the public data root, and CONSENT_RESULTS_DIR to an output root containing a copy of `revision-initial-partial/`, then run `bash run_all.sh`. The policy-audit snapshot expects a completed `revision/` under that output root. Use separate virtual environments for separate checkouts.

The original revision queue output is superseded for false actions by `revision-audit/queues.csv`. The correction excludes incident-ineligible patients with positive sepsis labels from the negative class. Prediction, incident-risk and calibration measurements did not change.

The main runs used an Apple M4 CPU, 16 GiB memory, Python 3.13 and two numerical threads. Peak memory was not measured. Locked dependencies, manifests, fitted model outputs and exact patient splits accompany the results.

`source-paired-consent.tar.gz` is the exact source for the matched inference-time comparison. It expects completed `revision/` and `revision-audit/` outputs and the local feature cache produced by the full stage. A clean default run recreates these prerequisites before comparing consent conditions. Provenance hashes identify all nine model files and parent prediction arrays; full-input scores are recomputed and checked before intervention. The comparison stage itself took 508 seconds, excluding setup and checks.

The current paper uses a two-column article layout with unnumbered structure and author–year citations, as requested by the author. The previously downloaded NeurIPS style file is retained but is not used by the current manuscript. No conference submission or acceptance is implied.

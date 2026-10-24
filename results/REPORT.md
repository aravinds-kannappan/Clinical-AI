# Consent-constrained clinical AI: executed research report

**Initial-stage supplement.** The larger primary EHR study and external-hospital evaluation are in [the sepsis report](sepsis/REPORT.md).

**Scope:** EHR plus mathematical consent/oversight evaluation is primary; public skeletons are secondary, following the user’s revised scope. No clinical validation or patient benefit is claimed.

## What ran
- **DEMO DATA:** 100 source MIMIC-IV demo patients, 99 eligible patients and 387 landmark decisions; 5 positive outcome windows. See `ehr_audit.json`.
- **OPEN DERIVED SKELETONS:** all five archives in Zenodo 12773013; compact ST-GCN, summary, topology-free and shuffled-edge comparators; participant-held-out evaluation.
- **SIMULATION:** exact graph policies, cached-derivative withdrawal, structural stress tests, expected-load and FCFS queue sweeps.
- **SYNTHETIC MATHEMATICAL CHECK:** CRC Monte Carlo with independent patient trajectories and correlated within-patient windows, plus deliberate score shift.
- **SEMI-SYNTHETIC:** observed skeleton windows paired with unrelated demo EHR profiles; no real patient linkage or causal association is inferred.
- **NOT RUN:** full credentialed MIMIC-IV, NTU, SAFER, raw-video pose extraction/identity attacks, clinical bed-exit/delirium endpoints, external-hospital or prospective clinical validation.

## H1: structure reveals risk
The implemented exact path check identifies unreviewed action paths in the permissive graph. Removing bypass edges and requiring physician review eliminates them. Consent removes persistent-storage paths while retaining bedside alert and ephemeral action reachability. This verifies the finite graph, not the completeness of a clinical system representation.
See `graph_scenarios.csv`, `bypass_witnesses.json`, `graph_centrality.csv`, `graph_stress.csv` and `withdrawal.csv`. Direct source-edge masking leaves cached derivative reuse possible; provenance-aware masking blocks it. Corruption exposure counts descendants, not demonstrated changes in clinical predictions.

## H2: constraints preserve utility
Discrimination/calibration on random held-out demo patients. Only ONE of the three prespecified seeds has positive test patients; AUROC/AP averages therefore contain only that evaluable seed. Other estimates remain undefined, not zero. Brier uses all three seeds:
- consent_no_labs: AUROC 0.1190; average precision 0.0256; Brier 0.0228.
- consent_no_vitals: AUROC 0.0000; average precision 0.0232; Brier 0.0127.
- full_ehr: AUROC 0.0198; average precision 0.0235; Brier 0.0172.
- metadata: AUROC 0.7976; average precision 0.1061; Brier 0.0116.

Consent variants are separately fitted using only permitted features. They isolate an information-restriction tradeoff; the public dataset contains no observed patient consent decisions. Patient-level intervals and paired effects are in `ehr_intervals.csv` and `ehr_paired_effects.csv`.
Review workload and privacy exposure remain separate from model discrimination. Queue overload or an all-alert fallback prevents interpreting structural compliance as useful operational oversight. Useful clinical performance is not established by this demo.

## H3: graph structure must earn its place
Secondary skeleton results, averaged across three training seeds after participant-held-out predictions are pooled:
- shuffled: AUROC 0.4053; Brier 0.0668.
- stgcn: AUROC 0.4198; Brier 0.0641.
- summary: AUROC 0.4950; Brier 0.1186.
- topology_free: AUROC 0.4186; Brier 0.0637.
Use `movement_paired_effects.csv` for paired differences and `movement_intervals.csv` for participant-bootstrap intervals. Five participants are insufficient to establish general graph superiority; overlapping windows do not increase the independent sample size. Models have the same graph training budget and fixed splits. No test-set winner was selected.

## Mathematical definitions and statistical interpretation
1. **Typed graph:** node/edge types, provenance, patient IDs, event timestamps and latency are explicit. Time-respecting reachability is separate from static paths.
2. **Consent:** A_allowed(i,p) = A ⊙ M(i,p). Tests check matrix equality, purpose and patient isolation, withdrawal and derivative reuse.
3. **Review:** enumerate all simple sensitive-source→action paths after deleting mandatory review nodes. Test equivalence exhaustively on all 64 forward DAGs over four vertices. Paths with cycles have simple witnesses, so a simple-path check is sufficient for static reachability. Availability is separately measured.
4. **Capacity:** sum_i E[r_i] ≤ K per hour. The empirical held-out score distribution estimates alert probabilities; arrival rates and service times are simulated. An expectation constraint is not a queue-length guarantee.
5. **CRC:** lambda_hat = inf{lambda: (n R_hat(lambda)+B)/(n+1) ≤ alpha}; alpha=0.05, B=1. Use exact score knots, inclusive ties, and lambda=1 if the feasible set is empty.
**Loss:** L_i = missed positive windows / max(1, number of positive windows); zero for no positive windows. This is an unconditional patient-average loss, not conditional false-negative rate. Report positive-patient missed fraction and sensitivity separately.
**Assumptions adjacent to CRC results:** Frozen predictor and loss; exchangeable calibration/future patient loss functions; bounded B=1, non-increasing right-continuous loss in lambda; terminal all-alert loss=0; no post-calibration alert suppression. Expectation over calibration and new patient, not a per-patient/subgroup guarantee. Shifted populations have no asserted guarantee.
Calibration sizes and fallback status are recorded for every model in `ehr_calibration.csv`. Observed n values: [16, 25]. The secondary movement calibration uses n=1, so the finite-sample correction is 1/2 and forces the terminal all-alert fallback at alpha=.05.

### Synthetic validation of the statistical procedure
The following checks use synthetic data only. Each n/shift setting has 600 independent calibration repetitions across three seeds, evaluated on 100 fresh synthetic patients per repetition; 95% intervals are Monte Carlo uncertainty, not a clinical risk bound.
- n=10, shifted=False, B=1, alpha=.05: mean patient missed loss 0.0000, Monte Carlo interval [0.0000, 0.0000]. Loss and assumptions as defined immediately above; shifted results have no asserted CRC guarantee.
- n=10, shifted=True, B=1, alpha=.05: mean patient missed loss 0.0000, Monte Carlo interval [0.0000, 0.0000]. Loss and assumptions as defined immediately above; shifted results have no asserted CRC guarantee.
- n=25, shifted=False, B=1, alpha=.05: mean patient missed loss 0.0240, Monte Carlo interval [0.0219, 0.0261]. Loss and assumptions as defined immediately above; shifted results have no asserted CRC guarantee.
- n=25, shifted=True, B=1, alpha=.05: mean patient missed loss 0.2535, Monte Carlo interval [0.2444, 0.2627]. Loss and assumptions as defined immediately above; shifted results have no asserted CRC guarantee.
- n=100, shifted=False, B=1, alpha=.05: mean patient missed loss 0.0442, Monte Carlo interval [0.0423, 0.0462]. Loss and assumptions as defined immediately above; shifted results have no asserted CRC guarantee.
- n=100, shifted=True, B=1, alpha=.05: mean patient missed loss 0.3605, Monte Carlo interval [0.3551, 0.3658]. Loss and assumptions as defined immediately above; shifted results have no asserted CRC guarantee.

## Causality, holdouts, subgroups and uncertainty
- EHR event and store timestamps must precede the 6/12/24-hour landmark. Unit tests perturb later and late-recorded events and verify unchanged past features. Outcomes are kept out of the feature matrix.
- Train/calibration/test splits are patient-disjoint. Imputation/scaling fit training patients only. Three fixed seeds are reported; seed 11 has 500 patient-bootstrap replicates and paired comparisons. Bootstrap intervals can be unreliable with sparse positive patients; valid replicate counts are supplied.
- Coarse anchor-era holdout and missingness shift are explicit stress tests. Anchor-year groups are not exact chronology; a strict calendar holdout cannot be claimed from these de-identified dates. A second hospital is unavailable.
- Gender and race subgroups include support counts; low-support cells are labeled. Group comparisons are exploratory, without multiplicity-adjusted inference. Motion participant/trial subgroups are in fold metrics; demographic attributes were not inferred.
- No event-rate-per-day estimate is computed from sparse EHR landmarks or skeleton frames with unverified frame timing. False-positive fraction and false-alert counts use explicitly defined opportunities.

## Privacy and the provider graph
Privacy outputs count prohibited storage reachability and cached-derivative reuse only. These do not measure membership inference, re-identification or reconstruction. No raw-versus-skeleton privacy benefit has been measured.
Provider→order→patient edges use pre-cutoff provider identifiers. The projected graph is descriptive and is not an access-log reproduction of Lu and Ma, a communication graph, or an outcome association. No predictive provider-graph model was fitted, so its structural centralities are not presented as predictive ablations.

## Limitations and evidence against overclaiming
The demo is small and selected; actual review capacity, reviewer competence, voluntary consent and clinical usefulness are unmeasured. The system graph is constructed, not audited from a deployed system. Synthetic queue arrivals and semi-synthetic pairing cannot identify clinical causal effects. Withdrawal invalidates future use in this implementation; it is not physical erasure or model unlearning. Real-time alerts may require ephemeral clinically meaningful information even when storage is denied. EHR writes are treated as storage and therefore blocked for video-derived denied storage purposes.
Small calibration sets can produce either trivial all-alert fallback or a permissive rule when the unconditional loss sees few positive patients. Neither proves a low conditional false-negative rate. Post-calibration dropping, review delays and distribution shift invalidate an unqualified risk-control interpretation.

## Reproduction and outputs
Run `bash run_all.sh`. Dependencies are locked in `uv.lock`; configuration is in `configs/protocol.json`. Inputs, publisher checksums and URLs are in `data_manifest.json`. The local experiment source snapshot and run identifier are recorded in `provenance.json`. Source includes unit tests, not just assertions in evaluation code.
Every analytical table is a CSV in this folder. Figure 1 is an aggregation of implemented allowed graph nodes; Figure 2 shows the actual consent graph (dashed grey edges are denied storage paths). Figures are exported as PDF, SVG and PNG. `index.html` is a self-contained interactive results page.

## Sources
- Johnson et al. MIMIC-IV demo v2.2: https://physionet.org/content/mimic-iv-demo/2.2/ (DEMO DATA).
- Koffi et al. Derived 3D skeleton UP-Fall data: https://zenodo.org/records/12773013 (CC BY 4.0); methods: https://www.alphaxiv.org/pdf/2502.19048.
- Angelopoulos et al. Conformal Risk Control, Eq. 4 and Theorem 1: https://www.alphaxiv.org/pdf/2208.02814?page=2.
- Yan et al. ST-GCN: https://www.alphaxiv.org/pdf/1801.07455. Compact adapted architecture, not benchmark reproduction.

## Run provenance
```json
{
  "run_id": "d6aca6bc-ab52-4799-85ca-396c5ee6fede",
  "commit": "1fc848a052a250719fba3f9573331e5db9915c2a",
  "python": "3.13.5",
  "configuration": {
    "seeds": [
      11,
      29,
      47
    ],
    "alpha": 0.05,
    "loss_bound": 1.0,
    "bootstrap_replicates": 500,
    "movement": {
      "prediction_time": "end of 32 observed frames",
      "outcome": "annotated impact in the final observed frame",
      "horizon_seconds": 0,
      "stride_frames": 8,
      "sample_frames": 32,
      "epochs": 20,
      "batch_size": 32,
      "learning_rate": 0.001,
      "channels": [
        32,
        64
      ],
      "split_unit": "participant",
      "temporal_holdout": "trial 3 of held-out participants: repetition-order stress only, no verified calendar dates",
      "clinical_metadata": "not available in motion-only benchmarks",
      "unavailable_labels": [
        "clinical bed exit",
        "clinical delirium",
        "future fall"
      ]
    },
    "ehr": {
      "prediction_time": "ICU admission plus 6, 12, 24 hours",
      "outcome": "death within the next 48 hours",
      "horizon_hours": 48,
      "landmarks_hours": [
        6,
        12,
        24
      ],
      "split_unit": "subject_id",
      "temporal_holdout": "2014 - 2016 anchor-year group; earlier group development",
      "site_holdout": "not possible: single institution",
      "vital_items": [
        220045,
        220179,
        220180,
        220181,
        220210,
        220277,
        223761,
        223762
      ],
      "lab_items": [
        50813,
        50912,
        51301,
        51265,
        50971,
        50983
      ],
      "sedative_items": [
        222168,
        221668,
        221744,
        225150
      ],
      "regularization_C": 1.0
    },
    "simulation": {
      "K_per_hour": [
        2,
        5,
        10,
        20,
        40,
        60
      ],
      "arrivals_per_hour": [
        5,
        15,
        30,
        60
      ],
      "service_minutes": [
        2,
        5,
        10
      ],
      "hours": 8,
      "queue_limit": 20,
      "withdrawal_hours": [
        0,
        4
      ],
      "max_wait_minutes": 15,
      "lambda_grid": [
        0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0
      ]
    },
    "privacy": {
      "measure": "closed-set participant re-identification balanced accuracy",
      "attack_split": "train trial 1, test trial 3; same identities, distinct recordings",
      "rgb_features": "per-channel 16-bin normalized histograms and 8x8 mean appearance",
      "skeleton_features": "root-centered trajectory mean, standard deviation and velocity; retain body scale",
      "classifier": "standardized regularized logistic regression",
      "limitation": "one specified attacker; not a proof of anonymity"
    }
  },
  "scope": "EHR + consent/oversight primary; skeletons secondary; no clinical validation"
}
```

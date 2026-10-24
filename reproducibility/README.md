# Reproduction and provenance

The complete public-data study has two stages. Published CSVs retain their original
run identifiers and source commits. The compressed source snapshots here contain
exactly the committed code used for each stage; no proposal, prompt or working
notes are included.

| Stage | Source commit | Run identifier | Output |
|---|---|---|---|
| Initial demo, graph, simulation and skeletons | 1fc848a | d6aca6bc-ab52-4799-85ca-396c5ee6fede | `results/` |
| Larger sepsis cohort and conditional-risk comparison | e32e8be7a7639a8a866bdd474a4c1194c01b703a | 1470edde-bcb7-48f9-88ec-d52684a41a05 | `results/sepsis/` |

The release uses the follow-up source, switches the default execution stage to
`all`, improves documentation, and corrects presentation-only mobile scrolling
and chart tooltip reset, clarifies the ODbL metadata, and clips diagram arrows to node boundaries. The follow-up graph includes both EHR and movement
parents in merged-object provenance. This is an explicit improvement over the
initial graph; use `results/sepsis/graph/` for that result. Its withdrawal test
checks that revoking either source blocks merged cached derivatives.

The original initial-stage attempt failed on a skeleton filename/header variant
before completing the movement evaluation. Its incomplete files are superseded
by the completed rerun. It is not an extra seed or independent experiment.

Run `bash run_all.sh` from the repository root for the current combined release.
For an exact historical stage, extract the corresponding archive into an empty
directory and run its `run_all.sh`. Both archives include `uv.lock`; Python was
3.13.5. Set `CONSENT_DATA_ROOT` to an absolute path containing the supplied
`data/raw` files to reuse them. Set `CONSENT_RESULTS_DIR` to a new directory to
keep the checked-in result snapshot intact. CPU arithmetic/library differences
can affect the last digits; no GPU is required.

The bootstrap uses 500 patient resamples and is prespecified for seed 11;
three-seed means and seed-specific outputs are separate quantities. Public
hospital B was never used for model or threshold selection. Conditional-risk
calibration uses a smaller event-positive calibration set and must not be
interpreted as an individual-patient or shifted-population guarantee.

Full credentialed MIMIC and NTU analyses were not run. Schema/access hooks do not
constitute validated full-data analyses. SAFER was omitted. The distributed data
are the approval-free sources described in `DATA_CARD.md`, under their original
licenses.

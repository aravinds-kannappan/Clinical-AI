# Answer to the research question

**The design and evaluation are possible; the full conjunction has not been demonstrated.** This revision gives a concrete reason: under the tested strict first-alert policy, useful score discrimination and positive challenge utility coexist with failure of the incident-review requirement.

## What changed the scientific answer

The revised study uses all 40,336 public patients, validation-tuned logistic regression, gradient boosting and a GRU. Mean pre-onset AUROC improves from 0.745 for logistic to 0.794 for boosting at hospital A; externally, the GRU reaches 0.752 versus logistic's 0.666. These are descriptive three-seed means, with every seed's patient-bootstrap intervals released.

Despite this improvement, all local first-alert grids are excluded by the simultaneous confidence certificate at a 5% conditional incident missed-event target—even with a budget of one review per patient. This rules out those finite grids under the sampling assumptions. It does not rule out every threshold, model, monitoring design or healthcare AI pipeline.

## Why a better predictor can still fail

A first alert has to occur inside the specified six-hour pre-onset window. An earlier alert consumes the one review and counts as a miss under this endpoint. At hospital A, the validation-selected boosting policy averages 0.193 reviews per patient and positive challenge utility of 0.332, but strict incident missed risk is 0.960. The utility rewards a wider warning window and a latched positive condition state. The metrics answer different questions.

This is also a mathematical issue. Nested score thresholds do not make timely first-alert loss monotone. The manuscript provides an explicit counterexample, a population feasibility characterization, and a finite-grid certificate that does not require monotonicity. It distinguishes a genuinely excluded grid from a sample too small to certify anything. The general certificate is an application of established simultaneous-confidence/Learn then Test methods, not an invented new general theorem.

## Consent and oversight

Consent is now patient-specific, with lab/vital opt-outs and hour-12 revocation that clears derived and recurrent state. These are simulated preferences. Their cost curves do not establish what real patients would choose.

The review audit uses the actual sepsis scores and 972 arrival/service/noise scenarios. It counts successful action only when a correct review completes before inferred onset. This makes oversight a process, but its parameter values remain assumptions. No human reviewers participated. Published provider response delays do not justify equating them with two-, five- or ten-minute active service times.

Review-path and storage constraints are verified on the modeled graph. Five hundred random DAGs broaden structural testing: 126 have a source-to-action path and 103 have an unreviewed bypass. These synthetic results show why placing a review node in a diagram is insufficient; they do not audit a deployed hospital system.

## Scope of the conclusion

There is **no row that establishes the original research question in full**. The empirical alert policies fail the stated risk target, while actual clinician effectiveness and patient benefit remain unmeasured. The strongest supported claim is that explicit controls and a mathematically valid evaluation can expose where a particular pipeline fails.

The strict window penalizes potentially useful early assessments. Workload also stops retrospectively at inferred onset for positive patients. A practical next study should evaluate continuing review or cooldown policies with an observable stopping rule and a guarantee matched to that policy. It should then measure clinician response and outcomes prospectively. Full credentialed MIMIC-IV and clinical deployment were outside the completed public-data study.

See [the paper](paper.pdf), [methods](METHODS.md), and [the measured outputs](results/revision/REPORT.md).

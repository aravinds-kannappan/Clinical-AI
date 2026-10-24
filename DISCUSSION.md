# Conclusion on the research question

**This study does not establish a complete affirmative answer.** It demonstrates
an implementable, auditable approach to consent and mandatory review, while
leaving clinically useful prediction and effective human oversight unestablished.

The research question requires all these properties simultaneously. Showing
that a graph obeys a rule is insufficient to show that a healthcare system
benefits patients or that human reviewers can manage its output.

## What the evidence establishes

**Sensitive data flows:** In the constructed system graph, purpose-specific
consent masks remove prohibited storage routes, and provenance-aware withdrawal
blocks future reuse of affected cached derivatives. These are exact properties
of the modeled graph, not evidence of informed consent or an audited deployment.

**Consequential decisions:** Requiring a review node on every modeled path to an
action eliminates the modeled bypasses. This establishes a structural review
requirement. It does not measure whether a clinician actually completes a timely,
competent review or takes the correct action.

**Model errors and useful prediction:** The 6,000-patient retrospective EHR study
finds a substantial risk-definition/workload tradeoff. With the full-EHR model
in the prespecified seed-11 internal test, the all-patient calibrated rule had
4.68% average patient missed-window loss but 50.14% average missed-window loss
among positive patients. Calibrating on positive patients reduced that conditional
loss to 4.13%, while alerting on 92.69% of hourly observations. These are fractions
of positive windows, averaged within the indicated patient population; they are
not percentages of patients completely missed. At the other hospital, conditional
missed loss for that same frozen rule increased to 26.25%.

These calibration procedures use alpha=.05 and B=1; calibration n was 600 for the
all-patient rule and 60 for the positive-patient rule. The loss is each patient's
missed-positive-window fraction, zero for patients with no positives. The
expectation guarantee requires a frozen predictor/loss, exchangeable calibration
and future patient loss functions, bounded non-increasing right-continuous loss,
a terminal zero-loss rule, and no post-calibration alert suppression. The
positive-patient rule additionally requires exchangeability conditional on
positive status. Neither individual patients nor the shifted hospital receive
an asserted guarantee. These reported test losses are point estimates, not
confidence bounds or evidence that every future test cohort meets the target.

The high alert fraction indicates a workload problem to investigate; it is not
proof of impossibility for every future design. Capacity parameters and queues
were simulated. Actual staffing, review time, review quality, alert suppression
policies and patient benefit were not measured.

## Hypothesis-level conclusion

| Hypothesis | Conclusion |
|---|---|
| H1: structure reveals risk | Supported within the constructed graph: path analysis reveals bypass/storage risks that accuracy does not describe. |
| H2: constraints preserve useful performance | Not established. Structural constraints work, but clinically useful performance together with manageable, effective review was not demonstrated. |
| H3: structure adds value over simpler approaches | Demonstrated as structural audit capability only. The small skeleton comparison does not establish predictive graph-model superiority; operational advantage was not evaluated. |

**Video is not necessary to study the core research question.** The EHR models,
explicit consent graph, loss definitions and review-capacity analysis can be
evaluated without video. Video/skeleton data would be needed for additional
claims specifically about movement monitoring or video privacy, which this
primary study does not make.

A defensible conclusion is: **explicit consent and review constraints are
technically feasible and mathematically auditable, but their coexistence with
clinically useful predictions and effective human oversight remains an open
empirical question.** Establishing that conjunction would require stronger
predictive validation, operational review studies and prospective clinical
evaluation; structural compliance and an expected-risk theorem alone do not
establish it.

Evidence: [primary report](results/sepsis/REPORT.md),
[exact metrics](results/sepsis/metrics.csv),
[paired statistical comparisons](results/sepsis/paired_effects.csv),
[graph checks](results/sepsis/graph/graph_scenarios.csv),
[secondary study](results/REPORT.md), and
[mathematical assumptions and proofs](MATHEMATICS.md).

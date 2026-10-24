# What the study concludes

The matched experiment now directly asks whether a sepsis AI system retains performance when its permitted inputs change. It shows a conditional, model- and source-dependent cost. All non-reference conditions lower mean AUROC within each model/hospital combination. Some reductions are small, but ranking alone can hide worse incident detection at the fixed threshold.

The clearest example is the hospital-B GRU without laboratory inputs: mean AUROC changes from 0.752 to 0.745, while missed-incident risk rises by 11.2 percentage points and review demand falls by 1.42 per patient. Small ranking differences do not establish preserved alert behavior. The three seed-specific missed-risk intervals all exclude zero. These are retrospective benchmark outcomes, not observed effects on patient health.

This supports framing the work as a sepsis benchmark and evaluation study. Its contribution is a reusable matched protocol, reference baselines, measured contrasts, uncertainty and documented failure cases. It is not a new learning algorithm or an ethical certification. Broader benchmarking would benefit from another clinical task and models trained specifically for permitted data.

The original research question also requires explicit consent and effective oversight. The implementation enforces modeled input restrictions and tests modeled review paths. That is narrower than obtaining valid informed consent, preventing data leakage or demonstrating effective clinicians. Reviewers and preferences are simulated. All models were originally trained on full public inputs, so training consent and removal of learned influence are not tested.

The secondary first-alert study finds every tested local grid infeasible at the declared 5% missed-risk target, including a one-review-per-patient budget. The problem is the strict first-review timing definition: early review can consume the available action before the valid window. Positive challenge utility does not resolve that different endpoint. Other policies, models and clinical review processes are not ruled out.

TRACER motivates the broader question about sensitive bedside monitoring; it uses different tasks and nonpublic video/record data. Its authors report ethics approval and restricted data handling while discussing consent and surveillance issues. This study neither reproduces TRACER nor alleges unauthorized collection or leakage.

The mathematics defines what a performance-preservation claim would require. A bounded-loss upper bound must lie below a prespecified, justified tolerance. A bootstrap interval crossing zero is not proof of equivalence. Statistical proofs cannot determine what patients should consent to or how much authority AI should receive.

The next comparisons should distinguish inference restriction, training adaptation and policy adaptation. Missingness-aware training, consent-aware training masks and source-specific models can be evaluated on the released protocol. Real participant preferences and prospective clinician outcomes remain necessary for claims about ethical deployment or patient benefit.

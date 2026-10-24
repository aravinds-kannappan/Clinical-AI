# Paired performance under consent restrictions

For a frozen predictor and decision rule, evaluate the full and permitted-input versions on the same patient. With bounded patient loss $L\in[0,1]$, define

$$D_i=L_i^{\mathrm{restricted}}-L_i^{\mathrm{full}},\qquad\Delta=\mathbb E[D_i].$$

For $J$ comparisons fixed independently of the evaluation sample, $D_i\in[-1,1]$ and Hoeffding's inequality plus a union bound imply, with probability at least $1-\delta$,

$$\Delta_j\le\bar D_j+\sqrt{\frac{2\log(J/\delta)}{n}}\quad\text{for every }j.$$

Proof: each upper-tail probability is at most $\exp(-nt^2/2)$; substitute the displayed deviation and sum the $J$ probabilities. Independence is required across evaluation patients, not across comparisons. For incident-positive conditional loss use the positive-patient sample and its conditional law. Predictors, policies and consent mechanisms must remain fixed for the stated deployment interpretation.

A bound below a **prespecified** tolerance can support bounded-loss non-inferiority. It cannot determine the ethically acceptable tolerance. This is a classical concentration argument, not a new theorem in statistical learning. AUROC is a ranking functional; its paired bootstrap interval does not follow from this patient-loss statement. The reported study has no clinically validated non-inferiority margin and makes no equivalence claim.

# Mathematical results

Full statements and proofs are in [the manuscript](paper.pdf), with editable [LaTeX source](paper.tex). The simultaneous-confidence construction applies established Learn then Test reasoning; it is not a new general risk-control framework.

## 1. The policy and the estimands

For a patient's score sequence, let $T_\tau$ be the first threshold crossing. For an incident-positive patient, the valid warning window is $[a,b]$.

$$
T_\tau=\inf\{t:S_t\ge\tau\},\quad L_\tau=\mathbf 1\{T_\tau\notin[a,b]\},\quad R_\tau=\mathbf 1\{T_\tau\le T\}.
$$

We require conditional incident risk $r(\tau)=\mathbb E[L_\tau\mid Z=1]\le\alpha$ and expected reviews per patient $w(\tau)=\mathbb E[R_\tau]\le K$. Workload uses the retrospective pre-onset monitoring interval for positive patients and the observed stay for negative patients. This benchmark stopping rule is not available prospectively without an onset-detection process.

## 2. First-alert loss need not be monotone

A pre-window score of 0.6 and an in-window score of 0.9 provide a counterexample. Threshold 0.8 gives a timely alert; threshold 0.5 gives an early alert and consumes the one review. Loss across thresholds 0.5, 0.8 and 1.0 is 1, 0 and 1. The review indicators remain nested.

Ordinary monotone-loss conformal risk control therefore cannot be applied to this first-alert loss without an additional assumption. Repeated-alert loss, which counts any crossing in the valid window, is a different, monotone endpoint.

## 3. Population feasibility

Let $A$ and $B$ be the pre-window and in-window score maxima; $C$ is the maximum over the review-monitoring interval. Define

$$
H(\tau)=\Pr(A<\tau\le B\mid Z=1),\qquad W(\tau)=\Pr(C\ge\tau).
$$

**Theorem.** If the risk-feasible set $\mathcal T_\alpha=\{\tau:H(\tau)\ge1-\alpha\}$ has a maximum $\tau_\star$, then

$$
K_{\min}=W(\tau_\star)\ge\Pr(Z=1)(1-\alpha).
$$

A jointly feasible threshold exists exactly when $K\ge K_{\min}$. An empty risk-feasible set cannot be rescued by increasing the review budget. A finite grid guarantees attainment when nonempty. The proof uses the exact timely-alert event and monotonicity of workload, not monotonicity of incident loss.

**Corollary.** When early consumption is impossible and the positive monitoring interval equals the warning window, continuous class-conditional maximum-score CDFs yield the familiar ROC identity

$$
K_{\min}=\pi(1-\alpha)+(1-\pi)\left[1-F_0(F_1^{-1}(\alpha))\right].
$$

This special-case identity is not a novel general feasibility result.

## 4. A finite-sample joint certificate

Freeze $M$ thresholds using training/validation data. With independent calibration patients, compute exact one-sided binomial lower and upper bounds for positive-patient risk and all-patient review probability. Each tail receives $\delta/(4M)$.

With probability at least $1-\delta$, all $4M$ bounds cover simultaneously. Hence:

- **Certified:** some policy has both upper bounds at or below $(\alpha,K)$.
- **Grid infeasible:** every policy has at least one lower bound above its target.
- **Undetermined:** neither statement is established.

Selection among certified policies preserves the guarantee. There is no monotonicity requirement. These certificates are per frozen model/grid; the confidence statement is not automatically joint across all fitted models and seeds. Prespecified overlapping groups can allocate $\delta$ by a further union bound.

## 5. Consent and hospital shift

A fixed measurable consent transformation preserves independence and identical distribution when the full patient/consent/randomization tuples have the same joint law in calibration and deployment. Consent need not be outcome-independent. Conditional ignorability alone does not protect against a changed consent mechanism.

For known bounded target/source density ratio $w\le B_w$, a Hoeffding construction bounds target conditional risk through a weighted numerator and a positive lower bound on weighted prevalence. The manuscript gives its complete statement. Estimated, clipped domain-classifier ratios used in the empirical diagnostic do **not** satisfy the known-ratio premise by construction.

## 6. Structural controls

Patient/purpose masks remove prohibited data-flow edges; withdrawal clears dependent cached state. Every sensitive-source-to-action path passes through review exactly when deleting review nodes disconnects those sources from actions. This is a standard graph equivalence and concerns the specified graph. It does not prove reviewer competence, timely action, or compliance by an external system.

`tests/test_joint_risk.py` checks the counterexample, binomial boundaries, certificate outcomes, evaluator agreement, constant features, and reviewer-error eligibility. Tests are mechanised checks, not substitutes for the proofs.

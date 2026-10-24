# Mathematical guarantees and their limits

This document distinguishes exact statements about the implemented finite graph
from statistical statements requiring assumptions about future patients.

## 1. Patient- and purpose-specific edge masks

For a fixed time t, index the vertices consistently in A and M(i,p). Define

$$A^{allowed}_{i,p}[u,v]=A[u,v]M_{i,p}[u,v],\quad M_{i,p}[u,v]\in\{0,1\}.$$

The implementation constructs a graph with edge (u,v) iff this product is 1.
Thus the adjacency equality is an identity, checked entry by entry. It is not
proof that the supplied consent policy represents informed consent.

A derived object's provenance is the union of its inputs' source provenance.
Future use for purpose p is allowed only if every contributing source remains
permitted for the same patient and p. Revocation invalidates cached derivatives
as well as direct reads. No physical deletion or model-unlearning claim follows.

## 2. Exact review-path equivalence

Let S and D be sensitive-source and consequential-action nodes, and let H be
mandatory review nodes, disjoint from S and D. Then

$$[\forall\pi\in\mathcal P_G(S,D),\ \pi\cap H\ne\varnothing]
\iff [\mathcal P_{G-H}(S,D)=\varnothing].$$

**Proof.** A surviving path in G-H is a path in G avoiding H and violates the
left condition. Conversely, any path in G avoiding H survives deletion of H.
Any reachable directed walk contains a simple path after removing cycles, so
simple-path witnesses are sufficient. The tests exhaustively compare both
formulations for the 64 forward DAGs on four ordered vertices and test bypass,
disconnection, patient isolation and temporal-order counterexamples.

For persistent storage that is completely forbidden, the stronger requirement
is no S-to-storage path at all, not merely a path passing through review.
A path to an ephemeral nurse alert can remain. An EHR write is still persistent
storage and is blocked if it would store a forbidden source's derivative.

Static reachability can overestimate feasible temporal paths. The temporal
routine propagates earliest arrival times, requires event order where specified,
and includes processing latency. Centrality ranks candidates for interventions;
it does not prove safety or reviewer competence.

## 3. Monotone patient loss and finite-sample correction

Let s_it be a frozen model score in [0,1]. At conservativeness lambda, alert iff
1-s_it <= lambda. Define

$$L_i(\lambda)=\frac{\sum_t y_{it}\mathbf1\{1-s_{it}>\lambda\}}
{\max(1,\sum_t y_{it})}.$$

Every summand is non-increasing and right-continuous in lambda. Therefore L_i
is non-increasing, right-continuous, lies in [0,1], and L_i(1)=0. Ties are
included together at the score knot. Calibration units are whole patients.

With B=1 and alpha=.05, choose

$$\widehat\lambda=\inf\{\lambda:(n\widehat R_n(\lambda)+1)/(n+1)\le .05\}.$$

If the set is empty, choose lambda=1. In particular, for n<19 the correction
1/(n+1) exceeds .05 even at zero empirical loss, so the rule must fall back to
alerting every opportunity. Repeated frames cannot be counted as extra patients.

**Why the expectation bound holds (proof sketch).** Assume exchangeable patient
loss functions and a frozen predictor, along with boundedness, monotonicity,
right-continuity and the terminal condition. Compare lambda_hat with the oracle
threshold selected using all n+1 loss functions. The extra loss is at most B,
so the finite-sample correction makes lambda_hat at least as conservative as
that oracle threshold. Monotonicity bounds the future loss by its loss at the
oracle threshold. Conditional on the unordered collection of loss functions,
exchangeability makes the future index uniform, so its expected loss equals
the average oracle loss, at most alpha. Taking expectations gives the result.
This averages over calibration and the future patient, not each realized
calibration set or individual patient. See [Conformal Risk Control, Eq. 4 and
Theorem 1](https://www.alphaxiv.org/pdf/2208.02814?page=2).

## 4. The estimand can hide clinically important misses

Let Z_i indicate at least one positive window. Since L_i=0 when Z_i=0,

$$\mathbb E[L_i]=\Pr(Z_i=1)\mathbb E[L_i\mid Z_i=1].$$

If positive-patient prevalence is below alpha, missing every positive window
can still satisfy the unconditional target. This does not contradict CRC: the
loss definition may be inadequate for the intended safety commitment.

The follow-up therefore calibrates a second rule on positive calibration
patients only, using their count n in the same finite-sample formula. Its
interpretation is expected conditional missed-window loss for a future positive
patient, under conditional exchangeability. Apply its threshold to all patients
to measure the workload cost. Neither rule has an asserted guarantee after
hospital shift, feature corruption, or post-calibration alert dropping.

## 5. Risk–capacity compatibility

For a specified period, let W(lambda)=sum_i E[r_i(lambda)]. Nested alerts make
W non-decreasing in lambda, while missed-event loss is non-increasing. Among
thresholds at least as conservative as lambda_hat, a capacity K is feasible
only if W(lambda_hat)<=K. If it fails there, increasing lambda cannot restore
capacity. This is a useful incompatibility check, not a guarantee that an
empirically estimated W equals future workload.

An expectation bound does not cap realized arrivals, waiting time or backlog.
The implementation therefore separately simulates a finite-buffer FCFS queue,
service times, overload, completed reviews and delay. Clinical actions cannot
inherit an alert-level risk statement without accounting for completed review
and correct action.

## 6. Statistical uncertainty

Patient-cluster bootstrap preserves within-patient dependence. Paired model
comparisons use the same resampled patient counts for both models. For AUROC,
weights replicate all rows belonging to each sampled patient. A tie-aware
weighted-rank calculation is tested against explicit resampling. Brier is a
proper probability score, not a pure calibration error; reliability bins are
reported independently. Synthetic Monte Carlo intervals quantify the simulation
estimator, not uncertainty about clinical benefit.

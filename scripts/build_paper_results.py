"""Build manuscript tables from completed CSV outputs; no model fitting."""
from pathlib import Path
import argparse
import pandas as pd
p=argparse.ArgumentParser();p.add_argument('--results',default='results');a=p.parse_args();root=Path(a.results)
m=pd.read_csv(root/'revision/metrics.csv');s=pd.read_csv(root/'revision-audit/selected_policies.csv');f=pd.read_csv(root/'revision/frontiers.csv');c=pd.read_csv(root/'revision/certificates.csv')
names={'logistic':'Logistic','boosting':'Boosting','gru':'GRU'}
lines=[r'''\paragraph{Stronger discrimination does not settle alert feasibility.}
Table~\ref{tab:discrimination} summarizes all three splits. Boosting has the highest mean AUROC in A; the GRU has the highest mean AUROC in B. These are descriptive rankings: the seed-specific test populations overlap. Average precision remains low, and the class-weighted models are not calibrated probabilities. Full patient-bootstrap intervals and Brier scores are in the appendix.
\begin{table}[t]
\centering
\caption{Pre-onset discrimination, mean across three seeds. AP denotes average precision. Per-seed 95\% patient-bootstrap intervals appear in Table~\ref{tab:allseeds}; seed averaging is not an independent-cohort meta-analysis.}
\label{tab:discrimination}
\begin{tabular}{lrrrr}\toprule
Model & AUROC A & AUROC B & AP A & AP B\\\midrule''']
for model in names:
    d=m[m.model==model].groupby('site').mean(numeric_only=True)
    lines.append(f"{names[model]} & {d.loc['A','auroc']:.3f} & {d.loc['B','auroc']:.3f} & {d.loc['A','average_precision']:.3f} & {d.loc['B','average_precision']:.3f} \\\\")
lines.append(r'''\bottomrule\end{tabular}\end{table}

\paragraph{The first-alert target is not achieved.}
For every model and seed, the local A and B calibrations certify grid infeasibility at $\alpha=0.05$, for every tested budget from 0.1 to 1 review per patient. There are 90 local calibration/budget outcomes; each certificate retains its stated per-grid confidence interpretation. The result concerns the frozen grids, not all thresholds or all monitoring designs. Increasing review capacity cannot repair a grid whose first-alert timing already violates the risk target.

\begin{figure}[t]
\centering\includegraphics[width=\linewidth]{figs/incident_frontier.pdf}
\caption{\textbf{The tested first-alert grids remain far from the target region.} All three seeds are shown (solid, dashed and dotted), with faint markers for dominated thresholds. Each model has 51 validation-quantile candidates plus endpoints before deduplication. Lines are frontier guides, not attainable interpolations. Shading marks risk $\le0.05$ and workload $\le0.5$. Panels show hospitals A and B.}
\label{fig:frontier}
\end{figure}

Figure~\ref{fig:frontier} also shows the realized test risks. Even the best test-grid point, selected retrospectively only to describe the frontier, misses at least 90.0\% of eligible incidents. This stringent endpoint treats a review just before the six-hour window as a miss, even if it might be useful clinically. The negative result is therefore about timely \emph{first} review under this definition, not about whether early alerts have clinical value.

\paragraph{Policy choice explains the apparent contradiction with utility.}
We additionally choose thresholds by validation challenge utility and freeze them before testing (Table~\ref{tab:policies}). Boosting in A achieves mean utility 0.332 with 0.193 reviews per patient, yet its strict incident missed risk is 0.960. Its three test splits contain 742 eligible incident observations in total, counting overlap across splits: 414 receive an early first alert and 298 receive none before onset. Only 30 receive their first alert in the specified window. The challenge utility credits a broader time window and a persistent positive state; it is not a surrogate for this first-review endpoint.

Repeated alerts recover more incidents but require several reviews per patient. At validation-selected utility thresholds, no model/site/policy combination has all three of positive utility, risk at most 0.05, and workload at most 0.5. This is the empirical answer to the declared joint target, not proof against alternative cooldown or continuing-review policies.
\begin{table}[t]
\centering\small
\caption{Validation-selected operating policies, means over three seeds. ``Repeated'' reviews every above-threshold hour. Utility uses full-stay states; risk and review count use the retrospective pre-onset endpoint. No test metric chooses a threshold.}
\label{tab:policies}
\begin{tabular}{lllrrr}\toprule
Model & Site & Policy & Missed risk & Reviews/patient & Utility\\\midrule''')
for model in names:
    for site in ['A','B']:
        for policy in ['once','hourly']:
            d=s[(s.model==model)&(s.site==site)&(s.policy==policy)].mean(numeric_only=True)
            lines.append(f"{names[model]} & {site} & {'First' if policy=='once' else 'Repeated'} & {d.risk:.3f} & {d.reviews_per_patient:.3f} & {d.challenge_utility:.3f} \\\\")
lines.append(r'''\bottomrule\end{tabular}\end{table}

\paragraph{Recalibration, consent and review.}
Local B calibration contains 230--242 eligible positives, compared with 219--253 in A. None of 14,400 overlapping calibration subsets (25, 50, 100 or 200 positives) certifies the 5\% first-alert risk target. Thus the fraction of test-risk violations \emph{among certified rules} is undefined, not zero. Four hundred positives are unavailable in these calibration pools; the study does not establish how much additional data would suffice. All 72 prespecified group/model/site/seed checks also exclude their tested grids.

Consent interventions do not restore feasibility. They change both scores and the descriptive fallback threshold, so a reduced review count need not be an improvement. For example, GRU opt-out at 50\% per feature group changes mean A missed risk from 0.952 to 0.979 while reviews fall from 0.207 to 0.104 per patient. These are simulated permissions, not observed patient preferences. The estimated-ratio repeated-alert diagnostic has external-site risk from 0.034 to 0.152 across model/seed combinations and carries no exact shift guarantee.

The corrected reviewer audit evaluates 972 queue scenarios on frozen scores. Across all these scenarios, end-to-end missed risk ranges from 0.912 to 0.987; a perfect reviewer cannot recover an incident that never receives a timely review. The simulation is not evidence about real clinician performance. Among 500 random DAGs, 126 contain a source-to-action path and 103 contain a path bypassing the randomly assigned review nodes. This illustrates why review nodes alone do not enforce review, while remaining a synthetic structural test.
''')
Path('revision_results.tex').write_text('\n'.join(lines)+'\n')
lines=[r'''\section{Seed-specific uncertainty and feasibility}
\begin{table}[h]\centering\small
\caption{All-seed pre-onset AUROC with 95\% percentile intervals from 500 whole-patient bootstrap replicates. Brier scores are point estimates; their intervals are released in the machine-readable metrics table. Intervals describe patient-sampling uncertainty conditional on each fitted model.}
\label{tab:allseeds}
\begin{tabular}{llrrrr}\toprule
Model & Seed & AUROC A [95\% CI] & AUROC B [95\% CI] & Brier A & Brier B\\\midrule''']
for model in names:
    for seed in [11,29,47]:
        a=m[(m.model==model)&(m.seed==seed)&(m.site=='A')].iloc[0];b=m[(m.model==model)&(m.seed==seed)&(m.site=='B')].iloc[0]
        lines.append(f"{names[model]} & {seed} & {a.auroc:.3f} [{a.auroc_lower:.3f}, {a.auroc_upper:.3f}] & {b.auroc:.3f} [{b.auroc_lower:.3f}, {b.auroc_upper:.3f}] & {a.brier:.3f} & {b.brier:.3f} \\\\")
lines.append(r'''\bottomrule\end{tabular}\end{table}

\begin{table}[h]\centering\small
\caption{Feasibility of the validation-selected first-alert policy under conditional incident loss. Each row aggregates three seeds: ``Y'' means every seed meets the empirical criterion; ``N'' means none does. Storage and review checks concern the specified graph, not a deployed system. Actual human oversight was not measured.}
\label{tab:feasible}
\begin{tabular}{llccccc}\toprule
Model & Site & Utility $>0$ & Risk $\le .05$ & Reviews $\le .5$ & Storage cut & Review path\\\midrule''')
for model in names:
    for site in ['A','B']:
        d=s[(s.model==model)&(s.site==site)&(s.policy=='once')]
        def yn(v):return 'Y' if v.all() else 'N' if not v.any() else 'Mixed'
        lines.append(f"{names[model]} & {site} & {yn(d.challenge_utility>0)} & {yn(d.risk<=.05)} & {yn(d.reviews_per_patient<=.5)} & Modeled & Modeled \\\\")
lines.append(r'''\bottomrule\end{tabular}\end{table}

\paragraph{Fixed-policy risk intervals.}
The policy audit reports 36 validation-selected operating points with exact pointwise 95\% binomial intervals in \texttt{selected\_policies.csv}. They are not simultaneous across models, sites and seeds. The confidence intervals in that table assess realized test risk; the certificate uses an independent calibration population. No certified policy is available for a certified-policy test-risk distribution.
''')
Path('supplementary_results.tex').write_text('\n'.join(lines)+'\n')
print('Built tables from',len(m),'model/site/seed estimates and',len(s),'fixed policy estimates.')

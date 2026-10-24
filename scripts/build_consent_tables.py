"""Generate the paired-consent appendix table from completed experiment outputs."""
from pathlib import Path
import argparse
import pandas as pd
p=argparse.ArgumentParser();p.add_argument('--results',type=Path,default=Path('results/consent-comparison'));args=p.parse_args()
d=pd.read_csv(args.results/'discrimination.csv');assert len(d)==144
scenarios=['full_input','optout_10','optout_30','optout_50','no_labs','no_vitals','metadata_only','revoke_30_at12']
lines=[r'''\begin{table*}[t]\centering\small\setlength{\tabcolsep}{4pt}
\caption{Mean pre-onset AUROC across three matched patient splits. Denial probabilities apply independently to the lab and vital groups; revocation uses probability 0.3 beginning at hour 12. Model parameters and test populations are unchanged. Across-seed means are descriptive; pointwise paired intervals for every split are released in the comparison CSV and illustrated for source-group restrictions.}
\begin{tabular}{llrrrrrrrr}\toprule
Model & Site & Full & 10\% & 30\% & 50\% & No labs & No vitals & Metadata & Revoke\\\midrule''']
for model,label in [('logistic','Logistic'),('boosting','Boosting'),('gru','GRU')]:
 for site in ['A','B']:
  a=d[(d.model==model)&(d.site==site)].groupby('scenario').auroc.mean()
  lines.append(' & '.join([label,site]+[f'{a[x]:.3f}' for x in scenarios])+r' \\')
lines.append(r'\bottomrule\end{tabular}\end{table*}')
Path('paper_sections/tables/paired_consent.tex').write_text('\n'.join(lines)+'\n')
print('Built paired table from',len(d),'measured comparisons.')

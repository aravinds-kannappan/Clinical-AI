"""Regenerate manuscript tables from saved results without changing prose.

Run from the repository root. Table layouts live in paper_sections/tables/*.tex.in.
"""
import argparse
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, default=Path('results'))
    args = parser.parse_args()
    metrics = pd.read_csv(args.results / 'revision/metrics.csv')
    policies = pd.read_csv(args.results / 'revision-audit/selected_policies.csv')
    names = {'logistic': 'Logistic', 'boosting': 'Boosting', 'gru': 'GRU'}
    rows = {key: [] for key in ('discrimination', 'policies', 'allseeds', 'feasible')}

    def add(table, values):
        rows[table].append(' & '.join(map(str, values)) + r' \\')

    def yn(values):
        return 'Y' if values.all() else 'N' if not values.any() else 'Mixed'

    for model, name in names.items():
        means = metrics[metrics.model == model].groupby('site').mean(numeric_only=True)
        add('discrimination', [name] + [f'{means.loc[site, metric]:.3f}'
            for metric, site in [('auroc', 'A'), ('auroc', 'B'),
                                 ('average_precision', 'A'), ('average_precision', 'B')]])
        for site in ('A', 'B'):
            subset = policies[(policies.model == model) & (policies.site == site)]
            for policy, label in [('once', 'First'), ('hourly', 'Repeated')]:
                mean = subset[subset.policy == policy].mean(numeric_only=True)
                add('policies', [name, site, label, f'{mean.risk:.3f}',
                                f'{mean.reviews_per_patient:.3f}', f'{mean.challenge_utility:.3f}'])
            once = subset[subset.policy == 'once']
            add('feasible', [name, site, yn(once.challenge_utility > 0),
                yn(once.risk <= .05), yn(once.reviews_per_patient <= .5), 'Modeled', 'Modeled'])
        for seed in (11, 29, 47):
            a = metrics[(metrics.model == model) & (metrics.seed == seed) & (metrics.site == 'A')].iloc[0]
            b = metrics[(metrics.model == model) & (metrics.seed == seed) & (metrics.site == 'B')].iloc[0]
            intervals = [f'{x.auroc:.3f} [{x.auroc_lower:.3f}, {x.auroc_upper:.3f}]' for x in (a, b)]
            add('allseeds', [name, seed, *intervals, f'{a.brier:.3f}', f'{b.brier:.3f}'])
    table_dir = Path('paper_sections/tables')
    for key, values in rows.items():
        template = (table_dir / f'{key}.tex.in').read_text()
        assert template.count('{{ROWS}}') == 1
        (table_dir / f'{key}.tex').write_text(template.replace('{{ROWS}}', '\n'.join(values)))
    print(f'Built four tables from {len(metrics)} model/site/seed and {len(policies)} policy estimates.')


if __name__ == '__main__':
    main()

"""Build the static site from checked-in results, without rerunning experiments."""
from pathlib import Path
import argparse, shutil
parser=argparse.ArgumentParser()
parser.add_argument('destination',type=Path)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
dest=args.destination.resolve();dest.mkdir(parents=True,exist_ok=True)
for p in (root/'results').rglob('*'):
    if p.is_file() and p.suffix in {'.html','.md','.csv','.json','.svg','.png','.pdf'}:
        target=dest/p.relative_to(root);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
(dest/'.nojekyll').touch()
(dest/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Consent-constrained clinical AI</title><meta http-equiv="refresh" content="0;url=results/sepsis/index.html"><a href="results/sepsis/index.html">Open interactive research results and discussion</a></html>''')
print(f'Static site: {dest}')

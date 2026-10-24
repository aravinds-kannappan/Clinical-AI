"""Describe the public cohort from the versioned full ZIP; no model evaluation."""
from pathlib import Path
import argparse,csv,io,json,zipfile,hashlib
p=argparse.ArgumentParser();p.add_argument('--archive',default='data/raw/sepsis-public/sepsis-public-full.zip');p.add_argument('--output',default='cohort_statistics.json');a=p.parse_args();archive=Path(a.archive)
stats={site:dict(patients=0,hours=0,event_positive=0,eligible_incident=0,initial_positive=0,onset_censored=0) for site in ['A','B']}
with zipfile.ZipFile(archive) as z:
 for name in z.namelist():
  if not name.endswith('.psv'):continue
  site=name.split('/')[0];rows=list(csv.DictReader(io.StringIO(z.read(name).decode()),delimiter='|'));d=stats[site];n=len(rows);positive=[i for i,r in enumerate(rows) if int(r['SepsisLabel'])==1];d['patients']+=1;d['hours']+=n
  if positive:
   first=positive[0];d['event_positive']+=1;d['initial_positive']+=int(first==0);d['onset_censored']+=int(first+6>=n);d['eligible_incident']+=int(first>0 and first+6<n)
result={'source':str(archive),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'sites':stats,'note':'Descriptive counts from public inputs, not a model experiment.'};Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(stats))

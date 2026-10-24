"""Figures for paired consent comparisons. Read versioned measured CSV files.

Regenerate with: uv run --locked python figs/paired_consent_figures.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
from orx_figstyle import use_style,save,PALETTE
root=Path(__file__).parent
use_style();plt.rcParams.update({'font.size':8,'axes.labelsize':8,'xtick.labelsize':7,'ytick.labelsize':7})
models=[('logistic','Logistic','blue','o'),('boosting','Boosting','orange','s'),('gru','GRU','green','^')]
rates={'full_input':0,'optout_10':.1,'optout_30':.3,'optout_50':.5}
d=pd.read_csv(root/'paired_discrimination.csv');p=pd.read_csv(root/'paired_policies.csv')
assert len(d)==144 and len(p)==288,'Require the complete prespecified comparison, not partial results'

def legend(fig):
 fig.legend(handles=[Line2D([],[],color=PALETTE[c],marker=mk,label=n,markersize=4,lw=1.2) for _,n,c,mk in models],ncol=3,loc='lower center',bbox_to_anchor=(.5,.005),frameon=False,fontsize=8)

fig,axes=plt.subplots(1,2,figsize=(6.75,3.1),sharey=True)
for ax,site,letter in zip(axes,['A','B'],['a','b']):
 for model,label,col,mark in models:
  sub=d[(d.site==site)&(d.model==model)&d.scenario.isin(rates)].copy();sub['rate']=sub.scenario.map(rates);g=sub.groupby('rate').auroc.agg(['mean','min','max']);x=g.index.to_numpy()
  ax.fill_between(x,g['min'],g['max'],color=PALETTE[col],alpha=.12,linewidth=0);ax.plot(x,g['mean'],color=PALETTE[col],marker=mark,lw=1.3,ms=4)
 ax.set(xlim=(-.015,.515),xticks=[0,.1,.3,.5],ylim=(.45,.86),xlabel='Denial probability per feature group');ax.grid(color='#e7e7e7',lw=.6);ax.text(0,1.055,f'({letter}) Hospital {site}',transform=ax.transAxes,fontsize=9)
axes[0].set_ylabel('Pre-onset AUROC (higher is better)');legend(fig);fig.subplots_adjust(left=.10,right=.98,top=.88,bottom=.25,wspace=.16);save(fig,str(root/'paired_discrimination'))

scenarios=[('no_labs','No labs'),('no_vitals','No vitals'),('metadata_only','Metadata only')]
fig,axes=plt.subplots(1,2,figsize=(6.75,4.65),sharex=True,sharey=True)
labels=[]
for row,(model,label,col,mark) in enumerate(models):
 for j,(scenario,short) in enumerate(scenarios):labels.append(f'{label} / {short}')
for ax,site,letter in zip(axes,['A','B'],['a','b']):
 for m,(model,label,col,mark) in enumerate(models):
  for j,(scenario,short) in enumerate(scenarios):
   y=m*3+j
   for k,(seed,mk) in enumerate([(11,'o'),(29,'s'),(47,'^')]):
    r=d[(d.site==site)&(d.model==model)&(d.scenario==scenario)&(d.seed==seed)].iloc[0];yy=y+(k-1)*.19
    ax.plot([100*r.delta_auroc_lower,100*r.delta_auroc_upper],[yy,yy],color=PALETTE[col],lw=.8,alpha=.8);ax.plot(100*r.delta_auroc,yy,marker=mk,color=PALETTE[col],ms=3,linestyle='none')
 ax.axvline(0,color='#68716d',lw=.8,ls='--');ax.set(yticks=range(9),yticklabels=labels,ylim=(8.6,-.6),xlabel='AUROC change (percentage points)');ax.grid(axis='x',color='#e7e7e7',lw=.5);ax.text(0,1.045,f'({letter}) Hospital {site}',transform=ax.transAxes,fontsize=9)
fig.legend(handles=[Line2D([],[],color='#52605a',marker=mk,label=f'Seed {seed}',linestyle='none',ms=4) for seed,mk in [(11,'o'),(29,'s'),(47,'^')]],ncol=3,loc='lower center',frameon=False,fontsize=8)
axes[0].set_ylabel('Model / input restriction',labelpad=6)
fig.subplots_adjust(left=.29,right=.985,top=.91,bottom=.16,wspace=.12);save(fig,str(root/'paired_effects'))

fig,axes=plt.subplots(2,2,figsize=(6.75,4.9),sharex=True,sharey='row')
for col,site in enumerate(['A','B']):
 for row,key in enumerate(['delta_risk','delta_reviews']):
  ax=axes[row,col]
  for model,label,color,mark in models:
   sub=p[(p.site==site)&(p.model==model)&(p.policy=='hourly')&p.scenario.isin(rates)].copy();sub['rate']=sub.scenario.map(rates);scale=100 if key=='delta_risk' else 1;sub['value']=sub[key]*scale;g=sub.groupby('rate').value.agg(['mean','min','max']);x=g.index.to_numpy()
   ax.fill_between(x,g['min'],g['max'],color=PALETTE[color],alpha=.12,linewidth=0);ax.plot(x,g['mean'],color=PALETTE[color],marker=mark,lw=1.2,ms=3.5)
  ax.axhline(0,color='#647169',lw=.7,ls='--');ax.grid(color='#e7e7e7',lw=.5);ax.set(xlim=(-.015,.515),xticks=[0,.1,.3,.5]);ax.text(.01,1.06,f'({"abcd"[row*2+col]}) Hospital {site}',transform=ax.transAxes,fontsize=9)
  if row==1:ax.set_xlabel('Denial probability per feature group')
axes[0,0].set_ylabel('Missed-risk change (percentage points)');axes[1,0].set_ylabel('Review change (reviews/patient)');legend(fig);fig.subplots_adjust(left=.12,right=.985,top=.92,bottom=.16,wspace=.16,hspace=.30);save(fig,str(root/'paired_policy_effects'))

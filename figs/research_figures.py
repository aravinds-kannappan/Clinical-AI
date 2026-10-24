"""Publication figures at 6.75 inches. Inputs are versioned measured CSV snapshots."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from orx_figstyle import use_style,save,PALETTE
root=Path(__file__).parent;use_style();plt.rcParams.update({'font.size':9,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8})
models=[('logistic','Logistic','blue','o'),('boosting','Boosting','orange','s'),('gru','GRU','green','^')]
f=pd.read_csv(root/'frontiers.csv');s=pd.read_csv(root/'selected_policies.csv');consent=pd.read_csv(root/'consent.csv')

def frontier_points(a):
    a=a.sort_values(['reviews_per_patient','conditional_incident_miss']);best=2;keep=[]
    for i,r in a.iterrows():
        if r.conditional_incident_miss<best:best=r.conditional_incident_miss;keep.append(i)
    return a.loc[keep]

fig,axes=plt.subplots(1,2,figsize=(6.75,3.55),sharey=True)
for ax,site,letter in zip(axes,['A','B'],['a','b']):
    zoom=ax.inset_axes([.30,.36,.65,.40]);zoom.set(xlim=(0,.65),ylim=(.89,1.005),xticks=[0,.3,.6],yticks=[.9,.95,1]);zoom.tick_params(labelsize=7,pad=2);zoom.grid(color='#e5e5e5',lw=.5);zoom.set_facecolor('#fff')
    for model,label,col,mark in models:
        for seed,ls in [(11,'-'),(29,'--'),(47,':')]:
            a=f[(f.model==model)&(f.site==site)&(f.seed==seed)&(f.policy=='once')];b=frontier_points(a)
            for axis in [ax,zoom]:
                axis.scatter(a.reviews_per_patient,a.conditional_incident_miss,s=7,color=PALETTE[col],marker=mark,alpha=.14,linewidths=0,zorder=2)
                axis.plot(b.reviews_per_patient,b.conditional_incident_miss,ls,color=PALETTE[col],marker=mark,markersize=2.7,lw=1,zorder=3)
    ax.axhline(.05,color='#a54a35',lw=1,ls='--');ax.axvline(.5,color='#8f9994',lw=.8,ls=':');ax.fill_between([0,.5],0,.05,color='#8cac9d',alpha=.25)
    ax.text(.04,1.055,f'({letter}) Hospital {site}',transform=ax.transAxes,fontsize=10)
    ax.text(.31,.79,'Detail of the upper region',transform=ax.transAxes,fontsize=8,color='#526059')
    ax.text(.04,.12,'Target: risk ≤ 0.05\nBudget: ≤ 0.5 reviews/patient',transform=ax.transAxes,fontsize=8,color='#43554e',linespacing=1.4)
    ax.set(xlim=(0,1),ylim=(0,1.03),xticks=[0,.25,.5,.75,1],yticks=[0,.25,.5,.75,1],xlabel='Reviews per patient (lower is better)');ax.set_xticklabels(['0','.25','.5','.75','1']);ax.grid(axis='y',color='#e8e8e8',lw=.6)
axes[0].set_ylabel('Conditional incident missed risk')
fig.legend(handles=[Line2D([],[],color=PALETTE[c],marker=mk,label=n,markersize=4,lw=1.3) for _,n,c,mk in models],ncol=3,loc='lower center',bbox_to_anchor=(.5,.005),frameon=False)
fig.subplots_adjust(left=.085,right=.985,top=.89,bottom=.23,wspace=.16)
save(fig,str(root/'risk_workload_detailed'))

fig,axes=plt.subplots(1,2,figsize=(6.75,2.8),sharex=True,sharey=True)
colors=[PALETTE['green'],PALETTE['orange'],'#a8b2b7']
for ax,site,letter in zip(axes,['A','B'],['a','b']):
    for row,(model,label,_,_) in enumerate(models):
        a=s[(s.model==model)&(s.site==site)&(s.policy=='once')];n=a.positive_incident_patients
        portions=np.array([(n-a.misses)/n,a.early_first_alerts/n,a.no_preonset_alerts/n]).T*100
        vals=portions.mean(0);left=0
        for value,col in zip(vals,colors):ax.barh(row,value,left=left,height=.5,color=col,edgecolor='white',linewidth=.7);left+=value
        lo,hi=portions[:,0].min(),portions[:,0].max();ax.plot([lo,hi],[row,row],color='#1b3027',lw=1.4);ax.plot([lo,lo],[row-.07,row+.07],color='#1b3027',lw=.7);ax.plot([hi,hi],[row-.07,row+.07],color='#1b3027',lw=.7)
        ax.text(102,row,f'{vals[0]:.1f}%',va='center',fontsize=8)
    ax.set(xlim=(0,118),ylim=(2.65,-.65),xticks=[0,25,50,75,100],yticks=range(3),yticklabels=[x[1] for x in models],xlabel='Eligible incidents (%)');ax.grid(axis='x',color='#eee',lw=.5);ax.set_axisbelow(True);ax.text(0,1.08,f'({letter}) Hospital {site}',transform=ax.transAxes,fontsize=10);ax.text(102,-.62,'Timely',fontsize=7,ha='left')
axes[1].tick_params(labelleft=True)
fig.legend(handles=[Patch(facecolor=colors[i],label=n) for i,n in enumerate(['First alert in window','First alert too early','No pre-onset alert'])],ncol=3,loc='lower center',bbox_to_anchor=(.5,.005),frameon=False,fontsize=8)
fig.subplots_adjust(left=.095,right=.985,top=.83,bottom=.28,wspace=.32)
save(fig,str(root/'first_alert_outcomes'))

fig,axes=plt.subplots(1,2,figsize=(6.75,3.0))
a=consent[(consent.site=='A')&(consent['mode']=='opt_out')]
for model,label,col,mark in models:
    b=a[a.model==model]
    for ax,key in zip(axes,['test_risk','reviews_per_patient']):
        g=b.groupby('optout_rate')[key].agg(['mean','min','max']);x=g.index.to_numpy();ax.fill_between(x,g['min'],g['max'],color=PALETTE[col],alpha=.12,linewidth=0);ax.plot(x,g['mean'],marker=mark,color=PALETTE[col],lw=1.3,markersize=4,label=label)
for ax,letter in zip(axes,['a','b']):
    ax.set(xlim=(-.015,.515),xticks=[0,.1,.3,.5],xlabel='Denial probability per feature group');ax.grid(color='#e8e8e8',lw=.6);ax.text(.02,1.04,f'({letter})',transform=ax.transAxes,fontsize=10)
axes[0].set(ylim=(.88,1.005),ylabel='Conditional incident missed risk')
axes[1].set(ylim=(0,.8),ylabel='Reviews per patient')
fig.legend(handles=[Line2D([],[],color=PALETTE[c],marker=mk,label=n,markersize=4,lw=1.3) for _,n,c,mk in models],ncol=3,loc='lower center',bbox_to_anchor=(.5,0),frameon=False)
fig.subplots_adjust(left=.095,right=.985,top=.92,bottom=.27,wspace=.28)
save(fig,str(root/'consent_cost'))

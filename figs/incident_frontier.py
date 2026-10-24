"""All-seed first-alert frontiers. Run: uv run --locked python figs/incident_frontier.py"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from orx_figstyle import use_style,save,PALETTE
root=Path(__file__).parent;d=pd.read_csv(root/'frontiers.csv');use_style()
fig,axes=plt.subplots(1,2,figsize=(5.5,2.8),sharey=True)
models=[('logistic','blue','o'),('boosting','orange','s'),('gru','green','^')]
for ax,site,label in zip(axes,['A','B'],['(a)','(b)']):
    for model,color,marker in models:
        for seed,ls in [(11,'-'),(29,'--'),(47,':')]:
            a=d[(d.site==site)&(d.model==model)&(d.seed==seed)&(d.policy=='once')].sort_values(['reviews_per_patient','conditional_incident_miss']);best=2;keep=[]
            ax.scatter(a.reviews_per_patient,a.conditional_incident_miss,s=6,marker=marker,color=PALETTE[color],alpha=.15,linewidths=0)
            for i,r in a.iterrows():
                if r.conditional_incident_miss<best:best=r.conditional_incident_miss;keep.append(i)
            a=a.loc[keep];ax.plot(a.reviews_per_patient,a.conditional_incident_miss,ls,color=PALETTE[color],linewidth=.9,marker=marker,markersize=2.3)
    ax.axhline(.05,color='#ad542d',ls='--',lw=.8)
    for k in [.25,.5,.75]:ax.axvline(k,color='#999',ls=':',lw=.6)
    ax.fill_between([0,.5],0,.05,color='#638c65',alpha=.2)
    ax.text(.03,.82,f'{label} Hospital {site}',transform=ax.transAxes,fontsize=8)
    ax.set(xlim=(0,1),ylim=(0,1.03),xticks=[0,.25,.5,.75,1],yticks=[0,.25,.5,.75,1],xlabel='Reviews per patient (lower is better)')
    ax.set_xticklabels(['0','.25','.5','.75','1'])
axes[0].set_ylabel('Incident missed risk (lower is better)')
handles=[Line2D([],[],color=PALETTE[c],marker=m,markersize=3,label=('GRU' if n=='gru' else n.title())) for n,c,m in models]
fig.legend(handles=handles,ncol=3,loc='lower center',bbox_to_anchor=(.5,0),frameon=False,fontsize=8)
fig.subplots_adjust(left=.1,right=.98,top=.97,bottom=.29,wspace=.15)
save(fig,str(root/'incident_frontier'),formats=('pdf','svg'))

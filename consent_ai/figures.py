"""Render actual system graph and measured outputs; no illustrative fake results."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from .orx_figstyle import use_style,save,PALETTE,TEXT

def arrow(ax,a,b,color='#777777',style='-'):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=8,linewidth=.8,color=color,linestyle=style,connectionstyle='arc3,rad=0'))

def diagrams(graphs,out):
    use_style();out=Path(out);out.mkdir(exist_ok=True)
    fig,ax=plt.subplots(figsize=(TEXT,1.65));ax.axis('off');ax.set_xlim(-.6,4.6);ax.set_ylim(-.65,.65)
    labels=['Video / EHR','Consent\ngate','Summary /\nprediction','Pager /\nphysician','Clinical\naction']
    grouping={'video':0,'skeleton':0,'ehr':0,'gate':1,'summary':2,'cache':2,'prediction':2,'pager':3,'physician':3,'action':4}
    g=graphs['consent_and_review'];edges=set((grouping[u],grouping[v]) for u,v in g.edges if u in grouping and v in grouping and grouping[u]!=grouping[v])
    for u,v in sorted(edges):arrow(ax,(u+.4,0),(v-.4,0))
    for x,label in enumerate(labels):
        ax.add_patch(FancyBboxPatch((x-.4,-.22),.8,.44,boxstyle='round,pad=0.02',facecolor='#e6f3fa' if x==1 else '#f5f5f5',edgecolor=PALETTE['blue'] if x==1 else '#555555',linewidth=.8));ax.text(x,0,label,ha='center',va='center',fontsize=7)
    fig.subplots_adjust(left=.025,right=.975,top=.95,bottom=.1);save(fig,str(out/'figure1_pipeline'),formats=('pdf','svg','png'))
    fig,ax=plt.subplots(figsize=(TEXT,5.8));ax.axis('off');ax.set_xlim(-1.75,1.75);ax.set_ylim(-.7,7.7)
    pos={'video':(0,7),'skeleton':(0,6),'gate':(0,5),'summary':(0,4),'prediction':(0,3),'pager':(0,2),'physician':(0,1),'action':(0,0),
         'ehr':(-1.15,5),'cache':(1.15,3.5),'archive':(1.15,6),'profile':(1.15,4.7),'ehr_write':(1.15,1)}
    for u,v in graphs['mandatory_review'].edges:
        allowed=g.has_edge(u,v);a=np.array(pos[u],float);b=np.array(pos[v],float);delta=b-a;dist=np.linalg.norm(delta)
        if dist:
            # Clip to rectangular node boundaries so horizontal arrowheads stay visible.
            unit=delta/dist;offset=min(.47/abs(unit[0]) if unit[0] else float('inf'),.23/abs(unit[1]) if unit[1] else float('inf'))
            arrow(ax,a+unit*offset,b-unit*offset,color=PALETTE['blue'] if allowed else '#bbbbbb',style='-' if allowed else '--')
    for n,(x,y) in pos.items():
        storage=n in ['archive','profile','ehr_write'];label={'ehr':'EHR','ehr_write':'EHR write','pager':'Nurse pager','physician':'Physician review','video':'Video buffer'}.get(n,n.capitalize())
        ax.add_patch(FancyBboxPatch((x-.43,y-.18),.86,.36,boxstyle='round,pad=.03',facecolor='#ffffff' if storage else '#edf5fa',edgecolor='#aaaaaa' if storage else '#35576a',linewidth=.8));ax.text(x,y,label,ha='center',va='center',fontsize=7,color='#777777' if storage else '#17324d')
    fig.subplots_adjust(left=.04,right=.96,top=.98,bottom=.02);save(fig,str(out/'figure2_consent_graph'),formats=('pdf','svg','png'))

def risk_capacity(capacity,queues,out):
    use_style();fig,ax=plt.subplots(figsize=(TEXT,3.1));d=capacity[(capacity.opportunities_per_hour==30)&(capacity.K==10)].sort_values('lambda_value')
    ax.plot(d.lambda_value,d.expected_reviews,'o-',color=PALETTE['blue'],markersize=3,label='Expected reviews')
    ax.axhline(10,color='#777777',linestyle='--',label='K = 10 per hour');ax.set_xlabel('Alert conservativeness, lambda');ax.set_ylabel('Reviews per hour');ax.set_ylim(bottom=0);ax.legend(frameon=False,fontsize=8)
    fig.subplots_adjust(left=.14,right=.97,bottom=.2,top=.96);save(fig,str(Path(out,'capacity_tradeoff')),formats=('pdf','svg','png'))


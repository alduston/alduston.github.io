#!/usr/bin/env python3
"""Regenerate the preliminary two-curve, reconstruction-matched FMNIST figure.

Usage: python tools/plot_fmnist_matched.py
Reads the committed CSV/JSON under assets/data and writes SVG and PNG under assets/img.
Only actual evaluations are plotted; there are no inferred seed bands or extrapolated epochs.
"""
from pathlib import Path
import csv,json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
META=ROOT/'assets/data/fmnist_reconstruction_matched.json'
DATA=ROOT/'assets/data/fmnist_reconstruction_matched.csv'

def main():
    meta=json.loads(META.read_text())
    with DATA.open(newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==10
    assert all(int(r['seed'])==42 for r in rows)
    ref=meta['reconstruction_reference_fid']
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.labelcolor':'#1f2328','text.color':'#1f2328','axes.edgecolor':'#727a82','xtick.color':'#5b636e','ytick.color':'#5b636e','svg.fonttype':'none','figure.facecolor':'white','savefig.facecolor':'white','axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(8.8,5.4))
    fig.text(.10,.94,'Fashion-MNIST · reconstruction-matched comparison',fontsize=16,fontweight='bold',ha='left')
    fig.text(.10,.887,'Same architecture · seed 42 · 10,000 samples · RK4-20',fontsize=10.5,color='#5b636e',ha='left')
    definitions=[('indep_tweedie','Two-stage Tweedie','#16906a','--','^'),('unrouted_csem_a0p5_s42','CSEM co-training · half pressure','#bf5700','-','o')]
    endpoints={}
    for method,label,color,ls,marker in definitions:
        r=sorted([x for x in rows if x['regime']==method],key=lambda x:int(x['epoch']))
        assert [int(x['epoch']) for x in r]==[100,200,300,400,500]
        assert len({x['cfg'] for x in r})==1
        x=[int(x['epoch']) for x in r];y=[float(x['fid_generated']) for x in r]
        assert all(math.isfinite(v) and v>0 for v in y)
        ax.plot(x,y,color=color,ls=ls,marker=marker,ms=6.5,lw=2.3,label=label,markeredgecolor='white',markeredgewidth=.9,zorder=3)
        ax.text(511,y[-1],f'{y[-1]:.3f}',color=color,va='center',fontsize=12,fontweight='semibold')
        endpoints[method]=y[-1]
    ax.axhspan(ref,meta['two_stage_reconstruction_fid'],color='#8e979f',alpha=.13,lw=0)
    ax.axhline(ref,color='#7b858e',ls=(0,(3,3)),lw=1.4)
    ax.text(112,ref+.12,f'Reconstruction reference ≈ 2.3  ({ref:.3f})',fontsize=10,color='#69737c',va='bottom')
    t=endpoints['indep_tweedie'];c=endpoints['unrouted_csem_a0p5_s42']
    ratio=100*(t-c)/(t-ref)
    assert abs(ratio-meta['reduction_in_gap_percent'])<1e-8
    ax.text(120,3.25,f'{ratio:.1f}%',fontsize=25,fontweight='bold',color='#bf5700',va='center')
    ax.text(120,2.90,'smaller generation-FID gap\nabove the reconstruction reference',fontsize=10.5,color='#5b636e',linespacing=1.4,va='center')
    ax.set(xlabel='Prior-training epoch (two-stage) / joint epoch (CSEM)',ylabel='Generation FID · lower is better',xticks=[100,200,300,400,500],yticks=[2.3,3,4,5,6],xlim=(85,555),ylim=(2.10,6.12))
    ax.grid(axis='y',color='#e3e6ea',lw=.75);ax.set_axisbelow(True)
    ax.legend(frameon=False,loc='upper right',fontsize=10,handlelength=2.8)
    fig.text(.10,.035,'Preliminary single-seed result. Fixed CFG: Tweedie 3.0; CSEM 2.0.\nTwo-stage training includes 500 VAE epochs before the 500 prior epochs shown.',fontsize=9,color='#5b636e',linespacing=1.4)
    fig.subplots_adjust(left=.10,right=.95,top=.82,bottom=.19)
    out=ROOT/'assets/img/csem_fid_fmnist_matched'
    fig.savefig(out.with_suffix('.png'),dpi=220)
    fig.savefig(out.with_suffix('.svg'))
    plt.close(fig)
    print(f'Wrote {out.name}.png and .svg; gap reduction {ratio:.6f}%')

if __name__=='__main__':main()

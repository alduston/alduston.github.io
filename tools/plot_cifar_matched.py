#!/usr/bin/env python3
"""Regenerate the CIFAR comparison from committed, measured seed-level data."""
from pathlib import Path
import csv
import json
import statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "assets/data/cifar_matched.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
meta = json.loads((ROOT / "assets/data/cifar_matched.json").read_text())
assert len(rows) == 64 and meta["seeds"] == [42, 43]
epochs = np.arange(50, 801, 50)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,
                     "axes.spines.top":False,"axes.spines.right":False,
                     "svg.fonttype":"path","figure.facecolor":"white"})
fig, ax = plt.subplots(figsize=(8.8,5.4))
fig.text(.115,.94,"CIFAR-10 · generation FID",fontsize=16,fontweight="bold")
fig.text(.115,.887,"Same architecture · seeds 42–43 · 10,000 samples · RK4-20",
         fontsize=10.5,color="#5b636e")
for method,label,color in [
    ("csem","CSEM co-training","#1565a5"),
    ("tweedie","Two-stage Tweedie (β=0.03)","#c86a25")]:
    by_seed = []
    for seed in meta["seeds"]:
        r = sorted((v for v in rows if v["regime"] == method and int(v["seed"]) == seed),
                   key=lambda v:int(v["epoch"]))
        assert [int(v["epoch"]) for v in r] == list(epochs)
        assert all(float(v["cfg"]) == meta["curve_cfg"] for v in r)
        by_seed.append([float(v["fid_generated"]) for v in r])
    values=np.asarray(by_seed)
    mu,sd=values.mean(axis=0),values.std(axis=0,ddof=1)
    ax.plot(epochs,mu,marker="o",ms=4.5,lw=2.2,color=color,label=label)
    ax.fill_between(epochs,mu-sd,mu+sd,color=color,alpha=.12,lw=0)
    ax.annotate(f"{mu[-1]:.2f}",(800,mu[-1]),xytext=(7,0),textcoords="offset points",
                va="center",color=color,fontweight="semibold")
    if method == "tweedie":
        endpoint=meta["regimes"][method]["mean_final_fid"]
        ax.axhline(endpoint,color=color,ls=":",lw=1,alpha=.55)
        ax.scatter([800],[endpoint],marker="D",s=48,facecolors="white",
                   edgecolors=color,linewidths=1.6,zorder=5,
                   label=f"Tweedie optimized final: {endpoint:.2f}")
    else:
        assert abs(mu[-1]-meta["regimes"][method]["mean_final_fid"])<1e-12
ticks = [8,10,12,15,20,30,50,70,90]
ax.set_yscale("log")
ax.set(xlim=(35,865),ylim=(7.6,100),xlabel="Prior-training epoch / joint epoch",
       ylabel="Generation FID (log scale)",xticks=list(range(100,801,100)))
ax.yaxis.set_major_locator(FixedLocator(ticks))
ax.yaxis.set_major_formatter(FixedFormatter([str(t) for t in ticks]))
ax.yaxis.set_minor_locator(NullLocator())
ax.grid(axis="y",color="#e4e7ea",lw=.75)
ax.legend(loc="upper right",frameon=False,fontsize=10)
fig.text(.115,.048,"Fixed CFG 2.5; curves show mean ± 1 sample SD. Diamond: final CFG 3.0.\n"
         "Two-stage training includes 800 VAE-pretraining epochs before the epochs shown.",
         fontsize=9,color="#5b636e",linespacing=1.4)
fig.subplots_adjust(left=.115,right=.96,top=.82,bottom=.20)
out=ROOT/"assets/img/csem_fid_cifar_matched"
fig.savefig(out.with_suffix(".png"),dpi=220)
fig.savefig(out.with_suffix(".svg"))
plt.close(fig)

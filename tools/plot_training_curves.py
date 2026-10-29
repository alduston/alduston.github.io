#!/usr/bin/env python3
"""Plot a metric (e.g. FID) against training epoch for the CSEM comparison, in the site's style.

Input: a long-format CSV with one row per (regime, seed, epoch):

    regime,seed,epoch,fid
    cotrained_csem,0,80,6.03
    cotrained_csem,1,80,6.11
    indep_csem,0,80,7.44
    indep_tweedie,0,80,7.65
    ...

Regime names are mapped to labels/colors below; unknown regimes are skipped with a warning.
With two or more seeds per point, the line is the mean and the band is a 95% t-interval of the
mean (or +/- one standard deviation with --band sd). With one seed, no band is drawn.

Usage:
    python tools/plot_training_curves.py runs_fmnist.csv assets/img/csem_fid_fmnist \
        --metric fid --ylabel "FID (lower is better)"

Writes <out>.svg and <out>.png (2x). The page references the .png by default.
"""
import argparse
import csv
import math
import sys
from collections import defaultdict

import logging
import matplotlib
matplotlib.use("Agg")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy

# Fixed order and colors (validated for colour-vision deficiency with the site's white surface).
# Line style and marker are a second encoding, so identity never rests on colour alone.
REGIMES = [
    ("cotrained_csem", "Co-trained, CSEM",            "#bf5700", "-",  "o"),
    ("indep_csem",     "Two-stage, CSEM target",      "#1f5a96", "--", "s"),
    ("indep_tweedie",  "Two-stage, denoising target", "#16906a", "--", "^"),
]
TEXT, MUTED, GRID = "#1f2328", "#5b636e", "#e3e6ea"

# Two-sided 97.5% Student-t quantiles for small seed counts (df = n - 1).
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262}


def summarize(values, band):
    n = len(values)
    mean = sum(values) / n
    if n < 2:
        return mean, None
    sd = math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1))
    half = sd if band == "sd" else T975.get(n - 1, 1.96) * sd / math.sqrt(n)
    return mean, half


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("out", help="output path without extension")
    ap.add_argument("--metric", default="fid")
    ap.add_argument("--ylabel", default="FID (lower is better)")
    ap.add_argument("--xlabel", default="Prior-training epoch")
    ap.add_argument("--title", default=None)
    ap.add_argument("--band", choices=["ci95", "sd"], default="ci95")
    ap.add_argument("--width", type=float, default=6.4)
    ap.add_argument("--height", type=float, default=4.2)
    args = ap.parse_args()

    data = defaultdict(lambda: defaultdict(list))  # regime -> epoch -> [values]
    with open(args.csv, newline="") as f:
        for row in csv.DictReader(f):
            data[row["regime"].strip()][float(row["epoch"])].append(float(row[args.metric]))

    known = {r[0] for r in REGIMES}
    for r in data:
        if r not in known:
            print(f"warning: skipping unknown regime '{r}'", file=sys.stderr)

    plt.rcParams.update({
        "font.family": ["Source Sans 3", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 11, "axes.edgecolor": MUTED, "axes.labelcolor": TEXT,
        "xtick.color": MUTED, "ytick.color": MUTED, "svg.fonttype": "none",
    })
    fig, ax = plt.subplots(figsize=(args.width, args.height))
    ends = []
    for key, label, color, ls, marker in REGIMES:
        if key not in data:
            continue
        epochs = sorted(data[key])
        stats = [summarize(data[key][e], args.band) for e in epochs]
        means = [m for m, _ in stats]
        if all(h is not None for _, h in stats):
            lo = [m - h for m, h in stats]
            hi = [m + h for m, h in stats]
            ax.fill_between(epochs, lo, hi, color=color, alpha=0.14, linewidth=0)
        ax.plot(epochs, means, ls, color=color, linewidth=2, marker=marker, markersize=6.5,
                markeredgecolor="white", markeredgewidth=1.2, label=label, zorder=3)
        ends.append((epochs[-1], means[-1]))

    # Direct label: final mean value at the end of each line, in text ink (not series colour),
    # nudged apart when two end values are close.
    lo_y, hi_y = ax.get_ylim()
    min_gap = 0.055 * (hi_y - lo_y)
    shifted = offset_copy(ax.transData, fig=fig, x=9, y=0, units="points")
    placed = []
    for x, y in sorted(ends, key=lambda p: p[1]):
        ty = y if not placed or y - placed[-1] >= min_gap else placed[-1] + min_gap
        placed.append(ty)
        ax.text(x, ty, f"{y:.2f}", transform=shifted, va="center", ha="left",
                fontsize=10.5, color=TEXT)

    ax.set_xlabel(args.xlabel)
    ax.set_ylabel(args.ylabel)
    if args.title:
        ax.set_title(args.title, loc="left", fontsize=12, color=TEXT, fontweight="semibold")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.margins(x=0.08)
    ax.legend(frameon=False, loc="upper right", fontsize=10.5, handlelength=2.6)
    fig.tight_layout()
    fig.savefig(args.out + ".svg")
    fig.savefig(args.out + ".png", dpi=200)
    print("wrote", args.out + ".svg", "and", args.out + ".png")


if __name__ == "__main__":
    main()

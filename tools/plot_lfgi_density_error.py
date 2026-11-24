#!/usr/bin/env python3
"""Regenerate assets/img/lfgi_density_error.png from assets/data/lfgi_acoustic_density_grid.npz.

The data file holds, on a 2 cm grid over the two-microphone source-localization posterior
(LFGI manuscript, acoustic application, bank seed 22003, N = 450), the exact log posterior
density and the log densities of four surrogates: the frozen probability flows of the LFGI-GN,
DPSMC-gate and Tweedie score estimates, and the BIC-selected Gaussian mixture fitted to the same
450 posterior samples. Log densities are in whitened coordinates; the figure converts them to
densities per square metre.

Every panel shows densities averaged over CELL x CELL blocks of the grid (6 cm cells), so each
pixel compares the mass that each density puts in that cell. Smooth densities are averaged from
the grid values. Tweedie's flow density is a Gaussian kernel density on the samples with a 2 mm
bandwidth, far below the grid spacing, so its cell masses are computed exactly from the kernels.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from scipy.special import logsumexp, log_ndtr

ROOT = Path(__file__).resolve().parents[1]
d = np.load(ROOT / "assets/data/lfgi_acoustic_density_grid.npz")

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["STIXGeneral"], "mathtext.fontset": "stix",
    "font.size": 12, "axes.titlesize": 13.5, "axes.labelsize": 12,
    "xtick.labelsize": 11, "ytick.labelsize": 11, "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5, "savefig.facecolor": "white",
})
INK, MUTED, RULE = "#1f2328", "#5b636e", "#9aa1a9"

CELL = 3                                   # grid points per cell side: 6 cm cells
h0 = float(d["h"])
n2, n1 = (len(d["l2"]) // CELL) * CELL, (len(d["l1"]) // CELL) * CELL


def cell_log_mean(lq):
    """Log of the mean density over each CELL x CELL block of grid points."""
    a = lq[:n2, :n1].astype(float).reshape(n2 // CELL, CELL, n1 // CELL, CELL)
    return logsumexp(a, axis=(1, 3)) - 2 * np.log(CELL)


def tweedie_cell_log_density():
    """Exact log mean density per cell of the Gaussian kernel density that Tweedie's flow produces."""
    tau = float(d["tau"]); a = np.exp(-tau); sd = np.sqrt(-np.expm1(-2 * tau))
    c, s = d["center"], d["scale"]; x = d["bank"].astype(float)
    g1, g2 = d["l1"].astype(float), d["l2"].astype(float)
    e1 = (np.r_[g1[:n1:CELL] - h0 / 2, g1[n1 - 1] + h0 / 2] - c[0]) / s[0]
    e2 = (np.r_[g2[:n2:CELL] - h0 / 2, g2[n2 - 1] + h0 / 2] - c[1]) / s[1]

    def log_interval(lo, hi):                 # log(Phi(hi) - Phi(lo)) without underflow
        upper = hi <= 0
        p = np.where(upper, log_ndtr(hi), log_ndtr(-lo)); q = np.where(upper, log_ndtr(lo), log_ndtr(-hi))
        return p + np.log1p(-np.exp(q - p))

    z1 = (e1[None] - a * x[:, :1]) / sd; z2 = (e2[None] - a * x[:, 1:]) / sd
    m1 = log_interval(z1[:, :-1], z1[:, 1:]); m2 = log_interval(z2[:, :-1], z2[:, 1:])
    logmass = logsumexp(m2[:, :, None] + m1[:, None, :], axis=0) - np.log(len(x))
    return logmass - np.log(np.diff(e1)[None, :] * np.diff(e2)[:, None])


logp = cell_log_mean(d["logp"])
logq = {k: cell_log_mean(d[f"logq_{k}"]) for k in ["lfgi", "dpsmc", "gmm"]}
logq["tweedie"] = tweedie_cell_log_density()
l1 = d["l1"][:n1].astype(float).reshape(-1, CELL).mean(1)
l2 = d["l2"][:n2].astype(float).reshape(-1, CELL).mean(1)
h = h0 * CELL
ext = [l1[0] - h / 2, l1[-1] + h / 2, l2[0] - h / 2, l2[-1] + h / 2]
dens = np.exp(logp + float(d["logjac"]))
v = np.sort(dens.ravel())[::-1]
inside = dens >= v[np.searchsorted(np.cumsum(v) / v.sum(), 0.999)]
# Surrogate flows were evaluated on the grid's 99.9% region plus a margin; keep fully evaluated cells.
inside &= d["evaluated"][:n2, :n1].reshape(n2 // CELL, CELL, n1 // CELL, CELL).all(axis=(1, 3))
w = np.where(inside, dens, 0.0)


def hdr(masses):
    v = np.sort(dens.ravel())[::-1]
    c = np.cumsum(v) / v.sum()
    return sorted(v[np.searchsorted(c, m)] for m in masses)


core = hdr([0.5, 0.9])
edge = hdr([0.999])
rec, truth = d["receivers"], d["truth"]

ERR_X = (0.0, 4.9)
YL = (-4.4, 5.9)
FULL_X = (-1.7, 4.9)
LIM = 2.0
panels = [("lfgi", "LFGI"), ("dpsmc", "DPSMC gate"), ("tweedie", "Tweedie"),
          ("gmm", "Gaussian mixture")]

# Place axes explicitly so every panel shares one height and one metre-to-inch scale.
W, LM, RM, GAP0, GAP = 8.8, 0.48, 0.06, 0.18, 0.10
TOP, XLAB, CBGAP, CBH, CBLAB, BOT = 0.33, 0.47, 0.17, 0.12, 0.45, 0.04
widths = [FULL_X[1] - FULL_X[0]] + [ERR_X[1] - ERR_X[0]] * len(panels)
scale = (W - LM - RM - GAP0 - GAP * (len(panels) - 1)) / sum(widths)
PH = (YL[1] - YL[0]) * scale
H = TOP + PH + XLAB + CBGAP + CBH + CBLAB + BOT
fig = plt.figure(figsize=(W, H))
lefts, x0 = [], LM
for i, wd in enumerate(widths):
    lefts.append(x0); x0 += wd * scale + (GAP0 if i == 0 else GAP)
pb = BOT + CBLAB + CBH + CBGAP + XLAB


def box(i):
    return [lefts[i] / W, pb / H, widths[i] * scale / W, PH / H]


def cbox(x_from, x_to):
    return [x_from / W, (BOT + CBLAB) / H, (x_to - x_from) / W, CBH / H]


def frame(ax, xlim):
    ax.set_xticks([0, 2, 4] if xlim[0] > -1 else [-1, 0, 1, 2, 3, 4])
    ax.set_yticks([-4, -2, 0, 2, 4])
    ax.set_xlim(*xlim); ax.set_ylim(*YL); ax.set_aspect("equal")
    ax.set_xlabel("x (m)", labelpad=1)
    for s in ax.spines.values():
        s.set_color(RULE)


# Exact posterior density.
ax0 = fig.add_axes(box(0))
cmap = plt.get_cmap("magma_r").copy(); cmap.set_under("white")
dn = LogNorm(vmin=dens.max() * 1e-4, vmax=dens.max())
im0 = ax0.imshow(np.clip(dens, dn.vmin * 0.999, None), origin="lower", extent=ext, cmap=cmap,
                 norm=dn, interpolation="bilinear", rasterized=True)
ax0.plot(rec[:, 0], rec[:, 1], "v", ms=6.5, color=INK, mec="white", mew=0.7, zorder=5)
for (rx, ry), lab, dx in zip(rec, ["mic 1", "mic 2"], [0.18, 0.2]):
    ax0.text(rx + dx, ry - 0.08, lab, fontsize=10.5, color=INK, va="top")
ax0.plot(*truth, "*", ms=11, color="#2a9d8f", mec="white", mew=0.7, zorder=6)
ax0.text(truth[0] - 0.22, truth[1] + 0.22, "true\nsource", fontsize=10.5, color=INK, ha="right", va="bottom",
         linespacing=0.95)
frame(ax0, FULL_X)
ax0.set_ylabel("y (m)", labelpad=1)
ax0.set_title("Exact posterior", pad=5)

# Pointwise log-density error of each surrogate.
en = Normalize(-LIM, LIM)
ecmap = plt.get_cmap("RdBu_r")
axes = []
for k, (key, title) in enumerate(panels):
    ax = fig.add_axes(box(k + 1))
    err = logq[key] - logp
    shown = np.ma.array(np.clip(err, -LIM, LIM), mask=~inside)
    im = ax.imshow(shown, origin="lower", extent=ext, cmap=ecmap, norm=en, interpolation="nearest",
                   rasterized=True)
    ax.contour(l1, l2, dens, levels=edge, colors=RULE, linewidths=0.7)
    ax.contour(l1, l2, dens, levels=core, colors=INK, linewidths=0.45, alpha=0.55)
    if key == "tweedie":
        ax.text(0.04, 0.015, "mass collapses\nonto the samples", transform=ax.transAxes, ha="left",
                va="bottom", fontsize=10, color=MUTED, linespacing=1.0)
    rms = np.sqrt(np.sum(w[inside] * err[inside] ** 2) / w.sum())
    txt = f"{rms:.2f}" if rms < 10 else f"{rms:,.0f}"
    ax.text(0.97, 0.985, f"RMS error\n{txt} nats", transform=ax.transAxes, ha="right", va="top",
            fontsize=11, color=INK, linespacing=1.0)
    frame(ax, ERR_X)
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.set_title(title, pad=5)
    axes.append(ax)

# Colour keys below the panels.
c0 = fig.add_axes(cbox(lefts[0] + 0.25, lefts[0] + widths[0] * scale - 0.25))
cb0 = fig.colorbar(im0, cax=c0, orientation="horizontal")
cb0.set_ticks([1e-3, 1e-2, 1e-1, 1])
cb0.set_ticklabels(["$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "1"])
cb0.set_label("density (m$^{-2}$)", labelpad=1)
cb0.outline.set_edgecolor(RULE); cb0.ax.tick_params(labelsize=10.5, length=2); cb0.ax.minorticks_off()

c1 = fig.add_axes(cbox(lefts[2], lefts[3] + widths[3] * scale))
cb1 = fig.colorbar(im, cax=c1, orientation="horizontal", extend="both", extendfrac=0.04)
cb1.set_ticks([-2, -1, 0, 1, 2])
cb1.set_label(r"$\log q-\log p$ (nats)", labelpad=1)
cb1.outline.set_edgecolor(RULE); cb1.ax.tick_params(labelsize=10.5, length=2)
c1.text(-0.075, 0.5, "too little\nmass", transform=c1.transAxes, ha="right", va="center", fontsize=10.5,
        color=MUTED, linespacing=0.95)
c1.text(1.075, 0.5, "too much\nmass", transform=c1.transAxes, ha="left", va="center", fontsize=10.5,
        color=MUTED, linespacing=0.95)

out = ROOT / "assets/img/lfgi_density_error.png"
fig.savefig(out, dpi=200)
print("wrote", out)

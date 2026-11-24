#!/usr/bin/env python3
"""Compute assets/data/lfgi_acoustic_density_grid.npz (input to plot_lfgi_density_error.py).

Needs the LFGI full project: extract Code/RunBundles/Acoustic2D_S2_20261119.zip and compile
acoustic2d_supplement/code/fast_field.cpp to libfast_field.so next to it. The frozen
supplement-stage code (fields, flows, target, mixtures, fast_field) is used unchanged, with the
manuscript display bank (seed 22003, N = 450), endpoint tau, horizon T and DOP853 tolerances.

LFGI-GN and DPSMC gate: frozen probability flow, integrated. Tweedie: its score is the exact score
of the OU-smoothed empirical law of the bank, so its flow density at tau is the Gaussian kernel
density with centres exp(-tau) x_i and variance 1 - exp(-2 tau), up to the O(e^-T) terminal
mismatch. On 11,424 grid points the integrated Tweedie flow matched this closed form to 0.13 nats
(median 0.018); integrating it everywhere takes over an hour because of basin switching near t = 0.

Usage: python -I compute_lfgi_density_grid.py <acoustic2d_supplement dir> <out.npz> <cache dir> [spacing_m]
About 5 minutes on two cores.
"""
import sys, time, json
from pathlib import Path
import numpy as np

stage = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
cache = Path(sys.argv[3])
h = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
sys.path.insert(0, str(stage / 'code'))

from flows import integrate                     # noqa: E402
from fields import Bank                        # noqa: E402
from scipy.special import logsumexp            # noqa: E402
from target import AcousticIP                  # noqa: E402
from mixtures import select_gmm                # noqa: E402

cfg = json.loads((stage / 'configs/campaign.json').read_text())
tgt = AcousticIP()
tau = min(cfg['tau_cap'], float(.5 * np.log1p(.01 / tgt.gn_upper)))
solver = dict(tau=tau, T=cfg['T'], rtol=cfg['rtol'], atol=cfg['atol'], chunk=cfg['chunk'],
              scalar_ridge=cfg['scalar_ridge'])
logZ = json.loads((stage / 'reference/quadrature.json').read_text())['logZ']
seed, N = 22003, 450
b = np.load(stage / f'prepared/seed{seed}.npz')
x, s, P = b['x'][:N], b['s'][:N], b['P'][:N]

# Grid in metres, whitened x = (ell - center) / scale.
l1 = np.arange(-1.7, 4.9 + 1e-9, h)
l2 = np.arange(-4.4, 5.9 + 1e-9, h)
L1, L2 = np.meshgrid(l1, l2)
ell = np.column_stack([L1.ravel(), L2.ravel()])
xg = (ell - tgt.center) / tgt.scale
logjac = -np.log(tgt.scale).sum()
logp = tgt.logp(xg) - logZ
dens = np.exp(logp + logjac)

v = np.sort(dens)[::-1]; cm = np.cumsum(v) / v.sum()
thr999 = v[np.searchsorted(cm, 0.999)]
inside = (dens >= thr999).reshape(L1.shape)
# Evaluate the flows on the 99.9% region dilated by two cells so the masked edge is clean.
ev = inside.copy()
for _ in range(2):
    e2 = ev.copy(); e2[1:] |= ev[:-1]; e2[:-1] |= ev[1:]; e2[:, 1:] |= ev[:, :-1]; e2[:, :-1] |= ev[:, 1:]; ev = e2
idx = np.flatnonzero(ev.ravel())
print(f'grid {L1.shape}, window mass {dens.sum()*h*h:.5f}, evaluating {len(idx)} points', flush=True)

res = dict(l1=l1, l2=l2, h=h, logp=logp.reshape(L1.shape), logjac=logjac, inside999=inside, evaluated=ev,
           receivers=tgt.receivers, truth=tgt.truth, center=tgt.center, scale=tgt.scale, logZ=logZ,
           tau=tau, T=cfg['T'], seed=seed, N=N, bank=x)
banks = {'lfgi': Bank(x, s, P),
         'dpsmc': Bank(x, s, np.broadcast_to(s.T @ s / N, P.shape).copy())}
for name, bank in banks.items():
    tick = time.time()
    z, Ld, calls = integrate(bank, xg[idx], 'lfgi', False, solver, str(cache / f'cache_final_{name}_h{h}'), f'final{h}')
    full = np.full(len(xg), np.nan)
    full[idx] = -.5 * (z * z).sum(1) - np.log(2 * np.pi) + Ld
    res[f'logq_{name}'] = full.reshape(L1.shape)
    print(f'{name}: {time.time()-tick:.0f}s', flush=True)

a_t, g_t = np.exp(-tau), -np.expm1(-2 * tau)
full = np.full(len(xg), np.nan)
full[idx] = np.concatenate([logsumexp(-((c[:, None] - a_t * x[None]) ** 2).sum(2) / (2 * g_t), axis=1)
                            for c in np.array_split(xg[idx], 64)]) - np.log(N) - np.log(2 * np.pi * g_t)
res['logq_tweedie'] = full.reshape(L1.shape)

g, info = select_gmm(x, cfg['gmm_K'], 50000 + seed)
res['logq_gmm'] = np.where(ev.ravel(), g.logq(xg), np.nan).reshape(L1.shape)
res['gmm_K'] = info['K']

site = {k: np.asarray(res[k], dtype=np.float32) for k in ['l1', 'l2', 'logp', 'logq_lfgi', 'logq_dpsmc', 'logq_tweedie', 'logq_gmm', 'bank']}
for k in ['h', 'logjac', 'logZ', 'tau', 'T', 'seed', 'N', 'gmm_K', 'inside999', 'evaluated', 'receivers', 'truth', 'center', 'scale']:
    site[k] = res[k]
site['provenance'] = np.array(json.dumps(dict(
    source='LFGI manuscript, acoustic two-microphone application (Online Appendix 1); frozen supplement-stage code from Code/RunBundles/Acoustic2D_S2_20261119.zip',
    bank='prepared/seed22003.npz, first 450 states (the manuscript display bank)',
    flows='LFGI-GN and DPSMC gate (unweighted clean-score second moment): frozen probability flow integrated with DOP853, rtol 1e-8, atol 1e-10 on log time, tau and T from configs/campaign.json, N(0,I) terminal density',
    tweedie='Tweedie score equals the exact score of the OU-smoothed empirical law of the bank, so its flow density at tau is the Gaussian kernel density with centres exp(-tau) x_i and variance 1-exp(-2 tau), up to the terminal mismatch at T; checked against the integrated flow on 11,424 grid points: max difference 0.13 nats, median 0.018',
    gmm='mixtures.select_gmm, K from {1,2,4,8} by bank-only BIC, seed 72003',
    exact='closed-form unnormalized posterior minus quadrature logZ (reference/quadrature.json)',
    coordinates='log densities are per whitened unit; add logjac for per square metre',
    region='inside999 = exact posterior highest-density region holding 99.9% of the mass; flows evaluated on it dilated by two cells')))
np.savez_compressed(out, **site)
print('saved', out, 'GMM K =', info['K'])

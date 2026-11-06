# alduston.github.io

Personal academic website. Plain HTML/CSS, no build step.

## Publish on GitHub Pages

Replace the repository contents with this folder (keep `.nojekyll`), commit, and push to `main`.
Pages deploys from `main`, folder `/ (root)`; the site updates at https://alduston.github.io within a
minute or two.

Copying this folder over the old checkout does not delete files that are no longer here. Delete
these from the repository explicitly (`git rm`):

- the stale nested copy of the site in `alduston.github.io/` and the root-level `style.css`
  (every page loads `assets/style.css`);
- retired figures in `assets/img/`, if present: `gad_darcy.png`, `gad_ess.png`,
  `gad_navier_stokes.png`, `gad_ns_pca.png`, `gad_acoustic_geometry.png`, `gad_gate_ablation.png`,
  `gad_mode_separation.png`, `gad_2d_benchmarks.png`, `lfgi_gate.png`, `lfgi_funnel_samples.png`,
  `lfgi_gmm24_samples.png`, `lfgi_score_rmse_sweep.png`, `lfgi_gate_error_t04.png`,
  `lfgi_gate_error_t08.png`, `lfgi_gate_error_t16.png`, and `tsi_blend.png`.

## Structure

```
index.html        Home: bio, internship note, featured CSEM block, other projects, news
research.html     One section per project (CSEM first), figures, results, protocol notes
papers.html       Preprints and manuscripts in preparation, with BibTeX
cv.html           HTML CV (mirrors assets/Alois_Duston_CV.pdf)
assets/style.css
assets/img/       Figures, diagram, social preview card, portrait
tools/            plot_training_curves.py (regenerates the CSEM results figure)
```

## Updating the CSEM results when the new runs finish

The CIFAR-10 numbers come from the current runs. The Fashion-MNIST figure and numbers come from the
earlier training configuration and are waiting on the architecture-matched audit.

1. Export the Fashion-MNIST runs to a long CSV, one row per regime, seed, and epoch:
   `regime,seed,epoch,fid`, where regime is `cotrained_csem`, `indep_csem`, or `indep_tweedie`.
2. Regenerate the figure in site style, with a 95% band over seeds:
   ```
   python tools/plot_training_curves.py runs_fmnist.csv assets/img/csem_fid_fmnist
   ```
   This overwrites `csem_fid_fmnist.png` and writes an `.svg` alongside it. The new figure uses
   orange for co-trained CSEM, blue for two-stage with the CSEM target, and green for two-stage with
   the denoising target, so update the colour words in the figure caption in `research.html`.
3. Update the three stat tiles, which appear identically in `research.html#csem` and `index.html`,
   and the Fashion-MNIST sentence beside the figure in `research.html#csem`.
4. Once the CSEM repository has a project-specific README, uncomment the `code` link in the CSEM
   `meta` line of `research.html`.

## Figures

- `csem_cotraining.svg`: architecture diagram drawn for the site. Its fonts are embedded and
  subset, so it renders the same inside `<img>` on every platform. Plain-text label edits work,
  but characters that were not in the original labels fall back to system fonts.
- `og_card.png`: the 1200×630 preview image that appears when the site is linked on LinkedIn,
  Slack, or email. It is a render of the diagram. Regenerate it if the diagram changes.
- `csem_fid_fmnist.png`: placeholder Fashion-MNIST FID curve (see above).
Each project section is a short pitch: a few plain-language points, one or two figures from the
paper, and a sentence of headline results. Detailed tables stay in the papers.

- `gad_*.png` come from the GAD manuscript (draft of 5 Nov 2026), Overleaf `Figures/`, rasterized
  at 1760 px wide (2× the 880 px column):
  - `gad_1d_progression.png`: Fig. 1, `gad_1d_progression.png` (footer line cropped, background white).
  - `gad_quake_geometry.png`: Fig. 6, `InverseRefactor/quake_geometry.pdf`.
  - `gad_accuracy_vs_requests.png`: Fig. 7, `InverseRefactor/inverse_accuracy_vs_requests.pdf`.
  - `gad_thumb.png`: the E2 row of Fig. 6 (NUTS reference, annealed GN-GAD), redrawn from
    `InverseRefactor/plot_data/quake_geometry.npz` with the manuscript's bins and colors, no axis text.
- `lfgi_*.png` come from the LFGI manuscript (draft of 6 Nov 2026), Overleaf `Figs/`:
  - `lfgi_gmm8_samples.png`: Fig. 2, `gmm8_heatmap.png`, re-tiled from one row of seven panels into
    rows of four and three (same panels, order, and axes; figure-wide title dropped).
  - `lfgi_darcy_density.png`: Fig. 5, `darcy_density_array.png`, left-column panels for LFGI, Tweedie,
    and MAP–Laplace placed side by side. Fig. 5 mislabels some of its other rows; those are not used.
  - `lfgi_thumb.png`: Fig. 2 plot areas, Tweedie beside LFGI, no axis text.
- `tsi_*.png` come from the TSI paper (`Paper/Paper_Figures/` in the SISC project):
  - `tsi_helix_samples.png`: the 9-D helix comparison, `5way.png`.
  - `tsi_ns_posterior.png`: the Navier–Stokes posterior histograms, `NShists2.png`.
  - `tsi_thumb.png`: top-row plot areas of `5way.png`, Tweedie beside Blend, no axis text.

## Common edits

- **Internship note:** the `seeking` paragraph on `index.html`. Remove it when the search is done.
- **New paper:** copy a `<div class="pub">…</div>` block in `papers.html`. When a manuscript
  becomes a preprint, change its tag on `research.html` and `index.html` to
  `<span class="tag preprint">Preprint</span>`.
- **News:** add an `<li>` at the top of the News list in `index.html`.
- **PDF CV:** replace `assets/Alois_Duston_CV.pdf`. The home page and the CV page both link to it.

## Open items

- Author list for the CSEM technical report (`papers.html`).
- `assets/Alois_Duston_CV.pdf` still has the old GAD bullet (Darcy and Navier–Stokes). Regenerate
  it from the CV source with the bullet now on `cv.html`.

# alduston.github.io

Personal academic website. Plain HTML/CSS, no build step.

## Publish on GitHub Pages

Copy these updated files into the repository root, preserving their relative paths and the other
repository files (including `.nojekyll`), then commit and push to `main`.
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

## Current Fashion-MNIST comparison (16 November 2026)

The homepage and research page use the preliminary seed-42, reconstruction-matched comparison:

| Method | Fixed CFG | Epoch-500 generation FID | Posterior reconstruction FID |
|---|---:|---:|---:|
| Two-stage Tweedie, beta0=0.03 | 3.0 | 4.454898680734743 | 2.3779708339246213 |
| Unrouted half-pressure CSEM co-training | 2.0 | 4.059284854396196 | 2.31571040014029 |

The 18.5% headline measures the reduction in the generation-FID gap above the measured CSEM
reconstruction reference: `(FID_Tweedie - FID_CSEM) / (FID_Tweedie - 2.31571040014029)`.
Reconstruction is an empirical comparison reference, not a mathematically guaranteed lower bound.
The raw generation-FID reduction is 8.9%. The site does not use the newer0.25-strength run in this
particular comparison because its reconstruction FID is1.915 rather than approximately2.3.

Both runs use the same flat VAE and width-192/depth-18 DiT architecture,500 prior/joint epochs,
10,000 samples, Gaussian starts and RK4-20. The two-stage pipeline additionally has500 VAE
pretraining epochs. These are preliminary test-grid-selected single-seed results, with one fixed
CFG per curve. No seed uncertainty band is inferred. The frozen-CSEM target-only curve is omitted
from this focused comparison. The full-half-pressure run's finalization originally reported a CPU
reload-check drift; the supplied data confirm all500 epochs and all evaluations, while subsequent
checkpoint recovery was not observed here. No claim of a verified completion record is added.

The plot has a new asset name to avoid reusing the cached historical figure. Reproduce it with:

```bash
python tools/plot_fmnist_matched.py
```

Inputs are `assets/data/fmnist_reconstruction_matched.csv` and `.json`; outputs are
`assets/img/csem_fid_fmnist_matched.png` and `.svg`. The JSON retains exact endpoints and selection,
evaluation, and source provenance. The homepage and research stat tiles must be updated together.
When repeated-seed comparisons are available, use one common cohort and a frozen guidance rule;
retain the original single-seed measurements in the source history.

## Figures

- `csem_cotraining.svg`: architecture diagram drawn for the site. Its fonts are embedded and
  subset, so it renders the same inside `<img>` on every platform. Plain-text label edits work,
  but characters that were not in the original labels fall back to system fonts.
- `og_card.png`: the 1200×630 preview image that appears when the site is linked on LinkedIn,
  Slack, or email. It is a render of the diagram. Regenerate it if the diagram changes.
- `csem_fid_fmnist_matched.png` / `.svg`: current measured two-curve comparison (see above).
- `csem_fid_fmnist.png`: historical figure, retained as an unused asset.
Each project section is a short pitch: a few plain-language points, one or two figures from the
paper, and a sentence of headline results. Detailed tables stay in the papers.

- `gad_*.png` come from the GAD manuscript (draft of 5 Nov 2026), Overleaf `Figures/`, rasterized
  at 1760 px wide (2× the 880 px column):
  - `gad_1d_progression.png`: Fig. 1, `gad_1d_progression.png` (footer line cropped, background white).
  - `gad_quake_geometry.png`: Fig. 6, `InverseRefactor/quake_geometry.pdf`.
  - `gad_accuracy_vs_requests.png`: Fig. 7, `InverseRefactor/inverse_accuracy_vs_requests.pdf`.
  - `gad_mala_vs_annealed_gad.png`: E2 plot areas from the supplied `Figures/InverseRefactor/quake_geometry.pdf`
    (GN-smMALA left, annealed GN-GAD right), retaining the manuscript's bins, colors, probability
    scale, and plotted domain, with axis text and panel letters removed. No density smoothing.
- `assets/GAD_Manuscript.pdf`: supplied manuscript dated 11 November 2026 (69 pages).
- `lfgi_*.png` come from the LFGI manuscript (draft of 6 Nov 2026), Overleaf `Figs/`:
  - `lfgi_gmm8_samples.png`: Fig. 2, `gmm8_heatmap.png`, re-tiled from one row of seven panels into
    rows of four and three (same panels, order, and axes; figure-wide title dropped).
  - `lfgi_darcy_density.png`: Fig. 5, `darcy_density_array.png`, left-column panels for LFGI, Tweedie,
    and MAP–Laplace placed side by side. Fig. 5 mislabels some of its other rows; those are not used.
  - `lfgi_thumb.png`: Fig. 2 plot areas, Tweedie beside LFGI, no axis text.
- `tsi_*.png` come from the TSI paper (`Paper/Paper_Figures/` in the SISC project):
  - `tsi_helix_samples.png`: the 9-D helix comparison, `5way.png`.
  - `tsi_mnist_posterior.png`: Fig. 4.7, the MNIST deblurring posterior histograms, `MNIST_hist2.png`
    (alpha flattened onto white, resized to 1760 px wide).
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

## GAD card image update

The Home and Papers pages now explicitly load `assets/img/gad_mala_vs_annealed_gad.png` to
avoid reusing the old thumbnail URL. The left panel is GN-smMALA; the right panel is annealed
GN-GAD. `gad_thumb.png` contains the same updated pair for older references.
The CSEM FMNIST result now uses the reconstruction-matched seed-42 comparison described above.

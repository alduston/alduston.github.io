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
- the retired figures `assets/img/gad_darcy.png`, `gad_ess.png`, `gad_navier_stokes.png`,
  `gad_ns_pca.png`, and `lfgi_gate.png`.

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

The results figure and numbers are placeholders from the earlier training configuration.

1. Export the runs to a long CSV, one row per regime, seed, and epoch:
   `regime,seed,epoch,fid`, where regime is `cotrained_csem`, `indep_csem`, or `indep_tweedie`.
2. Regenerate the figure in site style, with a 95% band over seeds:
   ```
   python tools/plot_training_curves.py runs_fmnist.csv assets/img/csem_fid_fmnist
   ```
   This overwrites `csem_fid_fmnist.png` and writes an `.svg` alongside it. The new figure uses
   orange for co-trained CSEM, blue for two-stage with the CSEM target, and green for two-stage with
   the denoising target, so update the colour words in the figure caption in `research.html`.
3. Update the numbers in three places:
   - the results table in `research.html#csem`;
   - the three stat tiles in `index.html`;
   - the protocol note in `research.html#csem`, which says the results come from an earlier
     configuration. Remove that sentence once the figure is replaced.
4. Once the CSEM repository has a project-specific README, uncomment the `code` link in the CSEM
   `meta` line of `research.html`.

## Figures

- `csem_cotraining.svg`: architecture diagram drawn for the site. Its fonts are embedded and
  subset, so it renders the same inside `<img>` on every platform. Plain-text label edits work,
  but characters that were not in the original labels fall back to system fonts.
- `og_card.png`: the 1200×630 preview image that appears when the site is linked on LinkedIn,
  Slack, or email. It is a render of the diagram. Regenerate it if the diagram changes.
- `csem_fid_fmnist.png`: placeholder Fashion-MNIST FID curve (see above).
- `gad_*.png` come from the GAD manuscript (draft of 5 Nov 2026), rasterized from the Overleaf
  figure PDFs at 1760 px wide (2× the 880 px column):

  | Site file | Manuscript figure | Overleaf source |
  |---|---|---|
  | `gad_1d_progression.png` | Fig. 1 | `Figures/gad_1d_progression.png` (footer line cropped, background set to white) |
  | `gad_mode_separation.png` | Fig. 2 | `Figures/gad_empirical_conditioning.pdf` |
  | `gad_gate_ablation.png` | Fig. 3 | `Figures/gate_ablation_r3_4x4_10k.pdf` |
  | `gad_2d_benchmarks.png` | Fig. 4 | `Figures/toy_sampler_comparison_60k.pdf` |
  | `gad_acoustic_geometry.png` | Fig. 5 | `Figures/InverseRefactor/acoustic_geometry.pdf` |
  | `gad_quake_geometry.png` | Fig. 6 | `Figures/InverseRefactor/quake_geometry.pdf` |
  | `gad_accuracy_vs_requests.png` | Fig. 7 | `Figures/InverseRefactor/inverse_accuracy_vs_requests.pdf` |

  `gad_thumb.png` (home card and papers list) redraws the E2 row of Fig. 6, NUTS reference beside
  annealed GN-GAD, from `Figures/InverseRefactor/plot_data/quake_geometry.npz` with the manuscript's
  bins, colormap, and color scale, without axis text so it reads at card size. The GAD results table
  in `research.html` copies the primary-metric columns of manuscript Tables 6 and 7.
- `tsi_blend.png` is a toy illustration generated for the site, and its caption says so.
- `lfgi_*.png` come from the LFGI manuscript (draft of 6 Nov 2026), `Figs/` in the Overleaf project.
  The sample-histogram figures re-tile the manuscript's single row of seven panels into rows of
  four and three (same panels, order, and axes; the figure-wide title is dropped):

  | Site file | Manuscript source |
  |---|---|
  | `lfgi_gmm8_samples.png` | Fig. 2, `gmm8_heatmap.png` (re-tiled) |
  | `lfgi_funnel_samples.png` | Fig. 3, `funnel_heatmaps.png` (re-tiled) |
  | `lfgi_gmm24_samples.png` | Fig. 4, `gmm24_heatmap.png` (re-tiled) |
  | `lfgi_score_rmse_sweep.png` | Fig. 1, `score_rmse_by_t.png` |
  | `lfgi_gate_error_t04/t08/t16.png` | Fig. 6, `gate_figs/risk_capture_04/08/16.png` |
  | `lfgi_darcy_density.png` | Fig. 5, `darcy_density_array.png`: header plus the LFGI, Tweedie, and MAP–Laplace rows |
  | `lfgi_thumb.png` | Fig. 2 plot areas, Tweedie beside LFGI, without axis text |

  The LFGI tables in `research.html` copy manuscript Tables 2–8: the score-RMSE column of Tables
  2–4, Table 5 without the central-slope column, and the evidence-error column of Tables 6–8.

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

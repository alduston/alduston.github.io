# alduston.github.io

Personal academic website. Plain HTML/CSS, no build step.

## Publish on GitHub Pages

Replace the repository contents with this folder (keep `.nojekyll`), commit, and push to `main`.
Pages deploys from `main`, folder `/ (root)`; the site updates at https://alduston.github.io within a
minute or two.

This version removes two leftovers from the previous upload: a stale nested copy of the site in
`alduston.github.io/` and a root-level `style.css`. Every page loads `assets/style.css`, which now
contains the CV-page rules that previously lived only in the root file. Delete both leftovers from
the repository when you push.

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
- `gad_*.png` are taken from the GAD manuscript draft.
- `tsi_blend.png` and `lfgi_gate.png` are toy illustrations generated for the site, and their
  captions say so.

## Common edits

- **Internship note:** the `seeking` paragraph on `index.html`. Remove it when the search is done.
- **New paper:** copy a `<div class="pub">…</div>` block in `papers.html`. When a manuscript
  becomes a preprint, change its tag on `research.html` and `index.html` to
  `<span class="tag preprint">Preprint</span>`.
- **News:** add an `<li>` at the top of the News list in `index.html`.
- **PDF CV:** replace `assets/Alois_Duston_CV.pdf`. The home page and the CV page both link to it.

## Open items

- Author list for the CSEM technical report (`papers.html`).

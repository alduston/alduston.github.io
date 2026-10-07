# alduston.github.io

Personal academic website. Plain HTML/CSS, no build step.

## Publish on GitHub Pages

1. Create a public repository named exactly `alduston.github.io` on GitHub.
2. Upload the contents of this folder (keep the `.nojekyll` file) to the repository root and push to `main`.
3. In the repository, go to **Settings → Pages**, set the source to "Deploy from a branch", branch `main`, folder `/ (root)`.
4. The site appears at https://alduston.github.io within a minute or two.

## Structure

```
index.html      Home: bio, links, project cards, news
research.html   One section per project, grouped by theme, with figures
papers.html     Preprints and manuscripts in preparation, with BibTeX
cv.html         Short CV
assets/style.css
assets/img/     Figures and portrait
```

## Common edits

- **Photo:** save a square photo as `assets/img/profile.jpg` and change the `src` of the
  `portrait` image in `index.html`.
- **New paper:** copy a `<div class="pub">…</div>` block in `papers.html`. Move a manuscript from
  "In preparation" to "Preprints" and change its status tag on `research.html` and `index.html`
  from `<span class="tag wip">In progress</span>` to `<span class="tag preprint">Preprint</span>`.
- **News:** add a `<li>` at the top of the News list in `index.html`.
- **PDF CV:** save as `assets/cv.pdf` and uncomment the link at the top of `cv.html`.

## Figures

- `gad_*.png` are taken from the GAD manuscript draft.
- `tsi_blend.png`, `lfgi_gate.png`, `csem_field.png` are toy illustrations generated for the site
  (captions say so); swap in paper figures whenever you prefer.

## Open items

- CV years (the `when` fields in `cv.html`).
- Author list for the CSEM technical report (`papers.html`).

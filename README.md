# Typewave clone

Local React 18 + Vite + Tailwind v3 rebuild of the single-page site at
https://typewave.blendmodes.com/, for local reference only.

```bash
npm install
npm run dev   # http://localhost:5273
```

Long-form copy in `src/content.js` is original placeholder text, not the live
site's marketing copy. Roobert/Vesterbro in `public/assets/` are commercial
fonts — licence them before publishing anything built from this.

## Information architecture

`ia.json` is the only IA file to hand-edit. `IA.md` and `matrix.csv` are
**generated** — never edit them directly; they are overwritten on every build.

```bash
node validate.mjs && node build.mjs
```

### What the data shows

- **1 route, 1 template, 13 sections.** The whole site is `/`, so every section
  is single-use and the validator lists all 13 as page-local. There is nothing
  to extract into a shared section component until a second page exists.
- **Reuse lives below the section level, not at it.** The one component shared
  across sections is `FigmaButton.jsx` (used by Navbar, Hero, Footer and
  FloatingCta); page-level motion is shared through `src/lib/` (Lenis, reveal,
  parallax, per-character compose) rather than through repeated sections.
- **6 of 13 sections are product explanation** (`FEATURES`) and carry nearly all
  the scroll-linked motion; 4 sections sit outside `<main>` (navbar before it;
  footer, floating CTA and type inspector after it).
- Every section names its rendering component via `implementedBy`, and all 13
  paths resolve to real files.

Other references in this folder: `CLONE_SPEC.md` (measured recon of the live
site), `ASSET_MANIFEST.md`, and `design-repo/` (AI-ready contracts; built
separately).

# Typewave design-repo

An AI-ready, machine-validated design system extracted from the **typewave-clone** project (a React + Vite +
Tailwind v3 clone of the live single-page marketing site <https://typewave.blendmodes.com/>, a Figma plugin by
Blend Modes). A generator composes a **PageSpec** (`schema/pagespec.schema.json`) from the closed set of
sections in `tokens/llm/component-allowlist.json`; `schema/semantic_validate.py` enforces everything JSON
Schema cannot.

**Status: `design-review-pending`, `productionApproved: false`.** Built 2026-10-20. A snapshot, not a mirror:
`extraction/verify_all.py` re-checks every cited conclusion against the current clone source.

## Layout

```
README.md  CHANGELOG.md  registry.manifest.json
tokens/00-foundation  color, typography (11 roles x 3 breakpoints), radius, spacing, breakpoint, motion, elevation, icon-size
tokens/10-semantic    color-roles, typography-roles, motion-roles
tokens/20-component   button, tag, badge, card, pricing, navbar, floating-cta, faq, typo-sim, type-inspector
tokens/30-layout      container, grid, section-spacing, z-index
tokens/themes         typewave-dark (the only theme)
tokens/llm            component-allowlist.json, token-catalog.json, token-policy.json
assets/asset-roles.json   closed asset-role vocabulary + generation/licensing policy + pinned compliance values
primitives/  components/  sections/   contracts (sections carry content schema, maxWords, motion, responsive)
templates/templates.json  page shapes + route map
compatibility/graph.json  rhythm/position/dependency/compliance rules with severity
schema/      pagespec.schema.json (draft-07), example.pagespec.json, semantic_validate.py, tests/adversarial_test.py
extraction/  measured-values.json, verify_all.py, drift_test.py
```

## Counts (recomputed from disk by `verify_all.py` check 9; this block is machine-checked)

<!-- counts:start -->
- tokensFoundation: 229
- tokensSemantic: 41
- tokensComponent: 59
- tokensLayout: 14
- primitives: 10
- components: 13
- sections: 13
- templates: 1
- routes: 1
- assetRoles: 23
- assetRolesSettable: 11
- pinnedPolicies: 20
- graphRules: 20
- adversarialMutations: 55
- adversarialControls: 4
- themes: 1
- measuredFacts: 29
<!-- counts:end -->

## Page shape

One real route, one template: `/` -> `template.home` (App.jsx mounts no router). Node order is the App.jsx render
order; navbar, hero and footer are required, every content section and both overlays are optional.

| Section | Category | Required | Motion patterns (evidenced) | reducedMotionFallback (const) |
|---|---|---|---|---|
| `shell.navbar` | shell | yes | nav-hide-on-scroll, mobile-menu | `instant-hide-show` |
| `hero.video-scale` | hero | yes | char-reveal-scroll-linked, fade-up, parallax, hero-video-scale, video-play-once | `static-full-scale-video` |
| `steps.sticky-stack` | steps | no | char-reveal-scroll-linked, fade-up, parallax, sticky-stack-scale | `static-unscaled-stack` |
| `cards.feature-carousel` | cards | no | char-reveal-scroll-linked, fade-up, swipe-carousel | `instant-visible` |
| `showcase.breakpoint-scrub` | showcase | no | char-reveal-scroll-linked, fade-up, scrub-progress, caption-slide-up | `static-final-frame` |
| `grid.preset-wave` | grid | no | char-reveal-scroll-linked, fade-up, sine-wave-bump | `static-folders` |
| `split.export-cards` | split | no | char-reveal-scroll-linked, fade-up | `instant-visible` |
| `pricing.ticket-plans` | pricing | no | char-reveal-scroll-linked, fade-up | `instant-visible` |
| `faq.sticky-accordion` | faq | no | char-reveal-scroll-linked, fade-up, accordion, sticky-lead-offset | `instant-toggle` |
| `form.newsletter-inline` | form | no | char-reveal-scroll-linked, fade-up | `instant-visible` |
| `shell.footer` | shell | yes | fade-up | `instant-visible` |
| `overlay.floating-cta` | overlay | no | floating-cta-visibility | `instant-hide-show` |
| `overlay.type-inspector` | overlay | no | cursor-follow-badge | `instant-opacity` |

Breakpoints are desktop-first with fixed px per breakpoint (desktop >=1025, tablet <=1024, mobile <=767; no
clamp()). Every section has a structured `responsive` list (`breakpoint`, `query`, machine-readable `changes`,
citations): e.g. the sticky stack becomes a static column, the feature cards become a snap carousel, preset
folders go 12 -> 8 -> 5 with wave amplitude 88 -> 50 -> 22, the navbar collapses into a full-screen menu and Lenis
smooth scroll is not created at <=1024.

## Structural oddities (documented, not normalised away)

1. **Copy is placeholder.** `src/content.js` holds ORIGINAL PLACEHOLDER copy written for the clone and
   length-matched to the recon counts. The example PageSpec uses that copy (minus the deviations below);
   budgets come from the measured counts. No live-site copy is transcribed anywhere in this repo. `verify_all.py` check 15 proves
   both directions: every long example string occurs in the clone's placeholder copy, and no string in this
   repo occurs in the live page text or the Lottie text layers. Exception found by that check: the clone's FAQ questions 2/3/5/6
   and plan subtitles are verbatim live-site strings, so the example rewords them (`exampleDeviations` in
   `extraction/measured-values.json`); the clone itself still ships them. Short functional UI labels (nav
   items, "Try it now", plan names) are kept; the clone's `<title>` equals the live title and is
   therefore NOT reused (the example title is a placeholder built from the clone hero copy).
2. **The Lottie is banned.** The breakpoint mockup is an HTML/CSS rebuild (`BreakpointMock.jsx`). The original
   `recon-assets/breakpoint-lottie.json` embeds the original copy as glyph text and GT Super Display glyphs;
   role `media.device-mockup` is pinned `html-rebuild-only` with the JSON as a `forbiddenSource`.
3. **Real company.** Closed `assetRole` vocabulary wired through schema (per-field `const`), allowlist and
   example, with a `generationPolicy` per role and **pinned values** for every compliance-critical role
   (a change to a different-but-valid policy fails `ASSET_ROLE_PINNED` and verify check 11):

| Role | Policy | Settable | Pinned |
|---|---|---|---|
| `brand.logo-wordmark` | `must-not-reproduce` | yes | pinned |
| `brand.logo-mark` | `must-not-reproduce` | yes | pinned |
| `meta.favicon` | `must-not-reproduce` | yes | pinned |
| `meta.og-image` | `generated-stand-in-only` | yes | pinned |
| `logo.third-party-tool` | `must-not-fabricate` | yes | pinned |
| `icon.figma-glyph` | `must-not-fabricate` | yes | pinned |
| `media.hero-video` | `generated-stand-in-only` | yes | pinned |
| `media.step-video` | `generated-stand-in-only` | yes | pinned |
| `media.figma-panel` | `generated-stand-in-only` | yes | pinned |
| `media.export-screenshot` | `generated-stand-in-only` | yes | pinned |
| `media.faq-screenshot` | `generated-stand-in-only` | yes | pinned |
| `media.device-mockup` | `html-rebuild-only` | no | pinned |
| `icon.ui-check` | `may-generate-new` | no | - |
| `icon.ui-chevron` | `may-generate-new` | no | - |
| `icon.preset-folder` | `may-generate-new` | no | - |
| `font.roobert` | `licensed-font-required` | no | pinned |
| `font.vesterbro` | `licensed-font-required` | no | pinned |
| `endpoint.checkout` | `must-not-reuse-live-endpoint` | no | pinned |
| `endpoint.newsletter-form` | `must-not-reuse-live-endpoint` | no | pinned |
| `endpoint.plugin-listing` | `must-not-reuse-live-endpoint` | no | pinned |
| `endpoint.company-mailbox` | `must-not-reuse-live-endpoint` | no | pinned |
| `endpoint.legal-pages` | `must-not-reuse-live-endpoint` | no | pinned |
| `script.affiliate` | `must-not-reuse-live-endpoint` | no | pinned |

4. **Live endpoints.** The clone still links the live checkouts, newsletter POST, plugin listing, company
   mailbox and legal pages. The example uses `example.com` placeholders and `LIVE_ENDPOINT_NOT_REUSED` rejects
   any of them. affiliate.js is excluded from the clone.
5. **Reduced motion.** Only the char reveal and the preset wave honour `prefers-reduced-motion` in source; the
   other section fallbacks are prescribed by this repo (`reducedMotionEvidence` in each contract).
6. **Pixel-audit parity** (document heights 11623 / 11242 / 11956 / 9290 at 1440 / 1280 / 768 / 375, typo
   simulator 424px, newsletter submit 86px) is a reported result with no audit file on disk; the original-side
   numbers are file-backed in CLONE_SPEC (see `extraction/measured-values.json` `reportedFacts`).
7. **No PageSpec token overrides exist** (styling is owned by contracts), so token drift is checked at the
   catalog layer (`token-policy.json` says so).

## Verify

```
python3 extraction/verify_all.py          # 16 checks; exit 1 on any FAIL
python3 schema/tests/adversarial_test.py  # every mutation rejected, every control passes
python3 schema/semantic_validate.py [spec.json ...]
python3 extraction/drift_test.py [--workdir DIR]   # proves the drift checks fail on injected drift
```

Requires Python 3.8+ with `jsonschema`. Scripts derive the repo root from `__file__`; citations to the sibling
clone project and the original files degrade to WARN when this folder is used standalone.
`registry.manifest.json` `entryPoints` list only files inside this folder.

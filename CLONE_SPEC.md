Source: https://typewave.blendmodes.com/

# Typewave clone: build spec

Recon date: 2026-10-20. Sources: live site measured with Playwright at 1440x900, 1280x800, 768x1024 and 375x812, plus the original compiled CSS (`../index-D4COY28s.css`), JS bundle (`../index-B7zdGq3H.js`) and saved DOM (`../Typewave .html`). Every number below comes from computed styles or the original source. Anything I could not measure is marked **UNVERIFIED**.

The original site is a single static HTML page with BEM class names. It uses vanilla JS with Lenis 1.3.18 and lottie-web, and has no framework. All styling is plain CSS with custom properties, so in Tailwind v3 you can port it as a global CSS layer (recommended: copy the token block and component rules) or map it to `theme.extend`. Class names are listed so behaviour hooks (JS selectors) can be reproduced 1:1.

**Content rule:** long copy is not transcribed. Each text block lists its role, character/word count, line count at 1440px and a short gist. Write placeholder copy of matching length so the line counts below still hold.

**Measurement note:** `.reveal` elements that were not yet revealed at measurement time carry `translateY(32px)`. Y positions in this doc are layout positions with that offset already removed where it matters.

---

## 0. Global

### Breakpoints (max-width, desktop-first)
| Name | Query | Notes |
|---|---|---|
| Desktop | `min-width: 1025px` | Lenis smooth scroll, sticky/scale effects, parallax, hero video scale |
| Tablet | `max-width: 1024px` | Hamburger nav, all scroll-scrub effects disabled or static, single-column layouts |
| Mobile | `max-width: 767px` | Container padding 24, mobile type scale, `.title-break` (`<br>`) hidden |

### Container / grid
- `.container`: `width:100%; max-width:1344px; margin-inline:auto; padding-inline:48px` (24px at ≤767). Content width is `min(vw,1344) − 96`, which gives **1248** at 1440 (x=96), **1184** at 1280 (x=48), **672** at 768 and **327** at 375 (x=24).
- `.row`: 12-col grid, gap 24 (16 at ≤1024). Only used conceptually. Sections use their own grids (below).
- `--section-padding`: **120px** desktop, **80px** at ≤1024, **40px** at ≤767. Most sections use it for top and bottom padding.
- `html { scroll-behavior:auto }`. At ≥1025, `html { overscroll-behavior:none }`.
- `body { background:#0f0f0e; color:#e6e3da; font-family:"Roobert",sans-serif; font-size:1rem; -webkit-font-smoothing:antialiased; -moz-osx-font-smoothing:grayscale }`.
- Reset: `*,*:before,*:after { margin:0; padding:0; box-sizing:border-box }`.
- On load, JS runs `history.scrollRestoration="manual"; window.scrollTo(0,0)`.
- `<html lang="en">`. Lenis adds the class `lenis` (plus `lenis-scrolling`, `lenis-smooth`, etc.) to `<html>`. The site ships no `.lenis` CSS.

### Fonts
- **Roobert** is the only family rendered. Only weights **400** and **500** actually load: the page preloads `Roobert-Regular-BNQS-qUa.woff2` and `Roobert-Medium-Jj6nDRYB.woff2` with `<link rel=preload as=font type=font/woff2 crossorigin>`.
- `@font-face` blocks declare Roobert 300/400/500/600/700/800 and the Vesterbro set (all `font-display:swap`, `url(/assets/<file>.woff2) format("woff2")`). `--font-secondary:"Vesterbro",sans-serif` is declared but **never used** on the page. Declaring the faces is harmless, but only 400/500 matter.
- Fallback stack: `"Roobert", sans-serif`.
- One exception: the cursor type-inspector badge uses `'SF Mono','Menlo',monospace` 11px.

### Head / meta (reproduce)
- `<title>`: `Typewave – Figma Plugin for Typographic Scales`. Meta description is ~180 chars, gist "plugin generates typographic scale one click".
- `theme-color #0F0F0E`. Favicons: `/favicon.svg` (svg) and `/favicon.png` (32x32). OG/Twitter image: `/cover.png` (1200x630), `twitter:card summary_large_image`.
- Two JSON-LD blocks: a `SoftwareApplication` (price 29.99 EUR) and an `FAQPage`. Generate the FAQPage from your placeholder FAQ copy.
- Lemon Squeezy affiliate (see section 14): `<script>window.lemonSqueezyAffiliateConfig = { store: "typewave" };</script>` then `<script src="https://lmsqueezy.com/affiliate.js" defer></script>`.

---

## 1. Design tokens

### Colors (CSS custom properties, exact)
| Token | Value | Use |
|---|---|---|
| `--color-bg` | `#0f0f0e` | page bg, pricing-plan outer bg, seam, figma-card media bg |
| `--color-surface` | `#191918` | cards, pricing panels, footer hero, FAQ/newsletter borders |
| `--color-text` | `#e6e3da` | primary text |
| `--color-text-muted` | `#7e7c77` | body copy in cards, captions, placeholders |
| `--color-brand` | `#e6f490` | brand highlight in titles, tag/badge bg, typo-sim select |
| `--color-accent` | `#d99f50` | declared, unused |
| `--color-danger` | `#df3535` | `.newsletter__feedback.is-error` (element not in DOM) |
| `--btn-primary-bg` / hover | `#e6e3da` / `#7e7c77` | text `#0f0f0e` |
| `--btn-ghost-text` / hover | `#e6e3da` / `#7e7c77` | transparent bg |
| `--btn-brand-bg` / hover | `#e6f490` / `#e6f490` (no visible hover) | text `#0f0f0e` |
| `--btn-secondary-bg` / hover | `#2a2928` / `#3a3937` | text `#e6e3da` (unused on page) |
| `--btn-dark-bg` / hover | `#0f0f0e` / `#2a2928` | text `#e6e3da` (unused on page) |
| Badge color 2 | `#FE8A3D` | step 2 badge, preset folder |
| Badge color 3 | `#0469FF` | step 3 badge, preset folder |
| Preset pink | `#DCBDC2` | preset folder |
| Typo-sim row divider | `rgba(230,227,218,0.08)` | 1px border-top |
| Floating CTA bg | `#0f0f0ecc` (rgba 15,15,14,.8) | with `backdrop-filter: blur(12px)` |
| Navbar fade | `linear-gradient(180deg,#0f0f0e,#0f0f0e00)` | 120px tall `::before` |
| Type-inspector badge | bg `#191918`, text `#E6F490`, border `1px solid #2A2928` | cursor badge |

### Radii
`--radius-xs:2px` (tag, select) · `--radius-sm:4px` (buttons, badge, media, exports media, FAQ image) · `--radius-md:8px` (cards, pricing, footer hero, hero video, floating CTA) · `--radius-lg:16px` (unused) · `--radius-full:9999px` (unused).

No box-shadows anywhere on the page.

### Spacing tokens
`--space-xs .25rem`, `--space-sm .5rem`, `--space-md 1rem`, `--space-lg 2rem`, `--space-xl 4rem` (declared, effectively unused). `--navbar-height:88px`, `--navbar-height-mobile:80px`, `--grid-gutter:24px`, `--grid-gutter-tablet:16px`, `--grid-gutter-mobile:16px`, `--grid-container-max:1344px`.

### Type scale (all Roobert; size / weight / line-height / letter-spacing)
| Class | Desktop (≥1025) | Tablet (≤1024) | Mobile (≤767) |
|---|---|---|---|
| `.display-1` | 96 / 500 / 1 / **-1.2px** | 72 / 500 / 1 / 0 | 40 / 500 / 1 / 0 |
| `.display-2` | 72 / 500 / 1 / **-1.2px** | 48 / 500 / 1 / 0 | 32 / 500 / 1 / 0 |
| `.display-3` | 56 / 500 / 1 / 0 | 32 / 500 / 1 / 0 | 24 / 500 / 1 / 0 |
| `.heading-1` | 32 / 500 / 1 / 0 | 32 / 500 / 1.125 / 0 | 24 / 500 / 1.143 / 0 |
| `.heading-2` | 24 / 500 / 1 / 0 | 24 / 500 / 1 / 0 | 20 / 500 / 1 / 0 |
| `.subtitle-1` | 20 / 500 / 1.4 / 0 | 18 / 500 / 1.4 / 0 | 16 / 500 / 1.2 / 0 |
| `.body-1` | 16 / 400 / 1.5 / 0 | 16 / 400 / 1.5 / 0 | 16 / 400 / 1.5 / 0 |
| `.body-2` | 14 / 400 / 1.429 / 0 | same | same |
| `.button-1` | 20 / 500 / 1 / 0 | 16 / 500 / 1.5 | 16 / 500 / 1.5 (unused on page) |
| `.button-2` | 16 / 500 / 1 / 0 | 14 / 500 / 1.429 | 14 / 500 / 1.429 |
| `.caption-1` | 10 / 500 / 1.333 / 0 | same | same |

The scale is fixed px per breakpoint, with no clamp() or vw sizing anywhere. Each class sets family, size, weight, line-height and letter-spacing from `--font-<role>-<prop>-<bp>` variables, so recreate the full variable set (desktop/tablet/mobile per role) or the equivalent Tailwind utilities.

### Easing / durations
| Name | Value | Used by |
|---|---|---|
| ease-standard | `cubic-bezier(0.4, 0, 0.2, 1)` | navbar hide (0.35s), hamburger lines (0.35s), mobile menu (0.3s), FAQ chevron (0.35s), FAQ lead `top` (0.35s), floating CTA (0.4s) |
| ease-decel | `cubic-bezier(0, 0, 0.2, 1)` | FAQ answer `grid-template-rows` (0.35s) |
| `ease` | CSS keyword | `.reveal` opacity/transform 0.7s; `.btn` background-color 0.2s |
| plain 0.2s | (ease default) | color hovers: `.faq__email`, `.faq__answer-link`, `.newsletter__submit`, `.footer__legal-link` |
| 0.15s | | `.typo-sim__select` border-color |
| 0.12s ease | | type-inspector badge opacity |
| Lenis | `duration:1.4, easing:t => 1 - Math.pow(1 - t, 5), smoothWheel:true` | desktop only |

There are no CSS `@keyframes` on the site. All motion is transitions or JS-driven inline styles.

---

## 2. Shared components

### Buttons `.btn`
Base: `display:inline-flex; align-items:center; gap:8px; border:none; cursor:pointer; text-decoration:none; transition:background-color .2s ease`. The text uses the `.button-2` class (16/500/1 desktop, 14/500/1.429 at ≤1024).
- `.btn--sm`: `height:40px; padding:0 16px; border-radius:4px`.
- `.btn--primary`: bg `#e6e3da`, text `#0f0f0e`; **hover bg `#7e7c77`**.
- `.btn--brand`: bg `#e6f490`, text `#0f0f0e`; hover is the same color, so there is no visible change.
- `.btn--ghost`: transparent; **hover text `#7e7c77`**. The color is not transitioned (only background-color is), so it changes instantly.
- `.btn__icon`: flex box holding the 16x17 Figma glyph SVG (`recon-assets/svg/figma-icon-btn.svg`). Label sits in `.btn__label`.
- Measured: "Try it now" primary sm is **125.3x40** at desktop and 117x40 at ≤1024. Nav ghost "How it works" is 124.3x40.

### Tag `.tag.caption-1` ("NEW")
`inline-flex; padding:2px 6px; background:var(--tag-bg, #e6f490); color:#0f0f0e; border-radius:2px`. 10px/500/13.33px. Measured **34.7x17.3**. Appears in nav ("AI Prompt"), the AI Prompt export card title, and the last "Everything included" item.

### Badge `.badge.button-2`
`32x32; border-radius:4px; background:var(--badge-bg, brand); color:#0f0f0e; flex center`. Holds a step number ("1", "2", "3").

---

## 3. Navbar `header.navbar`

### Structure
```
header.navbar
  div.navbar__inner.container
    a.navbar__logo [href="/" aria-label="Typewave homepage"] > svg 171x40   (recon-assets/svg/navbar-logo.svg)
    nav.navbar__nav
      button.btn.btn--ghost.btn--sm.button-2[data-scroll-to="#how-it-works"] > span.btn__label "How it works"
      button ... [data-scroll-to="#ai-prompt"] > span.btn__label "AI Prompt" + span.tag.caption-1 "NEW"
      button ... [data-scroll-to="#pricing"]  "Pricing"
      button ... [data-scroll-to="#faq"]      "FAQ"
    div.navbar__cta > a.btn.btn--primary.btn--sm.button-2 (Figma icon + "Try it now")  -> Figma community URL, target=_blank rel="noopener noreferrer"
    button.navbar__hamburger[aria-label="Open menu"] > span.navbar__hamburger-line--top + span.navbar__hamburger-line--bot
  div.navbar__mobile-menu
    nav.navbar__mobile-nav  (same 4 ghost buttons)
    div.navbar__mobile-cta  (same "Try it now" primary)
```

### Geometry
- `position:fixed; top:0; left:0; width:100%; z-index:100`.
- Desktop height is **88**: inner padding 24/48 plus 40px content. The inner is a `.container`, so it is centered at max 1344.
- Logo 171x40 at x = container-left + 48 (x=96 at 1440, x=48 at 1280).
- `.navbar__nav` is absolutely centered (`left:50%; transform:translate(-50%)`) with gap 4 and is **427.2px** wide.
- CTA is right-aligned.
- `::before`: absolute, full width, **120px** tall, gradient `#0f0f0e → transparent`, `pointer-events:none`. It is hidden when the menu is open.
- ≤1024:
  - Logo svg is `height:32px; width:auto` (136.8x32).
  - Nav and CTA are `display:none`. The hamburger is `display:flex; flex-direction:column; justify-content:center; gap:6px; 24x24` at the right edge (x=696 at 768, x=327 at 375; y=28).
  - Inner height is **80**. Padding is 24/48, and 24/24 at ≤767.
  - Each hamburger line is 24x2, `#e6e3da`, `transform-origin:center`, with a 0.35s ease-standard transition on transform and opacity.

### Behaviour
- **Hide on scroll down:** a rAF-throttled `scroll` listener. If `scrollY > lastY && scrollY > 80`, add `.navbar--hidden` (`translateY(-100%)`) and `html.navbar-hidden`. Otherwise remove both. Transition: `transform .35s cubic-bezier(.4,0,.2,1)`. It is skipped while the mobile menu is open.
- **Nav click:** close the menu, then `lenis.scrollTo(selector, { offset: -80 })`. At ≤1024 Lenis is replaced by a shim that runs `window.scrollTo({top: el.top + scrollY - 80, behavior:"smooth"})`.
- **Mobile menu (≤1024):**
  - The hamburger toggles `.navbar--open`. That sets the navbar to `background:#0f0f0e; height:100dvh; display:flex; flex-direction:column`, and the aria-label switches between "Open menu" and "Close menu".
  - While open, Lenis is stopped (`lenis.stop()`) and restarted on close. The shim's stop/start are no-ops, so native scroll is not locked (**known original behaviour**).
  - The lines morph into an X: top `translateY(4px) rotate(45deg)`, bottom `translateY(-4px) rotate(-45deg)`.
  - `.navbar__mobile-menu`:
    - Base: `flex:1; display:flex; column; justify-content:space-between; padding:0 24px 40px`.
    - Closed: `visibility:hidden; opacity:0; transform:scale(.96); transform-origin:top center; pointer-events:none`.
    - Open: visible, opacity 1, scale 1. Transition: opacity and transform 0.3s ease-standard.
  - `.navbar__mobile-nav`: column, centered, `flex:1; gap:8px`. Its buttons use display-3-mobile type: **24px/500/1**, `padding:10px 0`, height auto (44px tall).
  - `.navbar__mobile-cta .btn`: `width:100%; height:56px; justify-content:center`.
  - Resizing to ≥1025 closes the menu.

---

## 4. Hero `section.hero`

### Structure
```
section.hero
  div.container
    div.hero__wrapper [data-parallax="-0.02"]
      div.hero__content [data-parallax="-0.08"]
        h1.hero__title.display-1.reveal (--reveal-delay:0ms)
        p.hero__subtitle.subtitle-1.reveal (--reveal-delay:150ms)
        div.hero__cta.reveal (--reveal-delay:300ms) > a.btn.btn--primary.btn--sm (Figma icon + "Try it now") -> Figma URL
      div.hero__video-scale
        video.hero__image.reveal (--reveal-delay:450ms) src=/assets/intro-DrshnI3i.mp4 muted playsinline preload="auto"  (NO autoplay, NO loop attr)
```

### Copy
- **h1:** 48 chars / 8 words in 3 forced lines (`<br class="title-break">` between lines). Line 1 has 3 words, line 2 has 2 words, and line 3 (3 words, ends with ".") is wrapped in `span.hero__title--brand` (color brand). Gist: "create perfect type scale, one click". Centered. At 375 the `<br>`s are hidden and the title wraps naturally to 3 lines.
- **Subtitle:** 178 chars / 27 words, 3 lines at 1440 (612px wide), 5 lines at 768 (324px), 4 lines at 375. Gist: "plugin generates frames, styles, variables, exports". Centered.

### Layout
- Desktop (≥1025):
  - `.hero`: `min-height:100vh; padding-top:0; padding-bottom:120px`. JS then sets an inline `min-height` (see Motion), which is **1597.8px** at 1440x900 and **1471px** at 1280x800.
  - `.hero .container { position:relative }`.
  - `.hero__wrapper`: `display:flex; column; gap:160px; min-height:100vh; justify-content:center`. The content block is vertically centred in the first viewport: at 1440x900 `.hero__content` is 476 tall at y=212, and at 1280x800 it is at y=162.
  - `.hero__content`: flex column, **gap 32**. Measured at 1440: title 1248x288 at y=212, subtitle 612x84 at y=532, CTA at y=648.
  - `.hero__subtitle`: `max-width: calc(50% - 12px)` (612 at 1440, 580 at 1280); `margin-inline:auto`; `text-align:center`.
  - `.hero__cta`: flex, justify center.
  - `.hero__video-scale`: `position:absolute; left:0; width:100%; top:94vh` (CSS fallback, overwritten by JS); `transform-origin:center center; will-change:transform`. The width equals the container content width (1248 / 1184).
  - `.hero__image`: `display:block; width:100%; aspect-ratio:16/9; border-radius:8px; object-fit:cover`. Unscaled box is 1248x702 at 1440, 1184x666 at 1280.
- ≤1024:
  - `.hero` `padding-top: calc(80px + 80px) = 160px`, padding-bottom = section padding (80, or 40 at ≤767).
  - Wrapper gap **80**, with no min-height.
  - The video is in normal flow, unscaled: 672x378 at 768 and 327x184 at 375.
  - At 768 the subtitle is 18px/25.2 at 324px wide (still `calc(50% - 12px)`: 336 − 12 = 324). At ≤767 `max-width:100%`.

---

## 5. How it works `section.how-it-works#how-it-works`

### Structure
```
section.how-it-works#how-it-works
  div.container > div.how-it-works__wrapper
    div.how-it-works__header [data-parallax="-0.04"]
      h2.how-it-works__title.display-2.reveal (--reveal-delay:150ms)
    div.how-it-works__cards
      div.card  x3
        div.card__body
          div.card__top
            div.badge.button-2 (style --badge-bg: var(--color-brand) | #FE8A3D | #0469FF) "1" | "2" | "3"
            h3.card__title.heading-1
          p.card__text.body-1
        div.card__media
          video.card__image src=<def1|def2|loop3> loop muted playsinline preload="metadata"  (no autoplay attr)
```

### Copy
- **h2:** 62 chars / 10 words, 3 lines at 1440 (1040 wide). Line 1 has 4 words (ends "."). Line 2 starts with 2 plain words followed by a brand-colored span of 4 words (ends "!"), and that span wraps to a third line. Gist: "normally hours; with us seconds".
- **Card titles (heading-1):** 41ch/8w (3 lines @272px), 31ch/6w (2 lines), 47ch/7w (4 lines). Gists: "choose up to 5 hierarchies", "build your project scale", "export full system in Figma".
- **Card texts (body-1, muted):** 176ch/25w (6 lines), 233ch/34w (7 lines), 199ch/37w (6 lines) at 272px. Gists: "organize fonts into roles", "start from website preset", "builds frames, styles, variables, exports".

### Layout
- Section padding is 120 top and bottom (80 / 40 on smaller viewports).
- Wrapper: flex column with gap **72**, or 60 at ≤1024 and 40 at ≤767.
- Header: flex column, gap 16.
- Title: `max-width: calc(100%/12*10)` (83.333%). That is 1040 at 1440 and 987 at 1280. At 768 it measured 560 (48px, 3 lines); at 375 it is 273 (32px, 4 lines).
- Cards container: flex column with gap **80**, or 24 at ≤1024.
- `.card`:
  - `display:flex` (row), `background:#191918; border-radius:8px; overflow:hidden; position:sticky; transform-origin:center`, plus `will-change:transform` at ≥1025.
  - Sticky `top` is set inline by JS: `(innerHeight − firstCard.offsetHeight)/2`. That gives 100px at 1440x900 and 68px at 1280x800.
  - `.card__body`: `width: calc(25% + 24px)` (336 at 1440, 320 at 1280); `flex-shrink:0; padding:32px; display:flex; column`.
  - `.card__top`: flex column, gap 32.
  - `.card__text`: color `#7e7c77`, `margin-top:auto` (pinned to the card bottom).
  - `.card__media`: `flex:1; padding:32px`. `.card__image` is `display:block; width:100%; height:auto; border-radius:4px` (videos are 1200x900, so 4:3).
  - **Card size:** 1248x700 at 1440 (video 848x636); 1184x664 at 1280 (video 800x600).
- ≤1024:
  - `.card`: `flex-direction:column-reverse` (media on top), `position:static`, `transform:none !important`.
  - `.card__body`: width 100%.
  - `.card__media`: `padding:32px 32px 16px`.
  - `.card__text`: `margin-top:32px`.
  - At 768: card 672x772, media 504 tall (video 608x456), body 268.
- ≤767:
  - Body and media padding 24, media `padding-bottom:0`.
  - `.card__top` gap 24, `.card__text` margin-top 24.
  - At 375: card 327x560, video 279x209, title 24px/27.43.

---

## 6. Figma organization `section.figma-org` (no id)

### Structure
```
section.figma-org
  div.container > h2.figma-org__title.display-2.reveal
  div.figma-org__cards           <- NOT inside .container (it has its own padding / max-width)
    div.figma-card.reveal  (delays 0 / 100ms / 200ms)
      div.figma-card__media > img (frame-Cg0zK82j.png | styles-DpEOnP78.png | variable-fdRUIB1a.png, all 800x600, descriptive alt)
      h3.figma-card__title.heading-1   "Frames" | "Styles" | "Variables"
      p.figma-card__text.body-1
```

### Copy
- **h2:** 40ch/6w in 2 lines. Line 1 has 3 words (ends ","). Line 2 is all brand-colored, 3 words. Gist: "your file, perfectly organized".
- **Card texts:** 166ch/27w, 165ch/28w, 148ch/23w, each 4 lines at 336px. Gists: "a preview frame per level", "a text style per level", "every value becomes variable".

### Layout
- `.figma-org` is a flex column with `gap:80px` (60 at ≤1024, 40 at ≤767) and section padding.
- `.figma-org__cards` (desktop): `display:grid; grid-template-columns:repeat(3,1fr); gap:24px; padding-inline:48px; max-width:1344px; margin-inline:auto; width:100%`. Columns are 400px at 1440 and 378.66px at 1280.
- `.figma-card`: `background:#191918; border-radius:8px; padding:32px; flex column; gap:32px; overflow:hidden`. 400x508 at 1440, 379x516 at 1280.
- `.figma-card__media`: `aspect-ratio:4/3; border-radius:4px; overflow:hidden; background:#0f0f0e`. The img fills it with `object-fit:cover` (336x252 at 1440).
- Title is heading-1 in `#e6e3da`. Text is body-1 in `#7e7c77`.
- **≤1024 horizontal carousel:**
  - Container: `display:flex; flex-wrap:nowrap; overflow-x:auto; scroll-snap-type:x mandatory; gap:16px; scrollbar-width:none` (and `::-webkit-scrollbar{display:none}`); `max-width:none; margin-inline:0; padding-inline:0; scroll-padding-left:48px`.
  - Cards: `flex:0 0 80%; scroll-snap-align:start; opacity:1 !important; transform:none !important` (reveal is disabled).
  - The first card has `margin-left:48px` and the last has `margin-right:48px`.
  - At 768: card 614x649, media 550x413.
  - ≤767: `scroll-padding-left:24px`, flex-basis **75%**, first/last margins 24, card padding 24, gap 24. At 375 a card is 281x442.

---

## 7. Breakpoint (Lottie scrub) `section.breakpoint` (no id)

### Structure
```
section.breakpoint   (inline style height set by JS on desktop)
  div.breakpoint__header.container > h2.breakpoint__title.display-2.reveal
  div.breakpoint__sticky
    div.container.breakpoint__inner
      div.breakpoint__lottie            <- lottie-web mounts an <svg 1280x728> here (renderer "svg")
      p.breakpoint__caption-left.body-1  (muted)
      div.breakpoint__caption#typoSimulator
        div.typo-sim__grid  (rows rendered by JS, see below)
```

### Copy
- **h2:** 40ch/7w in 2 lines. Line 1 has 3 words. Line 2 is brand-colored, 4 words ending ".". Gist: "responsive no longer an issue".
- **caption-left:** 361ch/62w, 9 lines at 312px. Gist: "small sizes barely move; try below".

### Layout (desktop)
- `.breakpoint` inline `height: calc(100vh + 400px)`. The 400 comes from `totalFrames(50) × 8`, so the section is 1300 tall at 1440x900 and 1200 at 1280x800.
- `.breakpoint__header`: `padding-top:120px; padding-bottom:0` (264 tall at 1440).
- `.breakpoint__sticky`: `position:sticky; top:0; width:100%; height:100vh; display:flex; align-items:center`. Its `.container` is width 100%.
- `.breakpoint__inner`: `position:relative`.
- `.breakpoint__lottie`: block, width 100%. Its svg is `width:100%!important; height:auto!important`, so 1248x709.8 at 1440 and 1184x673 at 1280 (aspect 1280:728).
- `.breakpoint__caption-left`: `position:absolute; left:48px; bottom:0; width: calc((100% - 96px)/4)` (312 at 1440, 296 at 1280); `color:#7e7c77; transform:translateY(60vh); will-change:transform`.
- `.breakpoint__caption` (typo sim): the same but `right:48px`.

### Typo simulator `#typoSimulator` (rendered by JS)
- `.typo-sim__grid`: flex column, gap 24.
- `.typo-sim__row`: `display:flex; align-items:flex-start; justify-content:space-between; border-top:1px solid rgba(230,227,218,.08); padding:12px 0`. The last row has `padding-bottom:0`.
- `.typo-sim__label`: caption-1 (10/500/1.333) with **letter-spacing .07em (0.7px)**, uppercase, muted, `padding-top:3px`. Labels: "Desktop", "Tablet", "Mobile".
- `.typo-sim__value`: flex column, `align-items:flex-end`, gap 16.
- Desktop row has `select.typo-sim__select`:
  - `appearance:none; background:transparent; border:1px solid transparent; border-radius:2px; color:#e6f490; font: 400 14px Roobert; padding:2px 20px 2px 4px; cursor:pointer`.
  - Chevron is a background-image data-URI: 10x6 path `M1 1l4 4 4-4`, stroke `#7E7C77`, width 1.5, round caps. Position `right 4px center`, no-repeat.
  - `transition:border-color .15s` (no hover rule defined).
  - Options use bg `#191918` and text `#e6e3da`.
  - Option values are TOKENS `[10,11,12,13,14,15,16,17,18,20,22,24,26,28,30,32,36,40,44,48,52,56,60,64,68,72,80,88,96]`, labelled "Npx". Default is **96**.
- Tablet and mobile rows show `span.typo-sim__token` (14px/400 `#e6e3da`, e.g. "72px", "40px").
- Each row has `div.typo-sim__glyph` with the text "Ag", 500 weight, color text, inline `font-size:<size>px; line-height:<lh(size)>`.
- Formula (port exactly):
  ```js
  calcRaw(t,k) = t<=16 ? t : t*(1 - k*Math.sqrt((t-16)/80));  // k: tablet .25, mobile .6
  snap(v) = nearest value in TOKENS;  tablet = snap(calcRaw(d,.25)); mobile = snap(calcRaw(d,.6))
  lh(s) = s>=32 ? 1 : s>=20 ? 1.4 : s>=16 ? 1.5 : 1.333
  ```
  For 96 this gives tablet 72 and mobile 40. On `change`, re-render the grid.
- Size at 1440: 312x424. Rows are 160 tall at 96px.

### ≤1024
- `.breakpoint`: `height:auto !important; padding: <section-padding> 0; display:flex; column; gap:60px` (40 at ≤767).
- `.breakpoint__sticky`: static, height auto, block.
- Captions: `position:static; width:100%; transform:none!important; margin-top:24px`.
- Header padding-top is the section padding (80 / 40).
- At 768: lottie 672x382, caption-left 120 tall (5 lines), sim 424 tall. At 375: lottie 327x186.

### Lottie asset
- `recon-assets/breakpoint-lottie.json` was extracted verbatim from the bundle: Bodymovin 4.8.0, `w:1280 h:728 fr:25 ip:0 op:50` (50 frames, 2s), name "Breakpoint". Load it with `lottie.loadAnimation({container, renderer:"svg", loop:false, autoplay:false, animationData})`.
- **Content:** a device mockup morphs desktop browser → tablet → phone.
  - Frames 0–27: a 1280-wide browser window (`#191918` frame, `#2a2928` chrome and 3 dots, `#0f0f0e` inner).
  - Frames 27–33 and 33–41: intermediate sizes.
  - Frames 41–50: a phone with a notch dot.
  - Inside: a serif headline (GT Super Display Bold glyphs) shrinking 72 → 56 → 56 → 40, a paragraph (Roobert Medium 16, color 0.922 gray), a pill button (Roobert SemiBold 16, dark text on light pill), and a "Try it now / Pricing" floating bar along the bottom.
- **Text is baked in as glyph shapes** (56 glyphs in `chars`), so no font files are needed.
- **COPY WARNING:** the JSON's text layers contain the original marketing copy: a 2-line headline, a ~160-char paragraph, and a button label. To comply with the content rule, edit `layers[*].t.d.k[0].s.t` to placeholder text that uses only characters present in `chars` (any glyph missing from `chars` will not render), or rebuild the mockup another way. **Build must decide this. Do not ship the JSON unedited.**

---

## 8. Presets `section.presets` (no id)

### Structure
```
section.presets > div.container
  h2.presets__title.display-2.reveal
  div.presets__grid[data-tier]      <- children generated by JS
    div.presets__item  xN
      div.presets__folder (style color: <cycle>) > svg 96x84 (recon-assets/svg/preset-folder.svg; folder path fill=currentColor, "Ag" glyph fill #0F0F0E)
      p.presets__label.body-1  "Preset {i+1}"
```

### Copy
**h2:** 57ch/10w in 3 forced lines: 3 words, then 4 words, then a brand-colored 3-word line ending ".". Gist: "save presets, import anywhere".

### Layout
- `.presets__grid`: `display:grid; grid-template-columns:repeat(12,1fr); align-items:center; gap:24px; margin-top:48px; padding-top:104px` (the padding gives the wave room to rise).
  - Desktop: **12 items**, columns 82px at 1440 and 76.66 at 1280.
  - ≤1024: `repeat(8,1fr)`, gap 16, margin-top 36, padding-top 72, **8 items**, folder `max-width:80px` (70px columns at 768).
  - ≤767: `repeat(5,1fr)`, gap 16, margin-top 28, padding-top 40, **5 items**, folder `max-width:56px`, label 12px/18px (52.6px columns at 375).
- `.presets__item`: flex column, `align-items:flex-start`, gap 12, `will-change:transform; min-width:0`.
- `.presets__folder`: width 100%, `aspect-ratio:96/84`; svg is block 100%/100% (82x71.8 at 1440).
- `.presets__label`: muted, left-aligned, `white-space:nowrap`, body-1.
- Folder colors cycle in index order: `["#E6F490","#0469FF","#DCBDC2","#FE8A3D","#E6E3DA"]`.
- The tier is chosen by matchMedia: mobile `(max-width:767px)` gets 5, tablet `(max-width:1024px)` gets 8, otherwise 12. The grid re-renders on resize when the tier changes.

---

## 9. Exports `section.exports` (no id; the second card has `id="ai-prompt"`)

### Structure
```
section.exports > div.container > div.exports__wrapper
  h2.exports__title.display-2.reveal
  div.exports__cards
    div.exports__card.reveal
      div.exports__media > img css-export-DPacxBL7.jpg (707x553)
      div.exports__text
        h3.exports__card-title.heading-1 "CSS"
        p.exports__card-text.body-1
        div.exports__card-logos > svg32 (Cursor cube) + svg32 (VS Code)
    div.exports__card.exports__card--reverse.reveal#ai-prompt (--reveal-delay:100ms)
      div.exports__text
        h3.exports__card-title.heading-1 "AI Prompt" + span.tag.caption-1 "NEW"
        p.exports__card-text.body-1
        div.exports__card-logos > svg32 Claude + Cursor + OpenAI + Lovable
      div.exports__media > img ai-prompt-B1wIQtkI.jpg (707x553)
```

### Copy
- **h2:** 50ch/8w in 2 lines. Line 1 has 3 words. Line 2 has 1 plain word followed by a 3-word brand span ending ".". Gist: "design and dev never closer".
- **CSS text:** 325ch/51w, 5 lines at 506px. Gist: "every value exports as CSS variables".
- **AI text:** 468ch/77w, 7 lines. Gist: "describe font roles once for AI".

### Layout
- Wrapper and cards are both flex columns with **gap 80** (60 at ≤1024, 40 at ≤767).
- `.exports__card`: `grid; repeat(12,1fr); gap:24px; align-items:center`.
- Media: `grid-column:1/span 6; border-radius:4px; overflow:hidden; background:#0f0f0e`. The img is block, width 100%, height auto (612x479 at 1440, 580x454 at 1280).
- Text: `grid-column:8/span 5` (x=838, 506 wide at 1440).
- Reverse card: text `1/span 5`, media `7/span 6`.
- `.exports__card-title`: flex, `align-items:center`, gap 8 (tag sits inline).
- `.exports__card-text`: muted, margin-top 16.
- `.exports__card-logos`: flex, gap 16, margin-top 24. Logos are 32x32 SVGs filled `#E6E3DA`.
- ≤1024:
  - Cards are a single column (`grid-template-columns:1fr`) with gap 24, and all children use `grid-column:1`.
  - Reverse card media gets `order:-1`, so the image always comes first.
  - Media is 672x526 at 768 and 327x256 at 375.

---

## 10. Pricing `section.pricing#pricing`

### Structure
```
section.pricing#pricing > div.container > div.pricing__wrapper (flex column, no gap)
  h2.pricing__title.display-2.reveal   (4 words: 3 plain + 1 brand word in span.pricing__title--brand, ends ".")
  div.pricing__grid
    div.pricing-plan.pricing-plan--featured.reveal (delay 0ms)   [--featured has no extra CSS]
    div.pricing-plan.reveal (150ms)
    div.pricing-plan.reveal (300ms)
      div.pricing-plan__content
        div.pricing-plan__top
          div.pricing-plan__header
            p.pricing-plan__name.heading-2        "Freelancer" | "Studio" | "Enterprise"
            p.pricing-plan__subtitle.heading-2    "For individual creators" | "For teams and agencies" | "Need more licenses?"
          p.pricing-plan__license.body-2          "Single License" | "5 Licenses" | "Custom Licenses"
        div.pricing-plan__price.display-3         "€39,99" | "€159,99" | "Let's talk"
      div.pricing-plan__seam > div.pricing-plan__seam-notch
      div.pricing-plan__cta > a.btn.btn--brand.btn--sm.button-2 "Get Plan"   (3rd plan: btn--primary "Contact Us")
  div.pricing-includes.reveal
    h3.pricing-includes__title.heading-2 "Everything included"
    div.pricing-includes__columns
      ul.pricing-includes__list x2 > li.pricing-includes__item x4
        span.pricing-includes__check > svg 16x16 (check.svg: stroke white, width 2)
        span.pricing-includes__text.body-1
```
- Items in list 1: "Save Presets", "Export Frames", "Export Text Styles", "Primitives & Semantic Variables".
- Items in list 2: "Editable Design Tokens", "Desktop, Tablet and Mobile Breakpoints", "CSS Export", "Generate AI Prompt" + tag "NEW".
- Title gist: "buy once, forever"; 21ch, 1 line.

### Links
- Freelancer: `https://typewave.lemonsqueezy.com/checkout/buy/f38b86ac-2475-4b2b-a7a8-67abd5d7cfec` (`target=_blank rel="noopener noreferrer"`).
- Studio: `https://typewave.lemonsqueezy.com/checkout/buy/65e62acf-90b0-4084-90e6-62ab198548a4`.
- Enterprise: `mailto:hello@blendmodes.com?subject=Typewave%20Enterprise%20Licenses`.

### Layout
- `.pricing__grid`: `grid; repeat(3,1fr); gap:24px; align-items:start; margin-top:80px`. Columns are 400 at 1440 and 378.66 at 1280.
  - ≤1024: single column, gap 16, margin-top 60.
  - ≤767: margin-top 40.
- `.pricing-plan`: flex column, `background:#0f0f0e; border-radius:8px; overflow:hidden`. 400x364 at 1440.
- `.pricing-plan__content`: flex column, gap 32, padding 32, bg `#191918`, bottom-left and bottom-right radius 8 (240 tall).
- `.pricing-plan__top`: column, gap 16.
- `.pricing-plan__header`: column, gap 4.
- Name is heading-2 in text color. Subtitle is heading-2 muted. License is body-2 muted. Price is display-3: 56px desktop, 32 at ≤1024, and at ≤767 it is overridden to display-1-mobile, **40px**/1.
- **Ticket seam** `.pricing-plan__seam`:
  - `display:flex; height:12px; background:#0f0f0e`.
  - The `.pricing-plan__seam-notch` child: `position:relative; flex:1 1 auto; margin-inline:24px; background:#191918`.
  - `::before` and `::after`: 12x12 circles (`border-radius:50%`, bg `#0f0f0e`) at `top:50%`. Before is at `left:0; translate(-50%,-50%)`; after is at `right:0; translate(50%,-50%)`.
  - The effect is a perforation gap with semicircle notches.
- `.pricing-plan__cta`: flex, padding 32, bg `#191918`, top-left and top-right radius 8 (112 tall). Its button is `width:100%; height:48px; justify-content:center`.
- ≤767: content and CTA padding 24.
- `.pricing-includes`: flex column, gap 32, padding 48, margin-top 24, bg `#191918`, radius 8 (1248x284 at 1440).
  - Columns: `grid; repeat(2,1fr); gap:16px 88px` (532px columns at 1440).
  - List: flex column, gap 12, no bullets. Item: flex, `align-items:center`, gap 12.
  - ≤767: padding 24, gap 24, columns become `1fr` with gap 24.

---

## 11. FAQ `section.faq#faq`

### Structure
```
section.faq#faq > div.container > div.faq__inner
  div.faq__lead
    h2.faq__title.display-2.reveal   (2 lines: 1 word / brand span "& ..." 2 words; 19ch)
    a.faq__email.body-1.reveal (150ms) href="mailto:hello@blendmodes.com"   "hello@blendmodes.com"
  div.faq__list.reveal
    div.faq__item x7
      button.faq__question.subtitle-1
        span.faq__question-text
        span.faq__chevron > svg 24x24 (chevron.svg: path M8 10L12 14L16 10, stroke #E6E3DA width 2)
      div.faq__answer
        div.faq__answer-inner
          p.faq__answer-text.body-1  (1–2 per item; 2nd has inline style margin-top:16px)
          [item 4 only] img.faq__answer-image token-Dmg8Y-M9.png (869x650, alt ~87 chars)
          [item 7 only] the paragraph contains a.faq__answer-link mailto:hello@blendmodes.com
```

### Copy (questions are short UI labels; answers are gists only)
| # | Question chars/words | Answer paragraphs (chars, lines @612) | Answer gist |
|---|---|---|---|
| 1 | 36/5 "what does it generate" | 255 (5L) + 82 (2L) | "complete system, single source" |
| 2 | 37/6 "how responsive scaling works" | 473 (7L) | "set desktop, square-root scaling" |
| 3 | 35/6 "customize font hierarchy" | 331 (5L) | "rename, adjust, up to 5 families" |
| 4 | 46/9 "control over design tokens" | 324 (5L) + 206 (4L) + image | "edit tokens in settings" |
| 5 | 33/7 "what AI prompt is for" | 285 (5L) | "role definitions bundled for AI" |
| 6 | 29/5 "why it costs money" | 296 (5L) | "funds ongoing tool development" |
| 7 | 30/7 "found bug / need feature" | 20 + email link + 236 (≈5L total) | "reach out, we use it" |

### Layout
- `.faq__inner`: `grid; 1fr 1fr; gap:24px; align-items:start` (612 + 612 at 1440, 580 + 580 at 1280). ≤1024: single column, gap 48.
- `.faq__lead`:
  - Flex column, gap 32, `position:sticky; top: calc(88px + 32px) = 120px`, `transition: top .35s cubic-bezier(.4,0,.2,1)`.
  - When `html.navbar-hidden` is set, `top:32px`.
  - ≤1024: `position:static`.
- `.faq__email`: muted, underline, `text-underline-offset:3px`; **hover color `#e6e3da`** (0.2s).
- `.faq__item`: `border-top:1px solid #191918`. The last item also has `border-bottom:1px solid #191918`.
- `.faq__question`:
  - `width:100%; display:flex; align-items:center; justify-content:space-between; gap:16px; padding:24px 0`.
  - No bg or border; `color:#e6e3da; text-align:left; touch-action:manipulation`.
  - Height is 76 at desktop (20/28), 73 at 768 (18/25.2), 72 at 375 (16/19.2; questions wrap).
- `.faq__question-text`: `flex:1`.
- `.faq__chevron`: flex, `flex-shrink:0`, `transition:transform .35s cubic-bezier(.4,0,.2,1)`. Open state is `rotate(180deg)`.
- `.faq__answer`: `display:grid; grid-template-rows:0fr; overflow:hidden; transition:grid-template-rows .35s cubic-bezier(0,0,.2,1)`. Open state is `1fr`.
- `.faq__answer-inner`: `overflow:hidden; min-height:0`.
- `.faq__answer-text`: muted, `padding-bottom:24px`.
- `.faq__answer-image`: block, width 100%, `border-radius:4px; margin-bottom:24px`.
- `.faq__answer-link`: text color, underline offset 3; **hover color brand `#e6f490`**.
- **Behaviour:**
  - It is a single-open accordion. Clicking a question closes all items and then opens the clicked one; clicking an open item closes it.
  - Toggling sets `aria-expanded` on the button and `aria-hidden` on the answer.
  - On desktop (≥1025) a document click outside `.faq` closes all items.
  - All items start closed.

---

## 12. Newsletter `section.newsletter`

### Structure
```
section.newsletter > div.container > div.newsletter__inner
  div.newsletter__content.reveal > h2.newsletter__title.display-2   (2 words: 1 plain + 1 in span.newsletter__title--brand; 12ch)
  form.newsletter__form.reveal (150ms) action="https://typewave.lemonsqueezy.com/email-subscribe/external" method="post" target="_blank"
    div.newsletter__field
      input.newsletter__input.display-2 type=email name=email placeholder="your@email.com"
      button.newsletter__submit[type=submit aria-label="Subscribe"] > span.display-2 "→"
```

### Layout
- `.newsletter`: `padding-top:<section-padding>; padding-bottom:40px; border-top:1px solid #191918`.
- `.newsletter__inner`: flex column, `align-items:flex-start`, gap 0.
- Title is display-2 (72/48/32).
- Form: `width:100%; position:relative`.
- Field: flex, `align-items:center`, gap 32.
- Input:
  - `flex:1; min-width:0; background:none; border:none; outline:none; color:#e6e3da`, in display-2 type.
  - Placeholder color is `#7e7c77`.
  - Rendered height is **86** at desktop, 58 at 768 and 39 at 375. That is the input's natural line box, so do not force line-height.
- Submit: `background:none; border:none; padding:0; color:#e6e3da; cursor:pointer; transition:color .2s`; **hover color `#e6f490`**. The arrow glyph uses display-2 type (50x86 at 1440).
- `.newsletter__feedback` styles exist (absolute `top:calc(100% + 8px)`, muted / `.is-success` text / `.is-error` `#df3535`), but **no element or JS uses them**. The form is a plain POST in a new tab.

---

## 13. Footer `footer.footer`

### Structure
```
footer.footer (bg #0f0f0e)
  div.container.footer__container
    div.footer__hero.reveal
      div.footer__logo > svg 44x40 (footer-logo.svg)
      h1.footer__title.display-3  (2 lines: "The" + brand span 2 words + "for" / 3 words; 40ch)   [excluded from char-compose]
      div.footer__cta > a.btn.btn--primary.btn--sm (Figma icon + "Try it now") -> Figma URL
    div.footer__bottom.reveal (150ms)
      p.footer__copy.caption-1  "© 2026 Blendmodes"
      nav.footer__legal
        a.footer__legal-link.caption-1 "Privacy policy"      -> https://www.lemonsqueezy.com/privacy (blank, noopener)
        a.footer__legal-link.caption-1 "Terms & conditions"  -> https://www.lemonsqueezy.com/buyer-terms
```
Footer title gist: "starting point for all projects".

### Layout
- `.footer__container`: flex column, gap 60, padding 24 top and 40 bottom (inline padding from container).
- `.footer__hero`:
  - Flex column, `align-items:center`, gap 32, `text-align:center`, `padding:96px 0`, bg `#191918`, radius 8.
  - Size: 1248x448 at 1440, 672x400 at 768, 327x384 at 375. ≤767 adds `padding-inline:48px`.
- Footer title: 56px at desktop (529 wide, 2 lines), 32 at ≤1024, 24 at ≤767.
- `.footer__bottom`: flex, `space-between`, `align-items:center` (13.3 tall).
- `.footer__copy` is muted.
- `.footer__legal`: flex, gap 32.
- Legal link: muted, no underline; **hover color `#e6e3da` + underline** (offset 3px, color 0.2s).

---

## 14. Floating CTA, affiliate and type inspector

### Floating CTA `div.floating-cta` (sibling after footer)
- Contents: `a.btn.btn--primary.btn--sm` (Figma icon + "Try it now", Figma URL) and `button.btn.btn--ghost.button-2[data-scroll-to="#pricing"]` "Pricing". The ghost button has no `--sm`, so there is no padding (50x16).
- Styles:
  - `position:fixed; bottom:24px; left:50%; z-index:90; display:flex; align-items:center; gap:24px; padding:8px 24px 8px 8px; border-radius:8px; background:#0f0f0ecc; backdrop-filter:blur(12px); white-space:nowrap; pointer-events:none`.
  - Hidden state is `transform: translate(-50%, calc(100% + 24px))`.
  - Size: 231.2x56 desktop, 216x56 at ≤1024.
- `.is-ready` (added after two rAFs, so there is no transition on first paint) sets `transition: transform .4s cubic-bezier(.4,0,.2,1)`.
- `.is-visible` sets `transform:translate(-50%); pointer-events:auto`.
- **Visibility rule** (rAF-throttled scroll and resize): visible only when **all** of these hold:
  - `heroVideo.getBoundingClientRect().top <= 0`
  - `newsletterField.top > innerHeight`
  - the navbar is hidden (`.navbar--hidden`)
  
  In practice it slides up while scrolling down and hides when the user scrolls up (the navbar returns) or reaches the newsletter.
- The "Pricing" button runs `lenis.scrollTo("#pricing",{offset:-80})`.

### Affiliate (`https://lmsqueezy.com/affiliate.js`, third-party, deferred)
- Config: `window.lemonSqueezyAffiliateConfig = { store: "typewave" }`.
- If the URL has `?aff=<code>`, the script POSTs to `https://app.lemonsqueezy.com/affiliates/track` (with a FingerprintJS visitor id) and stores the click id in the cookie `ls_aff_ref`.
- It then rewrites every Lemon Squeezy checkout link on the page (and watches the DOM with MutationObserver) to append `?aff_ref=<clickId>`.
- There is no visual impact. Include the two script tags and keep checkout links as plain `<a href>` so the script can find them.

### Type-inspector cursor badge (desktop pointers only)
- Only runs if `matchMedia("(pointer: fine)")`.
- It appends a `<style>` and a `div.type-inspector-badge` to `<body>`. On `mousemove`, if the target is inside any element with one of the type-scale classes (`display-1 … caption-1`), the badge shows that class name (e.g. "display-2") at `clientX+16, clientY+16`.
- Badge styles: `position:fixed; z-index:99999; background:#191918; color:#E6F490; font:11px/1 'SF Mono','Menlo',monospace; padding:4px 8px; border-radius:4px; border:1px solid #2A2928; pointer-events:none; white-space:nowrap; opacity:0; transition:opacity .12s ease`. `.is-visible` sets opacity 1.
- It hides when the target is not a type-scale element, on `mouseleave` of the document, and on scroll if the element under the last cursor point is no longer a match.
- There is no custom cursor beyond this.

---

## 15. Motion inventory

| # | Effect | Target | Trigger | Implementation (exact) | Breakpoints |
|---|---|---|---|---|---|
| M1 | Smooth scroll | page | wheel | Lenis 1.3.x `{duration:1.4, easing:t=>1-Math.pow(1-t,5), smoothWheel:true}`, rAF loop `lenis.raf(t)`. Created only if `matchMedia("(max-width:1024px)")` is false **at load** (not re-evaluated). Otherwise use a shim whose `scrollTo` runs `window.scrollTo({behavior:"smooth"})` and whose `on/off/stop/start` are no-ops | ≥1025 |
| M2 | Reveal (fade-up) | every `.reveal` | IntersectionObserver `threshold:0.15`, once (unobserve) | `.reveal{opacity:0;transform:translateY(32px);transition:opacity .7s ease, transform .7s ease;transition-delay:var(--reveal-delay,0ms)}`; `.is-visible{opacity:1;transform:translateY(0)}`. On init and on resize, any element whose rect overlaps the viewport is revealed immediately | all (figma cards forced visible ≤1024) |
| M3 | Reveal stagger delays | see sections | | hero 0/150/300/450ms; how-it-works title 150; figma cards 0/100/200; export cards 0/100; plans 0/150/300; FAQ email 150; newsletter form 150; footer bottom 150; all others 0 | all |
| M4 | Scroll-composed characters | every `h1`/`h2` with `.display-1` or `.display-2` except `.footer__title` (hero h1 and all 8 section h2s, including newsletter) | scroll / resize (rAF-throttled, native `scroll` event) | Wrap each non-space run in `span.compose-word{display:inline-block}`, and each char in `span.compose-char{display:inline-block;will-change:opacity}`. Keep `<br>` and nested spans, recursing into element children. For each heading in the viewport: `start=0.9*vh`, `end=0.45*vh`, `E=clamp01((start-rect.top)/(start-end))`. For char i of n: `d=(i/n)*(1-0.35)`, `opacity=clamp01((E-d)/0.35)`. Opacity is set inline with no CSS transition (scrubbed). Skip if `prefers-reduced-motion: reduce` | all |
| M5 | Parallax | `[data-parallax]`: `.hero__wrapper` −0.02, `.hero__content` −0.08, `.how-it-works__header` −0.04 | Lenis `scroll` event | `el.style.transform = translateY(${lenis.scroll * factor}px)`, applied only while the closest `<section>` intersects the viewport. CSS `will-change:transform`. At ≤1024 transforms are cleared | ≥1025 |
| M6 | Hero video scale-up | `.hero__video-scale` | scroll (rAF) | **Position:** `top = vh − 0.06*vh − (H*(1−0.8))/2` (H = offsetHeight). That is 775.8px at 1440x900; only the top 6% of the scaled video peeks above the fold. **Scale:** `0.8 + 0.2*clamp01(scrollY / o)`, where `o = containerDocTop − (vh − scaledRectH)/2` is computed at init (≈676.8 at 1440x900), so it reaches scale 1 when centred. **Hero height:** `.hero` inline `min-height = max(vh, videoCenterDocY + H/2 − heroTop + sectionPadding)`. Recompute top, o and min-height on resize | ≥1025 |
| M7 | Hero video playback | `video.hero__image` (2.03s clip, no loop) | scroll | At init: `autoplay=false; loop=false; pause()`, plus a `play().then(pause)` prime. Plays at rate 1 once the user is scrolling **down** and the video centre is ≤ vh. When it fully leaves the viewport: `pause(); currentTime=0`, re-armed for the next entry. It plays once per entry and stops on the last frame | all |
| M8 | Sticky stacking cards | `.how-it-works__cards .card` | Lenis scroll (after `window.load`) | Cards are `position:sticky; top:r`, with `r=(vh − card0.offsetHeight)/2`. For card i: `p = 0.75 + 0.25*clamp01((vh − rect.top)/(vh − r))` (grows from 0.75 to 1 as it rises to centre). If there is a next card: `S = 1 − 0.25*clamp01((vh − next.top)/(vh − r))` (shrinks back to 0.75 as the next card arrives). `scale(min(p,S))`, `transform-origin:center`. Each card's video plays (`.play()`, once, loops via attr) the first time its scale ≥ 0.98 | ≥1025 |
| M8b | Card videos (≤1024) | `.card video` | `window.load` | all `.play()` immediately | ≤1024 |
| M9 | Lottie scrub (desktop) | `.breakpoint__lottie` | native scroll | `progress = clamp01((scrollY − sectionDocTop)/(section.offsetHeight − vh))`. `frame = clamp01((progress − 0.2)/0.6) * (totalFrames − 1)` via `anim.goToAndStop(frame, true)` (frames 0–49). Section height `calc(100vh + totalFrames*8 px)` is set on `DOMLoaded`, then a `resize` is dispatched | ≥1025 |
| M10 | Caption slide-up | `.breakpoint__caption-left`, `.breakpoint__caption` | same scroll | `translateY( (1 − clamp01((progress − 0.5)/0.5)) * vh * 0.6 px)`. CSS initial is `translateY(60vh)`; they rise into place over the second half of the scrub | ≥1025 |
| M9b | Lottie scrub (≤1024) | `.breakpoint__lottie` | scroll | `A = lottieDocTop + lottie.clientHeight − vh`, `C = lottieDocTop`, `progress = clamp01((scrollY − A)/(C − A))`, and the frame uses the same 0.2–0.8 window. Captions are static | ≤1024 |
| M11 | Preset folder wave | `.presets__item` | native scroll | `p = clamp01((0.8*vh − grid.top)/(0.8*vh − 0.2*vh))`. For item c of d: `m = (c/(d−1))*(1−0.35)`, `u = clamp01((p−m)/0.35)`, `translateY(−sin(u*π)*AMP)`. AMP is **88** desktop, **50** tablet, **22** mobile. The result is a single travelling bump left→right; each folder rises and settles back to 0. Skip if reduced motion | all |
| M12 | Navbar hide/show | `.navbar` | scroll direction | `.navbar--hidden{transform:translateY(-100%)}`, `.35s cubic-bezier(.4,0,.2,1)`. Hidden when scrolling down and `scrollY>80`. Toggles `html.navbar-hidden` | all |
| M13 | FAQ sticky lead offset | `.faq__lead` | `html.navbar-hidden` | `top` 120px ↔ 32px, `.35s cubic-bezier(.4,0,.2,1)` | ≥1025 |
| M14 | FAQ accordion | `.faq__answer`, `.faq__chevron` | click | rows `0fr→1fr` `.35s cubic-bezier(0,0,.2,1)`; chevron `rotate(180deg)` `.35s cubic-bezier(.4,0,.2,1)` | all |
| M15 | Floating CTA | `.floating-cta` | scroll | `translate(-50%, calc(100% + 24px))` → `translate(-50%)`, `.4s cubic-bezier(.4,0,.2,1)` (transition enabled after 2 rAFs) | all |
| M16 | Mobile menu | `.navbar__mobile-menu`, hamburger lines | click | menu `opacity 0→1`, `scale(.96)→1` (origin top center) `.3s` ease-standard; lines rotate ±45° with ±4px translate `.35s` | ≤1024 |
| M17 | Hover colors | buttons and links | hover | `.btn` bg `.2s ease`; ghost color (instant); email, links, submit color `.2s` | all |
| M18 | Type-inspector badge | cursor | mousemove | opacity `.12s ease`; follows cursor +16/+16 | pointer:fine |

JS init order (it matters for M4, which wraps characters after the reveal setup): `hydrateNavbar → hydrateHowItWorks (cards) → initBreakpoint (lottie) → initTypoSimulator → initPresets → hydrateFaq → initHeroVideoAutoplay → initFloatingCta → initTypeInspector → initReveal → initParallax(lenis) → initScrollCompose`.

React note: implement these as `useEffect` hooks attached to refs or class selectors after mount. M4 mutates heading DOM. Either render the char spans from React (preferred: split the strings in JSX, keeping brand spans and `<br className="title-break">`) or run the wrapper on a ref whose children React will not re-render.

---

## 16. Page geometry summary (section top y / height in px)

| Section | 1440x900 | 1280x800 | 768x1024 | 375x812 |
|---|---|---|---|---|
| hero | 0 / 1597.8 | 0 / 1471 | 0 / 1144 | 0 / 765 |
| how-it-works | 1597.8 / 2788 | 1471 / 2680 | 1144 / 2764 | 765 / 2028 |
| figma-org | 4385.8 / 972 | 4151 / 980 | 3908 / 965 | 2792 / 658 |
| breakpoint | 5357.8 / 1300 | 5131 / 1200 | 4873 / 1370 | 3451 / 1098 |
| presets | 6657.8 / 715.8 | 6331 / 711 | 6243 / 509 | 4549 / 320 |
| exports | 7373.5 / 1501.4 | 7042 / 1451 | 6752 / 1907 | 4869 / 1470 |
| pricing | 8874.9 / 1064 | 8494 / 1064 | 8659 / 1652 | 6339 / 1536 |
| faq | 9938.9 / 780 | 9558 / 780 | 10311 / 880 | 7875 / 742 |
| newsletter | 10718.9 / 319 | 10338 / 319 | 11192 / 227 | 8618 / 152 |
| footer | 11037.9 / 585.3 | 10657 / 585 | 11419 / 537 | 8769 / 521 |
| **document** | **11623** | **11242** | **11956** | **9290** |

(The how-it-works height includes the card stack. Card gap is 80 and three cards are 700 each at 1440.)

---

## 17. Assets

The full manifest with usage mapping is in `ASSET_MANIFEST.md` next to this file. Summary of what the live site loads:
- Fonts: only Roobert Regular (400) and Medium (500).
- Videos:
  - `intro-DrshnI3i.mp4`: 1920x1078, 2.03s, hero; `muted playsinline preload=auto`, no autoplay or loop.
  - `def1--g7RFuQa.mp4`: 1200x900, 8.88s, card 1.
  - `def2-0T0-0aPX.mp4`: 1200x900, 8.88s, card 2.
  - `loop3-CWAyqkgp.mp4`: 1200x900, 5.2s, card 3.
  - The card videos are `loop muted playsinline preload=metadata`, with no autoplay attribute (JS plays them). No poster attributes anywhere.
- Images:
  - `frame-Cg0zK82j.png`, `styles-DpEOnP78.png`, `variable-fdRUIB1a.png`: 800x600 PNG, figma cards.
  - `css-export-DPacxBL7.jpg`, `ai-prompt-B1wIQtkI.jpg`: 707x553 JPG, exports.
  - `token-Dmg8Y-M9.png`: 869x650, FAQ item 4.
  - None are lazy-loaded.
- Inline SVGs (extracted to `recon-assets/svg/`): navbar logo 171x40, footer logo mark 44x40, Figma button icon 16x17, check 16x16, chevron 24x24, preset folder 96x84, and logos (Cursor, VS Code, Claude, Cursor variant, OpenAI, Lovable) at 32x32 with fill `#E6E3DA`.
- Lottie JSON: `recon-assets/breakpoint-lottie.json`. Edit its baked copy before shipping (see section 7).

## 18. Unverified / not reachable
- The Lottie's internal keyframe easing was not analysed per layer. The JSON is used verbatim, so this is only relevant if you rebuild the mockup by hand.
- `affiliate.js` network behaviour is inferred from reading the minified third-party source and was not exercised with a live `?aff=` param.
- Hover was not interactively tested in the browser. Hover values come from the original CSS rules quoted above, which are authoritative.

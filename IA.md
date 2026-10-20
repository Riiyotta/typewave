# https://typewave.blendmodes.com/ (local React clone in this folder)

Source: https://typewave.blendmodes.com/ (local React clone in this folder)
Status: **measured-from-clone** · production approved: **false**
1 routes · 1 templates · 13 unique sections

> Generated from `ia.json` by `build.mjs`. Edit the JSON, not this file.

## Shape of the site

The largest 1 template (Home (single-page marketing site)) accounts for 1 of 1 routes (100%). The remaining 0 routes span 0 templates.

| template | routes | share |
|---|---:|---:|
| Home (single-page marketing site) | 1 | 100% |

## Page chrome

**1 routes carry chrome = `full`** — Home (single-page marketing site).

## Sections by reuse

How widely a section is shared determines whether it belongs in a shared
component library or stays local to its page.

| section | category | templates | routes | implementation | scope |
|---|---|---:|---:|---|---|
| `chrome.navbar` | CHROME | 1 | 1 | `src/components/Navbar.jsx` | Present on the single route (/), rendered before <main>. |
| `hero.product-intro` | HERO | 1 | 1 | `src/components/Hero.jsx` | Opens <main> on the single route (/). |
| `features.how-it-works-stack` | FEATURES | 1 | 1 | `src/components/HowItWorks.jsx` | Second block of <main> on the single route (/), anchor target #how-it-works. |
| `features.figma-organization-cards` | FEATURES | 1 | 1 | `src/components/FigmaOrg.jsx` | Third block of <main> on the single route (/). |
| `features.breakpoint-scrub` | FEATURES | 1 | 1 | `src/components/Breakpoint.jsx > BreakpointMock, TypoSimulator` | Fourth block of <main> on the single route (/). |
| `features.preset-folders` | FEATURES | 1 | 1 | `src/components/Presets.jsx` | Fifth block of <main> on the single route (/). |
| `features.export-cards` | FEATURES | 1 | 1 | `src/components/Exports.jsx` | Sixth block of <main> on the single route (/). |
| `commerce.pricing-plans` | COMMERCE | 1 | 1 | `src/components/Pricing.jsx` | Seventh block of <main> on the single route (/), anchor target #pricing. |
| `support.faq-accordion` | SUPPORT | 1 | 1 | `src/components/Faq.jsx` | Eighth block of <main> on the single route (/), anchor target #faq. |
| `conversion.newsletter-signup` | CONVERSION | 1 | 1 | `src/components/Newsletter.jsx` | Last block of <main> on the single route (/). |
| `chrome.footer` | CHROME | 1 | 1 | `src/components/Footer.jsx` | Present on the single route (/), rendered after <main>. |
| `conversion.floating-cta` | CONVERSION | 1 | 1 | `src/components/FloatingCta.jsx` | Rendered after the footer on the single route (/). |
| `overlay.type-inspector` | OVERLAY | 1 | 1 | `src/components/TypeInspector.jsx` | Mounted last on the single route (/). |

**0 shared sections** appear in more than one template and belong in a component library.

**13 single-use sections** appear in exactly one template. Building these
as "reusable" components up front would be speculative — keep them page-local
until a second caller actually appears.

## Templates

### Home (single-page marketing site) — `template.home`

1 route · `/` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.navbar` | page-local |
| 2 | HERO | `hero.product-intro` | page-local |
| 3 | FEATURES | `features.how-it-works-stack` | page-local |
| 4 | FEATURES | `features.figma-organization-cards` | page-local |
| 5 | FEATURES | `features.breakpoint-scrub` | page-local |
| 6 | FEATURES | `features.preset-folders` | page-local |
| 7 | FEATURES | `features.export-cards` | page-local |
| 8 | COMMERCE | `commerce.pricing-plans` | page-local |
| 9 | SUPPORT | `support.faq-accordion` | page-local |
| 10 | CONVERSION | `conversion.newsletter-signup` | page-local |
| 11 | CHROME | `chrome.footer` | page-local |
| 12 | CONVERSION | `conversion.floating-cta` | page-local |
| 13 | OVERLAY | `overlay.type-inspector` | page-local |

## Section reference

### CHROME

_Persistent page furniture rendered outside <main>: top navigation and footer._

**`chrome.navbar`** — Fixed 88px top bar (80px on mobile): brand mark, three in-page anchor links, and a Figma call-to-action button. Hides on scroll-down past 80px and returns on scroll-up; collapses to a hamburger with a full-height overlay menu at 1024px and below.

· Present on the single route (/), rendered before <main>. · appears on 1 routes · implemented by `src/components/Navbar.jsx`

**`chrome.footer`** — Large closing title with the brand logo and a Figma button, then a bottom row with copyright and legal links.

· Present on the single route (/), rendered after <main>. · appears on 1 routes · implemented by `src/components/Footer.jsx`

### HERO

_Page-opening block above and just below the fold._

**`hero.product-intro`** — Centered three-line display-1 headline (last line in the brand colour), a short subtitle and a Figma button, followed by a product demo video that peeks above the fold and scales from 0.8 to 1 as the page scrolls; the video plays once on scroll-down and rewinds on exit.

· Opens <main> on the single route (/). · appears on 1 routes · implemented by `src/components/Hero.jsx`

### FEATURES

_Product explanation modules showing what the plugin generates and how._

**`features.how-it-works-stack`** — Three-step explainer: a parallax section header above three sticky full-width video cards that scale between 0.75 and 1 as each arrives and is covered by the next; each card's video starts once it reaches 0.98 scale. Plain stacked autoplaying cards on mobile.

· Second block of <main> on the single route (/), anchor target #how-it-works. · appears on 1 routes · implemented by `src/components/HowItWorks.jsx`

**`features.figma-organization-cards`** — Three image cards showing the Figma artefacts the plugin creates (frames, text styles, variables), laid out as a 3-column grid on desktop and a horizontal swipe carousel at 1024px and below.

· Third block of <main> on the single route (/). · appears on 1 routes · implemented by `src/components/FigmaOrg.jsx`

**`features.breakpoint-scrub`** — Tall scroll stage (100vh + 400px) with a sticky device mockup that morphs desktop → tablet → phone across the middle 60% of its scroll, two captions that slide up over the second half, and an interactive type-size simulator panel. The mockup is an HTML/CSS rebuild; the original Lottie is not reused.

· Fourth block of <main> on the single route (/). · appears on 1 routes · implemented by `src/components/Breakpoint.jsx > BreakpointMock, TypoSimulator`

**`features.preset-folders`** — Row of coloured preset folder icons (12 / 8 / 5 per desktop / tablet / mobile) with a single sine-wave lift that travels left to right as the section scrolls through view.

· Fifth block of <main> on the single route (/). · appears on 1 routes · implemented by `src/components/Presets.jsx`

**`features.export-cards`** — Two side-by-side cards, each a screenshot plus title and paragraph, covering the CSS export and the AI-prompt export (the second card carries id ai-prompt).

· Sixth block of <main> on the single route (/). · appears on 1 routes · implemented by `src/components/Exports.jsx`

### COMMERCE

_Plans, prices and checkout entry points._

**`commerce.pricing-plans`** — Section title, three plan cards (two with checkout links, one enterprise mailto) each split by a 12px notched 'ticket' seam between price and button, then an 'everything included' feature list with one tagged item.

· Seventh block of <main> on the single route (/), anchor target #pricing. · appears on 1 routes · implemented by `src/components/Pricing.jsx`

### SUPPORT

_Question-and-answer content that resolves buyer objections._

**`support.faq-accordion`** — Two-column FAQ: a sticky lead column (title, contact link, illustration) whose top offset moves between 120px and 32px with the navbar, beside a single-open accordion list with rotating chevrons.

· Eighth block of <main> on the single route (/), anchor target #faq. · appears on 1 routes · implemented by `src/components/Faq.jsx`

### CONVERSION

_Lead capture and persistent call-to-action surfaces outside the main narrative._

**`conversion.newsletter-signup`** — Centered title, short text and an email field with an inline submit button that posts to an external newsletter endpoint in a new tab.

· Last block of <main> on the single route (/). · appears on 1 routes · implemented by `src/components/Newsletter.jsx`

**`conversion.floating-cta`** — Fixed bottom-centre pill holding a Figma button; slides in only while the navbar is hidden, the hero video has scrolled past, and the newsletter is not yet in view.

· Rendered after the footer on the single route (/). · appears on 1 routes · implemented by `src/components/FloatingCta.jsx`

### OVERLAY

_Pointer-following or fixed UI layered over the page, not part of the document flow._

**`overlay.type-inspector`** — Small monospace badge that follows the mouse and names the type-scale class of the text under the cursor; fine-pointer devices only, hidden on scroll.

· Mounted last on the single route (/). · appears on 1 routes · implemented by `src/components/TypeInspector.jsx`

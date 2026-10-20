Source: https://typewave.blendmodes.com/

# Asset manifest (Typewave clone)

| File (path in project) | Type | Intrinsic | Used in | Rendered size @1440 | Attributes / notes |
|---|---|---|---|---|---|
| public/assets/Roobert-Regular-BNQS-qUa.woff2 | font | 400 normal | all body/400 text | | preload as=font crossorigin |
| public/assets/Roobert-Medium-Jj6nDRYB.woff2 | font | 500 normal | headings, buttons, captions | | preload as=font crossorigin |
| public/assets/Roobert-{Light,SemiBold,Bold,Heavy}-*.woff2 | font | 300/600/700/800 | declared via @font-face, never rendered | | optional |
| public/assets/Vesterbro-*.woff2 (9 files) | font | | declared, never rendered (--font-secondary unused) | | optional |
| public/assets/intro-DrshnI3i.mp4 | video | 1920x1078, 2.03s | hero `video.hero__image` | 1248x702 (scaled 0.8→1) | muted playsinline preload="auto"; NO autoplay/loop; object-fit cover; aspect 16/9; radius 8 |
| public/assets/def1--g7RFuQa.mp4 | video | 1200x900, 8.88s | how-it-works card 1 | 848x636 | loop muted playsinline preload="metadata"; JS play() |
| public/assets/def2-0T0-0aPX.mp4 | video | 1200x900, 8.88s | card 2 | 848x636 | same |
| public/assets/loop3-CWAyqkgp.mp4 | video | 1200x900, 5.2s | card 3 | 848x636 | same |
| public/assets/frame-Cg0zK82j.png | png | 800x600 | figma-card 1 "Frames" | 336x252 | object-fit cover in 4:3 box |
| public/assets/styles-DpEOnP78.png | png | 800x600 | figma-card 2 "Styles" | 336x252 | |
| public/assets/variable-fdRUIB1a.png | png | 800x600 | figma-card 3 "Variables" | 336x252 | |
| public/assets/css-export-DPacxBL7.jpg | jpg | 707x553 | exports card "CSS" | 612x479 | width 100%, height auto |
| public/assets/ai-prompt-B1wIQtkI.jpg | jpg | 707x553 | exports card "AI Prompt" | 612x479 | |
| public/assets/token-Dmg8Y-M9.png | png | 869x650 | FAQ item 4 answer | 612x458 | radius 4, margin-bottom 24 |
| public/favicon.svg / favicon.png | icon | svg / 32x32 | `<link rel=icon>` | | |
| public/cover.png | png | 1200x630 | og:image / twitter:image | | |
| recon-assets/breakpoint-lottie.json | lottie | 1280x728, 25fps, 50 frames | `.breakpoint__lottie` | 1248x709.8 | contains ORIGINAL copy as glyph text layers — replace text before shipping (only chars present in `chars` render) |
| recon-assets/svg/navbar-logo.svg | svg | 171x40 | navbar logo | 171x40 (136.8x32 ≤1024) | |
| recon-assets/svg/footer-logo.svg | svg | 44x40 | footer hero mark | 44x40 | |
| recon-assets/svg/figma-icon-btn.svg | svg | 16x17 | `.btn__icon` in all "Try it now" buttons (x5) | 16x17 | |
| recon-assets/svg/check.svg | svg | 16x16 | pricing includes (x8) | | stroke white 2 |
| recon-assets/svg/chevron.svg | svg | 24x24 | FAQ chevrons (x7) | | stroke #E6E3DA 2 |
| recon-assets/svg/preset-folder.svg | svg | 96x84 | presets folders (JS-generated; fill=currentColor) | 82x71.8 | |
| recon-assets/svg/logo-cursor.svg | svg | 32x32 | CSS export card, logo 1 | | fill #E6E3DA |
| recon-assets/svg/logo-vscode.svg | svg | 32x32 | CSS export card, logo 2 | | |
| recon-assets/svg/logo-claude.svg | svg | 32x32 | AI Prompt card, logo 1 | | |
| recon-assets/svg/logo-cursor-ai-card.svg | svg | 32x32 | AI Prompt card, logo 2 (Cursor; differs only by clip id) | | |
| recon-assets/svg/logo-openai.svg | svg | 32x32 | AI Prompt card, logo 3 | | |
| recon-assets/svg/logo-lovable.svg | svg | 32x32 | AI Prompt card, logo 4 | | |

Third-party scripts: `https://lmsqueezy.com/affiliate.js` (defer) with `window.lemonSqueezyAffiliateConfig={store:"typewave"}`.
NPM deps implied: `lenis` (orig 1.3.18), `lottie-web`.

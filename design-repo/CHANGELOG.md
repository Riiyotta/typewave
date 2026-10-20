# Changelog

## 1.0.0 - 2026-10-20

Initial from-scratch build against the current typewave-clone source, CLONE_SPEC.md, ASSET_MANIFEST.md and the
original compiled CSS/JS.

- Tokens: 229 foundation, 41 semantic, 59 component, 14 layout; one theme (`typewave-dark`); LLM catalog/policy/allowlist.
- 13 section contracts (one per observed section type, App.jsx order), 13 components, 10 primitives; per-section motion enums with const-locked reducedMotionFallback; structured responsive fields.
- 1 template / 1 route (`/` -> `template.home`, homeRouteOnly).
- 20 graph rules (error/warn) with one validator implementation each; named exception for the overlay pair.
- 23 asset roles (11 settable, 20 pinned): company marks must-not-reproduce, third-party logos must-not-fabricate, product media generated-stand-in-only, Lottie html-rebuild-only, fonts licensed-font-required, live endpoints must-not-reuse-live-endpoint.
- Adversarial suite: 55 mutations (schema, structural, runtime, repository pinned-policy, warn-only) + 4 controls (example, new-content, every template synthesised generically).
- Finding (check 15): src/content.js is not fully placeholder - FAQ questions 2/3/5/6 and the three plan subtitles are identical to the live site. The example rewords them (recorded in measured-values.json exampleDeviations); the clone itself is unchanged (out of scope, read-only).
- verify_all.py: 16 checks incl. allowlist parity, citation range + expected text, original-file quotes, manifest/README counts, allowlistVersion, asset closure + pinned values, copy provenance, source-sync. drift_test.py proves the drift checks fail on injected drift.

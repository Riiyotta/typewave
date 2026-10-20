#!/usr/bin/env python3
"""Adversarial suite: every mutation must be REJECTED by the expected layer, every control must PASS.

Controls are synthesised GENERICALLY: for every template in templates/templates.json the suite builds
(a) a page with the template's full node list and (b) a required-nodes-only page, each assembled from that
template's own node list (node bodies borrowed from the example by section id), so a new or split template is
covered with zero new control code. A hand-written new-content control proves the compliance rules accept a
legitimate generated page (fresh copy, generated stand-ins, owner-supplied marks, the owner's own URLs).

Mutation kinds:
  schema      - the Draft-07 layer must reject (expected layer 'SCHEMA')
  structural  - a semantic rule id must fire as an error
  runtime     - per-instance maxWords / asset policy / live endpoint rules
  repository  - the PageSpec is untouched but the loaded repository is mutated (pinned-policy drift)
  warn-only   - a warn-severity rule must fire as a warning (and the page must stay valid)

Usage: python3 -I schema/tests/adversarial_test.py     (exit 1 on any failed expectation)
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'schema'))
import semantic_validate as sv  # noqa: E402

REPO = sv.Repo()
with open(os.path.join(ROOT, 'schema', 'example.pagespec.json'), encoding='utf-8') as f:
    EXAMPLE = json.load(f)


def node(spec, nid):
    return next(n for n in spec['nodes'] if n['id'] == nid)


def drop(spec, *ids):
    spec['nodes'] = [n for n in spec['nodes'] if n['id'] not in ids]


def prune_targets(spec):
    """Remove #targets that point at anchors no longer on the page (keeps synthesised controls coherent)."""
    anchors = set(sv._anchors(spec))
    for n in spec['nodes']:
        c = n['content']
        if n['section'] == 'shell.navbar':
            c['links'] = [l for l in c['links'] if l['target'][1:] in anchors]


def synth(template_id, required_only):
    t = REPO.templates['templates'][template_id]
    by_section = {n['section']: n for n in EXAMPLE['nodes']}
    s = copy.deepcopy(EXAMPLE)
    s['template'] = template_id
    s['route'] = t['routes'][0]
    s['nodes'] = [copy.deepcopy(by_section[tn['section']]) for tn in t['nodes'] if tn['required'] or not required_only]
    prune_targets(s)
    return s


def new_content_control():
    s = copy.deepcopy(EXAMPLE)
    s['meta']['title'] = 'Ramp – Responsive type in one pass'
    s['meta']['description'] = 'A design plugin that turns one base size into a responsive ramp of frames, styles and variables for your team.'
    for n in s['nodes']:
        c = n['content']
        if 'cta' in c and isinstance(c['cta'], dict) and 'icon' in c['cta']:
            c['cta']['href'] = 'https://ramp.example.org/install'
    h = node(s, 'hero')['content']
    h['title'] = 'Responsive type|in one|[single quiet pass.]'
    h['subtitle'] = 'Ramp turns one base size into a full responsive scale with frames, styles and variables, so your team stops arguing about font sizes.'
    h['video'] = {'assetRole': 'media.hero-video', 'assetRef': 'generated:ramp-hero'}
    node(s, 'nav')['content']['logo'] = {'assetRole': 'brand.logo-wordmark', 'assetRef': 'owner-supplied:ramp-wordmark'}
    node(s, 'footer')['content']['copyright'] = '© 2026 Ramp Studio'
    node(s, 'footer')['content']['legalLinks'] = [{'label': 'Privacy', 'href': 'https://ramp.example.org/privacy'}]
    ex = node(s, 'exports')['content']['cards']
    ex[0]['logos'] = []
    ex[1]['logos'] = []
    return s


NEW = new_content_control()


def controls():
    out = [('example.pagespec.json (unmutated)', copy.deepcopy(EXAMPLE)), ('new-content control', copy.deepcopy(NEW))]
    for tid in REPO.templates['templates']:
        out.append((f'{tid}: all template nodes', synth(tid, False)))
        out.append((f'{tid}: required nodes only', synth(tid, True)))
    return out


def M(kind, name, expect, fn=None, repo_fn=None):
    return {'kind': kind, 'name': name, 'expect': expect, 'fn': fn or (lambda s: None), 'repo_fn': repo_fn}


def setp(path_fn, key, value):
    def f(s):
        path_fn(s)[key] = value
    return f


def long(n):
    return ' '.join(['word'] * n)


def mv(s, nid, to):
    n = node(s, nid)
    s['nodes'].remove(n)
    s['nodes'].insert(to, n)


def pin(role, value):
    def f(repo):
        repo.assets['roles'][role]['generationPolicy'] = value
    return f


MUTATIONS = [
    # ---------------- schema layer
    M('schema', 'wrong template enum', 'SCHEMA', setp(lambda s: s, 'template', 'template.landing')),
    M('schema', 'invented section type alias', 'SCHEMA', setp(lambda s: node(s, 'hero'), 'section', 'hero.marketing')),
    M('schema', 'missing reducedMotionFallback', 'SCHEMA', lambda s: node(s, 'hero')['motion'].pop('reducedMotionFallback')),
    M('schema', 'reducedMotionFallback of another section', 'SCHEMA', setp(lambda s: node(s, 'hero')['motion'], 'reducedMotionFallback', 'instant-toggle')),
    M('schema', 'motion: invented field', 'SCHEMA', setp(lambda s: node(s, 'presets')['motion'], 'inventedAnimation', 'spin')),
    M('schema', 'motion: pattern not evidenced for section', 'SCHEMA', setp(lambda s: node(s, 'presets')['motion'], 'patterns', ['hero-video-scale'])),
    M('schema', 'motion: reveal delay not observed (75ms)', 'SCHEMA', setp(lambda s: node(s, 'hero')['motion'], 'revealDelaysMs', [0, 75])),
    M('schema', 'content: extra property', 'SCHEMA', setp(lambda s: node(s, 'hero')['content'], 'badge', 'Beta')),
    M('schema', 'content: required field removed (plan price)', 'SCHEMA', lambda s: node(s, 'pricing')['content']['plans'][0].pop('price')),
    M('schema', 'content: 4 pricing plans', 'SCHEMA', lambda s: node(s, 'pricing')['content']['plans'].append(copy.deepcopy(node(s, 'pricing')['content']['plans'][1]))),
    M('schema', 'invented assetRole', 'SCHEMA', setp(lambda s: node(s, 'hero')['content']['video'], 'assetRole', 'media.stock-video')),
    M('schema', 'real assetRole on the wrong field', 'SCHEMA', setp(lambda s: node(s, 'hero')['content']['video'], 'assetRole', 'media.step-video')),
    M('schema', 'title mini-syntax unbalanced', 'SCHEMA', setp(lambda s: node(s, 'hero')['content'], 'title', 'Craft a balanced|[type scale')),
    M('schema', 'pageSpecVersion drift', 'SCHEMA', setp(lambda s: s, 'pageSpecVersion', '2.0.0')),
    M('schema', 'extra top-level property', 'SCHEMA', setp(lambda s: s, 'styles', {'color': '#ff0000'})),
    M('schema', 'node extra property', 'SCHEMA', setp(lambda s: node(s, 'faq'), 'variant', 'compact')),
    M('schema', 'simulator default not a token (97px)', 'SCHEMA', setp(lambda s: node(s, 'breakpoint')['content']['simulator'], 'defaultDesktopPx', 97)),
    M('schema', 'javascript: href', 'SCHEMA', setp(lambda s: node(s, 'hero')['content']['cta'], 'href', 'javascript:alert(1)')),
    M('schema', 'FAQ item with neither paragraphs nor linkParagraph', 'SCHEMA', lambda s: node(s, 'faq')['content']['items'].__setitem__(0, {'question': 'Is it free?'})),
    M('schema', 'theme not schema-validated', 'SCHEMA', setp(lambda s: s, 'theme', 'typewave-light')),
    # ---------------- structural (template / position / dependency rules)
    M('structural', 'template/node mismatch: faq before pricing', 'TEMPLATE_NODE_SEQUENCE', lambda s: mv(s, 'faq', 7)),
    M('structural', 'duplicate one-per-page section (pricing twice)', 'TEMPLATE_NODE_SEQUENCE',
      lambda s: s['nodes'].insert(8, dict(copy.deepcopy(node(s, 'pricing')), id='pricing-2', anchorId='pricing-2'))),
    M('structural', 'required hero removed', 'TEMPLATE_NODE_SEQUENCE', lambda s: drop(s, 'hero', 'floating-cta')),
    M('structural', 'required footer removed', 'TEMPLATE_NODE_SEQUENCE', lambda s: drop(s, 'footer')),
    M('structural', 'second hero', 'ONE_HERO', lambda s: s['nodes'].insert(2, dict(copy.deepcopy(node(s, 'hero')), id='hero-2'))),
    M('structural', 'route not allowed for homeRouteOnly template', 'ROUTE_ALLOWED', setp(lambda s: s, 'route', '/pricing')),
    M('structural', 'navbar not first', 'NAV_FIRST', lambda s: mv(s, 'nav', 1)),
    M('structural', 'hero not directly after navbar', 'HERO_FOLLOWS_NAV', lambda s: mv(s, 'hero', 2)),
    M('structural', 'content section after footer', 'FOOTER_CLOSES_MAIN', lambda s: mv(s, 'newsletter', 10)),
    M('structural', 'overlay before footer', 'OVERLAYS_AFTER_FOOTER', lambda s: mv(s, 'type-inspector', 10)),
    M('structural', 'floating CTA without newsletter', 'FLOATING_CTA_DEPENDENCIES', lambda s: drop(s, 'newsletter')),
    M('structural', 'nav link to a missing anchor', 'ANCHOR_TARGETS_RESOLVE', lambda s: node(s, 'nav')['content']['links'][0].__setitem__('target', '#features')),
    M('structural', 'anchor target lost (AI Prompt card anchor removed)', 'ANCHOR_TARGETS_RESOLVE', lambda s: node(s, 'exports')['content']['cards'][1].pop('anchorId')),
    M('structural', 'duplicate anchorId', 'ANCHOR_IDS_UNIQUE', setp(lambda s: node(s, 'faq'), 'anchorId', 'pricing')),
    # ---------------- runtime
    M('runtime', 'maxWords overflow: hero subtitle', 'MAX_WORDS', setp(lambda s: node(s, 'hero')['content'], 'subtitle', long(36))),
    M('runtime', 'maxWords overflow: FAQ answer paragraph', 'MAX_WORDS', lambda s: node(s, 'faq')['content']['items'][1]['paragraphs'].__setitem__(0, long(100))),
    M('runtime', 'maxWords overflow: nested includes item', 'MAX_WORDS', lambda s: node(s, 'pricing')['content']['includes']['columns'][1][0].__setitem__('text', long(7))),
    M('runtime', 'maxWords overflow: page meta.title', 'MAX_WORDS', setp(lambda s: s['meta'], 'title', long(11))),
    M('runtime', 'proprietary original asset reused (asset:intro-video)', 'ASSET_REF_POLICY', setp(lambda s: node(s, 'hero')['content']['video'], 'assetRef', 'asset:intro-video')),
    M('runtime', 'owner-supplied original screenshot for generated-stand-in-only role', 'ASSET_REF_POLICY',
      setp(lambda s: node(s, 'figma-org')['content']['cards'][0]['image'], 'assetRef', 'owner-supplied:frame-png')),
    M('runtime', 'AI-generated company wordmark (must-not-reproduce)', 'ASSET_REF_POLICY', setp(lambda s: node(s, 'nav')['content']['logo'], 'assetRef', 'generated:wordmark')),
    M('runtime', 'AI-generated third-party logo (must-not-fabricate)', 'ASSET_REF_POLICY',
      setp(lambda s: node(s, 'exports')['content']['cards'][0]['logos'][0], 'assetRef', 'generated:cursor-logo')),
    M('runtime', 'AI-generated Figma glyph (must-not-fabricate)', 'ASSET_REF_POLICY', setp(lambda s: node(s, 'hero')['content']['cta']['icon'], 'assetRef', 'generated:figma')),
    M('runtime', 'live checkout URL reused', 'LIVE_ENDPOINT_NOT_REUSED',
      setp(lambda s: node(s, 'pricing')['content']['plans'][0]['cta'], 'href', 'https://typewave.lemonsqueezy.com/checkout/buy/f38b86ac-2475-4b2b-a7a8-67abd5d7cfec')),
    M('runtime', 'live newsletter POST target reused', 'LIVE_ENDPOINT_NOT_REUSED',
      setp(lambda s: node(s, 'newsletter')['content']['form'], 'action', 'https://typewave.lemonsqueezy.com/email-subscribe/external')),
    M('runtime', 'live Figma Community plugin URL reused', 'LIVE_ENDPOINT_NOT_REUSED',
      setp(lambda s: node(s, 'hero')['content']['cta'], 'href', 'https://www.figma.com/community/plugin/1615417453541684477/typewave')),
    M('runtime', 'company mailbox reused (Enterprise mailto)', 'LIVE_ENDPOINT_NOT_REUSED',
      setp(lambda s: node(s, 'pricing')['content']['plans'][2]['cta'], 'href', 'mailto:hello@blendmodes.com?subject=Typewave%20Enterprise%20Licenses')),
    M('runtime', 'Lemon Squeezy legal page reused', 'LIVE_ENDPOINT_NOT_REUSED',
      lambda s: node(s, 'footer')['content']['legalLinks'][0].__setitem__('href', 'https://www.lemonsqueezy.com/privacy')),
    # ---------------- repository (pinned compliance policies; different-but-VALID values)
    M('repository', 'pinned policy drift: media.hero-video -> may-generate-new', 'ASSET_ROLE_PINNED', repo_fn=pin('media.hero-video', 'may-generate-new')),
    M('repository', 'pinned policy drift: logo.third-party-tool -> may-generate-new', 'ASSET_ROLE_PINNED', repo_fn=pin('logo.third-party-tool', 'may-generate-new')),
    M('repository', 'pinned policy drift: endpoint.checkout -> may-generate-new', 'ASSET_ROLE_PINNED', repo_fn=pin('endpoint.checkout', 'may-generate-new')),
    M('repository', 'pinned policy drift: media.device-mockup (Lottie ban) -> generated-stand-in-only', 'ASSET_ROLE_PINNED',
      repo_fn=pin('media.device-mockup', 'generated-stand-in-only')),
    M('repository', 'pinned policy drift: font.roobert -> may-generate-new', 'ASSET_ROLE_PINNED', repo_fn=pin('font.roobert', 'may-generate-new')),
    # ---------------- warn-only rules (page stays valid, warning must fire)
    M('warn-only', 'pinned scroll stages adjacent (feature cards dropped)', 'NO_CONSECUTIVE_SCROLL_STAGES', lambda s: drop(s, 'figma-org')),
    M('warn-only', 'two featured plans', 'PRICING_FEATURED_SINGLE', lambda s: node(s, 'pricing')['content']['plans'][1].__setitem__('featured', True)),
]


def layers(msgs):
    return {m.split(':', 1)[0] for m in msgs}


def run():
    fails = 0
    print('CONTROLS (must produce 0 errors and 0 warnings)')
    for name, spec in controls():
        errs, warns = sv.validate(spec, REPO)
        ok = not errs and not warns
        fails += not ok
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: {len(errs)} error(s), {len(warns)} warning(s)")
        for m in (errs + warns)[:6]:
            print('        ', m)
    print('MUTATIONS (must be rejected by the expected layer)')
    for m in MUTATIONS:
        spec = copy.deepcopy(EXAMPLE)
        m['fn'](spec)
        repo = REPO
        if m['repo_fn']:
            repo = REPO.clone()
            m['repo_fn'](repo)
        errs, warns = sv.validate(spec, repo)
        if m['kind'] == 'warn-only':
            ok = not errs and m['expect'] in layers(warns)
        else:
            ok = m['expect'] in layers(errs)
        fails += not ok
        print(f"  {'PASS' if ok else 'MISSED'}  [{m['kind']}] {m['name']} -> expected {m['expect']}; got {sorted(layers(errs)) or '-'}"
              + (f" warn {sorted(layers(warns))}" if warns else ''))
    n_ctrl = len(controls())
    print(f'\n{len(MUTATIONS)} mutations, {n_ctrl} controls: ' + ('ALL EXPECTATIONS MET' if not fails else f'{fails} FAILED'))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(run())

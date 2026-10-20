#!/usr/bin/env python3
"""Semantic validator for Typewave PageSpecs.

Enforces what JSON Schema (draft-07) cannot express:
  * the PageSpec's declared `template` is cross-referenced against THAT template's real node list
    (order, required nodes, no repeats of non-repeatable nodes) - not nodes[] in isolation;
  * route restriction (template.home is homeRouteOnly: "/");
  * rhythm / position / dependency rules from compatibility/graph.json, at the severity the graph declares;
  * reducedMotionFallback presence + the section's const value, and motion patterns within the section's set;
  * per-instance maxWords budgets (every node, every budgeted path, plus page-level meta budgets);
  * asset-role closure, assetRef policy per role, pinned compliance policies (repository integrity);
  * live third-party endpoints of the real site (Lemon Squeezy checkout / newsletter / legal, Figma Community
    plugin URL, company mailto, affiliate.js) are never reused.

Every rule id in compatibility/graph.json has exactly one implementation in RULES below, and the severity
used at runtime is READ FROM THE GRAPH (one source of truth). extraction/verify_all.py checks the two id sets
match in both directions.

Usage:  python3 -I schema/semantic_validate.py [pagespec.json ...]   (default: schema/example.pagespec.json)
Exit code 1 if any error-severity finding. Requires the `jsonschema` package for the Draft-07 layer.
"""
import copy
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # design-repo/


def _load(root, rel):
    with open(os.path.join(root, rel), encoding='utf-8') as f:
        return json.load(f)


class Repo:
    """Everything the validator needs, loaded from this design-repo (never from outside it)."""

    def __init__(self, root=ROOT):
        self.root = root
        self.schema = _load(root, 'schema/pagespec.schema.json')
        self.templates = _load(root, 'templates/templates.json')
        self.graph = _load(root, 'compatibility/graph.json')
        self.assets = _load(root, 'assets/asset-roles.json')
        self.sections = {}
        sdir = os.path.join(root, 'sections')
        for fn in sorted(os.listdir(sdir)):
            if fn.endswith('.json'):
                d = _load(root, 'sections/' + fn)
                self.sections[d['id']] = d
        self.rules = {r['id']: r for r in self.graph['rules']}
        self.asset_ids = {}
        for role, r in self.assets['roles'].items():
            for a in r['assets']:
                self.asset_ids[a['id']] = role

    def clone(self):
        return copy.deepcopy(self)


# ---------------------------------------------------------------- helpers

def count_words(s):
    """Words as a reader sees them: the title mini-syntax markers | [ ] are layout, not words."""
    return len(re.sub(r'[|\[\]]', ' ', s).split())


_SEG = re.compile(r'^([A-Za-z0-9_-]*)((?:\[\])*)$')


def values_at(obj, path):
    """Resolve a budget path such as 'cards[].text' or 'includes.columns[][].text' to the strings it names."""
    cur = [obj]
    for seg in path.split('.'):
        m = _SEG.match(seg)
        if not m:
            raise ValueError('bad budget path ' + path)
        name, br = m.group(1), m.group(2).count('[]')
        nxt = []
        for v in cur:
            if name:
                if isinstance(v, dict) and name in v:
                    nxt.append(v[name])
            else:
                nxt.append(v)
        for _ in range(br):
            flat = []
            for v in nxt:
                if isinstance(v, list):
                    flat.extend(v)
            nxt = flat
        cur = nxt
    return [v for v in cur if isinstance(v, str)]


def walk(obj, path=''):
    """Yield (path, key, value) for every dict entry and list item, depth-first."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f'{path}.{k}' if path else k
            yield p, k, v
            yield from walk(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = f'{path}[{i}]'
            yield p, None, v
            yield from walk(v, p)


def nodes_of(spec):
    n = spec.get('nodes')
    return [x for x in n if isinstance(x, dict)] if isinstance(n, list) else []


def idx(spec, pred):
    return [i for i, n in enumerate(nodes_of(spec)) if pred(n.get('section', ''))]


# ---------------------------------------------------------------- rules

def r_template_node_sequence(spec, repo):
    out = []
    tid = spec.get('template')
    tpl = repo.templates['templates'].get(tid)
    if tpl is None:
        return [f'declared template {tid!r} does not exist in templates/templates.json']
    tn = tpl['nodes']
    j = 0
    seen = set()
    for i, n in enumerate(nodes_of(spec)):
        key = (n.get('section'), n.get('variant'))
        k = next((k for k in range(j, len(tn)) if (tn[k]['section'], tn[k].get('variant')) == key), None)
        if k is None:
            earlier = any((t['section'], t.get('variant')) == key for t in tn[:j])
            if earlier:
                out.append(f'nodes[{i}] {key[0]} is out of {tid} order or repeats a non-repeatable node')
            else:
                out.append(f'nodes[{i}] {key[0]} is not a node of {tid}')
            continue
        if key in seen and not tn[k]['repeatable']:
            out.append(f'nodes[{i}] {key[0]} repeats a non-repeatable node')
        seen.add(key)
        j = k if tn[k]['repeatable'] else k + 1
    for t in tn:
        if t['required'] and (t['section'], t.get('variant')) not in seen:
            out.append(f'required {tid} node {t["key"]} ({t["section"]}) is missing')
    return out


def r_route_allowed(spec, repo):
    tpl = repo.templates['templates'].get(spec.get('template'))
    if tpl is None:
        return []  # reported by TEMPLATE_NODE_SEQUENCE
    if spec.get('route') not in tpl['routes']:
        return [f'route {spec.get("route")!r} is not a route of {spec.get("template")} (allowed: {tpl["routes"]})']
    return []


def r_nav_first(spec, repo):
    n = nodes_of(spec)
    if not n or n[0].get('section') != 'shell.navbar':
        return ['the first node must be shell.navbar']
    return []


def r_hero_follows_nav(spec, repo):
    if spec.get('template') in repo.rules['HERO_FOLLOWS_NAV'].get('exemptTemplates', []):
        return []
    h = idx(spec, lambda s: s.startswith('hero.'))
    if not h:
        return ['no hero node to follow the navbar']
    if h[0] != 1:
        return [f'the hero must be nodes[1] (directly after shell.navbar); found at nodes[{h[0]}]']
    return []


def r_one_hero(spec, repo):
    if spec.get('template') in repo.rules['ONE_HERO'].get('exemptTemplates', []):
        return []
    h = idx(spec, lambda s: s.startswith('hero.'))
    return [] if len(h) == 1 else [f'exactly one hero.* node required, found {len(h)}']


def r_footer_closes_main(spec, repo):
    f = idx(spec, lambda s: s == 'shell.footer')
    if not f:
        return ['shell.footer missing']
    out = []
    for i, n in enumerate(nodes_of(spec)):
        s = n.get('section', '')
        if i > f[0] and not s.startswith('overlay.'):
            out.append(f'nodes[{i}] {s} follows shell.footer; only overlay.* nodes may follow it')
    return out


def r_overlays_after_footer(spec, repo):
    f = idx(spec, lambda s: s == 'shell.footer')
    if not f:
        return []
    return [f'nodes[{i}] {nodes_of(spec)[i]["section"]} is an overlay placed before shell.footer'
            for i in idx(spec, lambda s: s.startswith('overlay.')) if i < f[0]]


def r_floating_cta_dependencies(spec, repo):
    secs = [n.get('section') for n in nodes_of(spec)]
    if 'overlay.floating-cta' not in secs:
        return []
    need = repo.rules['FLOATING_CTA_DEPENDENCIES']['params']['requires']
    return [f'overlay.floating-cta needs {s} on the same page (its visibility rule reads it)' for s in need if s not in secs]


def _anchors(spec):
    out = []
    for n in nodes_of(spec):
        if n.get('anchorId'):
            out.append(n['anchorId'])
        for _, k, v in walk(n.get('content', {})):
            if k == 'anchorId' and isinstance(v, str):
                out.append(v)
    return out


def r_anchor_targets_resolve(spec, repo):
    anchors = set(_anchors(spec))
    out = []
    for i, n in enumerate(nodes_of(spec)):
        for p, k, v in walk(n.get('content', {})):
            if k in ('target', 'href') and isinstance(v, str) and v.startswith('#'):
                if v[1:] not in anchors:
                    out.append(f'nodes[{i}].content.{p} -> {v} has no matching anchorId on the page')
    return out


def r_anchor_ids_unique(spec, repo):
    a = _anchors(spec)
    d = sorted({x for x in a if a.count(x) > 1})
    return [f'anchorId {x!r} is used more than once' for x in d]


def r_no_consecutive_scroll_stages(spec, repo):
    st = set(repo.rules['NO_CONSECUTIVE_SCROLL_STAGES']['params']['scrollStages'])
    n = nodes_of(spec)
    return [f'nodes[{i}] {n[i]["section"]} and nodes[{i + 1}] {n[i + 1]["section"]} are both pinned scroll stages'
            for i in range(len(n) - 1) if n[i].get('section') in st and n[i + 1].get('section') in st]


def r_no_adjacent_same_category(spec, repo):
    rule = repo.rules['NO_ADJACENT_SAME_CATEGORY']
    exc = {tuple(e['pair']) for e in rule.get('namedExceptions', [])}
    n = nodes_of(spec)
    out = []
    for i in range(len(n) - 1):
        a, b = n[i].get('section'), n[i + 1].get('section')
        ca = repo.sections.get(a, {}).get('category')
        cb = repo.sections.get(b, {}).get('category')
        if ca and ca == cb and (a, b) not in exc:
            out.append(f'nodes[{i}] {a} and nodes[{i + 1}] {b} share category {ca!r}')
    return out


def r_reduced_motion_fallback(spec, repo):
    out = []
    for i, n in enumerate(nodes_of(spec)):
        c = repo.sections.get(n.get('section'))
        if c is None:
            continue
        m = n.get('motion')
        if not isinstance(m, dict) or 'reducedMotionFallback' not in m:
            out.append(f'nodes[{i}] {c["id"]}: motion.reducedMotionFallback is missing')
        elif m['reducedMotionFallback'] != c['motion']['reducedMotionFallback']:
            out.append(f'nodes[{i}] {c["id"]}: reducedMotionFallback {m["reducedMotionFallback"]!r} != contract '
                       f'{c["motion"]["reducedMotionFallback"]!r}')
    return out


def r_motion_patterns_allowed(spec, repo):
    out = []
    for i, n in enumerate(nodes_of(spec)):
        c = repo.sections.get(n.get('section'))
        m = n.get('motion')
        if c is None or not isinstance(m, dict):
            continue
        pats = m.get('patterns') or []
        if not pats:
            out.append(f'nodes[{i}] {c["id"]}: motion.patterns is empty')
        for p in pats:
            if p not in c['motion']['allowedPatterns']:
                out.append(f'nodes[{i}] {c["id"]}: motion pattern {p!r} is not evidenced for this section')
    return out


def r_max_words(spec, repo):
    out = []
    for i, n in enumerate(nodes_of(spec)):
        c = repo.sections.get(n.get('section'))
        if c is None:
            continue
        for b in c['content']['wordBudgets']:
            for v in values_at(n.get('content', {}), b['path']):
                w = count_words(v)
                if w > b['maxWords']:
                    out.append(f'nodes[{i}] {c["id"]}.{b["path"]}: {w} words > maxWords {b["maxWords"]}')
    tpl = repo.templates['templates'].get(spec.get('template'))
    for b in (tpl or {}).get('pageWordBudgets', []):
        for v in values_at(spec, b['path']):
            w = count_words(v)
            if w > b['maxWords']:
                out.append(f'{b["path"]}: {w} words > maxWords {b["maxWords"]}')
    return out


def _media(spec):
    for p, k, v in walk(spec):
        if isinstance(v, dict) and 'assetRole' in v:
            yield p, v


def r_asset_role_closed(spec, repo):
    roles = repo.assets['roles']
    out = []
    for p, v in _media(spec):
        r = roles.get(v.get('assetRole'))
        if r is None:
            out.append(f'{p}: assetRole {v.get("assetRole")!r} is not in the closed role vocabulary')
        elif not r['settableInPageSpec']:
            out.append(f'{p}: assetRole {v.get("assetRole")!r} is not settable in a PageSpec')
    return out


def r_asset_ref_policy(spec, repo):
    roles = repo.assets['roles']
    pols = repo.assets['policies']
    out = []
    for p, v in _media(spec):
        role = v.get('assetRole')
        r = roles.get(role)
        ref = v.get('assetRef', '')
        if r is None or not isinstance(ref, str) or ':' not in ref:
            continue
        prefix = ref.split(':', 1)[0]
        pol = r['generationPolicy']
        allowed = pols.get(pol, {}).get('allowedRefPrefixes', [])
        if prefix not in allowed:
            out.append(f'{p}: assetRef {ref!r} uses {prefix + ":"} but role {role} is {pol!r} (allowed: {allowed})')
        elif prefix == 'asset' and repo.asset_ids.get(ref) != role:
            out.append(f'{p}: {ref!r} is not a registered asset of role {role}')
    return out


def r_asset_role_pinned(spec, repo):
    roles = repo.assets['roles']
    pols = set(repo.assets['policies'])
    out = []
    for role, r in roles.items():
        if r['generationPolicy'] not in pols:
            out.append(f'role {role}: policy {r["generationPolicy"]!r} is not in the closed policy set')
    for role, want in repo.assets['pinnedPolicies'].items():
        if role not in roles:
            out.append(f'pinned role {role} is missing from assets/asset-roles.json')
        elif roles[role]['generationPolicy'] != want:
            out.append(f'pinned role {role} has policy {roles[role]["generationPolicy"]!r}; it is pinned to {want!r}')
    return out


def r_live_endpoint_not_reused(spec, repo):
    live = []
    for role, r in repo.assets['roles'].items():
        for v in r.get('liveValues', []):
            live.append((v.lower(), role))
    out = []
    for p, k, v in walk(spec):
        if isinstance(v, str):
            low = v.lower()
            for pat, role in live:
                if pat in low:
                    out.append(f'{p}: {v!r} reuses a live endpoint of the real site ({role})')
                    break
    return out


def r_pricing_featured_single(spec, repo):
    out = []
    for i, n in enumerate(nodes_of(spec)):
        if n.get('section') != 'pricing.ticket-plans':
            continue
        plans = n.get('content', {}).get('plans', [])
        f = [j for j, pl in enumerate(plans) if isinstance(pl, dict) and pl.get('featured')]
        if len(f) > 1 or (f and f[0] != 0):
            out.append(f'nodes[{i}] pricing: featured plans at {f}; the observed layout marks only the first plan')
    return out


RULES = {
    'TEMPLATE_NODE_SEQUENCE': r_template_node_sequence,
    'ROUTE_ALLOWED': r_route_allowed,
    'NAV_FIRST': r_nav_first,
    'HERO_FOLLOWS_NAV': r_hero_follows_nav,
    'ONE_HERO': r_one_hero,
    'FOOTER_CLOSES_MAIN': r_footer_closes_main,
    'OVERLAYS_AFTER_FOOTER': r_overlays_after_footer,
    'FLOATING_CTA_DEPENDENCIES': r_floating_cta_dependencies,
    'ANCHOR_TARGETS_RESOLVE': r_anchor_targets_resolve,
    'ANCHOR_IDS_UNIQUE': r_anchor_ids_unique,
    'NO_CONSECUTIVE_SCROLL_STAGES': r_no_consecutive_scroll_stages,
    'NO_ADJACENT_SAME_CATEGORY': r_no_adjacent_same_category,
    'REDUCED_MOTION_FALLBACK': r_reduced_motion_fallback,
    'MOTION_PATTERNS_ALLOWED': r_motion_patterns_allowed,
    'MAX_WORDS': r_max_words,
    'ASSET_ROLE_CLOSED': r_asset_role_closed,
    'ASSET_REF_POLICY': r_asset_ref_policy,
    'ASSET_ROLE_PINNED': r_asset_role_pinned,
    'LIVE_ENDPOINT_NOT_REUSED': r_live_endpoint_not_reused,
    'PRICING_FEATURED_SINGLE': r_pricing_featured_single,
}


def schema_errors(spec, repo):
    import jsonschema
    v = jsonschema.Draft7Validator(repo.schema)
    return [f"SCHEMA: /{'/'.join(map(str, e.absolute_path))}: {e.message[:180]}" for e in v.iter_errors(spec)]


def validate(spec, repo=None):
    """Return (errors, warnings). Each message is prefixed by the layer/rule id that produced it."""
    repo = repo or Repo()
    errors = schema_errors(spec, repo)
    warnings = []
    for rid, fn in RULES.items():
        rule = repo.rules.get(rid)
        sev = rule['severity'] if rule else 'error'
        try:
            msgs = fn(spec, repo)
        except Exception as e:  # malformed input that the schema layer already rejected
            msgs = [f'could not evaluate ({type(e).__name__}: {e})']
        for m in msgs:
            (errors if sev == 'error' else warnings).append(f'{rid}: {m}')
    return errors, warnings


def main(argv):
    paths = argv[1:] or [os.path.join(ROOT, 'schema', 'example.pagespec.json')]
    repo = Repo()
    bad = 0
    for p in paths:
        with open(p, encoding='utf-8') as f:
            spec = json.load(f)
        errs, warns = validate(spec, repo)
        print(f'{os.path.basename(p)}: {len(errs)} error(s), {len(warns)} warning(s)')
        for e in errs:
            print('  ERROR', e)
        for w in warns:
            print('  warn ', w)
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

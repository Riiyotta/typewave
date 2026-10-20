#!/usr/bin/env python3
"""One-shot verification for this design-repo. Exit 1 on any FAIL.

Checks (each drift-sensitive check is proven to fail on injected drift by extraction/drift_test.py):
  1  json        every *.json parses
  2  schema      pagespec.schema.json is valid Draft-07; example.pagespec.json has 0 schema errors
  3  semantic    semantic_validate.py: 0 errors / 0 warnings on the example
  4  adversarial schema/tests/adversarial_test.py: every mutation rejected, every control passes
  5  allowlist   parity: contract files on disk <-> tokens/llm/component-allowlist.json <-> pagespec.schema.json
  6  contracts   section content/motion == schema definitions; budgets >= observed; templates reference real
                 sections; every route mapped to exactly one template; components compose real primitives
  7  graph       compatibility/graph.json rule ids == semantic_validate.RULES (both ways); severities valid;
                 the validator accepts a PageSpec synthesised from every template (rules agree with templates.json)
  8  versions    manifest.allowlistVersion == allowlist.version (MACHINE-CHECKED); pageSpecVersion == schema const
  9  counts      manifest.counts and the README counts block recomputed from the files
 10  citations   every measuredFrom entry resolves: path:line[-line] within the file AND `expect` text inside the
                 range; @original/<file> quotes (minified originals) must occur in that file. @repo/ paths are
                 inside this folder (always checked); project-relative and @original/ paths are WARN-skipped
                 when the sibling clone project / original files are absent (standalone copy).
 11  assets      closed role/policy vocabulary; PINNED policy values hold; schema/allowlist roles agree; no media,
                 font or Lottie files shipped; forbidden Lottie not imported by the clone (sibling only)
 12  tokens      every {ref} resolves; theme == foundation; catalog == token leaves; policy keys are catalog keys
 13  manifest    required fields; status/approval; entryPoints exist and are inside design-repo/
 14  paths       no absolute local machine paths in any text file
 15  copy        example long strings come from the clone's placeholder copy (src/content.js / index.html), and no
                 string in this repo reproduces the live site's copy (original HTML text + Lottie text layers)
 16  source-sync re-checks conclusions against CURRENT source: App.jsx section order == template node order;
                 package.json versions == manifest; Lottie/affiliate.js absent from the clone

Usage: python3 extraction/verify_all.py [--project PATH] [--counts]
  --project PATH  the clone project to resolve external citations against (default: parent of design-repo/)
  --counts        print the recomputed counts as JSON and exit
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # design-repo/
PROJECT = os.path.dirname(ROOT)
if '--project' in sys.argv:
    PROJECT = os.path.abspath(sys.argv[sys.argv.index('--project') + 1])
ORIGINAL = os.path.dirname(PROJECT)
SIBLING = os.path.isfile(os.path.join(PROJECT, 'src', 'App.jsx')) and os.path.isfile(os.path.join(PROJECT, 'CLONE_SPEC.md'))
ORIG_PRESENT = SIBLING and os.path.isfile(os.path.join(ORIGINAL, 'index-D4COY28s.css'))
sys.path.insert(0, os.path.join(ROOT, 'schema'))
sys.path.insert(0, os.path.join(ROOT, 'schema', 'tests'))

RESULTS = []
CHECKS = []


def check(name):
    def deco(fn):
        def run():
            F, W, I = [], [], []
            try:
                fn(F, W, I)
            except Exception as e:  # a crashing check is a failing check
                F.append(f'{type(e).__name__}: {e}')
            RESULTS.append((name, F, W, I))
        CHECKS.append(run)
        return run
    return deco


def load(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return json.load(f)


def json_files():
    for d, _, fs in os.walk(ROOT):
        for f in sorted(fs):
            if f.endswith('.json'):
                yield os.path.relpath(os.path.join(d, f), ROOT)


def ids_in(folder):
    return sorted(f[:-5] for f in os.listdir(os.path.join(ROOT, folder)) if f.endswith('.json'))


def read_text(full):
    with open(full, encoding='utf-8') as f:
        return f.read()


@check('1 json')
def c_json(F, W, I):
    n = 0
    for rel in json_files():
        try:
            load(rel)
            n += 1
        except Exception as e:
            F.append(f'{rel}: {e}')
    I.append(f'{n} json files parse')


@check('2 schema')
def c_schema(F, W, I):
    import jsonschema
    s = load('schema/pagespec.schema.json')
    jsonschema.Draft7Validator.check_schema(s)
    errs = list(jsonschema.Draft7Validator(s).iter_errors(load('schema/example.pagespec.json')))
    for e in errs:
        F.append(f"{'/'.join(map(str, e.absolute_path))}: {e.message[:150]}")
    I.append(f'Draft-07 meta-schema OK; example.pagespec.json: {len(errs)} schema error(s)')


@check('3 semantic')
def c_semantic(F, W, I):
    import semantic_validate as sv
    errs, warns = sv.validate(load('schema/example.pagespec.json'))
    F.extend(errs)
    F.extend(f'(warning on the example) {w}' for w in warns)
    I.append(f'example: {len(errs)} error(s), {len(warns)} warning(s)')


@check('4 adversarial')
def c_adv(F, W, I):
    import io
    import contextlib
    import adversarial_test as at
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = at.run()
    last = buf.getvalue().strip().splitlines()[-1]
    if rc != 0:
        F.append(last)
        F.extend(l.strip() for l in buf.getvalue().splitlines() if l.strip().startswith(('FAIL', 'MISSED')))
    I.append(last)


def schema_role_consts(o, out, defs=None, seen=None):
    """Collect every assetRole const a schema fragment accepts, following local #/definitions refs."""
    if defs is None:
        defs = load('schema/pagespec.schema.json')['definitions']
    seen = set() if seen is None else seen
    if isinstance(o, dict):
        r = o.get('$ref')
        if isinstance(r, str) and r.startswith('#/definitions/') and r not in seen:
            seen.add(r)
            schema_role_consts(defs.get(r[len('#/definitions/'):], {}), out, defs, seen)
        ar = o.get('properties', {}).get('assetRole') if isinstance(o.get('properties'), dict) else None
        if isinstance(ar, dict):
            for part in ar.get('allOf', [ar]):
                if 'const' in part:
                    out.add(part['const'])
        for v in o.values():
            schema_role_consts(v, out, defs, seen)
    elif isinstance(o, list):
        for v in o:
            schema_role_consts(v, out, defs, seen)
    return out


@check('5 allowlist')
def c_allow(F, W, I):
    a = load('tokens/llm/component-allowlist.json')
    s = load('schema/pagespec.schema.json')
    for kind in ('sections', 'primitives', 'components'):
        listed = {e['id']: e['file'] for e in a[kind]}
        disk = ids_in(kind)
        for i in sorted(set(listed) - set(disk)):
            F.append(f'phantom allowlist {kind} entry with no contract file: {i}')
        for i in sorted(set(disk) - set(listed)):
            F.append(f'contract file with no allowlist entry: {kind}/{i}.json')
        for i, f in listed.items():
            if i in disk and f != f'{kind}/{i}.json':
                F.append(f'allowlist file path wrong for {i}: {f}')
    for e in a['sections']:
        d = s['definitions'].get(f"content.{e['id']}")
        m = s['definitions'].get(f"motion.{e['id']}")
        if d is None or m is None:
            F.append(f"schema has no content/motion definition for {e['id']}")
            continue
        if sorted(d['properties']) != e['settableProperties']:
            F.append(f"{e['id']}: allowlist settableProperties {e['settableProperties']} != schema {sorted(d['properties'])}")
        if sorted(m['properties']) != e['motionFields']:
            F.append(f"{e['id']}: allowlist motionFields != schema motion properties")
        if os.path.isfile(os.path.join(ROOT, 'sections', e['id'] + '.json')):
            sec = load(f"sections/{e['id']}.json")
            if sec['variants'] != e['variants']:
                F.append(f"{e['id']}: allowlist variants != contract variants")
            if sorted(sec['assetRoles']) != e['assetRoles']:
                F.append(f"{e['id']}: allowlist assetRoles != contract assetRoles")
            if sorted(schema_role_consts(d, set())) != e['assetRoles']:
                F.append(f"{e['id']}: allowlist assetRoles {e['assetRoles']} != roles its schema fields accept {sorted(schema_role_consts(d, set()))}")
            if m['properties']['patterns']['items']['enum'] != sec['motion']['allowedPatterns']:
                F.append(f"{e['id']}: schema motion pattern enum != contract allowedPatterns")
    if sorted(s['definitions']['node']['properties']) != a['nodeProperties']:
        F.append('allowlist nodeProperties != schema node properties')
    if sorted(s['properties']) != a['pageProperties']:
        F.append('allowlist pageProperties != schema top-level properties')
    if sorted(s['definitions']['node']['properties']['section']['enum']) != sorted(e['id'] for e in a['sections']):
        F.append('schema node.section enum != allowlist sections')
    if a['templates'] != sorted(load('templates/templates.json')['templates']) or a['templates'] != sorted(s['properties']['template']['enum']):
        F.append('allowlist templates != templates.json != schema template enum')
    I.append(f"{len(a['sections'])} sections, {len(a['primitives'])} primitives, {len(a['components'])} components in parity with disk + schema")


@check('6 contracts')
def c_contracts(F, W, I):
    s = load('schema/pagespec.schema.json')
    t = load('templates/templates.json')
    secs = {i: load(f'sections/{i}.json') for i in ids_in('sections')}
    prims = set(ids_in('primitives'))
    for i, d in secs.items():
        if d['id'] != i:
            F.append(f'sections/{i}.json declares id {d["id"]}')
        if d['content']['schema'] != s['definitions'].get(f'content.{i}'):
            F.append(f'{i}: content.schema differs from pagespec.schema.json definitions.content.{i}')
        const = s['definitions'][f'motion.{i}']['properties']['reducedMotionFallback'].get('const')
        if const != d['motion']['reducedMotionFallback']:
            F.append(f'{i}: schema reducedMotionFallback const {const} != contract {d["motion"]["reducedMotionFallback"]}')
        if set(d['motion']['patternEvidence']) != set(d['motion']['allowedPatterns']):
            F.append(f'{i}: every allowed motion pattern needs patternEvidence (and nothing else)')
        for b in d['content']['wordBudgets']:
            if b['maxWords'] < max(b['observedMaxWords'], b.get('specWords', 0)):
                F.append(f'{i}.{b["path"]}: maxWords below the observed copy')
        if not d.get('responsive'):
            F.append(f'{i}: no structured responsive field')
        for r in d.get('responsive', []):
            if not isinstance(r.get('changes'), dict) or not r['changes'] or not r.get('measuredFrom'):
                F.append(f'{i}: responsive entry {r.get("breakpoint")} must carry structured changes + citations')
    used = set()
    for tid, tt in t['templates'].items():
        keys = [n['key'] for n in tt['nodes']]
        if len(keys) != len(set(keys)):
            F.append(f'{tid}: duplicate node keys')
        for n in tt['nodes']:
            used.add(n['section'])
            if not isinstance(n.get('required'), bool) or not isinstance(n.get('repeatable'), bool):
                F.append(f'{tid}: node {n["key"]} must declare boolean required/repeatable')
            if n['section'] not in secs:
                F.append(f'{tid}: node {n["key"]} references missing section {n["section"]}')
    for i in sorted(set(secs) - used):
        F.append(f'section {i} is not used by any template')
    paths = [r['path'] for r in t['routes']]
    if len(paths) != len(set(paths)):
        F.append('a route is listed more than once')
    declared = [(r, tid) for tid, tt in t['templates'].items() for r in tt['routes']]
    for r in t['routes']:
        owners = [tid for rr, tid in declared if rr == r['path']]
        if owners != [r['template']]:
            F.append(f'route {r["path"]} must be declared by exactly its template {r["template"]}; declared by {owners}')
    for rr, tid in declared:
        if rr not in paths:
            F.append(f'{tid} declares route {rr} that is missing from the route map')
    for c in ids_in('components'):
        for p in load(f'components/{c}.json')['composes']:
            if p not in prims:
                F.append(f'component {c} composes unknown primitive {p}')
    I.append(f'{len(secs)} section contracts match the schema; {len(t["templates"])} template(s), {len(paths)} route(s) mapped 1:1')


@check('7 graph')
def c_graph(F, W, I):
    import semantic_validate as sv
    import adversarial_test as at
    g = load('compatibility/graph.json')['rules']
    gid = {r['id'] for r in g}
    v = set(sv.RULES)
    for r in sorted(gid - v):
        F.append(f'graph rule {r} has no validator implementation')
    for r in sorted(v - gid):
        F.append(f'validator rule {r} is not declared in compatibility/graph.json')
    for r in g:
        if r['severity'] not in ('error', 'warn'):
            F.append(f'{r["id"]}: severity {r["severity"]!r}')
    secs = set(ids_in('sections'))
    for r in g:
        for e in r.get('namedExceptions', []):
            for sid in e['pair']:
                if sid not in secs:
                    F.append(f'{r["id"]}: named exception references unknown section {sid}')
        for sid in r.get('params', {}).get('scrollStages', []) + r.get('params', {}).get('requires', []):
            if sid not in secs:
                F.append(f'{r["id"]}: params reference unknown section {sid}')
    n = 0
    for tid in load('templates/templates.json')['templates']:
        for req in (False, True):
            errs, warns = sv.validate(at.synth(tid, req))
            n += 1
            for m in errs + warns:
                F.append(f'{tid} ({"required-only" if req else "all nodes"}) is rejected by the graph/validator: {m}')
    I.append(f'{len(gid)} graph rules <-> {len(v)} validator rules; {n} template-synthesised specs accepted')


@check('8 versions')
def c_versions(F, W, I):
    m = load('registry.manifest.json')
    a = load('tokens/llm/component-allowlist.json')
    if m['allowlistVersion'] != a['version']:
        F.append(f"manifest allowlistVersion {m['allowlistVersion']} != allowlist version {a['version']}")
    s = load('schema/pagespec.schema.json')
    if m['pageSpecVersion'] != s['properties']['pageSpecVersion']['const']:
        F.append('manifest pageSpecVersion != schema pageSpecVersion const')
    I.append(f"allowlistVersion {a['version']} matches (machine-checked); pageSpecVersion == schema const; repositoryVersion is documentation-only")


def count_leaves(o):
    n = 0
    if isinstance(o, dict):
        if '$value' in o:
            return 1
        for k, v in o.items():
            if not k.startswith('$'):
                n += count_leaves(v)
    return n


def count_tokens(layer):
    d = os.path.join(ROOT, 'tokens', layer)
    return sum(count_leaves(load(f'tokens/{layer}/{f}')) for f in sorted(os.listdir(d)) if f.endswith('.json'))


def recount():
    import adversarial_test as at
    t = load('templates/templates.json')
    ad = load('assets/asset-roles.json')
    roles = ad['roles']
    return {
        'tokensFoundation': count_tokens('00-foundation'), 'tokensSemantic': count_tokens('10-semantic'),
        'tokensComponent': count_tokens('20-component'), 'tokensLayout': count_tokens('30-layout'),
        'primitives': len(ids_in('primitives')), 'components': len(ids_in('components')), 'sections': len(ids_in('sections')),
        'templates': len(t['templates']), 'routes': len(t['routes']), 'assetRoles': len(roles),
        'assetRolesSettable': sum(1 for r in roles.values() if r['settableInPageSpec']), 'pinnedPolicies': len(ad['pinnedPolicies']),
        'graphRules': len(load('compatibility/graph.json')['rules']), 'adversarialMutations': len(at.MUTATIONS),
        'adversarialControls': len(at.controls()), 'themes': len([f for f in os.listdir(os.path.join(ROOT, 'tokens', 'themes')) if f.endswith('.json')]),
        'measuredFacts': len(load('extraction/measured-values.json')['facts']),
    }


@check('9 counts')
def c_counts(F, W, I):
    m = load('registry.manifest.json')['counts']
    real = recount()
    for k, v in real.items():
        if m.get(k) != v:
            F.append(f'manifest counts.{k} = {m.get(k)} but files say {v}')
    for k in sorted(set(m) - set(real)):
        F.append(f'manifest counts.{k} is not recomputed by verify_all')
    txt = read_text(os.path.join(ROOT, 'README.md'))
    blk = re.search(r'<!-- counts:start -->(.*?)<!-- counts:end -->', txt, re.S)
    if not blk:
        F.append('README.md has no counts block')
    else:
        rd = dict(re.findall(r'^- (\w+): (\d+)$', blk.group(1), re.M))
        for k, v in real.items():
            if rd.get(k) != str(v):
                F.append(f'README counts {k} = {rd.get(k)} but files say {v}')
        for k in sorted(set(rd) - set(real)):
            F.append(f'README counts {k} is not recomputed by verify_all')
    I.append(', '.join(f'{k}={v}' for k, v in real.items()))


CITE_RE = re.compile(r'^(?P<path>[^:]+):(?P<a>\d+)(?:-(?P<b>\d+))?$')


def citations():
    for rel in json_files():
        stack = [load(rel)]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == 'measuredFrom' and isinstance(v, list):
                        for c in v:
                            yield rel, c
                    else:
                        stack.append(v)
            elif isinstance(o, list):
                stack.extend(o)


_FILES = {}


def file_text(full):
    if full not in _FILES:
        _FILES[full] = read_text(full)
    return _FILES[full]


@check('10 citations')
def c_cites(F, W, I):
    n_int = n_ext = n_orig = n_skip = 0
    for rel, c in citations():
        if not isinstance(c, dict) or 'cite' not in c:
            F.append(f'{rel}: citation must be an object with "cite": {c!r}')
            continue
        ref = c['cite']
        if ref.startswith('@original/'):
            fname = ref[len('@original/'):]
            if 'quote' not in c or '/' in fname or '..' in fname:
                F.append(f'{rel}: @original citations need a bare file name and a "quote": {ref}')
                continue
            if not ORIG_PRESENT:
                n_skip += 1
                continue
            full = os.path.join(ORIGINAL, fname)
            if not os.path.isfile(full):
                F.append(f'{rel}: cited original file missing: {fname}')
            elif c['quote'] not in file_text(full):
                F.append(f'{rel}: quote not found in {fname}: {c["quote"][:70]!r}')
            n_orig += 1
            continue
        m = CITE_RE.match(ref)
        if not m or 'expect' not in c:
            F.append(f'{rel}: malformed line citation (need path:line[-line] + expect): {ref!r}')
            continue
        path, a, b = m.group('path'), int(m.group('a')), int(m.group('b') or m.group('a'))
        if path.startswith('@repo/'):
            full = os.path.join(ROOT, path[6:])
            n_int += 1
        else:
            if os.path.isabs(path) or '..' in path.split('/'):
                F.append(f'{rel}: citation path must be project-relative: {ref}')
                continue
            if not SIBLING:
                n_skip += 1
                continue
            full = os.path.join(PROJECT, path)
            n_ext += 1
        if not os.path.isfile(full):
            F.append(f'{rel}: cited file missing: {path}')
            continue
        L = file_text(full).split('\n')
        if a < 1 or b < a or b > len(L):
            F.append(f'{rel}: {ref} out of range (file has {len(L)} lines)')
            continue
        if c['expect'] not in '\n'.join(L[a - 1:b]):
            F.append(f'{rel}: {ref} does not contain the expected text {c["expect"][:60]!r} (cited code moved or changed)')
    if n_skip:
        W.append(f'{n_skip} external citation(s) skipped: sibling clone project / original files not found next to design-repo/ (expected for a standalone copy)')
    I.append(f'{n_int} internal + {n_ext} project line citations (range + expected text) + {n_orig} original-file quotes resolved' + (f', {n_skip} skipped' if n_skip else ''))


MEDIA_EXT = ('.mp4', '.webm', '.mov', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.woff', '.woff2', '.ttf', '.otf', '.lottie')


@check('11 assets')
def c_assets(F, W, I):
    doc = load('assets/asset-roles.json')
    roles = doc['roles']
    pol = doc['policies']
    for p, d in pol.items():
        bad = set(d['allowedRefPrefixes']) - {'asset', 'generated', 'owner-supplied'}
        if bad:
            F.append(f'policy {p}: unknown ref prefixes {sorted(bad)}')
    for k, r in roles.items():
        if r['generationPolicy'] not in pol:
            F.append(f'{k}: policy {r["generationPolicy"]} not in the closed policy set')
        if r['settableInPageSpec'] and not pol.get(r['generationPolicy'], {}).get('allowedRefPrefixes'):
            F.append(f'{k}: settable role whose policy allows no assetRef prefix')
    for k, v in doc['pinnedPolicies'].items():
        if k not in roles:
            F.append(f'pinned role {k} missing')
        elif roles[k]['generationPolicy'] != v:
            F.append(f'PINNED policy drift: {k} is {roles[k]["generationPolicy"]!r}, must be {v!r}')
    for k, r in roles.items():
        if r['generationPolicy'] != 'may-generate-new' and k not in doc['pinnedPolicies']:
            F.append(f'compliance-critical role {k} ({r["generationPolicy"]}) is not pinned')
        if r['generationPolicy'] == 'must-not-reuse-live-endpoint' and not r.get('liveValues'):
            F.append(f'endpoint role {k} has no liveValues to enforce')
    settable = sorted(k for k, r in roles.items() if r['settableInPageSpec'])
    s = load('schema/pagespec.schema.json')
    if sorted(s['definitions']['assetRole']['enum']) != settable:
        F.append('schema definitions.assetRole enum != settable asset roles')
    if load('tokens/llm/component-allowlist.json')['assetRoles'] != settable:
        F.append('allowlist assetRoles != settable asset roles')
    used = schema_role_consts({k: v for k, v in s['definitions'].items() if k != 'assetRole'}, set())
    schema_role_consts(s['properties'], used)
    for r in sorted(used - set(settable)):
        F.append(f'schema field uses non-settable/unknown role {r}')
    for r in sorted(set(settable) - used):
        F.append(f'settable role {r} is not used by any schema field')
    ids = [a['id'] for r in roles.values() for a in r['assets']]
    if len(ids) != len(set(ids)):
        F.append('duplicate asset ids')
    for d, _, fs in os.walk(ROOT):
        for f in fs:
            if f.lower().endswith(MEDIA_EXT) or 'lottie' in f.lower():
                F.append(f'media/font/Lottie file shipped inside design-repo: {os.path.relpath(os.path.join(d, f), ROOT)}')
    if SIBLING:
        for r in roles.values():
            for a in r['assets']:
                if not os.path.isfile(os.path.join(PROJECT, a['source'])):
                    F.append(f"asset source missing in clone: {a['source']}")
            for fs in r.get('forbiddenSources', []):
                hits = [os.path.join(dp, fn) for dp, _, fns in os.walk(os.path.join(PROJECT, 'src')) for fn in fns
                        if os.path.basename(fs) in file_text(os.path.join(dp, fn))]
                if hits:
                    F.append(f'forbidden source {fs} is referenced by the clone: {[os.path.relpath(h, PROJECT) for h in hits]}')
    else:
        W.append('asset sources / forbidden-source usage not checked: no sibling clone project')
    I.append(f'{len(roles)} roles ({len(settable)} settable), {len(doc["pinnedPolicies"])} pinned policies hold, {len(ids)} registered assets, no media/font/Lottie files shipped')


def token_tree():
    tree = {}
    for layer in ('00-foundation', '10-semantic', '20-component', '30-layout'):
        for f in sorted(os.listdir(os.path.join(ROOT, 'tokens', layer))):
            if f.endswith('.json'):
                tree.update({k: v for k, v in load(f'tokens/{layer}/{f}').items() if not k.startswith('$')})
    return tree


def resolve(tree, ref):
    parts = ref.split('.')
    for i in range(len(parts), 0, -1):
        top = '.'.join(parts[:i])
        if top in tree:
            node = tree[top]
            for p in parts[i:]:
                if not isinstance(node, dict) or p not in node:
                    return None
                node = node[p]
            return node
    return None


def leaves(o, p=''):
    for k, v in o.items():
        if k.startswith('$'):
            continue
        if isinstance(v, dict) and '$value' in v:
            yield p + k, v
        elif isinstance(v, dict):
            yield from leaves(v, p + k + '.')


@check('12 tokens')
def c_tokens(F, W, I):
    tree = token_tree()
    n = 0
    for layer in ('10-semantic', '20-component', '30-layout'):
        for f in os.listdir(os.path.join(ROOT, 'tokens', layer)):
            for ref in re.findall(r'\{([a-z0-9][a-z0-9.-]*)\}', json.dumps(load(f'tokens/{layer}/{f}'))):
                n += 1
                if resolve(tree, ref) is None:
                    F.append(f'tokens/{layer}/{f}: unresolved token reference {{{ref}}}')
    th = load('tokens/themes/typewave-dark.json')
    roles = ['color-roles.' + p for p, _ in leaves(tree['color-roles'])]
    for r in roles:
        e = th['resolves'].get(r)
        tgt = resolve(tree, resolve(tree, r)['$value'].strip('{}'))
        if e is None:
            F.append(f'theme does not resolve {r}')
        elif tgt is None or e['value'] != tgt['$value']:
            F.append(f'theme value for {r} ({e["value"]}) != foundation ({tgt and tgt["$value"]})')
    for r in sorted(set(th['resolves']) - set(roles)):
        F.append(f'theme resolves unknown role {r}')
    cat = load('tokens/llm/token-catalog.json')['categories']
    real = {top: dict(leaves(body)) for top, body in tree.items()}
    for top in sorted(set(cat) | set(real)):
        a, b = cat.get(top, {}), real.get(top, {})
        for k in sorted(set(a) - set(b)):
            F.append(f'token-catalog lists {top}.{k} that no token file holds')
        for k in sorted(set(b) - set(a)):
            F.append(f'token {top}.{k} is missing from token-catalog')
        for k in sorted(set(a) & set(b)):
            if a[k]['value'] != b[k]['$value']:
                F.append(f'token-catalog value for {top}.{k} is stale')
    for k in load('tokens/llm/token-policy.json')['rawValueRestrictions']:
        if k not in cat:
            F.append(f'token-policy key {k!r} is not a real catalog category')
    I.append(f'{n} token references resolve; theme resolves {len(roles)} colour roles; catalog {sum(len(v) for v in cat.values())} tokens == token leaves')


@check('13 manifest')
def c_manifest(F, W, I):
    m = load('registry.manifest.json')
    flat = [p for v in m['entryPoints'].values() for p in (v if isinstance(v, list) else [v])]
    for p in flat:
        if os.path.isabs(p) or p.startswith('..') or '/../' in p or p.startswith('@'):
            F.append(f'entryPoint outside design-repo: {p}')
        elif not os.path.exists(os.path.join(ROOT, p)):
            F.append(f'entryPoint missing: {p}')
    for k in ('repositoryId', 'status', 'productionApproved', 'defaultTheme', 'schemaValidatedThemes', 'versionFieldNote', 'allowlistVersion', 'pageSpecVersion'):
        if k not in m:
            F.append(f'manifest missing {k}')
    if m.get('status') != 'design-review-pending':
        F.append('status must stay design-review-pending')
    if m.get('productionApproved') is not False:
        F.append('productionApproved must stay false until human design review')
    themes = [f[:-5] for f in os.listdir(os.path.join(ROOT, 'tokens', 'themes')) if f.endswith('.json')]
    if m.get('defaultTheme') not in themes or sorted(m.get('schemaValidatedThemes', [])) != sorted(load('schema/pagespec.schema.json')['properties']['theme']['enum']):
        F.append('defaultTheme / schemaValidatedThemes disagree with tokens/themes or the schema theme enum')
    I.append(f'{len(flat)} entry points, all inside design-repo/')


@check('14 paths')
def c_paths(F, W, I):
    pats = ['/' + 'Users/', '/' + 'private/tmp', '/' + 'home/', '/' + 'var/folders', 'C:' + '\\\\']
    n = 0
    for d, _, fs in os.walk(ROOT):
        if '__pycache__' in d:
            continue
        for f in fs:
            full = os.path.join(d, f)
            try:
                txt = read_text(full)
            except (UnicodeDecodeError, OSError):
                continue
            n += 1
            for p in pats:
                if p in txt:
                    F.append(f'{os.path.relpath(full, ROOT)} contains an absolute local path ({p})')
    I.append(f'{n} text files scanned')


def norm(s):
    return ' '.join(html.unescape(s).lower().split())


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def original_corpus():
    parts = []
    page = os.path.join(ORIGINAL, 'Typewave .html')
    if os.path.isfile(page):
        t = re.sub(r'<style\b.*?</style>', ' ', file_text(page), flags=re.S | re.I)
        parts.append(re.sub(r'<[^>]+>', ' ', t))
    lot = os.path.join(PROJECT, 'recon-assets', 'breakpoint-lottie.json')
    if os.path.isfile(lot):
        def texts(o):
            if isinstance(o, dict):
                if isinstance(o.get('t'), str) and isinstance(o.get('s'), (int, float)):
                    yield o['t']
                for v in o.values():
                    yield from texts(v)
            elif isinstance(o, list):
                for v in o:
                    yield from texts(v)
        parts.extend(texts(json.loads(file_text(lot))))
    return norm(' \n '.join(parts))


PROVENANCE_MIN_WORDS = 6   # example strings this long must come from the clone's placeholder copy
GUARD_MIN_WORDS = 4        # repo strings this long must not occur in the live site's copy


def clone_corpus():
    parts = [file_text(os.path.join(PROJECT, 'index.html'))]
    for dp, _, fns in os.walk(os.path.join(PROJECT, 'src')):
        for fn in sorted(fns):
            if fn.endswith(('.js', '.jsx')):
                parts.append(file_text(os.path.join(dp, fn)))
    return norm(' \n '.join(parts))


@check('15 copy')
def c_copy(F, W, I):
    ex = load('schema/example.pagespec.json')
    dev = load('extraction/measured-values.json').get('exampleDeviations', [])
    allowed = {d['value'] for d in dev}
    all_ex = set(strings(ex))
    for d in dev:
        if d['value'] not in all_ex:
            F.append(f'stale exampleDeviations entry (value not in the example): {d["path"]}')
    longs = sorted({s for s in all_ex if len(s.split()) >= PROVENANCE_MIN_WORDS} - allowed)
    if SIBLING:
        clone = clone_corpus()
        for s in longs:
            if norm(re.sub(r'[|\[\]]', ' ', s)) not in clone and norm(s) not in clone:
                F.append(f'example string is not the clone placeholder copy (src/ or index.html) and not a recorded deviation: {s[:70]!r}')
    else:
        W.append('example copy provenance not checked: no sibling clone project')
    corpus = original_corpus() if ORIG_PRESENT else ''
    n = 0
    if corpus:
        for rel in json_files():
            for s in strings(load(rel)):
                if len(s.split()) >= GUARD_MIN_WORDS:
                    n += 1
                    if norm(s) in corpus:
                        F.append(f'{rel}: reproduces live-site copy: {s[:70]!r}')
        if SIBLING:
            src = [norm(s) for s in re.findall(r"'([^'\n]{12,})'", file_text(os.path.join(PROJECT, 'src', 'content.js')))]
            hits = [s for s in src if len(s.split()) >= GUARD_MIN_WORDS and s in corpus]
            if hits:
                W.append(f'the CLONE (outside this repo) ships {len(hits)} src/content.js string(s) identical to live-site copy; '
                         'the example rewords them (exampleDeviations). Strings not printed on purpose.')
    else:
        W.append('original-copy guard not run: original page / Lottie not found (standalone copy)')
    I.append(f'{len(longs)} long example strings {"traced to" if SIBLING else "NOT traced (standalone) to"} the clone placeholder copy (+{len(allowed)} recorded deviations); '
             f'{n} repo strings (>= {GUARD_MIN_WORDS} words) checked against the live-site copy')


@check('16 source-sync')
def c_sync(F, W, I):
    if not SIBLING:
        W.append('skipped: no sibling clone project (standalone copy)')
        return
    app = file_text(os.path.join(PROJECT, 'src', 'App.jsx'))
    ret = app[app.index('return ('):]
    order = re.findall(r'<([A-Z][A-Za-z]+) />', ret)
    t = load('templates/templates.json')['templates']['template.home']
    want = [n['component'] for n in t['nodes']]
    if order != want:
        F.append(f'App.jsx render order {order} != template.home node order {want}')
    pkg = json.loads(file_text(os.path.join(PROJECT, 'package.json')))
    deps = dict(pkg.get('dependencies', {}), **pkg.get('devDependencies', {}))
    stated = load('registry.manifest.json')['source']['cloneDependencies']
    for k, v in stated.items():
        if deps.get(k) != v:
            F.append(f'manifest states {k} {v} but package.json has {deps.get(k)}')
    if 'lottie-web' in deps:
        F.append('lottie-web is a dependency again: the Lottie must not be reused')
    if 'affiliate.js' in file_text(os.path.join(PROJECT, 'index.html')).replace('<!-- Lemon Squeezy affiliate.js intentionally omitted', ''):
        F.append('index.html references affiliate.js')
    I.append(f'App.jsx order == template.home ({len(order)} components); {len(stated)} dependency versions match package.json; no lottie-web / affiliate.js')


def main():
    if '--counts' in sys.argv:
        print(json.dumps(recount()))
        return 0
    for c in CHECKS:
        c()
    bad = 0
    mode = 'present' if SIBLING else 'ABSENT - standalone mode'
    print(f'verify_all  (design-repo/; sibling clone project: {mode}; original files: {"present" if ORIG_PRESENT else "absent"})')
    for name, F, W, I in RESULTS:
        status = 'FAIL' if F else ('WARN' if W else 'PASS')
        bad += bool(F)
        print(f'[{status}] {name:14s} {"; ".join(I)}')
        for x in F[:25]:
            print(f'        FAIL  {x}')
        if len(F) > 25:
            print(f'        ... {len(F) - 25} more')
        for x in W:
            print(f'        warn  {x}')
    print(f'\n{len(RESULTS) - bad}/{len(RESULTS)} checks passed')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())

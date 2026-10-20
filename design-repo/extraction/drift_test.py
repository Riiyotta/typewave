#!/usr/bin/env python3
"""Drift proof: shows that verify_all.py's drift checks actually FAIL on injected drift.

For each case the whole design-repo is copied into a scratch directory, ONE drift is injected, and
verify_all.py is run against the copy (with --project pointing at the real clone project when it exists, so
external citations are resolvable). The case passes only if verify_all exits 1 AND the named check FAILs.
Finally the real, unmodified repo must exit 0.

Usage: python3 extraction/drift_test.py [--workdir DIR]   (default: a fresh tempfile.mkdtemp())
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.dirname(ROOT)
HAS_PROJECT = os.path.isfile(os.path.join(PROJECT, 'src', 'App.jsx'))


def jload(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def jsave(p, o):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(o, f, indent=2, ensure_ascii=False)
        f.write('\n')


def edit_json(rel, fn):
    def go(repo):
        p = os.path.join(repo, rel)
        o = jload(p)
        fn(o)
        jsave(p, o)
    return go


def edit_text(rel, fn):
    def go(repo):
        p = os.path.join(repo, rel)
        with open(p, encoding='utf-8') as f:
            t = f.read()
        with open(p, 'w', encoding='utf-8') as f:
            f.write(fn(t))
    return go


def first_cite(o, pred):
    """Return the first measuredFrom entry (dict) satisfying pred, depth-first."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'measuredFrom' and isinstance(v, list):
                for c in v:
                    if pred(c):
                        return c
            r = first_cite(v, pred)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = first_cite(v, pred)
            if r is not None:
                return r
    return None


def set_cite(rel, pred, mut):
    def f(o):
        c = first_cite(o, pred)
        assert c is not None, 'no citation to mutate'
        mut(c)
    return edit_json(rel, f)


CASES = [
    ('phantom allowlist entry', '5 allowlist',
     edit_json('tokens/llm/component-allowlist.json', lambda o: o['sections'].append(dict(o['sections'][0], id='hero.phantom', file='sections/hero.phantom.json')))),
    ('orphan contract file (no allowlist entry)', '5 allowlist',
     lambda repo: shutil.copy(os.path.join(repo, 'primitives', 'tag.json'), os.path.join(repo, 'primitives', 'orphan.json'))),
    ('out-of-range internal citation (@repo/)', '10 citations',
     set_cite('compatibility/graph.json', lambda c: c['cite'].startswith('@repo/'), lambda c: c.__setitem__('cite', re.sub(r':\d+$', ':99999', c['cite'])))),
    ('in-range citation with wrong expected text', '10 citations',
     set_cite('compatibility/graph.json', lambda c: c['cite'].startswith('@repo/'), lambda c: c.__setitem__('expect', 'text that is not on that line'))),
    ('wrong manifest count', '9 counts', edit_json('registry.manifest.json', lambda o: o['counts'].__setitem__('sections', o['counts']['sections'] + 1))),
    ('README count drift', '9 counts', edit_text('README.md', lambda t: re.sub(r'^- graphRules: \d+$', '- graphRules: 99', t, flags=re.M))),
    ('wrong allowlistVersion', '8 versions', edit_json('registry.manifest.json', lambda o: o.__setitem__('allowlistVersion', '9.9.9'))),
    ('pinned policy changed to a different VALID value', '11 assets',
     edit_json('assets/asset-roles.json', lambda o: o['roles']['media.hero-video'].__setitem__('generationPolicy', 'may-generate-new'))),
    ('graph rule with no validator implementation', '7 graph',
     edit_json('compatibility/graph.json', lambda o: o['rules'].append(dict(o['rules'][0], id='INVENTED_RULE')))),
    ('entryPoint outside design-repo', '13 manifest', edit_json('registry.manifest.json', lambda o: o['entryPoints'].__setitem__('spec', '../CLONE_SPEC.md'))),
    ('absolute local path injected', '14 paths', edit_text('CHANGELOG.md', lambda t: t + '\nsee ' + '/' + 'Users/someone/design-repo\n')),
    ('stale token catalog value', '12 tokens',
     edit_json('tokens/llm/token-catalog.json', lambda o: o['categories']['color']['brand'].__setitem__('value', '#FF0000'))),
]
if HAS_PROJECT:
    CASES.append(('out-of-range external citation (clone source)', '10 citations',
                  set_cite('sections/hero.video-scale.json', lambda c: c['cite'].startswith('src/'), lambda c: c.__setitem__('cite', re.sub(r':[\d-]+$', ':99999', c['cite'])))))
    CASES.append(('original-file quote that does not exist', '10 citations',
                  set_cite('tokens/00-foundation/motion.json', lambda c: c['cite'].startswith('@original/'), lambda c: c.__setitem__('quote', 'duration:9.9'))))


def run_verify(repo):
    cmd = [sys.executable, os.path.join(repo, 'extraction', 'verify_all.py')]
    if HAS_PROJECT:
        cmd += ['--project', PROJECT]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout


def main():
    work = sys.argv[sys.argv.index('--workdir') + 1] if '--workdir' in sys.argv else tempfile.mkdtemp(prefix='typewave-drift-')
    os.makedirs(work, exist_ok=True)
    fails = 0
    for i, (name, check, inject) in enumerate(CASES):
        case = os.path.join(work, f'case{i:02d}', 'design-repo')
        shutil.rmtree(os.path.dirname(case), ignore_errors=True)
        shutil.copytree(ROOT, case, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
        inject(case)
        rc, out = run_verify(case)
        failed_checks = re.findall(r'^\[FAIL\] (\d+ [\w-]+)', out, re.M)
        ok = rc == 1 and check in failed_checks
        fails += not ok
        detail = next((l.strip() for l in out.splitlines() if l.strip().startswith('FAIL ')), '')
        print(f"  {'CAUGHT' if ok else 'MISSED'}  {name}: exit {rc}, failing checks {failed_checks}\n          {detail[:150]}")
    rc, out = run_verify(ROOT)
    print(f"  {'PASS' if rc == 0 else 'FAIL'}  real repo (unmodified): exit {rc}; {out.strip().splitlines()[-1]}")
    fails += rc != 0
    print(f'\n{len(CASES)} drift cases in {work}: ' + ('ALL CAUGHT, real repo passes' if not fails else f'{fails} PROBLEM(S)'))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())

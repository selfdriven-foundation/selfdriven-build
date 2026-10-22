"""Make Artifact-ready copies of the two TrialThread pages.
usage: python3 scripts/publish-prep.py <plan_url or -> <observer_url or ->"""
import re, shutil, sys
from pathlib import Path
SRC = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent.parent / '_publish'  # copies to publish; not the source
plan_url, obs_url = (a if a != '-' else None for a in sys.argv[1:3])

def strip(s):
    s = re.sub(r'(?i)<!doctype html>\s*', '', s)
    for t in ['<html lang="en">', '<head>', '</head>', '<body>', '</body>', '</html>', '<meta charset="utf-8">']:
        s = s.replace(t, '')
    s = re.sub(r'<meta name="viewport"[^>]*>\n?', '', s)
    return s.strip() + '\n'

# observer
OBS = 'areas-of-focus/02-enablement/workings/trialthread-observer-app.html'
s = strip((SRC / OBS).read_text())
p = plan_url or '#'
s = s.replace('<a href="../../../trialthread-plan.html">← Plan</a>', f'<a href="{p}">← Plan</a>')
s = s.replace('<a href="../../../trialthread-plan.html">Back to the plan</a> · <a href="../../06-accountability/workings/06-accountability-trialthread-observer.md">Design notes (markdown)</a>',
              f'<a href="{p}">Back to the plan</a> (design notes are under Observer)')
(OUT / 'observer').mkdir(parents=True, exist_ok=True)
(OUT / 'observer/trialthread-observer.html').write_text(s)

# plan
s = strip((SRC / 'trialthread-plan.html').read_text())
o = obs_url or OBS
s = s.replace(f'href="{OBS}"', f'href="{o}"')
for rel in (OBS, '../../02-enablement/workings/trialthread-observer-app.html', '../../../' + OBS):
    s = s.replace(f'({rel})', f'({o})')
s = s.replace('<a class="btn" id="mdvRaw"', '<a class="btn" id="mdvRaw" hidden')
(OUT / 'plan').mkdir(parents=True, exist_ok=True)
(OUT / 'plan/trialthread-plan.html').write_text(s)
ref = OUT / 'plan/areas-of-focus/01-direction/references'
ref.mkdir(parents=True, exist_ok=True)
for f in (SRC / 'areas-of-focus/01-direction/references').glob('*.jpg'):
    shutil.copy(f, ref / f.name)
print('ok', 'plan_url=', plan_url, 'obs_url=', obs_url)

# index (front door): links out to the two published pages
s = strip((SRC / 'index.html').read_text())
s = s.replace('href="trialthread-plan.html"', f'href="{plan_url or "trialthread-plan.html"}"')
s = s.replace(f'href="{OBS}"', f'href="{obs_url or OBS}"')
(OUT / 'index').mkdir(parents=True, exist_ok=True)
(OUT / 'index/trialthread-index.html').write_text(s)
print('index ok')

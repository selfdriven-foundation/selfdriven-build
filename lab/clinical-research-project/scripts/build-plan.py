#!/usr/bin/env python3
"""Rebuild the TrialThread plan outputs from TRIALTHREAD-PLAN.md.

1. Split the master plan's "## 0N · Area" sections into
   areas-of-focus/0N-<area>/workings/0N-<area>-trialthread.md (overwrites those
   generated files only; other workings files are left alone).
2. Embed the master plan and every workings/*.md into trialthread-plan.html
   between the EMBED markers, so the in-page markdown preview works when the
   page is opened straight from disk (file:// can't fetch).

Run from anywhere:  python3 scripts/build-plan.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "TRIALTHREAD-PLAN.md"
PAGE = ROOT / "trialthread-plan.html"
AREAS = {"01": "direction", "02": "enablement", "03": "protocols", "04": "sustainability",
         "05": "processes", "06": "accountability", "07": "engagement", "08": "organisational"}
BEGIN, END = "<!--EMBED:BEGIN-->", "<!--EMBED:END-->"


def rebase_links(md: str, prefix: str) -> str:
    """Point relative links written from the repo root at the same targets from a deeper folder."""
    def fix(m):
        target = m.group(2)
        if re.match(r"(https?:|mailto:|#|/|\.\./)", target):
            return m.group(0)
        return f"{m.group(1)}({prefix}{target})"
    return re.sub(r"(\[[^\]]*\])\(([^)\s]+)\)", fix, md)


def split():
    s = PLAN.read_text()
    notes = re.search(r"(?ms)^## What the notes said\n.*?(?=^---\n\n## 01)", s).group(0)
    for part in re.split(r"(?m)^(?=## 0[1-8] · )", s):
        m = re.match(r"## (0[1-8]) · ", part)
        if not m:
            continue
        n = m.group(1)
        name = AREAS[n]
        body = part.rstrip().rstrip("-").rstrip()
        if n == "01":
            body += "\n\n---\n\n" + notes.rstrip()
        body = rebase_links(body.replace(f"## {n} · ", "## ", 1), "../../../")
        header = (f"# TrialThread — {n} · {name.capitalize()}\n\n"
                  "> Generated from [`TRIALTHREAD-PLAN.md`](../../../TRIALTHREAD-PLAN.md) by "
                  "`scripts/build-plan.py`. Edit the master plan, then rebuild. "
                  "Interactive: [`trialthread-plan.html`](../../../trialthread-plan.html).\n\n")
        out = ROOT / f"areas-of-focus/{n}-{name}/workings/{n}-{name}-trialthread.md"
        out.write_text(header + body + "\n")
        print("split ", out.relative_to(ROOT))


def embed():
    files = [PLAN] + sorted(ROOT.glob("areas-of-focus/*/workings/*.md"))
    blocks = []
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        text = f.read_text().replace("</script", "<\\/script")
        blocks.append(f'<script type="text/markdown" data-path={json.dumps(rel)}>\n{text}\n</script>')
    page = PAGE.read_text()
    if BEGIN not in page or END not in page:
        raise SystemExit(f"markers {BEGIN} … {END} not found in {PAGE.name}")
    head, rest = page.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    PAGE.write_text(head + BEGIN + "\n" + "\n".join(blocks) + "\n" + END + tail)
    print(f"embed  {len(files)} markdown files into {PAGE.name}")


if __name__ == "__main__":
    split()
    embed()

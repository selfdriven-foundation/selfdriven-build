#!/usr/bin/env python3
"""File intake and routing for a conducting portfolio.

Every move is appended to logs/file-log.md. Nothing is ever deleted or
overwritten: superseded material is filed to an area's _archive/ instead.

  aof.py intake PATH... [--copy]          bring files into areas-of-focus/00-inbox/
  aof.py file ITEM AREA [FOLDER]          place an inbox item (or any path) into an area
         [--topic T] [--dated] [--version N]
  aof.py inbox                            list the inbox with ages; flags anything > 7 days
  aof.py log [-n N] [--area AREA]         show the most recent file-log rows

AREA is a number, slug or both: 5, 05, processes, 05-processes.
FOLDER is one of workings (default), references, shared, sessions, _archive.

Standard library only.
"""
import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AOF = ROOT / "areas-of-focus"
INBOX = AOF / "00-inbox"
LOG = ROOT / "logs" / "file-log.md"

AREAS = ["01-direction", "02-enablement", "03-protocols", "04-sustainability",
         "05-processes", "06-accountability", "07-engagement", "08-organisational"]
FOLDERS = ["workings", "references", "shared", "sessions", "_archive"]
INBOX_MAX_DAYS = 7
# Dates inside documents are D MMM YYYY; in filenames DDMMYYYY (portfolio-layout.md).
LOG_TIME = "%-d %b %Y %H:%M"
LOG_TIME_PARSE = "%d %b %Y %H:%M"
LOG_HEADER = (
    "# File log\n\n"
    "Append-only. Written by `scripts/aof.py`; every intake and placement is one row.\n"
    "Git holds the history of this file — never edit or delete a row.\n\n"
    "| When | Action | From | To |\n"
    "|---|---|---|---|\n"
)
IGNORED = {".gitkeep", ".DS_Store"}


def die(msg):
    sys.exit(f"aof: {msg}")


def rel(p):
    p = Path(p).resolve()
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def log_row(action, src, dest, dry):
    row = f"| {datetime.now().strftime(LOG_TIME)} | {action} | `{rel(src)}` | `{rel(dest)}` |\n"
    if dry:
        print(f"  (dry run) would log: {row.strip()}")
        return
    LOG.parent.mkdir(exist_ok=True)
    if not LOG.exists():
        LOG.write_text(LOG_HEADER)
    with LOG.open("a") as f:
        f.write(row)


def read_log():
    if not LOG.exists():
        return []
    rows = []
    for line in LOG.read_text().splitlines():
        m = re.match(r"\| (.+?) \| (\w+) \| `(.+?)` \| `(.+?)` \|$", line)
        if m:
            rows.append(m.groups())
    return rows


def resolve_area(arg):
    a = arg.strip().lower().strip("/")
    for area in AREAS:
        num, slug = area.split("-", 1)
        if a in (area, slug, num, num.lstrip("0")):
            return area
    die(f"unknown area '{arg}'. Use one of: {', '.join(AREAS)}")


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if not s:
        die(f"topic '{text}' has nothing usable for a filename")
    return s


def move(src, dest, copy, dry):
    if dest.exists():
        die(f"'{rel(dest)}' already exists — refusing to overwrite. "
            f"Use --topic/--version, or file the old one to _archive first.")
    verb = "copy" if copy else "move"
    print(f"{verb}: {rel(src)} -> {rel(dest)}")
    if dry:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not copy:
        shutil.move(src, dest)
    elif src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


def cmd_intake(args):
    for p in args.paths:
        src = Path(p).expanduser().resolve()
        if not src.exists():
            die(f"no such file: {p}")
        if src.is_relative_to(AOF):
            die(f"'{rel(src)}' is already inside areas-of-focus — use `file` to move it between areas")
        dest = INBOX / src.name
        move(src, dest, args.copy, args.dry_run)
        log_row("intake", src, dest, args.dry_run)


def cmd_file(args):
    item = Path(args.item).expanduser()
    src = item if item.exists() else INBOX / args.item
    if not src.exists():
        die(f"'{args.item}' not found as a path or in 00-inbox/")
    src = src.resolve()
    area = resolve_area(args.area)
    if args.folder not in FOLDERS:
        die(f"folder must be one of: {', '.join(FOLDERS)}")

    ext = src.suffix if src.is_file() else ""
    stem = slug(args.topic) if args.topic else src.name[: len(src.name) - len(ext)]
    if args.dated:
        stem += "-" + datetime.now().strftime("%d%m%Y")
    if args.version:
        stem += f"-v{args.version}"
    dest = AOF / area / args.folder / (stem + ext)
    move(src, dest, False, args.dry_run)
    log_row("archive" if args.folder == "_archive" else "file", src, dest, args.dry_run)


def inbox_items():
    if not INBOX.exists():
        return []
    return sorted(p for p in INBOX.iterdir() if p.name not in IGNORED)


def cmd_inbox(args):
    items = inbox_items()
    if not items:
        print("00-inbox is empty.")
        return
    # Age counts from intake (the log), not the file's mtime: a move keeps the old mtime.
    intaken = {}
    for when, action, _src, dest in read_log():
        if action == "intake":
            try:
                intaken[dest] = datetime.strptime(when, LOG_TIME_PARSE)
            except ValueError:
                pass
    now = datetime.now()
    overdue = 0
    print(f"00-inbox — {len(items)} item(s). Nothing stays longer than {INBOX_MAX_DAYS} days.\n")
    for p in items:
        since = intaken.get(rel(p))
        source = "intake"
        if since is None:
            since, source = datetime.fromtimestamp(p.stat().st_mtime), "mtime, not logged"
        days = (now - since).days
        flag = ""
        if days > INBOX_MAX_DAYS:
            overdue += 1
            flag = "   <- OVERDUE: place it at this week's check-in"
        print(f"  {p.name:<48} {days:>3}d  ({source}){flag}")
    if overdue:
        print(f"\n{overdue} overdue. Route each with: which score is worse off without it?")


def cmd_log(args):
    rows = read_log()
    if args.area:
        area = resolve_area(args.area)
        rows = [r for r in rows if f"areas-of-focus/{area}/" in r[2] + r[3]]
    if not rows:
        print("No file-log rows" + (" for that area." if args.area else " yet."))
        return
    for when, action, src, dest in rows[-args.n:]:
        print(f"{when:<18} {action:<8} {src}  ->  {dest}")


def main():
    ap = argparse.ArgumentParser(prog="aof.py", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("intake", help="bring files into 00-inbox/")
    p.add_argument("paths", nargs="+")
    p.add_argument("--copy", action="store_true", help="copy instead of move")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_intake)

    p = sub.add_parser("file", help="place an item into an area folder")
    p.add_argument("item", help="name of an inbox item, or any path")
    p.add_argument("area")
    p.add_argument("folder", nargs="?", default="workings")
    p.add_argument("--topic", help="rename to <topic> (slugified)")
    p.add_argument("--dated", action="store_true", help="append today as -DDMMYYYY")
    p.add_argument("--version", type=int, help="append -v<N>")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_file)

    p = sub.add_parser("inbox", help="list inbox items and their ages")
    p.set_defaults(fn=cmd_inbox)

    p = sub.add_parser("log", help="show recent file-log rows")
    p.add_argument("-n", type=int, default=20)
    p.add_argument("--area")
    p.set_defaults(fn=cmd_log)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()

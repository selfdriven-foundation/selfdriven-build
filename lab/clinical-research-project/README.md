# Peter & Giau — conducting portfolio

One set of eight Areas of Focus covering everything in flight. Projects are
**tags** that flow *through* the areas; they do not get areas of their own.

Stood up 22 Oct 2026 from `templates/areas-of-focus/`. Conductor: Peter & Giau.
Area states (active / dormant), projects and the horizon live in
[`portfolio-manifest.json`](portfolio-manifest.json).

---

## The eight areas

| # | Area | Owns |
|---|---|---|
| 00 | [Inbox](areas-of-focus/00-inbox/) | Anything not yet placed. Sorted weekly, never a home. |
| 01 | [Direction](areas-of-focus/01-direction/01-direction-conducting-score.md) | Which projects exist, why, and which one you'd drop first |
| 02 | [Enablement](areas-of-focus/02-enablement/02-enablement-conducting-score.md) | The actual making: tooling, prototypes, data, design |
| 03 | [Protocols](areas-of-focus/03-protocols/03-protocols-conducting-score.md) | Accounts, domains, keys, hosting, standards |
| 04 | [Sustainability](areas-of-focus/04-sustainability/04-sustainability-conducting-score.md) | What it costs, what it earns |
| 05 | [Processes](areas-of-focus/05-processes/05-processes-conducting-score.md) | How work runs: the workflow, the scripts, this portfolio |
| 06 | [Accountability](areas-of-focus/06-accountability/06-accountability-conducting-score.md) | What's been promised to other people |
| 07 | [Engagement](areas-of-focus/07-engagement/07-engagement-conducting-score.md) | Who knows this exists |
| 08 | [Organisational](areas-of-focus/08-organisational/08-organisational-conducting-score.md) | Your cadence, collaborators, stewardship |

Dormant is a **recorded state**, not a gap. Every area has the same five folders:

| Folder | Test |
|---|---|
| `workings/` | This area is making it |
| `references/` | Someone else made it; we read it |
| `shared/` | We made it; other areas must read it |
| `sessions/` | A dated record of a working session |
| `_archive/` | Superseded, but the record needs it. Move, never delete. |

---

## Files and logs — `scripts/aof.py`

Standard-library Python; nothing to install. Run from this folder. Every intake
and placement is appended to `logs/file-log.md`. Nothing is overwritten or
deleted: a name clash stops the move.

```sh
scripts/aof.py intake ~/Downloads/thing.pdf          # into 00-inbox/ (--copy to leave the original)
scripts/aof.py inbox                                 # inbox with ages; flags anything > 7 days
scripts/aof.py file thing.pdf 05                     # -> 05-processes/workings/thing.pdf
scripts/aof.py file thing.pdf enablement references  # area by number or slug; any of the five folders
scripts/aof.py file thing.pdf 01 --topic "Hosting options" --dated
                                                     # -> 01-direction/workings/hosting-options-<DDMMYYYY>.pdf
scripts/aof.py file old-spec.md 03 _archive          # superseded: archive, never delete
scripts/aof.py log --area 05 -n 50                   # recent file-log rows, optionally per area
```

Add `--dry-run` to `intake` or `file` to see the move and log row first.

**Routing rule:** which score is worse off without it? Where there are two
answers, it goes to the area that owns the decision; the other links it from
`references/`.

---

## Naming

| Thing | Pattern | Example |
|---|---|---|
| Score | `<nn>-<area>-conducting-score.md` | `05-processes-conducting-score.md` |
| Session record / dated doc | `<topic>-<DDMMYYYY>.md` | `weekly-checkin-25102026.md` |
| Anything versioned | `<topic>-v<n>.md` | `trust-stack-spec-v2.md` |

Dates in filenames are `DDMMYYYY`; inside documents, `D MMM YYYY`.

---

## How a week runs

`/conducting week --root <this folder>`, or by hand, about ten minutes:

1. **Empty the inbox.** `scripts/aof.py inbox`, then `file` each item.
2. **Walk the eight.** Each area's last `This week` block and when it was touched.
3. **Carry forward first**, keeping the original raised-date.
4. **Take new lines.** One status word, one plain sentence, project tag where it has one.
5. **Derive the agenda.** Every `BLOCKED` and `FLAGGED` line, lifted out.
6. **Name what's silent.** An area that wrote nothing is reported silent, with its age.
7. **Commit.** The diff is the history.

### The six status words

Closed vocabulary — no seventh.

| Status | Means | To the agenda |
|---|---|---|
| `SHIPPED` | Done, in the record, evidence linked | no |
| `MOVED` | Progressed; evidence linked | no |
| `PENDING` | Awaiting this week's check-in | no |
| `PARKED` | Not this week, and here is why | no |
| `FLAGGED` | Something is wrong and it isn't moving | **yes** |
| `BLOCKED` | Needs a decision — name it | **yes** |

```markdown
- **SHIPPED** — One plain sentence. [evidence](link) `project-tag`
```

---

## What does not go here

Product code (it lives in its own repo; the score links to it), secrets,
generated copies (the console is built, not edited), and anything no score is
worse off without.

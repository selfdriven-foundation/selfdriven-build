# TrialThread — 05 · Processes

> Generated from [`TRIALTHREAD-PLAN.md`](../../../TRIALTHREAD-PLAN.md) by `scripts/build-plan.py`. Edit the master plan, then rebuild. Interactive: [`trialthread-plan.html`](../../../trialthread-plan.html).

## Processes — the workflows and the ingestion pipeline

### The CRA lifecycle today (and the hand-offs that hurt)

| Stage | What happens | Systems touched today | Manual pain |
|---|---|---|---|
| **Feasibility & selection** | Site questionnaires, PSV | Email, spreadsheets, CTMS | Duplicate questionnaires |
| **Start-up** | Essential documents, ethics/governance, CTN, contracts | eTMF, email, sponsor portals | Chasing CVs, GCP certs, licences, lab normals and accreditation |
| **Site initiation visit (SIV)** | Training, delegation log, ISF set-up | ISF (paper/e), CTMS, training LMS | Re-keying training and delegation into trackers |
| **Interim monitoring visits (IMV)** | SDV/SDR, ICF checks, IP accountability, ISF review, deviations, queries | EDC, ISF, CTMS, spreadsheets | Report written after the visit from notes; findings re-typed into CTMS |
| **Between visits** | Remote review, query follow-up, actions | EDC, email | Queries answered in two places; actions lost in email |
| **Safety** | SAE reporting and reconciliation | Safety DB, EDC | Manual line-by-line reconciliation |
| **Close-out (COV)** | Final reconciliation, archiving, IP return | ISF, eTMF, CTMS | TMF/ISF reconciliation by hand |

### The future flow: the ingestion pipeline

```
 SOURCE            INGEST                         CHECK              FLOW                 PROVE
 ───────           ─────────────────────────      ───────────        ─────────────        ─────────
 paper scan ─┐     1 capture   (phone/scanner/    5 check in         7 route to roles     9 sign (ACDC)
 eSource ────┤        upload/connector/email-in)     bounds             (RBAC + blinding)  10 hash → Nexus
 PDF/Word ───┼──▶  2 classify  (essential-doc        (Rule/Std/      8 raise query /      11 file to ISF/
 system API ─┤        type, study, site, subject)    Policy)            deviation /           eTMF; push to
 email ──────┘     3 extract   (data points, dates, 6 reconcile         action                EDC/CTMS
                      versions, signatures)            (vs EDC, CTMS,
                   4 confirm   (human, low-           eTMF, protocol
                      confidence fields first)        version)
```

Each step writes an event to the trail. Steps 2–3 may use AI; step 4 is
always human for anything bound for the EDC or a regulated decision.

### Ten "fundamental scripts" that pay off on day one

These are deliberately small, mostly deterministic automations — the
spreadsheet killers. Each becomes a module.

| # | Automation | Replaces | Rule tier |
|---|---|---|---|
| 1 | **Document expiry radar** — CVs, GCP certificates, licences, lab accreditation, normal ranges; chase 60/30/7 days before | Expiry spreadsheet | Policy |
| 2 | **ICF version guard** — every signed consent checked against the version approved on the signing date | Manual ICF log check | Rule + Standard |
| 3 | **Delegation × training cross-check** — nobody performs a delegated task without current training and PI sign-off | Visual log review | Standard |
| 4 | **Visit window calculator** — windows from protocol; flags out-of-window at scheduling and at entry | Paper calendars | Rule |
| 5 | **Query ageing & chaser** — one queue across EDCs; ageing alerts; answers linked to the record | Query spreadsheet + email | Policy |
| 6 | **Deviation log & classifier** — capture once, propose classification with cited rules, trend by site and protocol section | Deviation spreadsheet | Rule + Policy |
| 7 | **Monitoring report drafter** — findings captured in visit mode become the report and follow-up letter | Writing from notes | Policy |
| 8 | **ISF ⇄ eTMF reconciliation** — what should exist (from Appendix C and the study) vs what does, at both ends | Manual reconciliation | Standard |
| 9 | **IP accountability reconciliation** — dispensing vs returns vs IxRS | Manual counts | Rule |
| 10 | **SAE reconciliation** — EDC vs safety database line matching | Line-by-line review | Standard |

Plus: **ledger-derived site payments** (visits completed and verified → payment events).

### Discovery action items (from the whiteboard)

1. **SOP of all processes** — map every process Giau runs, as steps (generic,
   from public GCP knowledge and her experience; never an employer's SOP text).
2. **Systems inventory** — every system used: category, examples, what goes in,
   what comes out, who enters it, how often it's re-keyed.
3. **Query** — anatomy of a query: who raises, where, how it's answered,
   how long it takes, how often it's duplicated.
4. **Data point** — follow one data point from source to database lock, and
   count the hops.
5. **Breaches map (high level)** — the common deviation and finding types, where
   they originate, and which rule would have caught them at the door.

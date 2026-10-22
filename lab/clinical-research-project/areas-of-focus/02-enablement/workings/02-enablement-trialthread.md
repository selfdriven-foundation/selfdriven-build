# TrialThread — 02 · Enablement

> Generated from [`TRIALTHREAD-PLAN.md`](../../../TRIALTHREAD-PLAN.md) by `scripts/build-plan.py`. Edit the master plan, then rebuild. Interactive: [`trialthread-plan.html`](../../../trialthread-plan.html).

## Enablement — architecture, AI, verified context graph

### Architecture in seven layers

```
┌────────────────────────────────────────────────────────────────────────────┐
│ 7  EXPERIENCE   Role-based UI · CRA cockpit · site portal · inspector view │
├────────────────────────────────────────────────────────────────────────────┤
│ 6  WORKFLOW     Queries · deviations · actions · visits · approvals · $    │
├────────────────────────────────────────────────────────────────────────────┤
│ 5  CONTEXT      Verified context graph (Emergence): rules ↔ records ↔ why  │
├────────────────────────────────────────────────────────────────────────────┤
│ 4  RULES        Rule → Standard → Policy engine ("check in bounds")        │
├────────────────────────────────────────────────────────────────────────────┤
│ 3  RECORDS      Canonical record store · versions · data points · links    │
├────────────────────────────────────────────────────────────────────────────┤
│ 2  INGEST       Intake · classify · extract · human confirm · hash         │
├────────────────────────────────────────────────────────────────────────────┤
│ 1  TRUST        KERI identifiers · ACDC credentials · Nexus hash ledger    │
└────────────────────────────────────────────────────────────────────────────┘
         ↕ connectors: CTMS · EDC · eTMF · eISF · safety DB · IxRS · email
```

**1 · Trust.** Every person, organisation, site and AI agent has a KERI
identifier (AID). Qualifications (GCP certificate, licence, delegation) are
issued as ACDC credentials and can be selectively disclosed — a CRA can prove
"GCP-current" without sharing the certificate. Every record version and every
signature is hashed and the hash anchored in the Nexus ledger. Content stays in
the regulated store; the ledger proves it hasn't changed. This is the
selfdriven Human Interface Kit's *identity → protect → onchain* pattern:
SSI generated locally, hashed and protected locally, hash persisted only
when it needs to be shared.

**2 · Ingest.** One intake for every record (detail in §05). Deterministic
where possible (barcode, template, form fields); AI where needed
(classification, handwriting, extraction), always with a human confirmation
step and a confidence score.

**3 · Records.** A canonical model for trial records: *Study, Protocol
(versions, amendments), Site, Person, Role, Delegation, Training, Document
(essential document type per ICH E6(R3) Appendix C), Visit, Data point, Query,
Deviation, Action item, Finding, Signature, Payment event.* Every record is
versioned, nothing is deleted, every change is attributable (ALCOA++).

**4 · Rules.** Three tiers, as on the whiteboard:

| Tier | Source | Example rule |
|---|---|---|
| **Rule** | The protocol | "Visit 4 occurs Day 28 ± 3." "Exclusion 7: eGFR < 45." "ICF v3.0 required from 12 Mar." |
| **Standard** | ICH GCP, 21 CFR, TGA, NHMRC | "Consent must be obtained before any study procedure." "Electronic signature must show printed name, date/time and meaning." |
| **Policy** | Sponsor / CRO / site SOPs | "Trip report finalised within 10 working days." "GCP training renewed every 3 years." "Major deviations escalated to PM in 24 h." |

Rules are authored as data (not code), versioned, and each one is linked to
the clause it implements. A breach produces a typed finding — never a silent
failure.

**5 · Context.** The verified context graph (below).

**6 · Workflow.** Queries, deviations, actions, visit scheduling, approvals
and payment events, all raised *against* a record, routed by role, with
due-dates from the Policy tier.

**7 · Experience.** Role-based web app, tablet "visit mode" that works
offline at site, and a read-only, time-boxed inspector/auditor view.

**Connectors.** Read from and write to the sponsor's systems through their
APIs where they exist (most major CTMS/EDC/eTMF vendors publish APIs; CDISC
ODM is the common EDC exchange format), and through structured export/import
where they don't. The product is useful even with zero integrations — the
CRA's own workspace — and gets more useful with each one.

### The Emergence engine: a verified context graph for decisions

Emergence already turns unstructured regulatory text into typed knowledge
atoms and edges, with a gated, deterministic ingestion contract (no LLM in the
path between source and atom), and a synthesis layer where claims are backed by
atom evidence with amendment/supersede tracking. Clinical research is a
near-perfect fit for the same machinery:

**Atom types (clinical)**

| Atom | Example |
|---|---|
| `regulation-clause` | 21 CFR 11.10(e) — audit trails |
| `guideline-clause` | ICH E6(R3) Annex 1, sponsor section — monitoring (clause no. to confirm) |
| `protocol-requirement` | Protocol v4.0 §6.3 — Visit 4 window Day 28 ± 3 |
| `sop-step` | Sponsor SOP MON-004 step 7 — report finalised in 10 working days |
| `record` | Delegation log, site 012, version 6, hash `9f2…` |
| `data-point` | Visit 4 date = 2026-11-02 |
| `finding` | Visit 4 out of window by 2 days |
| `decision` | Classified *minor* deviation; no impact on primary endpoint |
| `signature` | ACDC credential: CRA AID `E7x…`, meaning "reviewed", 2026-11-04 10:12 AEDT |

**Edge types:** `implements` (SOP step → guideline clause), `requires`
(protocol requirement → data point), `evidences` (record → requirement),
`derived-from` (data point → record), `breaches` (finding → requirement),
`justified-by` (decision → clause / requirement / finding), `signed-by`
(decision → signature), `supersedes` (protocol v4 → v3).

**A decision trace** — what the "Why?" button on any decision shows:

```
DECISION  Minor deviation · Site 012 · Subject 012-007 · Visit 4
  ├─ justified-by → FINDING  Visit 4 on Day 33; window Day 25–31 → out by 2 days
  │      ├─ breaches → PROTOCOL v4.0 §6.3  "Visit 4 Day 28 ± 3"
  │      └─ derived-from → DATA POINT visit date ← RECORD source worksheet p.2 (hash 4ac…)
  ├─ justified-by → SOP DEV-002 §4  "out-of-window visits without safety impact = minor"
  │      └─ implements → ICH E6(R3) Annex 1 — non-compliance (clause no. to confirm)
  ├─ proposed-by → AI agent `deviation-classifier` v0.3 (confidence 0.91)
  └─ signed-by → CRA (ACDC "reviewed & classified"), PM (ACDC "acknowledged")
```

Every edge is checkable; every node is hashed; the trace is the audit
evidence. When the protocol is amended, `supersedes` edges show exactly which
decisions were made under which version. Patterns across the graph — "which
SOP steps generate the most deviations?", "which protocol sections cause most
queries?" — become the *breaches map* from the whiteboard, and feed back into
protocol design (quality by design, ICH E8(R1)).

What carries over from the Archy/Koboris insurance work: the ingestion contract
(membrane, gates, null-diff reconciliation), the regulatory ladder pattern
(law → standard → guide → code → disclosure becomes Act → GCP → guidance →
SOP → protocol), KERI/ACDC evidence chips, and the mesh-review discipline for
judging whether a proposed edge is true and useful.

### Where AI helps (and where it must not)

| Use | Type | Human step |
|---|---|---|
| Classify an incoming document into the essential-document taxonomy | Document AI | Coordinator confirms |
| Extract fields (dates, names, versions, signatures present) | Document AI / OCR | Confirm low-confidence fields |
| Read handwriting on paper source worksheets | Vision model | Mandatory confirm for any data point bound for EDC |
| Draft the monitoring visit report and follow-up letter from visit findings | LLM | CRA edits and signs |
| Propose deviation classification with cited rules | LLM + rules + graph | CRA decides |
| Draft query text | LLM | CRA sends |
| Spot anomalies (identical vitals across visits, implausible timing, data that's "too clean") | Statistical + ML | Feeds risk-based monitoring; CRA reviews |
| Answer "what does the protocol say about…" | Retrieval over the graph, cited | Informational only |
| Turn a protocol into a draft rules set and visit schedule | LLM | Data manager / PM validates before use |

**Never:** sign, approve, finalise a classification, change source data,
contact a site or participant, or unblind.

### Selfdriven Human Interface Kit — what we reuse

| Kit capability | In TrialThread |
|---|---|
| **Identity (SSI)** — generate a DID / AID on device | Every user and AI agent gets an identifier; credentials (GCP, licence, delegation) bound to it. |
| **Proof you're human** — WebAuthn / passkeys (biological signature) | Passkey login and Part 11-grade signature ceremony: re-authenticate at the moment of signing. |
| **Data proofs & protection** — hash + encrypt locally | Records hashed on arrival; sensitive content encrypted at rest; hash shared to the Nexus only. |
| **Collective engagement** — human and AI community members, MCP | Study team as a "community"; AI agents as registered members with mandates; MCP connectors to sponsor systems. |
| **Discoverability — human in the loop** | The "Why?" trace and the inbox of things awaiting a human decision. |
| **Geo-proof tasks** (ZK location proofs) | Optional: prove an on-site monitoring visit happened at the site, without tracking the CRA's location. |
| **3.0 visual system** — Poppins, warm neutral palette, ember accent `#DE5A31` | The UI language of the prototype. |

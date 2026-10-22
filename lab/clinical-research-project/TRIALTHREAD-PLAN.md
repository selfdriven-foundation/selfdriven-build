# TrialThread — one verified thread from source to submission

> **Working name.** Not trademark-checked. A concept plan for a clinical-research
> operations tool, drafted 22 Oct 2026 from the whiteboard and paper notes Peter
> and Giau made (both photos are in `areas-of-focus/01-direction/references/`).
>
> **Status:** concept / pre-discovery. Nothing here is validated with buyers yet.
> Regulatory references are accurate to the best of our knowledge at drafting;
> every one is marked for checking against the current text before it is relied on.

**Interactive version:** [`trialthread-plan.html`](trialthread-plan.html) (open in a browser).

---

## Contents

- [0 · Executive summary](#0--executive-summary)
- [What the notes said](#what-the-notes-said)
- [01 · Direction — problem, opportunity, product](#01--direction--problem-opportunity-product)
- [02 · Enablement — architecture, AI, verified context graph](#02--enablement--architecture-ai-verified-context-graph)
- [03 · Protocols — the regulations and how the product meets them](#03--protocols--the-regulations-and-how-the-product-meets-them)
- [04 · Sustainability — market, model, money](#04--sustainability--market-model-money)
- [05 · Processes — the workflows and the ingestion pipeline](#05--processes--the-workflows-and-the-ingestion-pipeline)
- [06 · Accountability — roles, access, audit, AI governance](#06--accountability--roles-access-audit-ai-governance)
- [07 · Engagement — users, interface, go-to-market](#07--engagement--users-interface-go-to-market)
- [08 · Organisational — team, roadmap, risks, next steps](#08--organisational--team-roadmap-risks-next-steps)

---

## 0 · Executive summary

**The problem.** A Clinical Research Associate (CRA) is the person a sponsor or
CRO sends to make sure a trial site is protecting participants and producing
trustworthy data. In practice a large share of the job is administrative
reconciliation: copying the same fact between the CTMS, EDC, eTMF, the
Investigator Site File, sponsor spreadsheets and email; chasing expired
certificates and unsigned logs; re-typing visit findings into monitoring
reports; and keeping trackers in Excel because no system talks to another.
Every manual hop is a chance for a transcription error, a missed deviation or
a gap an auditor will find. The risk is systemic, not individual: it is built
into how the systems are (not) connected.

**The opportunity.** ICH E6(R3) — the new Good Clinical Practice guideline,
now being adopted by the FDA, EMA and TGA — explicitly pushes the industry
towards risk-proportionate, quality-by-design, technology-enabled trials and
asks for data governance and computerised-system controls that the current
spreadsheet layer cannot evidence. That creates a window for a tool that
**sits across the existing systems instead of replacing them**, captures
each record once, checks it against the rules automatically, and leaves a
verifiable trail of who did what, when, and why.

**The product.** TrialThread is a records-ingestion and workflow layer for
clinical trial operations:

1. **Ingest once.** Any record — scanned paper source, an eSource export, a
   signed delegation log, a CV, a lab certificate, a monitoring finding —
   enters through one intake. It is classified, the data points are extracted,
   and it is hashed on arrival.
2. **Check in bounds.** A rules engine — layered *Rule → Standard → Policy*,
   exactly as on the whiteboard — checks every record against the protocol,
   the sponsor's SOPs and the regulations (visit windows, consent versions,
   eligibility, expiry dates, delegation and training).
3. **Flow to every role.** The same verified record flows to the coordinator,
   investigator, CRA, project manager, data manager, auditor and finance, each
   seeing only what their role permits. Queries, deviations and actions are
   raised against the record itself, not in an email.
4. **Prove it.** Every output is hashed into a ledger (the notes call this the
   **Nexus**), every signature is a verifiable credential (KERI/ACDC), and
   every decision is a node in a **verified context graph** (built on the
   Emergence engine) linking it back to the regulation clause, protocol
   section, SOP step and source record that justify it.
5. **AI assists; humans sign.** AI drafts the monitoring report, proposes a
   deviation classification, pre-fills the query, flags the anomaly. A named
   human accepts, edits or rejects — and that choice is recorded.

6. **Observe, don't do.** Eight AI observers check 100% of the CRA work; a
   human conductor (Giau) reviews what they raise, signs, and presents
   a verifiable picture to the board. She is once removed from doing the work,
   so she can judge it (the selfdriven observer framework).

**The wedge.** Start with the part of the job that contains **no participant
data**: essential-document management, site-file health, trackers, action
items, deviation logs and monitoring-report drafting. It is where the
spreadsheets live, it avoids privacy risk in the first release, and it is
where a CRA feels the pain every week.

**The ask of the next 90 days.** Not code. Twelve structured interviews (CRAs,
coordinators, a PM, a QA auditor), the SOP and system inventory the whiteboard
lists as action items, a protocol-deviation "breaches map", and a clickable
prototype of the CRA cockpit to put in front of them.

---

## What the notes said

Our reading of the two photos. Where the handwriting is ambiguous we say so
— correct anything we've misread.

**Whiteboard (`whiteboard-cra-workflow-notes-22102026.jpg`)**

| On the board | What we take it to mean |
|---|---|
| **Study Protocols → Source Worksheets → (1) Source**: clinic, paper, electronic → audit trail | The protocol defines what has to be captured at each visit; source worksheets are built from it; source data is recorded at the clinic on paper or electronically and must carry an audit trail. |
| **(2) Electronic Data Capture** — "clinic enters data" crossed out → "allocated to 'System'" — "**NO data entry staff required!**" | The big idea: source is captured once and the system populates the EDC. No second transcription by site staff. |
| **CRA reviews / ~~verifies~~ + raises queries** | The CRA's role shifts from transcription checking (SDV) to reviewing and querying — risk-based source data *review*. |
| **(3) Investigator Site File** — electronic / paper; **(E) electronic Trial Master File** — CRA reviews | The two document stores the protocol also feeds: the site's own file and the sponsor's master file. They must reconcile. |
| **CTMS** (top right) | The CTMS sits above everything for tracking sites, visits, milestones and payments. |
| **KERI / ACDC — INFRA**; identifier diagram | Use KERI identifiers and ACDC credentials as the trust infrastructure. |
| **AI → System → HASH → Share… — "ALL OUTPUTS AKA: NEXUS"** | Every output of the system is hashed and shareable; the collection is the Nexus. |
| **S.C / ADV / PM / CRA** (ticked) **= OUTPUT** (written vertically) | Roles: Study Coordinator, ADV (possibly an advisor or ethics/governance role; to confirm), Project Manager, CRA. Each role gets its own output from the same system. |
| **Rule — Standard — Policy** | The layered rules engine. |
| **CRA – R, PM – F?** | Role permissions: CRA read (review), PM full? We read this as the start of an RBAC matrix. |
| **x emails** | Kill email as the record. |
| **Action items:** SOP of all processes · systems being used (name, examples) · Query · Data point · Breaches map (H.L — high level?) | Discovery to-do list. Carried into §08. |
| **Protocol deviations** (red, underlined) | A first-class object. |
| **P1 – host (paper); P3/4 – (hospitals + paper)** | Phase 1 units vs Phase 3/4 hospital sites, both still paper-heavy. |

**Paper mind map (`paper-mind-map-ecosystem-notes-22102026.jpg`)**

| On the page | What we take it to mean |
|---|---|
| **GCP — Good Clinical Practice** → **System Ledger** | GCP is the frame; the system ledger is the spine. |
| **GOV / FDA / TGA → SOP**; **TGA, SOP** repeated | Regulators set the rules that SOPs implement. |
| **Clin(ic)**, **Pharma**, **CRO**, **CRA** (crossed), **Auditor**, **$** | The actors and the money flows between them. |
| **Brand / Sponsor — Dr — controlled** | The sponsor (brand owner) and the doctor/investigator; controlled documents. |
| **Data / Dativ(?)**, **Associates(?)**, **Maps**, **"Not system kill"(?)** | Data and its mapping — and, we think, *not a system-killer*: overlay the existing systems, don't replace them. |
| **Track changes ↔ Billing** | Billing derived from the change ledger — invoice what the trail proves was done. |
| **Burden / Accountability** | Who carries the admin burden vs who is accountable. |
| **"Check in bounds"**, **MF** | Automatic bounds checking; Master File. |

---

## 01 · Direction — problem, opportunity, product

### Problem statement

> Clinical trial sites, CRAs and sponsors run regulated, safety-critical work
> through a patchwork of disconnected systems held together by spreadsheets,
> email and manual re-keying. The same fact is entered three to five times,
> reconciled by hand, and evidenced after the fact. This makes errors
> inevitable, deviations late to surface, inspections stressful, and skilled
> people's time disappear into admin. The risk is structural: no single place
> holds a record, its checks, its approvals and its reason together.

### Who feels it, and how

| Who | Pain (in their words, to be confirmed in interviews) |
|---|---|
| **CRA** (Giau's role) | "I have a login for every sponsor's CTMS, EDC and eTMF, plus their spreadsheets." Monitoring-visit reports take hours after each visit. Chasing sites for expired GCP certificates and unsigned delegation logs. Raising the same query twice because it was answered by email. Trip-report deadlines. Travel. |
| **Study coordinator** | Transcribing paper source into EDC. Answering queries in three places. Keeping the ISF current for every visit. |
| **Principal investigator** | Signing stacks of logs. Accountable for oversight of everything delegated. |
| **Project manager / CTM** | Site status lives in CRA heads and spreadsheets until the report lands. Deviation trends visible weeks late. |
| **Data manager** | Query ageing; reconciliation of EDC vs safety database vs lab data. |
| **QA / auditor** | Reconstructing what happened from fragments. TMF completeness. |
| **Finance** | Site payments reconciled manually against visit completion. |

### Where the systemic risk comes from

1. **Duplicate entry.** Source → paper worksheet → EDC → CRA's spreadsheet →
   monitoring report. Each hop is a transcription error waiting to happen,
   and Source Data Verification exists largely to catch errors the process
   itself introduced.
2. **No shared truth.** CTMS, EDC, eTMF, ISF, safety database and IxRS each
   hold part of the picture; the reconciliation is human.
3. **Shadow spreadsheets.** Trackers for documents, deviations, actions,
   payments and training sit outside validated systems — no audit trail, no
   access control, no version history, invisible to an inspector until asked.
4. **Email as the record.** Decisions, query answers and approvals live in
   inboxes.
5. **Late detection.** A visit out of window, a consent signed on a superseded
   version, or an unqualified person performing a delegated task is found at
   the next monitoring visit — weeks later — rather than when it happens.
6. **Evidence after the fact.** Inspection readiness is a project, not a state.

### Opportunity

- **Regulatory pull.** ICH E6(R3) (finalised January 2025) re-centres GCP on
  quality by design, risk-proportionate monitoring, data governance and
  fit-for-purpose computerised systems — including those the *site* uses. The
  US FDA has published it as guidance, the EMA applied it from July 2025, and
  the TGA is adopting it for Australia (confirm the TGA effective date).
- **Australian momentum.** The National Clinical Trials Front Door and the
  national one-stop-shop work, the National Clinical Trials Governance
  Framework for health services, and a push to grow Australia's share of
  global trials (fast CTN start-up, R&D tax incentive) all reward sites that
  can show good operational governance.
- **Technology readiness.** Document AI is now good enough to classify and
  extract from scanned essential documents reliably *when a human confirms*.
  Verifiable-credential infrastructure (KERI/ACDC) is mature enough to sign
  and chain records without a central authority.
- **A gap in the market.** Big platforms (Veeva, Medidata, Oracle) serve the
  sponsor; site tools (Florence, CRIO, Advarra) serve the site. The CRA —
  who works *across* sponsors, CROs and sites — has no tool of their own, and
  nothing makes the link between a decision and its justification provable.

### Product vision

**TrialThread is the verified thread that runs through a trial: every record
captured once, checked against the rules on arrival, routed to everyone who
needs it, and provable to anyone entitled to ask.**

### Principles (the ones we'd defend when tired)

1. **Not a system-killer.** Overlay and connect the systems sponsors already
   mandate; never ask a site to abandon its EDC or eTMF.
2. **Capture once.** A fact is entered at source, once. Everything else is a
   reference to it.
3. **Check at the door.** Rules run when a record arrives, not at the next
   visit.
4. **AI proposes, a named human disposes.** No AI output becomes a record
   without a human accepting it, and the acceptance is itself recorded.
5. **Every decision carries its reason.** A deviation classification, a query,
   an approval links to the clause, section and source that justify it.
6. **Least privilege, by default.** Role and blinding decide what anyone sees.
7. **Start without patient data.** The first release touches essential
   documents and operations only.

### What we will not do

- Build an EDC, a safety database or an IxRS.
- Put participant-identifiable data on any public ledger. The ledger holds
  hashes and credentials, never content.
- Let AI sign, approve, classify finally, or contact a site on its own.
- Use any employer's SOPs, data or documents to build or demo the product.

---

## 02 · Enablement — architecture, AI, verified context graph

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

---

## 03 · Protocols — the regulations and how the product meets them

> Check every item against the current official text before relying on it.
> Status reflects our understanding as of October 2026.

### International (applies in both markets)

| Instrument | What it governs | What it means for TrialThread |
|---|---|---|
| **ICH E6(R3) Good Clinical Practice** (Principles + Annex 1 final Jan 2025; Annex 2 on decentralised/pragmatic elements in progress) | The core GCP standard: roles of investigator and sponsor, monitoring, data governance, computerised systems, essential records (Appendix C). | The spine of the Standard tier. Essential-records taxonomy drives document classification. Data-governance and computerised-system sections define our validation, audit trail and access-control obligations. |
| **ICH E8(R1)** General considerations for clinical studies | Quality by design; critical-to-quality factors. | The breaches map feeds CtQ factor identification. |
| **ICH E2A / E2B(R3)** | Expedited safety reporting, ICSR format. | SAE reconciliation automation; we don't replace the safety database. |
| **ICH E9 / E9(R1)** | Statistical principles, estimands. | Context for deviation-impact assessment. |
| **ISO 14155:2020** | GCP for medical-device investigations. | Device-trial variant of the Standard tier. |
| **ALCOA++** data-integrity principles (attributable, legible, contemporaneous, original, accurate + complete, consistent, enduring, available, traceable) | Data-integrity expectations of all regulators. | Design rule for the record store. |
| **ISPE GAMP 5 (2nd ed.)** / risk-based CSV | How regulated users validate computerised systems. | Our validation package and the evidence we hand customers. |
| **ISO/IEC 27001, ISO/IEC 42001** | Information security; AI management system. | Certification targets (27001 first). |

### Australia

| Instrument | What it governs | Implication |
|---|---|---|
| **Therapeutic Goods Act 1989 & Therapeutic Goods Regulations 1990** — CTN and CTA schemes | Legal basis for supplying unapproved goods in trials. | Track CTN/CTA status and notifications per site. |
| **TGA adoption of ICH GCP** (E6(R2) with TGA annotations; transition to E6(R3)) | GCP as applied in Australia, incl. TGA annotations (e.g. record retention — 15 years for adult trials under the annotation; confirm under E6(R3)). | Retention rules in the Policy tier; jurisdiction-aware. |
| **TGA Australian Clinical Trial Handbook** | Practical guidance on the CTN/CTA schemes and sponsor responsibilities. | Reference content in the graph. |
| **NHMRC National Statement on Ethical Conduct in Human Research (2023, updated)** | HREC review, consent, ethics. | Consent-version and HREC-approval rules. |
| **NHMRC Safety monitoring and reporting in clinical trials involving therapeutic goods (2016)** | Who reports what safety information, to whom, when. | Safety-reporting timelines in the Policy tier. |
| **Australian Code for the Responsible Conduct of Research (2018)** | Research integrity, record keeping. | Retention and integrity rules. |
| **National Clinical Trials Governance Framework** (ACSQHC, part of NSQHS accreditation) | Health-service governance of trials. | A site-side buyer driver: evidence for accreditation. |
| **Privacy Act 1988 (APPs)** as amended (incl. 2024 reforms), **state health-records laws** (e.g. Health Records Act 2001 (Vic), HRIP Act 2002 (NSW)) | Personal and health information. | Data residency in Australia; consent-based use; breach notification (NDB scheme). Wedge release avoids participant data. |
| **Medicines Australia standard CTRA / indemnity forms**, **ANZCTR** registration | Contracts and trial registration. | Contract milestones → payment events; registration status tracked. |
| **ASD Essential Eight**, Notifiable Data Breaches scheme | Cyber baseline. | Security programme. |

### United States

| Instrument | What it governs | Implication |
|---|---|---|
| **21 CFR Part 11** Electronic records; electronic signatures | Validation, audit trails, access control, e-signature manifestation and linking, record copies, retention. | Core design constraint — see control matrix below. |
| **FDA guidance: Electronic Systems, Electronic Records and Electronic Signatures in Clinical Investigations — Q&A (final, Oct 2024)** | How Part 11 applies to clinical investigations, incl. systems used by sites, and to DHTs. | Applies to TrialThread directly when used by sites or sponsors. |
| **21 CFR Part 50** (informed consent), **Part 56** (IRBs), **Part 312** (INDs; investigator and sponsor obligations, records), **Part 812** (IDEs), **Part 54** (financial disclosure) | The US clinical-investigation framework. | Standard-tier rules (e.g. 312.62 investigator records; 312.57 sponsor records). |
| **45 CFR 46** (Common Rule) | Federally funded human-subjects research. | Ethics rules for non-FDA trials. |
| **HIPAA Privacy & Security Rules** (45 CFR 160, 164) | PHI at covered entities. | BAA with US sites; minimum-necessary access. |
| **FDA: Oversight of Clinical Investigations — A Risk-Based Approach to Monitoring** (2013) and **Q&A (2023)** | Risk-based monitoring. | Our monitoring model: centralised + targeted on-site. |
| **FDA: Use of Electronic Informed Consent Q&A**; **Decentralised Clinical Trials guidance (2024)** | eConsent and DCT elements. | Future modules. |
| **FDA draft guidance: Considerations for the Use of AI to Support Regulatory Decision-Making for Drug and Biological Products (Jan 2025)** | Risk-based credibility assessment for AI models. | Our AI governance follows its context-of-use and credibility framework. |
| **ICH E6(R3) as FDA guidance** | US adoption of the new GCP. | Same as international. |
| **FDAAA 801 / 42 CFR Part 11** (ClinicalTrials.gov) | Registration and results. | Track registration and results deadlines. |

### Watch list (for later markets)

EU Clinical Trials Regulation 536/2014 and CTIS; GDPR; EU AI Act (an AI
system used in clinical-trial operations is unlikely to be high-risk by itself,
but confirm); UK MHRA clinical-trials regulations reform (2025–26).

### Control matrix — 21 CFR Part 11 / ICH E6(R3) data-governance → feature

| Requirement | Reference | How TrialThread meets it |
|---|---|---|
| System validation | 11.10(a); E6(R3) computerised systems | Risk-based validation package (URS, risk assessment, test evidence) per release; customer-facing validation summary. |
| Accurate and complete copies for inspection | 11.10(b) | Export any record with its full trail; time-boxed inspector view. |
| Record protection & retention | 11.10(c) | Immutable versioning, hash-anchored, retention policy per jurisdiction. |
| Limited system access | 11.10(d) | RBAC + study/site scoping + blinding segregation (§06). |
| Secure, computer-generated, time-stamped audit trail | 11.10(e) | Append-only event log; every create/modify carries who, when, what, why; Nexus hash anchors. |
| Operational & authority checks | 11.10(f)(g) | Workflow enforces sequence (e.g. consent before procedures); permission checked at every action. |
| Device checks | 11.10(h) | Device-bound passkeys; site-mode device registration. |
| Training of users | 11.10(i) | Training records are credentials; rules block untrained users from delegated tasks. |
| Signature manifestation (name, date/time, meaning) | 11.50 | Every signature displays all three; stored in the ACDC. |
| Signature/record linking | 11.70 | Signature is cryptographically bound to the record hash — cannot be copied to another record. |
| Unique signatures; two components / biometric | 11.100, 11.200 | One identity per person; passkey + PIN/biometric at signing. |
| Data governance across the lifecycle | E6(R3) data governance | Graph shows provenance of every data point; metadata retained. |
| Risk-proportionate approach | E6(R3) principles | Risk scores per site drive monitoring intensity. |

---

## 04 · Sustainability — market, model, money

### Market and buyers

| Segment | Who pays | Why they pay |
|---|---|---|
| **Independent / contract CRAs** | The CRA | A personal workspace across all their sponsors: one task list, report drafting, document chasing. Low price, fast adoption, word of mouth. |
| **Sites & SMOs** (hospital research units, Phase 1 units, site networks) | Site / research office | Less transcription, inspection-ready ISF, evidence for the National Clinical Trials Governance Framework, faster start-up. |
| **CROs** (especially small and mid-size Australian CROs) | CRO operations | More sites per CRA, shorter report cycles, fewer findings, cross-sponsor visibility. |
| **Sponsors / biotechs** (Australia hosts many early-phase biotech trials) | Clinical operations / QA | Inspection readiness, oversight evidence for E6(R3), the decision graph. |

Australia is a strong beachhead: a large early-phase trial sector with many
smaller sponsors and CROs, the CTN scheme's fast start-up, and an ecosystem
small enough to reach through a few associations. Market sizing to be done
properly in discovery (sources: MTPConnect / Clinical Trials Australia sector
reports, ANZCTR registration counts, ARCS membership).

### Competitive landscape (public products, for positioning only)

| Category | Examples | Their centre of gravity | Our angle |
|---|---|---|---|
| Unified sponsor platforms | Veeva Vault Clinical, Medidata, Oracle Clinical One | Sponsor-mandated CTMS/EDC/eTMF | We don't compete; we connect across them. |
| Site eRegulatory / eISF | Florence, Advarra eRegulatory | Site binders | We add cross-system flow, rules and provable decisions. |
| Site eSource / site CTMS | CRIO, Clinical Conductor (Advarra), RealTime | Site operations | We serve the CRA and the sponsor-site seam too. |
| Risk-based monitoring analytics | CluePoints and others | Centralised statistical monitoring | We feed RBM with clean, provenanced data; partner rather than compete. |
| Mid-market all-in-one | Castor, OpenClinica, REDCap (academic) | Study build | Connector targets. |

**Differentiators:** CRA-centric and cross-sponsor; rules-at-the-door; the
verified decision graph ("Why?"); credential-based identity and signatures;
non-invasive (no rip-and-replace).

### Revenue model (hypotheses to test)

| Tier | Price shape | Contents |
|---|---|---|
| **CRA Personal** | Monthly per CRA | Workspace, trackers, report drafting, document chaser. No participant data. |
| **Site** | Per site per active study, monthly | eISF health, intake, rules, coordinator workflows, inspector view. |
| **CRO / Sponsor** | Per study, banded by sites and phase | Everything + connectors, decision graph, oversight dashboards, validation pack. |
| **Add-ons** | Usage | Ledger-derived site billing (invoice from the trail), AI document processing volume, extra connectors. |

The whiteboard's *track changes → billing* link is also a product: site
payments calculated from what the ledger proves was done, removing a major
source of site-sponsor friction.

### Cost drivers

Computerised-system validation per release; ISO 27001 (then SOC 2 Type II for
US buyers); Australian-hosted infrastructure (data residency); AI inference;
clinical/regulatory advisory; professional indemnity and cyber insurance.

### Measures that would prove value

Hours saved per monitoring visit; monitoring-report cycle time; query ageing;
documents expired at site (target zero); deviations detected same-day vs at
next visit; inspection/audit findings per site; transcription errors per 1,000
data points; site payment cycle time.

---

## 05 · Processes — the workflows and the ingestion pipeline

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

---

## 06 · Accountability — roles, access, audit, AI governance

### Roles

| Role | Typical person | Scope |
|---|---|---|
| **PI** | Principal investigator | Their site, all studies they lead |
| **Sub-I** | Sub-investigator | Delegated tasks at their site |
| **SC** | Study coordinator | Site operations, source, ISF |
| **Site Admin / Reg** | Research office, regulatory coordinator | Site documents, governance, contracts |
| **Pharmacist** | Unblinded site pharmacist | IP — unblinded |
| **CRA** | Monitor (sponsor/CRO) | Assigned sites, assigned studies |
| **Lead CRA / CTM** | Clinical trial manager | All sites in a study/region |
| **PM** | Project manager | Study-wide, operations + finance view |
| **DM** | Data manager | Data and queries, study-wide |
| **MM / Safety** | Medical monitor, pharmacovigilance | Safety data, medical review |
| **QA / Auditor** | Sponsor QA, independent auditor | Read-only, time-boxed, full trail |
| **Inspector** | TGA / FDA (via site or sponsor) | Read-only, time-boxed, scoped to what is requested |
| **Finance** | Site/sponsor finance | Payment events only |
| **AI agent** | Registered agent with a mandate | Proposes only; listed per study |
| **Participant** (later) | eConsent, ePRO | Their own records |

### Access matrix (C create · R read · U update · S sign · A approve · — none)

| Object | PI | SC | Site Admin | CRA | CTM/PM | DM | MM | QA/Insp | Finance | AI agent |
|---|---|---|---|---|---|---|---|---|---|---|
| Source record (identifiable) | R S | C R U | — | R (on site / remote SDR, if permitted) | — | — | R (safety) | R | — | propose extract |
| Data point (coded) | R S | C U | — | R + query | R | R + query | R | R | — | propose |
| Essential document | R S | C R U | C R U | R + request | R | — | — | R | — | classify |
| Delegation log | S A | C U | R | R | R | — | — | R | — | check |
| Query | R | R answer | — | C R close | R | C R close | C R | R | — | draft |
| Deviation | R S | C R | — | C R classify | R A | R | R | R | — | propose class |
| Monitoring report | R (letter) | R (letter) | — | C U S | R A | — | — | R | — | draft |
| Rules (Policy) | — | — | — | R | C U A | R | — | R | — | propose |
| Payment event | R | R | R | R | R A | — | — | R | C R U | — |
| Unblinded IP data | — | — | — | (unblinded CRA only) | — | — | — | (unblinded QA) | — | — |

The whiteboard's "CRA – R, PM – F" is the start of this table; it needs
validating against real study role definitions.

### Audit & accountability mechanics

- **Append-only event log** for every action (who · AID · role · when · what ·
  before/after · reason), hash-chained, periodically anchored to the Nexus.
- **Signatures as credentials** carrying name, time and meaning
  (reviewed / approved / authored / acknowledged), bound to the record hash.
- **Segregation of duties** enforced (the author of a report cannot approve it;
  blinded and unblinded spaces never mix).
- **Burden vs accountability** made visible: who did the work (often the SC)
  vs who is accountable (the PI) are both on the record, which is what ICH
  E6(R3) investigator-oversight expectations need.
- **Inspector mode**: a time-boxed, read-only, scoped view with full trails and
  the "Why?" graph, so an inspection request is answered in minutes.

### AI governance

- Every AI agent is registered: identity (AID), purpose, model and version,
  **may / must-ask / never** mandate, owner.
- Every AI output is stored as a *proposal* with inputs, model version and
  confidence; the human decision on it is a separate signed event.
- Context-of-use and credibility assessment per FDA's 2025 draft AI guidance;
  higher-risk uses (anything touching data bound for the EDC or a safety
  decision) need higher evidence and mandatory human review.
- Monitoring of AI accuracy against human decisions — drift triggers review.
- ISO/IEC 42001 as the target management system.

### TrialThread Observer: AI checks the work, the conductor observes it

Eight AI observers, one per Area of Focus, check **100% of the CRA work**
continuously: every consent form, report statement, visit window, training
record and query. They record what conforms and raise what doesn't, with
evidence attached. **Giau, as conductor, doesn't do the checking; she observes
it.** She confirms, regrades or dismisses each finding, signs with her passkey,
and presents a signed, verifiable picture to the board. Being once removed from
doing the work is what lets her judge it. This is the selfdriven observer
framework applied to clinical operations: observers hold KERI identifiers
delegated from the conductor's, they are read-only, their keys are time-limited,
and every observation is signed.

Full design, the eight clinical observers, the president's one-minute version
and a synthetic end-to-end case (HALCYON-3, Site 012):
[`06-accountability-trialthread-observer.md`](areas-of-focus/06-accountability/workings/06-accountability-trialthread-observer.md)
· animated app design: [`trialthread-observer-app.html`](areas-of-focus/02-enablement/workings/trialthread-observer-app.html).

---

## 07 · Engagement — users, interface, go-to-market

### The interface (built on the selfdriven Human Interface Kit 3.0 language)

Warm neutral canvas, ember accent (`#DE5A31`), Poppins type, quiet motion.
Passkey sign-in; the signing ceremony is a deliberate, visible moment.

| Screen | For | What it does |
|---|---|---|
| **Today** (CRA cockpit) | CRA | One list across every sponsor and site: visits, queries ageing, documents expiring, actions due, deviations awaiting classification. Site health tiles. |
| **Intake** | SC, Site Admin, CRA | Drop anything in. Watch it classify, extract and check. Confirm the flagged fields. |
| **Record** | Everyone (scoped) | The record, its versions, its data points, its checks, its signatures — and the thread back to source. |
| **Why?** | Everyone (scoped) | The decision trace from the context graph. |
| **Visit mode** | CRA | Tablet, offline-capable. Checklist generated from the rules; findings captured once → report draft. |
| **Queries / Deviations / Actions** | CRA, SC, DM, PM | Boards raised against records, with due dates from the Policy tier. |
| **Site file health** | Site Admin, CRA, PM | ISF and eTMF completeness vs Appendix C and the study plan. |
| **Breaches map** | PM, QA, sponsor | Where deviations and findings originate, by protocol section and SOP step. |
| **Inspector view** | QA, Inspector | Time-boxed, read-only, full trails. |
| **Rules studio** | PM, DM | Protocol → rules, authored as data, linked to clauses. |

### Go-to-market

1. **Design partner:** Giau, plus 3–5 CRAs she trusts (outside work hours, no
   employer data).
2. **Discovery interviews (12):** 5 CRAs, 3 study coordinators, 1 PI, 1 PM/CTM,
   1 data manager, 1 QA auditor. Script focuses on the five action items.
3. **Prototype → CRA Personal beta** with no participant data.
4. **Channels (Australia):** ARCS Australia, ACTA (Australian Clinical Trials
   Alliance), clinical trial networks, research-office communities, LinkedIn
   content from Giau's lived experience.
5. **First site pilot** with a research unit that's working on governance
   framework accreditation.
6. **CRO conversation** once the personal tier shows hours saved.

### Story in one line

*"A CRA spends half her week moving facts between systems. TrialThread moves
them once, checks them on arrival and proves it — so she can spend her time on
participants and data quality."*

---

## 08 · Organisational — team, roadmap, risks, next steps

### Roadmap

| Phase | When (indicative) | Outcome | Contains participant data? |
|---|---|---|---|
| **0 · Discovery** | Nov 2026 – Jan 2027 | 12 interviews; process map; systems inventory; breaches map; clickable prototype; decision to proceed | No |
| **1 · CRA Personal (alpha)** | Feb – May 2027 | Today cockpit, document radar, action/deviation logs, report drafter; KERI identity + signatures; 10 beta CRAs | No |
| **2 · Site pilot** | Jun – Dec 2027 | Intake + classification for essential documents, ISF health, delegation × training, ICF guard; validation package v1; ISO 27001 underway | Limited (consent metadata), AU-hosted |
| **3 · Source → EDC** | 2028 | Paper/eSource capture to EDC via connectors with human confirmation; SDR workflows; Part 11 assessment; first CRO/sponsor | Yes, fully controlled |
| **4 · Graph & oversight** | 2028+ | Decision graph across studies; breaches map; RBM feed; US entry | Yes |

### Team (minimum credible)

Product/tech lead (Peter); clinical-operations domain lead (Giau — role to be
agreed around her employment); regulatory/QA advisor (CSV and GCP auditor
background); engineer(s); later, a privacy/security lead.

### Risks

| Risk | Likelihood | Impact | Response |
|---|---|---|---|
| **Employment conflict / IP** — Giau's employment contract likely has confidentiality, IP-assignment and outside-work clauses | High | High | Read the contract first; get advice if unclear; build only from public knowledge and generic experience; never use employer documents, SOPs, systems or data; consider disclosure to employer. |
| Sponsors mandate their own systems | High | Medium | Overlay, don't replace; CRA-personal tier needs no integrations. |
| Validation burden slows releases | Medium | High | Risk-based CSV from day one; automated test evidence. |
| Privacy breach | Low (phase 1) | Very high | No participant data until phase 2; AU hosting; encryption; least privilege. |
| AI error accepted uncritically | Medium | High | Confidence display, mandatory review for high-risk uses, accuracy monitoring. |
| Ledger misunderstood as "patient data on a blockchain" | Medium | Medium | Hashes and credentials only; plain-language explainer for ethics committees. |
| Long sales cycles | High | Medium | Bottom-up via CRAs and sites. |
| Incumbent copies features | Medium | Medium | The graph and cross-sponsor position are hard to copy. |

### Next steps (the next four weeks)

1. **Giau** checks her employment contract's IP / outside-work clauses. *(Do this first.)*
2. **Peter + Giau** validate this reading of the notes and correct anything misread.
3. **Giau** drafts the generic process map and systems inventory (action items 1–2).
4. **Peter** builds a clickable prototype of the Today cockpit and Intake from the interactive plan.
5. **Both** write the interview script and line up the first five interviews.
6. **Peter** sketches the clinical atom/edge types in an Emergence scratch repo using public texts only (ICH E6(R3), 21 CFR 11, a public protocol template).

---

*Drafted by Claude for Peter and Giau, 22 Oct 2026. Concept only: not legal,
regulatory or medical advice.*

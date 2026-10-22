# TrialThread — 01 · Direction

> Generated from [`TRIALTHREAD-PLAN.md`](../../../TRIALTHREAD-PLAN.md) by `scripts/build-plan.py`. Edit the master plan, then rebuild. Interactive: [`trialthread-plan.html`](../../../trialthread-plan.html).

## Direction — problem, opportunity, product

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

# TrialThread — 06 · Accountability

> Generated from [`TRIALTHREAD-PLAN.md`](../../../TRIALTHREAD-PLAN.md) by `scripts/build-plan.py`. Edit the master plan, then rebuild. Interactive: [`trialthread-plan.html`](../../../trialthread-plan.html).

## Accountability — roles, access, audit, AI governance

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
[`06-accountability-trialthread-observer.md`](../../../areas-of-focus/06-accountability/workings/06-accountability-trialthread-observer.md)
· animated app design: [`trialthread-observer-app.html`](../../../areas-of-focus/02-enablement/workings/trialthread-observer-app.html).

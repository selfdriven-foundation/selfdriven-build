# TrialThread — 08 · Organisational

> Generated from [`TRIALTHREAD-PLAN.md`](../../../TRIALTHREAD-PLAN.md) by `scripts/build-plan.py`. Edit the master plan, then rebuild. Interactive: [`trialthread-plan.html`](../../../trialthread-plan.html).

## Organisational — team, roadmap, risks, next steps

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

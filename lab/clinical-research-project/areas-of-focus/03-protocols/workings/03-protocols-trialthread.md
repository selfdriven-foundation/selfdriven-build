# TrialThread — 03 · Protocols

> Generated from [`TRIALTHREAD-PLAN.md`](../../../TRIALTHREAD-PLAN.md) by `scripts/build-plan.py`. Edit the master plan, then rebuild. Interactive: [`trialthread-plan.html`](../../../trialthread-plan.html).

## Protocols — the regulations and how the product meets them

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

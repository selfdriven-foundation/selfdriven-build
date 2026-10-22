# TrialThread Observer: AI checks the CRA work, a human observes it

> Part of the TrialThread concept plan, drafted 22 Oct 2026. Builds on the
> selfdriven observer framework (`GitHub/selfdriven-observer/lab`): octonomous
> observers do the checking, and a human conductor holds the judgement and the
> signature. Interactive design: [`trialthread-observer-app.html`](../../02-enablement/workings/trialthread-observer-app.html).
> All people, sponsors, studies and numbers in this document are synthetic.

---

## 1 · The idea in one paragraph

Today a CRA does the monitoring work *and* writes the report that says the
work was done well. Their lead checks a sample, and QA audits a smaller sample
months later. TrialThread Observer turns that around. **Eight AI observers check
100% of the CRA work, continuously**: every consent form, every report
statement, every visit window, every training record, every query. They record
what conforms, and raise what doesn't, with the evidence attached.
**Giau, as conductor, doesn't do the checking. She observes it.** She reviews
each finding, confirms, regrades or dismisses it, signs with her passkey, and
presents a signed, verifiable picture to the board, CEO, VP or president.
Because she is once removed from doing the work, she can judge it.

## 2 · Why "once removed" matters

| When you **do** the work | When you **observe** the work |
|---|---|
| You check what you remember doing | You check what the record shows |
| Self-review bias: you see what you meant to write | No authorship to defend |
| Sampling, because time is short: 5 of 38 consent forms | The observers read 38 of 38; you review only what they raise |
| Report is a narrative you wrote | Report is a signed record anyone can verify |
| Errors surface at the next visit or audit | Errors surface the day they are recorded |
| The board gets your assurance | The board gets your judgement on evidence |

This is the separation GCP already expects at the level of the organisation
(monitoring, quality control and independent audit are different functions)
brought down to the level of everyday work. The rule of thumb from the
observer framework: **machines watch at volume; people decide.**

**Observing the work, not the worker.** The observers report on records and
processes, not on people's performance. CRAs see every observation about their
own work first and can reply before Giau reviews it. The board sees study-level
assurance, never a CRA league table.

## 3 · The eight clinical observers

One observer per Area of Focus, each holding its own KERI identifier
**delegated from Giau's identifier** (a `dip` event), so its authority traces to
a person. Every observer is **read-only**: it never changes the systems it
watches. Its keys are **time-limited** and pre-rotated, so a compromised
observer can be replaced without losing its history. Every observation is
**signed** and anchored in the observer's key event log (an `ixn` event).

> Numbering follows this portfolio (01 Direction … 08 Organisational). The
> observer lab page orders the middle areas differently; the mapping is the same.

| # | Observer | What it observes, 100% of the population | Example criterion | Grounding |
|---|---|---|---|---|
| 01 | **Direction**: study risk | Key risk indicators per site vs thresholds; quality tolerance limits | Site deviation rate ≤ 1.5× study mean | ICH E6(R3) risk-based quality management; E8(R1) critical-to-quality factors |
| 02 | **Enablement**: competence | GCP currency, protocol training, delegation × training, CRA study training | No delegated task without current training | E6(R3) qualified staff; 21 CFR 312.53 |
| 03 | **Protocols**: consent & protocol | Every ICF version vs approval date; eligibility; visit windows; prohibited medications | Consent signed on the version approved on that date | NHMRC National Statement; 21 CFR 50; protocol |
| 04 | **Sustainability**: IP & money | IP accountability, temperature excursions, site payments vs verified visits | Dispensed − returned = IxRS balance | E6(R3) investigational product; CTRA |
| 05 | **Processes**: monitoring conduct | Visit cadence vs monitoring plan; report and follow-up letter timeliness; action closure; source review coverage | Report final ≤ 10 working days after visit | Monitoring plan; sponsor SOP |
| 06 | **Accountability**: records & trail | ISF/eTMF completeness; audit-trail integrity; signature manifestation; **report statements vs the record** | Every "no issues" statement is consistent with the record | 21 CFR 11; E6(R3) Appendix C |
| 07 | **Engagement**: communication | Query response times; open actions; escalations answered; decisions living only in email | Queries answered ≤ 5 working days | Sponsor SOP |
| 08 | **Organisational**: roles & segregation | Author ≠ approver; blinded/unblinded separation; access for joiners and leavers; CRA workload balance | No one approves their own report | E6(R3) roles; 21 CFR 11.10(d) |

**Mandates.** Every observer has a *may / must-ask / never* mandate.
*May:* read connected records, evaluate criteria, sign observations, raise
findings. *Must ask:* anything touching unblinded data; any new criterion.
*Never:* change a record, contact a site or participant, grade a finding as
final, or rank individuals.

## 4 · The observation lifecycle

```
OBSERVE → EVALUATE → SIGN → REVIEW → CORRECT → PRESENT
 observer   observer   observer  Giau      site/team  Giau → board
 reads all  grades vs  ixn event confirms  CAPA under signed pack
 records    criteria   anchored  regrades  E6(R3)     for any
                                 dismisses quality    date range
                                 + passkey management
```

**Grades** (from the observer framework, mapped to clinical language):
*conforming* · *opportunity for improvement* · *nonconformity*. Nonconformities
are proposed as *minor* or *important/major* in line with the sponsor's
deviation classification. **Only Giau's signature makes a grade final.**

**Example observation record** (an ACDC credential, synthetic):

```json
{
  "observation": "obs_HAL3-012-0419",
  "criterion": "ICF signed on version approved at signing date",
  "grounding": ["NHMRC National Statement 2.2", "Protocol HALCYON-3 v3.0 §5"],
  "result": "nonconformity",
  "proposedGrade": "important",
  "population": { "observed": 38, "of": 38 },
  "detail": "Subject 012-019 signed ICF v2.1 on 14 Oct 2026; v3.0 approved 2 Oct 2026",
  "relatedStatement": "IMV-4 report §3: 'ICF review (5 of 38 sampled): no issues'",
  "observer": { "kind": "octonomous", "area": "03 Protocols",
                "aid": "EPr0t…3Kq", "delegator": "EGiau…7Wd" },
  "keriEvent": { "type": "ixn", "sn": 4211, "digest": "sha256:5b9e…c21f" },
  "review": { "by": "Giau (conductor)", "signedWith": "passkey",
              "decision": "confirmed", "note": "Sampling followed the monitoring plan; root cause is the plan, not the CRA." }
}
```

## 5 · Giau's role: the conductor

- **Daily (≈20 min):** the review queue, meaning findings awaiting a human, ordered by risk.
- **Weekly:** conversations with CRAs and sites where a finding needs context
  (notes are signed and linked to the observations they cover); spot-check a
  random sample of *conforming* observations to keep the observers honest.
- **Monthly:** the board pack: state, findings, corrections, decisions needed.
- **What she signs:** every finding's final grade; every dismissal (with a reason);
  the board pack; changes to observer criteria.
- **What she never delegates:** the judgement on a finding, the conversation
  with a person, and the words that go to the board.

## 6 · Presenting to a president: the one-minute version

> **One thing: we stopped marking our own homework.**
>
> Last month our CRAs did 1,284 pieces of monitoring work on HALCYON-3. Eight
> AI observers checked all of it, not a sample. 1,243 items conformed and are
> on a signed record. 41 raised a signal, 37 were cleared with evidence, and 4
> came to me. I reviewed each one, spoke to the people involved, and signed.
> One mattered: a participant consented on an out-of-date form. The site's
> sampling would not have caught it until next quarter. It was found in a day,
> corrected in a week, and the fix is a change to how we monitor, not blame
> for a person.
>
> **What I need from you:** approve monitoring plan v2, which moves 100% of
> consent checks to the observers and gives our CRAs about six days a month
> back for participant-safety review.

Three things the president should take away: **coverage** (100%, not a sample),
**independence** (the person presenting didn't do the work), and **proof**
(every number links to a signed record an auditor or inspector can verify
without trusting us).

## 7 · Synthetic end-to-end case: HALCYON-3, Site 012

*Fictional sponsor Example Therapeutics; fictional Phase 3 study HALCYON-3
(MRD-417 in moderate-to-severe asthma); 10 sites (6 AU, 4 US); 6 CRAs.*

| # | Scene | Who | What happens |
|---|---|---|---|
| 1 | **The work happens** | CRA S. Okafor | Interim monitoring visit 4 at Site 012 (Mon 19 Oct). Findings captured in visit mode; report drafted and signed Thu 22 Oct. Report §3: "ICF review (5 of 38 sampled): no issues." |
| 2 | **Eight observers check everything** | Observers 01–08 | Within minutes of signing, 214 checks run on the visit and its records. 03 Protocols reads all 38 consent forms. 05 Processes confirms report timeliness (day 3 of 10). 06 Accountability compares every report statement to the record. |
| 3 | **A signal the sample missed** | 03 Protocols + 06 Accountability | Subject 012-019 consented on ICF v2.1 on 14 Oct; v3.0 was approved 2 Oct. The report statement "no issues" is inconsistent with the record. 01 Direction also notes Site 012's visit-window deviations are 2.1× the study mean (KRI amber). |
| 4 | **Giau observes** | Giau | Opens the finding: evidence trace, the 38/38 population, the report statement. Talks to the CRA: the sample of 5 followed the monitoring plan. Confirms the finding as an *important deviation*, records that the root cause is the plan's sampling and the site's version control, and signs with her passkey. |
| 5 | **Correct the system, not the person** | Site, PM, Giau | Re-consent 012-019 within 7 days (done 27 Oct). Site version-control CAPA. Monitoring plan v2 proposed: ICF checks become 100% observed; CRA sampling time moves to safety review. |
| 6 | **Everything is signed** | Record | Observer `ixn` events, CRA reply, Giau's ACDC review, CAPA and closure, each hashed and anchored. |
| 7 | **The president's view** | Board | Board pack signed by Giau: three questions, three answers, one decision requested. |
| 8 | **Inspection-ready any day** | Inspector / auditor | Scoped, time-limited credential for 16–20 Nov opens the record for that window, then expires on its own. |

## 8 · The production app

| Screen | For | What it does |
|---|---|---|
| **Observe** | Giau, PM | Live feed of observations across studies and sites; population coverage per observer; KRIs. |
| **Review** | Giau | The queue of findings awaiting a human. Confirm, regrade or dismiss (dismissal needs a reason); sign with a passkey. |
| **Thread** | Giau, auditor | The end-to-end trace for any finding: records → observations → review → CAPA → closure. |
| **Respond** | CRA, site | The CRA sees observations about their work first and can reply or add context before review. |
| **Board** | President, CEO, VP | Presentation mode: three questions, signed answers, decisions requested, drill-down to evidence. |
| **Observers** | Giau | The eight observers: AID, delegation, scope, key expiry, mandate, accuracy against human decisions. |
| **Access** | Giau, QA | Issue scoped, dated credentials to auditors and inspectors. |

**Architecture delta on the TrialThread plan:** the observers sit on top of the
Records, Rules and Context layers (L3 to L5). They read through the same
connectors, evaluate against the same Rule/Standard/Policy tiers, and write
observations as atoms into the same Emergence context graph, so every finding
gets a "Why?" trace for free.

## 9 · Regulatory fit

- **ICH E6(R3):** supports the sponsor's quality management, risk-based quality
  control and oversight of delegated activities. It does **not** replace
  monitoring, and it does **not** replace QA audit, which stays independent.
- **21 CFR Part 11:** observations and reviews are electronic records with
  signatures bound to the record hash; Giau's signature shows name, time and meaning.
- **FDA draft AI guidance (2025):** each observer has a defined context of use
  and a credibility assessment; accuracy against human decisions is monitored.
- **ISO/IEC 42001:** AI management system as the governance frame.

## 10 · Risks specific to the observer

| Risk | Response |
|---|---|
| Automation bias: Giau rubber-stamps | Dismissals need a reason; random sample of conforming results for human spot-check; observer accuracy shown on every finding |
| CRAs feel surveilled | Observe the work, not the worker; CRA sees and can reply first; no individual ranking reaches the board |
| Observer misses a class of error | Criteria reviewed quarterly against audit and inspection findings; new criteria need conductor sign-off |
| Over-trust by the board | Board pack states coverage and limits plainly; QA audit remains independent |
| Compromised observer | Delegated, time-limited, pre-rotated keys; conductor can revoke; history preserved |

## 11 · Pilot

One study, two sites, two observers first (03 Protocols and 05 Processes),
Giau as conductor, eight weeks, measured against the existing sampled QC:
findings caught, days to detection, conductor review time, CRA hours returned.

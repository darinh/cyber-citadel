# The Campaign Briefing  (7B)
*Worked Example · Aegis Hospital — One real system walked end to end through the RMF — categorize, select, tailor, implement, assess, authorize, monitor — with a named human cast (System Owner, AO, ISSO, Privacy Officer, Assessor).*

*[TITLE: ACT II · BRIEFING — THE CAMPAIGN BRIEFING — One real system, end to end · Aegis Regional Hospital]*
**VEGA:** Before we study the campaign step by step, let's watch a real one unfold — start to finish.
**NOVA:** A real system? Not the metaphor?
**VEGA:** A real system. And this time, apprentice, you're running it.

*[THE CAST · REAL ROLES: Meet the team]*
  • Maya — System Owner: accountable for the system day to day
  • The CIO — Authorizing Official (AO): signs to accept the risk
  • Raj — ISSO: the hands-on security officer for this system
  • Sam — Privacy Officer: guards the patients' personal data
  • Stellaris Audit Co. — the independent Assessor
**VEGA:** Security isn't done by one hero. It's a team: Maya owns the system day to day; the CIO is the authorizing official who signs for the risk; Raj is the hands-on security officer; Sam guards the patients' privacy; and an outside firm, Stellaris, assesses the work.
**NOVA:** So 'doing 800-53' is really a group of people, each with a named role and hat.

*[PLAIN ENGLISH: Information system (made concrete)]*
  meaning: Aegis Regional Hospital runs a Patient Records System: a web app plus a database, used by about 800 clinicians, hosted on-premises, holding patients' medical records.
  everyday example: Web app + database + 800 users + sensitive health records = one information system to authorize.
**VEGA:** Here's our system. Not 'a computer' — an app, a database, the staff who use it, and the data they protect.
**NOVA:** And those records are PII — personal, and protected by law.

*[DIAGRAM: Step 1–2: Prepare, then Categorize the impact]*
  Confidentiality MODERATE → Integrity HIGH → Availability HIGH
**VEGA:** First, prepare — set roles and context. Then categorize: how bad is the worst case for C, I, and A?
**VEGA:** Confidentiality, Moderate. But Integrity is High — a wrong dose could kill. Availability is High — downtime closes the ER.
**NOVA:** And the high-water mark takes the worst of the three...
**VEGA:** So the whole system is categorized HIGH. One High pulls it all up.

*[SELECT · SP 800-53B: Step 3: Select the starting controls]*
  • The HIGH security baseline from SP 800-53B — 370 controls and enhancements
  • PLUS the Privacy baseline (96) — because the system processes PII
  • This is the starting kit, not the finished list
**VEGA:** Maya opens 800-53B and draws the HIGH baseline — and the privacy baseline, because of those patient records.
**NOVA:** A starting kit, sized to the stakes.

*[PLAIN ENGLISH: Common control (inheritance)]*
  meaning: A control someone else provides for you, so you don't build it yourself. You 'inherit' it. Controls can be common (provided), system-specific (yours alone), or hybrid (shared).
  everyday example: PE-3 (physical access) is common (the data center). AC-6 (least privilege) is system-specific. CP-2 (contingency plan) is often hybrid.
**NOVA:** Does Maya's team really configure every one of 370 controls?
**VEGA:** No. The data center already provides physical security, PE-3, for every tenant. Maya inherits it — that's a common control.

*[TAILOR · NOT DELETE: Step 4: Tailor the baseline to fit]*
  • Scope out only what truly doesn't apply: this app is wired-only, so AC-18 (Wireless Access) is out of its boundary
  • Inherit PE-3 (physical access) from the data center — a common control
  • Add controls from a healthcare (HIPAA) overlay
  • Set parameters: AC-2 disables inactive accounts after 60 days
**VEGA:** Tailoring is fitting the kit to the system — not an excuse to delete protections.
**NULL:** I look for the one control you wrongly tailored away.
**VEGA:** Which is why every change is justified and written down — we drop wireless only because this system has none.

*[IMPLEMENT · SP 800-53: Step 5: Implement the controls]*
  • IA-2: multi-factor login for all 800 clinicians
  • SC-28: encrypt the patient database at rest
  • SI-2: patch servers on a set schedule
  • CP-9: a nightly backup kept offline, where ransomware can't reach it
**VEGA:** Now Raj's team puts the controls to work. The catalog says WHAT; they choose HOW.
**NOVA:** Same requirement, many possible tools.

*[ASSESS · SP 800-53A: Step 6: Assess — do they actually work?]*
  • Stellaris (independent) EXAMINES the security plan
  • INTERVIEWS Raj and the admins
  • TESTS the system: a vulnerability scan and a phishing simulation
  • The findings become a Security Assessment Report — the SAR
**VEGA:** An outside assessor checks the work three ways: examine, interview, test.
**NOVA:** Selecting a control isn't proof it works. Assessment is.

*[PLAIN ENGLISH: Residual risk]*
  meaning: The risk that's left after your controls are in place. It never reaches zero — so a senior leader has to look at what remains and decide if it's acceptable.
**NOVA:** What about the weaknesses the assessor found?
**VEGA:** The risk that remains — residual risk. The CIO weighs it before anyone goes live.

*[AUTHORIZE · MONITOR: Step 7–8: Authorize, then Monitor forever]*
  • The CIO reviews the SAR, accepts the residual risk, signs a 3-year ATO
  • 12 open findings go on a POA&M — each with an owner and a due date
  • Monitor: quarterly scans, annual reviews, re-authorize after the big upgrade
  • A system is never simply 'done'
**VEGA:** The CIO signs the authorization to operate. Then the watch begins — and never ends.
**NULL:** Good. Because neither do I.

*[NOTEBOOK: The campaign, in one breath]*
  • Categorize the system (HIGH) → select a baseline (800-53B) → tailor it to fit.
  • Implement the controls → assess them (examine/interview/test → SAR).
  • Authorize (the ATO, accepting residual risk; gaps → POA&M) → monitor forever.
  remember: One system, one team, seven steps — that's the RMF.
**NOVA:** I just watched a whole system get secured, start to finish.
**VEGA:** You did. Now we'll slow down and learn each step in depth — starting with the framework itself.

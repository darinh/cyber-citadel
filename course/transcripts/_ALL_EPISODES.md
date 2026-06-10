# The Citadel Awakens  (00)
*Orientation — What 800-53 is, why it exists, how to read a control, why baselines moved to 800-53B, and where it all fits in the RMF.*

*[TITLE: EPISODE 00 — THE CITADEL AWAKENS — Security & Privacy Controls · NIST SP 800-53r5]*
**NULL:** Every gap, every shortcut, every forgotten door — I will find it.
**VEGA:** Not tonight. Welcome to the Aegis Citadel. I'm Vega, and I'll be your guide.
**NARRATOR:** Every modern organization runs on information. Protect it, and you thrive. Lose it, and you fall.

*[MAP: AEGIS CITADEL]*
**VEGA:** Picture an organization's information as a walled city. At its heart sits the Crown Data — the records, secrets, and services everyone depends on.
**NULL:** I don't want your walls. I want what they guard — the Crown Data. Lose it once, and there is no second copy of trust.
**NOVA:** I'm Nova — newly appointed, and honestly new to all of this. Can we start from the very beginning?
**VEGA:** We will. First, a few words everyone uses and almost no one defines.

*[PLAIN ENGLISH: NIST]*
  stands for: National Institute of Standards and Technology
  meaning: A U.S. government lab that writes widely used security and technology guidance. It isn't a police force — but its playbooks are followed across government, and far beyond it.
**NOVA:** So who writes all of this?
**VEGA:** NIST does. Think of them as the standards lab for digital defense.

*[PLAIN ENGLISH: Information system]*
  meaning: The people, hardware, software, networks, and data that work together to collect, store, process, or move information.
  everyday example: A hospital's patient-records app, a company's email, a bank's website — even the phone in your pocket.
**VEGA:** The thing we're protecting is an information system.
**NOVA:** So... not just a computer?
**VEGA:** Far more. The people and processes count too.

*[PLAIN ENGLISH: Security control]*
  meaning: A safeguard or countermeasure you put in place to protect a system and its information — and to bring risk down.
  everyday example: A lock on a door, a password requirement, a smoke alarm, or a backup of your files.
**NOVA:** And a 'control' is...?
**VEGA:** A safeguard. Something deliberate that reduces risk. NIST SP 800-53 is a giant, organized catalog of them.

*[PLAIN ENGLISH: Risk]*
  meaning: How likely something bad is, multiplied by how badly it would hurt. Security is the work of lowering risk to a level you can live with.
  everyday example: An unlocked door (a vulnerability) plus a burglar nearby (a threat) makes a real risk of theft.
**NOVA:** Everyone keeps saying 'risk.'
**VEGA:** Risk is likelihood times impact. A threat is who or what could hurt you; a vulnerability is the weakness they'd use; risk is the chance — and the cost — if they do.

*[DIAGRAM: Three things every control protects — the C-I-A triad]*
  Confidentiality → Integrity → Availability
**VEGA:** Every control in the catalog serves three goals. Remember them as C-I-A.
**VEGA:** Confidentiality — keep secrets secret. Integrity — keep data correct and untampered. Availability — keep it working when you need it.
**NOVA:** Confidentiality, Integrity, Availability. The reason every guardian exists.

*[LAW · CATALOG · FRAMEWORK: Three words people mix up]*
  • FISMA (Federal Information Security Modernization Act) — the LAW: U.S. agencies and many contractors must protect their information and systems
  • NIST SP 800-53 — the CATALOG: the menu of controls you can put to work
  • The RMF (SP 800-37) — the FRAMEWORK: the step-by-step process that ties it together
**NOVA:** Why does any of this exist?
**VEGA:** A law says you must protect systems. A catalog lists what you can use. A framework is the process that connects them.
**VEGA:** The law is FISMA — the Federal Information Security Modernization Act. 800-53 is the catalog. The RMF is the process. Hold those three apart, and everything else clicks.

*[PLAIN ENGLISH: Security vs. privacy]*
  meaning: Security protects information and systems from unauthorized access, change, or disruption. Privacy protects people from harm caused by how their personal information is handled. They overlap — but they are different goals.
**NOVA:** Isn't privacy just part of security?
**VEGA:** They overlap, but they aim at different things. In Revision 5, security and privacy finally share one catalog.

*[ORIENTATION: What is NIST SP 800-53?]*
  • A catalog of security AND privacy controls for information systems and organizations
  • Published by NIST; Revision 5 released in September 2020
  • The backbone of U.S. federal security — and used widely beyond government too
**NOVA:** So this 'eight-hundred fifty-three' everyone cites — what is it, exactly?
**VEGA:** A catalog. A giant, well-organized menu of controls you put to work.

*[MAP: TWENTY FAMILIES, TWENTY DISTRICTS]*
**VEGA:** The catalog is organized into twenty families. We'll walk them as twenty districts of the city.
**VEGA:** A district isn't really a place — it's a family of related safeguards: policies, processes, and technical controls.
**NOVA:** Twenty? That's a lot of ground.
**VEGA:** So we'll group them into six layers of defense. By the end, you'll remember every one.

*[HOW TO READ A CONTROL: Anatomy of a control]*
  • Identifier, e.g., AC-6 (family plus a number)
  • Control, the requirement itself (the 'what')
  • Discussion, context and rationale, informative, not prescriptive
  • Related controls, links to other controls
  • Enhancements, optional add-ons that strengthen it, e.g., AC-6(1)
  • References, pointers to supporting sources
**VEGA:** Every control shares the same anatomy. Learn it once, and you can read them all.
**VEGA:** First the identifier, like AC-6 — the family and a number.
**VEGA:** Then the control itself: the requirement, what you must actually do.
**NOVA:** And the discussion explains it?
**VEGA:** It gives context and rationale — helpful, but not itself a requirement.
**VEGA:** Related controls point to neighbors. Enhancements add strength — AC-6(1) is an enhancement of AC-6. References point outside the catalog.
**ARCHIVIST:** Identifier. Control. Discussion. Related controls. Enhancements. References.

*[CONTROL: AC-6 Least Privilege]*
  what it means: Give every user and process only the access they truly need — nothing more.
  why it matters: We'll meet AC-6 again at the Outer Walls. For now, notice the shape: ID, title, meaning.
**VEGA:** Here's a single control. AC-6, Least Privilege.
**NOVA:** Clean. An ID, a title, and what it means.

*[VERBATIM] “Employ the principle of least privilege, allowing only authorized accesses for users (or processes acting on behalf of users) that are necessary to accomplish assigned organizational tasks.” — NIST SP 800-53r5  ·  AC-6 Least Privilege*
**VEGA:** When you see a gold card, the Archivist is reading the catalog's real words — word for word.
**ARCHIVIST:** Employ the principle of least privilege, allowing only authorized accesses for users (or processes acting on behalf of users) that are necessary to accomplish assigned organizational tasks.

*[PLAIN ENGLISH: Baseline]*
  meaning: A ready-made starting set of controls, matched to how much harm a system's failure would cause. You begin from the baseline, then adjust it to fit.
  everyday example: Like a 'basic, standard, or premium' security package you start from, then customize.
**NOVA:** People keep saying 'baseline.'
**VEGA:** A starting kit of controls — Low, Moderate, or High, sized to the stakes.

*[TITLE: BASELINES MOVED OUT — Low / Moderate / High now live in NIST SP 800-53B]*
**NOVA:** Hold on — where are the Low, Moderate, and High baselines kept?
**VEGA:** Sharp eye. In Revision 5 they moved out, into a companion book: 800-53B.
**NARRATOR:** 800-53 is the catalog of controls. 800-53B holds the baselines and tailoring guidance.

*[DIAGRAM: Where 800-53 lives: the Risk Management Framework]*
  Prepare → Categorize → Select → Implement → Assess → Authorize → Monitor
**VEGA:** 800-53 doesn't stand alone. It plugs into a process called the Risk Management Framework.
**VEGA:** In plain terms: prepare, decide how much the system matters, pick controls, put them in place, check they work, get a leader to approve it, then watch it forever.
**NOVA:** And the catalog is 800-53; the baselines in 800-53B help choose which controls we start with.
**VEGA:** We'll walk all seven steps in Act Two. For now, just know the catalog has a home.

*[THE CAST: Your guides]*
  • VEGA — your veteran guide through the Citadel
  • NOVA — newly appointed; she asks what you're thinking
  • THE ARCHIVIST — reads the catalog's exact words, on the gold cards
  • THE NULL — the threats, failures, and bad shortcuts the controls help manage
**NARRATOR:** Three guides ride with you.
**NULL:** ...and one rides against you.

*[MAP: THE ROAD AHEAD — SIX LAYERS]*
**VEGA:** Six layers lie ahead. The Outer Walls. The Watchtowers. The Keepers of the Pact.
**VEGA:** The High Council. The Forge. The Vaults and Lifelines. Then the finale: Siege Night.

*[DISCLAIMER: Before we ride]*
  • This series is a memory aid, not a substitute for the standard
  • On-screen IDs and gold quotes are taken from the official catalog
  • For real decisions, always consult NIST SP 800-53r5 and 800-53B
**NARRATOR:** One honest note before we ride out.
**VEGA:** The story is ours. The control text is theirs — real, and shown on screen.

*[QUIZ] In plain terms, a security 'control' is best described as:*
  A. A type of computer
  B. A safeguard that reduces risk (answer)
  C. A government agency
**VEGA:** Let's make it stick. What's a control? Pause, and answer.

*[QUIZ] Where do the Low, Moderate, and High control baselines live now?*
  A. In 800-53 itself
  B. In NIST SP 800-53B (answer)
  C. In the RMF
**NOVA:** Quick check. Where do the baselines live now? Pause, and answer.

*[QUIZ] How many control families does 800-53 Revision 5 have?*
  A. Twelve
  B. Seventeen
  C. Twenty (answer)
**VEGA:** And how many families guard our city?

*[NOTEBOOK: Episode 00 — foundations]*
  • NIST writes the guidance; an information system is people + tech + data working together.
  • A control is a safeguard that lowers risk (risk = likelihood × impact); every control serves C-I-A.
  • FISMA is the law, 800-53 is the catalog, the RMF is the process; baselines live in 800-53B.
  remember: Law, catalog, framework — keep them apart.
**NOVA:** Notebook open. That's the whole map on one page.
**VEGA:** That's your foundation. Next, we ride for the Outer Walls.
**NULL:** I'll be waiting at the gate.


---

# The Outer Walls  (01)
*AC · IA · PE — Who gets in, and what they may touch: access control, identity, and physical security.*

*[BREACH OF THE WEEK: 2021 — One old password darkens a fuel pipeline.]*
  Attackers signed into a forgotten VPN account that had no second factor, and a pipeline serving much of the U.S. East Coast went offline. Not a zero-day — just one unguarded door.
  MITRE ATT&CK: Valid Accounts · T1078
**NULL:** Every gap, every shortcut, every forgotten door — I will find it.
**VEGA:** Not tonight. One stolen login should never be enough to end a city.
**NOVA:** So where do we begin?
**VEGA:** Where every attacker does — at the wall.

*[MAP: AEGIS CITADEL — NIGHTFALL]*
**NULL:** Every fortress has a door. I only need one careless soul to leave one open.
**VEGA:** Then meet the three guardians of the gate. I'm Vega. This is the apprentice, Nova.
**NOVA:** Let's walk the walls.

*[TITLE: 01 — THE OUTER WALLS — Access Control · Identity · Physical]*
**VEGA:** Layer one is the perimeter, who gets in, and what they may touch.
**NARRATOR:** Three families stand the wall: Access Control, Identification, and Physical.

*[MAP: THE OUTER WALLS]*
**VEGA:** Three districts light up the map: AC, IA, and PE.
**NOVA:** The gatekeepers of the city.

*[GUARDIAN: AC Access Control — “The Gatekeeper”]*
  guards: Who may enter the city, and what they may touch.
  in reality: Policies and mechanisms that decide which users and processes may use which systems and data.
**VEGA:** First, the Gatekeeper, Access Control.
**VEGA:** It decides who may enter, and exactly what they may touch.
**VEGA:** In the real world, that's the policies and mechanisms deciding which users and processes may use which systems and data.

*[CONTROL: AC-2 Account Management]*
  what it means: Create, manage, review, and remove accounts across their whole lifecycle.
  why it matters: Stale or rogue accounts are a favorite way in; managing them closes that door.
**NOVA:** Where does access begin?
**VEGA:** With accounts. AC-2 governs every account from birth to deletion.

*[CONTROL: AC-6 Least Privilege]*
  what it means: Give every user and process only the access they truly need — nothing more.
  why it matters: If an account is stolen, least privilege limits how far the intruder can reach.
**VEGA:** Then the rule that saves you again and again, AC-6, Least Privilege.
**NULL:** Less for them to give me when I take an account...

*[VERBATIM] “Employ the principle of least privilege, allowing only authorized accesses for users (or processes acting on behalf of users) that are necessary to accomplish assigned organizational tasks.” — NIST SP 800-53r5  ·  AC-6 Least Privilege*
**ARCHIVIST:** Employ the principle of least privilege, allowing only authorized accesses for users (or processes acting on behalf of users) that are necessary to accomplish assigned organizational tasks.

*[DIAGRAM: How the gate decides]*
  User / Process → Policy Decision → Enforcement Gate
**VEGA:** Every request runs the same path: a policy decides, and a gate enforces it.
**VEGA:** Say Alice works in payroll. Policy lets her open payroll records; the same gate blocks Bob from marketing.
**NOVA:** Decide, then enforce. AC-3 is the enforcement.

*[CHEAT CARD: Access Control]*
  • AC-2 Account Management — manage the full account lifecycle
  • AC-3 Access Enforcement — enforce approved authorizations
  • AC-6 Least Privilege — grant only the minimum access needed
  remember: “Right person, right door, right reason.”
**VEGA:** Lock these three into memory.

*[GUARDIAN OATH — AC] “None pass unknown; none hold more than they need.” (AC-3 · AC-6)*
**VEGA:** Say the Gatekeeper's oath with me. None pass unknown; none hold more than they need.

*[GUARDIAN: IA Identification and Authentication — “The Seal-Bearer”]*
  guards: Proves you are who you claim, before you pass.
  in reality: Verifying the identity of users, devices, and processes before granting access.
**VEGA:** Next, the Seal-Bearer, Identification and Authentication.
**NOVA:** Access Control trusts a name. This guardian proves the name is real.

*[CONTROL: IA-2 Identification and Authentication (Organizational Users)]*
  what it means: Uniquely identify and authenticate organizational users before granting access.
  why it matters: It's the difference between 'someone' and a known, accountable person.
**VEGA:** IA-2 demands proof of identity for every organizational user.
**VEGA:** Its enhancements are where multi-factor authentication lives.

*[PLAIN ENGLISH: Multi-factor authentication (MFA)]*
  stands for: Something you know + something you have + something you are
  meaning: Proving who you are with two or more different kinds of evidence — so one stolen password isn't enough to get in.
  everyday example: A password (know) plus a one-time code from your phone (have) — or a fingerprint (are).
**NOVA:** Multi-factor authentication — what is that, exactly?
**VEGA:** Two kinds of proof instead of one. It's why the pipeline breach we opened with would have failed.

*[CONTROL: IA-5 Authenticator Management]*
  what it means: Manage authenticators — passwords, tokens, certificates — across their lifecycle.
  why it matters: Weak or leaked credentials are a top breach vector; this control hardens them.
**NOVA:** And the passwords and tokens themselves?
**VEGA:** IA-5 manages them, strength, rotation, protection.

*[VERBATIM] “Uniquely identify and authenticate organizational users and associate that unique identification with processes acting on behalf of those users.” — NIST SP 800-53r5  ·  IA-2 Identification and Authentication (Organizational Users)*
**ARCHIVIST:** Uniquely identify and authenticate organizational users and associate that unique identification with processes acting on behalf of those users.

*[CHEAT CARD: Identification and Authentication]*
  • IA-2 Identification and Authentication (Organizational Users) — prove who organizational users are (MFA via enhancements)
  • IA-5 Authenticator Management — manage passwords, tokens, and certificates
  • IA-8 Identification and Authentication (Non-organizational Users) — authenticate non-organizational users too
  remember: “Prove it, before you move it.”
**VEGA:** Identity first. Always.

*[GUARDIAN OATH — IA] “Prove the name, or the gate stays shut.” (IA-2)*
**VEGA:** The Seal-Bearer's oath. Prove the name, or the gate stays shut.

*[GUARDIAN: PE Physical and Environmental Protection — “The Wall-Warden”]*
  guards: Holds the physical gates, and guards against fire and flood.
  in reality: Physical access controls plus protection from hazards like fire, power loss, and water.
**VEGA:** Last on the wall, the Wall-Warden, Physical and Environmental Protection.
**NULL:** Why pick a lock... when I can walk through an open door?
**VEGA:** In reality, PE is physical access control — guards, badges, locks — plus protection from hazards like fire, power loss, and water.

*[CONTROL: PE-3 Physical Access Control]*
  what it means: Enforce who may physically enter — with guards, badges, locks, and logs.
  why it matters: Code can't stop a person who strolls into the server room; PE can.
**VEGA:** PE-3 enforces physical access at the doors themselves.
**NOVA:** Tailgating, propped doors, lost badges, this is where you stop them.

*[CONTROL: PE-6 Monitoring Physical Access]*
  what it means: Monitor and review physical access to facilities.
  why it matters: Watching the doors turns a break-in into an alarm, not a mystery.
**VEGA:** And PE-6 watches and logs who comes and goes.

*[VERBATIM] “Enforce physical access authorizations at [entry and exit points] by:” — NIST SP 800-53r5  ·  PE-3 Physical Access Control*
**ARCHIVIST:** Enforce physical access authorizations at [entry and exit points] by:

*[CHEAT CARD: Physical and Environmental Protection]*
  • PE-2 Physical Access Authorizations — authorize who may enter facilities
  • PE-3 Physical Access Control — enforce entry at the doors
  • PE-6 Monitoring Physical Access — monitor and log physical access
  remember: “Lock the doors — and watch them.”
**VEGA:** Physical security is security.

*[GUARDIAN OATH — PE] “A door is a decision — and I decide.” (PE-3)*
**VEGA:** And the Wall-Warden's oath. A door is a decision — and I decide.

*[HOW IT FITS: The Outer Walls in the RMF]*
  • These families are SELECTED from a 800-53B baseline for your system
  • Then IMPLEMENTED as technical and physical controls
  • And ASSESSED and MONITORED by the High Council (CA, later in the series)
**VEGA:** Remember the framework? The wall is where you implement what you selected.
**NOVA:** Select from the baseline, implement here, assess later.

*[QUIZ] Which guardian proves you are who you claim, before you pass?*
  A. AC — Access Control
  B. IA — Identification & Authentication (answer)
  C. PE — Physical
**NOVA:** Guardian check. Who proves your identity? Pause, and answer.

*[QUIZ] 'Only the access you truly need' is which control?*
  A. AC-2 Account Management
  B. AC-6 Least Privilege (answer)
  C. IA-5 Authenticator Management
**VEGA:** And the rule that limits the blast radius?

*[QUIZ] An intruder tailgates through a propped door into the server room. Which family should stop it?*
  A. PE — Physical (answer)
  B. AU — Audit
  C. SR — Supply Chain
**NOVA:** Scenario: someone tailgates into the server room. Whose watch is that?

*[NOTEBOOK: Episode 01 — the Outer Walls]*
  • AC decides who may do what (AC-2, AC-3, AC-6).
  • IA proves the name is real before you pass — MFA lives in IA-2's enhancements.
  • PE guards the physical doors and environment (PE-2, PE-3, PE-6).
  remember: Right person, right door, right reason.
**NOVA:** Notebook: the wall is access, identity, and physical — working together.
**VEGA:** Three guardians, one wall. The perimeter holds.
**NULL:** Fine. I'll stop knocking... and start hiding.
**VEGA:** Then we'll need the watchtowers. Next time.


---

# The Watchtowers  (02)
*AU · SI · IR — See the intruder, keep the system honest, and respond: audit, integrity, incident response.*

*[BREACH OF THE WEEK: 2017 — A missed patch, unseen for weeks.]*
  A known flaw in a public web app went unpatched. With monitoring crippled by an expired security certificate, the intrusion ran undetected for about 76 days while data on roughly 147 million people was taken.
  MITRE ATT&CK: Exploit Public-Facing App · T1190
**NULL:** Every gap, every shortcut, every forgotten door — I will find it.
**VEGA:** Not tonight. Even if you slip in, you will not move unseen.
**NOVA:** Because someone's watching?
**VEGA:** Because the watchtowers never sleep.

*[MAP: INSIDE THE WALLS]*
**NULL:** I slipped a careless credential past your wall. Now I move in the shadows.
**VEGA:** Shadows don't last here. The watchtowers never sleep.

*[TITLE: 02 — THE WATCHTOWERS — Audit · Integrity · Incident Response]*
**VEGA:** Layer two assumes someone got in. Now we see them, stop the rot, and respond.
**NARRATOR:** Three families keep watch: Audit, System Integrity, and Incident Response.

*[MAP: THE WATCHTOWERS]*
**NOVA:** AU, SI, and IR. The eyes, the immune system, and the firefighters.

*[GUARDIAN: AU Audit and Accountability — “The Chronicler”]*
  guards: Records every footstep, so no deed goes unseen.
  in reality: Logging security-relevant events and being able to review them and hold actors accountable.
**VEGA:** The Chronicler, Audit and Accountability.
**VEGA:** It records every footstep, so no deed goes unseen.
**VEGA:** In reality, that's logging security-relevant events so you can review them and hold people accountable.

*[PLAIN ENGLISH: Audit log]*
  meaning: A timestamped record of what happened on a system — who signed in, what they touched, what changed. It is the evidence you read after something goes wrong.
  everyday example: Like a building's sign-in sheet and camera timeline, but for a computer system.
**NOVA:** What exactly is a 'log'?
**VEGA:** A diary the system keeps. A Windows Event Log, a syslog, a tool like Splunk — same idea.

*[CONTROL: AU-2 Event Logging]*
  what it means: Decide which events the system logs to support the audit function.
  why it matters: You can't review what you never recorded; logging is where accountability begins.
**VEGA:** AU-2 chooses what's worth logging.
**NULL:** So I'll just delete the logs when I'm done.

*[CONTROL: AU-9 Protection of Audit Information]*
  what it means: Protect audit information and logging tools from unauthorized change or deletion.
  why it matters: This is what stops an intruder from erasing their own tracks.
**VEGA:** Not so fast. AU-9 protects the logs themselves.
**NOVA:** So the Null can't quietly rewrite history.

*[VERBATIM] “Identify the types of events that the system is capable of logging in support of the audit function:” — NIST SP 800-53r5  ·  AU-2 Event Logging*
**ARCHIVIST:** Identify the types of events that the system is capable of logging in support of the audit function:

*[CHEAT CARD: Audit and Accountability]*
  • AU-2 Event Logging — decide what events to log
  • AU-3 Content of Audit Records — capture enough detail in each record
  • AU-6 Audit Record Review, Analysis, and Reporting — review and analyze the logs
  • AU-9 Protection of Audit Information — protect the logs from tampering
  remember: “Log it, protect it, read it.”
**VEGA:** A log no one reads, or one that can be erased, is no log at all.

*[GUARDIAN OATH — AU] “Every footstep written; no page erased.” (AU-2 · AU-9)*
**VEGA:** The Chronicler's oath. Every footstep written; no page erased.

*[GUARDIAN: SI System and Information Integrity — “The Healer”]*
  guards: Finds the rot, cures the sickness, keeps the truth true.
  in reality: Flaw remediation, malicious-code protection, system monitoring, and integrity verification.
**VEGA:** The Healer, System and Information Integrity.
**NOVA:** It finds the rot, cures the sickness, and keeps the truth true.
**VEGA:** In reality, that's patching flaws, blocking malicious code, monitoring for intrusions, and verifying nothing was tampered with.

*[CONTROL: SI-2 Flaw Remediation]*
  what it means: Find, report, and fix system flaws — and patch them in good time.
  why it matters: Unpatched flaws are the cracks attackers pour through; SI-2 seals them.
**VEGA:** SI-2 is flaw remediation, the discipline of patching.

*[CONTROL: SI-4 System Monitoring]*
  what it means: Monitor the system to detect attacks, intrusions, and unusual activity.
  why it matters: It's the tower's spyglass, watching traffic and behavior for trouble.
**VEGA:** And SI-4 watches the system for signs of an intruder.
**NULL:** Every move I make... another tower turns my way.

*[MAP: THE WATCH CATCHES A SHADOW]*
**NULL:** Six days I moved in your shadows before a single tower turned.
**NOVA:** Six days?!
**VEGA:** Six days — but SI-4 saw the anomaly, and AU-9 kept the logs he tripped. He got in. He did not get out clean.
**NULL:** ...this time.

*[VERBATIM] “Identify, report, and correct system flaws;” — NIST SP 800-53r5  ·  SI-2 Flaw Remediation*
**ARCHIVIST:** Identify, report, and correct system flaws;

*[CHEAT CARD: System and Information Integrity]*
  • SI-2 Flaw Remediation — patch flaws promptly
  • SI-3 Malicious Code Protection — stop malicious code
  • SI-4 System Monitoring — monitor for intrusions
  • SI-7 Software, Firmware, and Information Integrity — verify software and data integrity
  remember: “Patch, detect, verify.”
**VEGA:** Integrity is keeping the system clean and honest.

*[GUARDIAN OATH — SI] “Find the rot, close the wound, keep it true.” (SI-2 · SI-4 · SI-7)*
**VEGA:** The Healer's oath. Find the rot, close the wound, keep it true.

*[GUARDIAN: IR Incident Response — “The Firewatch”]*
  guards: Sounds the alarm and contains the blaze.
  in reality: Detecting, reporting, analyzing, containing, and recovering from security incidents.
**VEGA:** The Firewatch, Incident Response.
**VEGA:** When something burns, it sounds the alarm and contains the blaze.
**VEGA:** In reality, that's detecting, reporting, analyzing, containing, and recovering from security incidents.

*[PLAIN ENGLISH: Security incident]*
  meaning: An event that actually harms a system or its data, or breaks the rules meant to protect them — a real breach, not just a warning light.
  everyday example: A ransomware infection, a stolen laptop full of patient data, or a hijacked account.
**NOVA:** When does a threat become an 'incident'?
**VEGA:** The moment it stops being hypothetical — malware runs, data leaks, a system goes down.

*[CONTROL: IR-4 Incident Handling]*
  what it means: Run a capability to detect, contain, eradicate, and recover from incidents.
  why it matters: A breach is a question of when; IR-4 is having the answer rehearsed.
**NOVA:** What happens the moment we spot the Null?
**VEGA:** IR-4 takes over, handling the incident end to end.

*[DIAGRAM: The incident response lifecycle]*
  Preparation → Detection & Analysis → Containment → Eradication → Recovery
**VEGA:** Every incident follows a rhythm: prepare, detect, contain, eradicate, recover.
**NOVA:** And IR-8 writes the plan that makes it routine.

*[VERBATIM] “Implement an incident handling capability for incidents that is consistent with the incident response plan and includes preparation, detection and analysis, containment, eradication, and recovery;” — NIST SP 800-53r5  ·  IR-4 Incident Handling*
**ARCHIVIST:** Implement an incident handling capability for incidents that is consistent with the incident response plan and includes preparation, detection and analysis, containment, eradication, and recovery;

*[CHEAT CARD: Incident Response]*
  • IR-2 Incident Response Training — train people for their incident roles
  • IR-4 Incident Handling — handle incidents end to end
  • IR-6 Incident Reporting — report incidents to the right people
  • IR-8 Incident Response Plan — write and maintain the response plan
  remember: “Plan, detect, contain, recover.”
**VEGA:** The best responders practiced before the fire.

*[GUARDIAN OATH — IR] “When it burns, we are already running.” (IR-4 · IR-8)*
**VEGA:** The Firewatch's oath. When it burns, we are already running.

*[HOW IT FITS: The Watchtowers in the RMF]*
  • AU, SI, and IR power the MONITOR step — continuous vigilance
  • They embody the Detect and Respond security functions
  • Protect your logs (AU-9) or the whole watch can be blinded
**VEGA:** Selecting and implementing was the wall. Watching is how you keep it.

*[QUIZ] An intruder tries to delete the logs to hide. Which control blocks that?*
  A. AU-2 Event Logging
  B. AU-9 Protection of Audit Information (answer)
  C. SI-4 System Monitoring
**NOVA:** Scenario: the Null deletes logs. What stops it? Pause, and answer.

*[QUIZ] Which family detects, contains, and recovers from a breach?*
  A. IR — Incident Response (answer)
  B. AU — Audit
  C. AC — Access Control
**VEGA:** And who runs toward the fire?

*[NOTEBOOK: Episode 02 — the Watchtowers]*
  • AU sees and remembers — and protects its own records (AU-2, AU-6, AU-9).
  • SI keeps the system clean and honest: patch, detect, verify (SI-2, SI-4, SI-7).
  • IR turns a crisis into a rehearsed routine (IR-4, IR-6, IR-8).
  remember: Log it, protect it, read it — then run toward the fire.
**NOVA:** Notebook: assume they got in, then see them, heal the system, and answer fast.
**VEGA:** Seen, healed, and answered. The towers hold.
**NULL:** Then I'll turn your own people against you.
**VEGA:** Then we ride to the Keepers of the Pact.


---

# The Keepers of the Pact  (03)
*AT · PS · PT — People and privacy: awareness training, personnel security, and PII processing & transparency.*

*[BREACH OF THE WEEK: 2020 — They didn't hack the computer. They called the staff.]*
  Attackers phoned employees, talked their way into an internal admin tool, and hijacked high-profile accounts. The exploit was a person, not a port.
  MITRE ATT&CK: Phishing · T1566
**NULL:** Every gap, every shortcut, every forgotten door — I will find it.
**VEGA:** Not tonight. And the easiest door of all is a person who hasn't been trained.
**NOVA:** So the people are the perimeter too?
**VEGA:** The most-attacked one. Let's defend them.

*[MAP: THE HUMAN GATE]*
**NULL:** Walls and towers? Tedious. People are so much easier to fool.
**VEGA:** Which is why the strongest controls guard the people, and their data.

*[TITLE: 03 — THE KEEPERS OF THE PACT — Training · Personnel · Privacy]*
**VEGA:** Layer three is human. Train them, trust them carefully, and honor their data.
**NARRATOR:** Three families keep the pact: Awareness & Training, Personnel Security, and Privacy.

*[MAP: THE KEEPERS OF THE PACT]*
**NOVA:** AT, PS, and PT. The teacher, the oathkeeper, and the privacy herald.

*[GUARDIAN: AT Awareness and Training — “The Drillmaster”]*
  guards: Trains every citizen to spot a trick at the gate.
  in reality: Security and privacy awareness plus role-based training so people recognize and resist threats.
**VEGA:** The Drillmaster, Awareness and Training.
**VEGA:** A trained citizen spots the trick at the gate before it opens.
**VEGA:** In reality, that's security and privacy training so people recognize and resist threats like phishing.

*[PLAIN ENGLISH: Phishing]*
  meaning: A fake message — email, text, or phone call — designed to trick a person into giving up a password or clicking something harmful.
  everyday example: An 'urgent' email that looks like IT, asking you to 'verify your password' on a lookalike page.
**NOVA:** What is 'phishing,' exactly?
**VEGA:** Bait for people. A message that looks legitimate but is a trap — and it's how most breaches actually begin.

*[CONTROL: AT-2 Literacy Training and Awareness]*
  what it means: Give every user security and privacy awareness training — including phishing.
  why it matters: People are the most-targeted control surface; awareness is the cheapest strong defense.
**NOVA:** How do you stop a perfect phishing email?
**VEGA:** You train the human. AT-2 builds that instinct in everyone — the instinct that hangs up on the kind of call we opened with.

*[CONTROL: AT-3 Role-based Training]*
  what it means: Give people role-based training for their specific security duties.
  why it matters: An admin, a developer, and a clerk face different risks; AT-3 tailors the lesson.
**VEGA:** And AT-3 trains people for their particular role.

*[VERBATIM] “Provide security and privacy literacy training to system users (including managers, senior executives, and contractors):” — NIST SP 800-53r5  ·  AT-2 Literacy Training and Awareness*
**ARCHIVIST:** Provide security and privacy literacy training to system users (including managers, senior executives, and contractors):

*[CHEAT CARD: Awareness and Training]*
  • AT-2 Literacy Training and Awareness — awareness training for everyone (incl. phishing)
  • AT-3 Role-based Training — role-based training for specific duties
  • AT-4 Training Records — keep training records
  remember: “A trained user is a control.”
**VEGA:** The cheapest firewall you own is an alert human.

*[GUARDIAN OATH — AT] “The sharpest blade is an alert mind.” (AT-2)*
**VEGA:** The Drillmaster's oath. The sharpest blade is an alert mind.

*[GUARDIAN: PS Personnel Security — “The Oathkeeper”]*
  guards: Vets every guard, and reclaims the keys when they leave.
  in reality: Screening personnel and adjusting access on transfer or termination; insider-risk safeguards.
**VEGA:** The Oathkeeper, Personnel Security.
**NULL:** Every guard you hire... could be mine.
**VEGA:** In reality, that's screening people, adjusting access when they move or leave, and guarding against insider risk.

*[CONTROL: PS-3 Personnel Screening]*
  what it means: Screen people before granting access — and rescreen as needed.
  why it matters: Trust is granted, not assumed; screening is how the citadel vets its guards.
**VEGA:** PS-3 screens people before they're trusted with access.

*[CONTROL: PS-4 Personnel Termination]*
  what it means: When someone leaves, revoke access and recover assets — promptly.
  why it matters: A departing admin who keeps access is a breach waiting to happen.
**NOVA:** And when a guard leaves?
**VEGA:** PS-4 reclaims the keys, on the way out the door.

*[VERBATIM] “Upon termination of individual employment:” — NIST SP 800-53r5  ·  PS-4 Personnel Termination*
**ARCHIVIST:** Upon termination of individual employment:

*[CHEAT CARD: Personnel Security]*
  • PS-3 Personnel Screening — screen people before access
  • PS-4 Personnel Termination — revoke access on termination
  • PS-5 Personnel Transfer — adjust access on transfer
  • PS-7 External Personnel Security — hold external workers to the same bar
  remember: “Vet them in, and key them out.”
**VEGA:** Access should follow the person, and leave when they do.

*[GUARDIAN OATH — PS] “Trust is earned at the gate, and returned at the door.” (PS-3 · PS-4)*
**VEGA:** The Oathkeeper's oath. Trust is earned at the gate, and returned at the door.

*[GUARDIAN: PT Personally Identifiable Information Processing and Transparency — “The Privacy Herald”]*
  guards: Protects citizens' personal stories, and tells them how they are used.
  in reality: Lawful, transparent processing of personally identifiable information, with consent and notice.
**VEGA:** The Privacy Herald, P-T, Processing and Transparency of personal data.
**NOVA:** New in Revision 5, privacy now stands beside security.
**VEGA:** In reality, that's processing people's personal data lawfully and openly — with notice and consent where required.

*[PLAIN ENGLISH: PII]*
  stands for: Personally Identifiable Information
  meaning: Information that can identify a specific person — on its own, or combined with other data.
  everyday example: A name with a Social Security number, a home address, a medical record, or an account number.
**NOVA:** P-I-I keeps coming up.
**VEGA:** Personally identifiable information — the data that points to a real human being. Privacy is about protecting it, and the person.

*[CONTROL: PT-2 Authority to Process Personally Identifiable Information]*
  what it means: Have lawful authority before processing people's personal information.
  why it matters: Privacy starts with a simple question: are we even allowed to do this?
**VEGA:** PT-2 demands a documented authority to process personal data.

*[CONTROL: PT-5 Privacy Notice]*
  what it means: Tell people, clearly, how their personal information is used.
  why it matters: Transparency is the promise behind the pact: no secret uses of personal data.
**VEGA:** And PT-5 gives people honest notice of how their data is used.

*[DIAGRAM: The privacy pact, in order]*
  Authority to process → Purpose + Notice → Consent (where required) → Lawful processing
**VEGA:** Authority first, then purpose and notice, then consent where required, and process only as authorized.
**NOVA:** Permission where needed, and honesty, before the data is used.

*[VERBATIM] “Determine and document the [authority] that permits the [processing] of personally identifiable information;” — NIST SP 800-53r5  ·  PT-2 Authority to Process Personally Identifiable Information*
**ARCHIVIST:** Determine and document the [authority] that permits the [processing] of personally identifiable information;

*[CHEAT CARD: Personally Identifiable Information Processing and Transparency]*
  • PT-2 Authority to Process Personally Identifiable Information — have authority to process PII
  • PT-3 Personally Identifiable Information Processing Purposes — process PII only for stated purposes
  • PT-4 Consent — get consent where required
  • PT-5 Privacy Notice — give a clear privacy notice
  remember: “Allowed, honest, and only as promised.”
**VEGA:** Security protects the data. Privacy honors the person.

*[GUARDIAN OATH — PT] “By what right, for what purpose, with whose leave?” (PT-2 · PT-5)*
**VEGA:** The Privacy Herald's oath. By what right, for what purpose, with whose leave?

*[HOW IT FITS: The Keepers in the RMF]*
  • These are people and program controls, not just technical ones
  • PT weaves privacy through the whole catalog — new in Revision 5
  • In practice: train, screen, and process personal data lawfully and openly
**VEGA:** Not every control is a firewall. Some are a habit, a contract, a promise.

*[QUIZ] A departing administrator still has their access a week later. Which control failed?*
  A. PS-4 Personnel Termination (answer)
  B. AT-2 Awareness Training
  C. PT-5 Privacy Notice
**NOVA:** Scenario: a leaver kept their access. Which guardian dropped the ball?

*[QUIZ] Which family is new in Revision 5 and governs personal-data processing?*
  A. AT — Training
  B. PS — Personnel
  C. PT — PII Processing & Transparency (answer)
**VEGA:** And which guardian is the newcomer to the catalog?

*[NOTEBOOK: Episode 03 — the Keepers of the Pact]*
  • AT trains the human firewall, including phishing (AT-2, AT-3, AT-4).
  • PS vets people in and keys them out (PS-3, PS-4, PS-5, PS-7).
  • PT keeps personal data (PII) lawful, honest, and as-promised (PT-2, PT-3, PT-5).
  remember: People are the perimeter — train them, screen them, and honor their data.
**NOVA:** Notebook: not every control is a firewall — some are a habit, a contract, a promise.
**VEGA:** People kept, the pact honored.
**NULL:** Then I'll strike where no one is even looking. Your plans.
**VEGA:** Then it's time to meet the High Council.


---

# The High Council  (04)
*RA · PL · PM · CA — Govern and assess: risk assessment, planning, program management, and assessment & authorization.*

*[BREACH OF THE WEEK: 2015 — Records of millions, taken on an unauthorized system.]*
  Background-investigation files on about 21 million people were stolen. Auditors had warned for years that key systems were running without a current authorization to operate.
  MITRE ATT&CK: Governance failure · no valid ATO
**NULL:** Every gap, every shortcut, every forgotten door — I will find it.
**VEGA:** Not tonight. And the deepest gaps aren't in the walls — they're in the decisions above them.
**NOVA:** Decisions can be a vulnerability?
**VEGA:** The costliest kind. Welcome to the High Council.

*[MAP: THE INNER KEEP]*
**NULL:** Strike the plans, and every wall is built on sand.
**VEGA:** Then it's time you met the High Council, where the realm is governed.

*[TITLE: 04 — THE HIGH COUNCIL — Risk · Planning · Program · Assessment]*
**VEGA:** Layer four is governance, the decisions above any single wall.
**NARRATOR:** Four families rule the keep: Risk Assessment, Planning, Program Management, and Assessment & Authorization.

*[MAP: THE HIGH COUNCIL]*
**NOVA:** RA, PL, PM, and CA. The seer, the cartographer, the steward, and the inspector.

*[GUARDIAN: RA Risk Assessment — “The Seer”]*
  guards: Reads the omens: what could go wrong, and how badly.
  in reality: Identifying and analyzing risk, including vulnerability scanning and threat assessment.
**VEGA:** The Seer, Risk Assessment — though this seer never merely guesses.
**VEGA:** It doesn't read omens; it measures them: what could go wrong, how likely, and how badly.
**VEGA:** In reality, that's analyzing risk with hard evidence — vulnerability scans and threat intelligence.

*[CONTROL: RA-3 Risk Assessment]*
  what it means: Assess the risk to the system — threats, vulnerabilities, likelihood, and impact.
  why it matters: Risk is the compass; it tells you which controls actually matter for your system.
**VEGA:** RA-3 is the formal risk assessment, the basis for every choice.

*[CONTROL: RA-5 Vulnerability Monitoring and Scanning]*
  what it means: Scan for vulnerabilities, and act on what you find.
  why it matters: An unscanned, unpatched service is the unseen crack in the wall.
**NOVA:** How do we find the cracks before the Null does?
**VEGA:** RA-5, vulnerability monitoring and scanning, hunts them down.

*[VERBATIM] “Monitor and scan for vulnerabilities in the system and hosted applications [organization-defined frequency and/or randomly in accordance with organization-defined process] and when new vulnerabilities potentially affecting the system are identified and reported;” — NIST SP 800-53r5  ·  RA-5 Vulnerability Monitoring and Scanning*
**ARCHIVIST:** Monitor and scan for vulnerabilities in the system and hosted applications [organization-defined frequency and/or randomly in accordance with organization-defined process] and when new vulnerabilities potentially affecting the system are identified and reported;

*[CHEAT CARD: Risk Assessment]*
  • RA-3 Risk Assessment — assess threats, vulnerabilities, and impact
  • RA-5 Vulnerability Monitoring and Scanning — scan for vulnerabilities and remediate
  • RA-7 Risk Response — respond to the risks you find
  remember: “Know the risk before you spend a coin.”
**VEGA:** Risk first. It tells you where to spend your strength.

*[GUARDIAN OATH — RA] “I do not guess the storm; I measure it.” (RA-3 · RA-5)*
**VEGA:** The Seer's oath. I do not guess the storm; I measure it.

*[GUARDIAN: PL Planning — “The Cartographer”]*
  guards: Draws the map of the defense before the march.
  in reality: System security and privacy plans, rules of behavior, and security architecture.
**VEGA:** The Cartographer, Planning.
**NOVA:** It draws the map of the defense before the march.
**VEGA:** In reality, that's the system security and privacy plan, the rules of behavior, and the security architecture.

*[CONTROL: PL-2 System Security and Privacy Plans]*
  what it means: Write a security and privacy plan for the system — the single source of truth.
  why it matters: The plan says what the system is, who runs it, and which controls protect it.
**VEGA:** PL-2 is the system security and privacy plan, the master map.

*[CONTROL: PL-8 Security and Privacy Architectures]*
  what it means: Design a security and privacy architecture, on purpose, up front.
  why it matters: Architecture decides where the walls go before a single stone is laid.
**VEGA:** And PL-8 plans the architecture, defense by design.

*[VERBATIM] “Develop security and privacy plans for the system that:” — NIST SP 800-53r5  ·  PL-2 System Security and Privacy Plans*
**ARCHIVIST:** Develop security and privacy plans for the system that:

*[CHEAT CARD: Planning]*
  • PL-2 System Security and Privacy Plans — the system security & privacy plan
  • PL-4 Rules of Behavior — rules of behavior for users
  • PL-8 Security and Privacy Architectures — security & privacy architecture
  remember: “Plan the map before the march.”
**VEGA:** No plan, no defense, just luck.

*[GUARDIAN OATH — PL] “No march without a map.” (PL-2)*
**VEGA:** The Cartographer's oath. No march without a map.

*[GUARDIAN: PM Program Management — “The High Steward”]*
  guards: Governs the whole realm's defense, above any single wall.
  in reality: Organization-wide governance: the security and privacy program, roles, risk strategy, and resources.
**VEGA:** The High Steward, Program Management.
**VEGA:** It governs the whole realm's defense, above any single system.
**VEGA:** In reality, that's organization-wide governance: the security and privacy program, roles, risk strategy, and resources.

*[CONTROL: PM-9 Risk Management Strategy]*
  what it means: Set an organization-wide strategy to manage risk.
  why it matters: PM steers the whole program; these controls run org-wide, not per-system.
**NOVA:** Who sets the strategy for everything?
**VEGA:** PM-9, the risk management strategy for the entire organization.

*[ACCURACY ANCHOR: A note on Program Management]*
  • PM controls are organization-wide, not tied to one system
  • They are deployed independently of the Low / Moderate / High baselines
  • Think governance: leadership, strategy, resources, and oversight
**VEGA:** Important: PM controls aren't selected per system from a baseline.
**VEGA:** They run across the whole organization, all the time.

*[VERBATIM] “Develops a comprehensive strategy to manage:” — NIST SP 800-53r5  ·  PM-9 Risk Management Strategy*
**ARCHIVIST:** Develops a comprehensive strategy to manage:

*[CHEAT CARD: Program Management]*
  • PM-2 Information Security Program Leadership Role — name the security program leadership
  • PM-9 Risk Management Strategy — the organization-wide risk strategy
  • PM-11 Mission and Business Process Definition — define mission and business processes
  • PM-31 Continuous Monitoring Strategy — the continuous monitoring strategy
  remember: “Govern the whole, not just the parts.”
**VEGA:** Program management is the realm thinking as one.

*[GUARDIAN OATH — PM] “One realm, one strategy — always.” (PM-1 · PM-9)*
**VEGA:** The High Steward's oath. One realm, one strategy — always.

*[GUARDIAN: CA Assessment, Authorization, and Monitoring — “The Inspector”]*
  guards: Tests the defenses and signs off before the gates open.
  in reality: Assessing controls, formally authorizing systems to operate, and continuously monitoring them.
**VEGA:** The Inspector, Assessment, Authorization, and Monitoring.
**NOVA:** It tests the defenses, and signs off before the gates open.
**VEGA:** In reality, that's assessing controls, formally authorizing a system to operate, and watching it continuously.

*[CONTROL: CA-6 Authorization]*
  what it means: An authorizing official formally accepts the risk and authorizes the system to operate.
  why it matters: Authorization is a named, accountable leader putting their signature on the risk.
**VEGA:** CA-6, authorization, the authorizing official says 'I accept this risk.' The agency we opened with ran key systems without this signature.
**NULL:** A signature won't stop me.
**VEGA:** No. But it puts a name on the wall the day something does. And CA-7 keeps watching after the ink dries.

*[PLAIN ENGLISH: Authorization to Operate (ATO)]*
  stands for: ATO = Authorization to Operate, granted by the Authorizing Official (AO)
  meaning: A senior leader's formal, signed decision that a system's remaining risk is acceptable — so it may go live. It accepts risk; it does not guarantee safety.
**NOVA:** So a real person signs for the risk?
**VEGA:** The authorizing official — a senior, accountable leader — grants the A-T-O, and owns that decision.

*[CONTROL: CA-2 Control Assessments]*
  what it means: Independently assess whether the controls actually work.
  why it matters: Selecting a control isn't enough; CA-2 checks it truly does its job.
**VEGA:** CA-2 plans and runs the assessment, using procedures from companion doc 800-53A.

*[PLAIN ENGLISH: POA&M]*
  stands for: POA&M = Plan of Action & Milestones (CA-5)
  meaning: A living to-do list of every known weakness you haven't fixed yet — each with an owner and a due date. It's how honest teams drive risk down over time.
**NOVA:** And the gaps we find but can't close today?
**VEGA:** They go on the POA&M. CA-5 requires it, and the authorizing official keeps an eye on it.

*[VERBATIM] “Select the appropriate assessor or assessment team for the type of assessment to be conducted;” — NIST SP 800-53r5  ·  CA-2 Control Assessments*
**ARCHIVIST:** Select the appropriate assessor or assessment team for the type of assessment to be conducted;

*[CHEAT CARD: Assessment, Authorization, and Monitoring]*
  • CA-2 Control Assessments — assess that controls work (per 800-53A)
  • CA-5 Plan of Action and Milestones — track weaknesses in a POA&M
  • CA-6 Authorization — authorize the system to operate
  • CA-7 Continuous Monitoring — monitor continuously
  remember: “Test it, sign it, watch it.”
**VEGA:** Assess, authorize, and never stop monitoring.

*[GUARDIAN OATH — CA] “Test before you trust; watch after you sign.” (CA-2 · CA-6 · CA-7)*
**VEGA:** The Inspector's oath. Test before you trust; watch after you sign.

*[HOW IT FITS: The High Council drives the RMF]*
  • RA → categorize and assess risk
  • PL → plan; PM → govern the whole program
  • CA → assess, authorize, and monitor the system
**VEGA:** If a layer maps onto the framework, it's this one.
**NOVA:** Risk, planning, governance, and assessment, the work behind the RMF lifecycle.

*[QUIZ] A new system is ready to go live. Who formally accepts the risk to operate it?*
  A. CA-6 Authorization (answer)
  B. RA-3 Risk Assessment
  C. PL-2 System Plan
**NOVA:** Scenario: go-live day. Whose signature is required? Pause, and answer.

*[QUIZ] Where are known weaknesses tracked until they're fixed?*
  A. In the system plan
  B. In a POA&M (CA-5) (answer)
  C. In the audit log
**VEGA:** And where do we record the gaps we haven't closed yet?

*[NOTEBOOK: Episode 04 — the High Council]*
  • RA finds and ranks risk with evidence (RA-3, RA-5, RA-7).
  • PL plans the defense; PM governs the whole organization (PL-2, PL-8; PM-9, PM-2).
  • CA assesses, authorizes (the ATO), tracks gaps (POA&M), and monitors (CA-2, CA-5, CA-6, CA-7).
  remember: Govern the whole; test it, sign it, watch it.
**NOVA:** Notebook: this layer is the brain — it decides what the walls are even for.
**VEGA:** The realm is governed. Now, to where it's all built.
**NULL:** Built? I'll poison it at the source.
**VEGA:** Then we descend to the Forge.


---

# The Forge  (05)
*SA · CM · MA · SR — Build, configure, maintain, and source securely, including the supply chain.*

*[BREACH OF THE WEEK: 2020 — The malware was shipped in, signed and trusted.]*
  Attackers hid a backdoor inside a routine software update from a trusted vendor; roughly 18,000 organizations installed it themselves. They didn't break in — they were built in.
  MITRE ATT&CK: Supply Chain Compromise · T1195.002
**NULL:** Every gap, every shortcut, every forgotten door — I will find it. Or I'll have you build it for me.
**VEGA:** Not tonight. We harden the forge itself — how systems are built, configured, and supplied.
**NOVA:** Even the parts we buy?
**VEGA:** Especially those.

*[MAP: THE FORGE]*
**NULL:** Why break in, when I can be built in? A flaw here, a tampered part there...
**VEGA:** Then we harden the forge itself, where systems are made and supplied.

*[TITLE: 05 — THE FORGE — Acquisition · Configuration · Maintenance · Supply Chain]*
**VEGA:** Layer five is how you build, buy, configure, maintain, and source.
**NARRATOR:** Four families work the forge: System Acquisition, Configuration Management, Maintenance, and Supply Chain Risk Management.

*[MAP: THE FORGE]*
**NOVA:** SA, CM, MA, and SR. The quartermaster, the blueprint-master, the smith, and the caravan-master.

*[GUARDIAN: SA System and Services Acquisition — “The Quartermaster”]*
  guards: Buys and builds only what can be trusted.
  in reality: Building security into the development life cycle and into systems and services you acquire.
**VEGA:** The Quartermaster, System and Services Acquisition.
**VEGA:** It buys and builds only what can be trusted.
**VEGA:** In reality, that's building security into the development life cycle, and into the systems and services you acquire.

*[CONTROL: SA-8 Security and Privacy Engineering Principles]*
  what it means: Apply security and privacy engineering principles when you design and build.
  why it matters: Security bolted on later is weak; SA-8 bakes it in from the first sketch.
**VEGA:** SA-8 builds security in by design, not as an afterthought.

*[CONTROL: SA-22 Unsupported System Components]*
  what it means: Replace unsupported components — software past its end of life.
  why it matters: Unsupported software gets no patches; it's a permanently open window.
**NOVA:** What about software no one updates anymore?
**VEGA:** SA-22 says replace it, or arrange alternate support. Unsupported is risk you must manage.

*[VERBATIM] “Apply the following systems security and privacy engineering principles in the specification, design, development, implementation, and modification of the system and system components:” — NIST SP 800-53r5  ·  SA-8 Security and Privacy Engineering Principles*
**ARCHIVIST:** Apply the following systems security and privacy engineering principles in the specification, design, development, implementation, and modification of the system and system components:

*[CHEAT CARD: System and Services Acquisition]*
  • SA-3 System Development Life Cycle — build security into the life cycle
  • SA-4 Acquisition Process — put security in acquisition contracts
  • SA-8 Security and Privacy Engineering Principles — engineer with security principles
  • SA-22 Unsupported System Components — replace unsupported components
  remember: “Build it secure, or don't buy it.”
**VEGA:** Trust is forged in, never sprinkled on.

*[GUARDIAN OATH — SA] “Built in, never sprinkled on.” (SA-8)*
**VEGA:** The Quartermaster's oath. Built in, never sprinkled on.

*[GUARDIAN: CM Configuration Management — “The Master of Blueprints”]*
  guards: Keeps the master plans and forbids unsanctioned change.
  in reality: Baseline configurations and change control so systems stay in a known, secure state.
**VEGA:** The Master of Blueprints, Configuration Management.
**NULL:** One quiet, undocumented change... and I have a door no one remembers.
**VEGA:** In reality, that's keeping a known, approved configuration and controlling every change, so systems stay in a trusted state.

*[PLAIN ENGLISH: Two kinds of 'baseline']*
  meaning: Heads up: 'baseline' means two different things. A CONTROL baseline (from 800-53B) is your starting set of controls. A CONFIGURATION baseline (CM-2) is the known-good snapshot of a system's settings, versions, and components.
**NOVA:** We already met 'baseline' back in Episode 00.
**VEGA:** Different baseline. That was the control baseline. CM-2 is the configuration baseline — drift from it, and you have a question to answer.

*[CONTROL: CM-2 Baseline Configuration]*
  what it means: Keep a known, documented baseline configuration of the system.
  why it matters: If you don't know the 'normal,' you can't spot the tampering.
**VEGA:** CM-2 holds the baseline, the master blueprint of the system.

*[CONTROL: CM-7 Least Functionality]*
  what it means: Turn off what you don't need — least functionality.
  why it matters: Every extra service and port is another door; CM-7 closes the unused ones.
**VEGA:** CM-7 is least functionality. Computers talk on numbered channels — ports — and run background programs — services.
**NOVA:** And every one you don't need is another door.
**VEGA:** Exactly. CM-7 closes the ports and services you never use.

*[VERBATIM] “Develop, document, and maintain under configuration control, a current baseline configuration of the system;” — NIST SP 800-53r5  ·  CM-2 Baseline Configuration*
**ARCHIVIST:** Develop, document, and maintain under configuration control, a current baseline configuration of the system;

*[CHEAT CARD: Configuration Management]*
  • CM-2 Baseline Configuration — keep a known baseline configuration
  • CM-3 Configuration Change Control — control every change
  • CM-7 Least Functionality — least functionality — disable the unneeded
  • CM-8 System Component Inventory — inventory your components
  remember: “Know normal; approve every change.”
**VEGA:** A known system is a defensible system.

*[GUARDIAN OATH — CM] “A known system is a defended system.” (CM-2 · CM-7)*
**VEGA:** The Blueprint-Master's oath. A known system is a defended system.

*[GUARDIAN: MA Maintenance — “The Smith”]*
  guards: Tends the machinery, and watches who holds the tools.
  in reality: Controlled system maintenance, including safeguards for remote and third-party maintenance.
**VEGA:** The Smith, Maintenance.
**NOVA:** It tends the machinery, and watches who holds the tools.
**VEGA:** In reality, that's controlled system maintenance — including safeguards for remote and third-party work.

*[CONTROL: MA-2 Controlled Maintenance]*
  what it means: Control and log maintenance — who, what, when, and approved.
  why it matters: Maintenance touches the guts of a system; uncontrolled, it's a perfect cover.
**VEGA:** MA-2 controls maintenance, scheduled, approved, and recorded.

*[CONTROL: MA-4 Nonlocal Maintenance]*
  what it means: Guard remote maintenance sessions tightly.
  why it matters: A remote maintenance link is a powerful door; MA-4 keeps it locked and watched.
**NULL:** Your remote support line was going to be my way in.
**VEGA:** MA-4 saw to that. Remote maintenance, tightly controlled.

*[VERBATIM] “Schedule, document, and review records of maintenance, repair, and replacement on system components in accordance with manufacturer or vendor specifications and/or organizational requirements;” — NIST SP 800-53r5  ·  MA-2 Controlled Maintenance*
**ARCHIVIST:** Schedule, document, and review records of maintenance, repair, and replacement on system components in accordance with manufacturer or vendor specifications and/or organizational requirements;

*[CHEAT CARD: Maintenance]*
  • MA-2 Controlled Maintenance — control and record maintenance
  • MA-4 Nonlocal Maintenance — secure remote maintenance
  • MA-5 Maintenance Personnel — vet maintenance personnel
  remember: “Mind the hands on the machine.”
**VEGA:** Maintenance is access. Treat it like access.

*[GUARDIAN OATH — MA] “Every tool is a key, and I guard the keys.” (MA-2 · MA-4)*
**VEGA:** The Smith's oath. Every tool is a key, and I guard the keys.

*[GUARDIAN: SR Supply Chain Risk Management — “The Caravan-Master”]*
  guards: Guards the roads your supplies travel, all the way to the source.
  in reality: Managing risk from suppliers, components, and the supply chain: authenticity and provenance.
**VEGA:** The Caravan-Master, Supply Chain Risk Management, new in Revision 5.
**VEGA:** It guards the roads your supplies travel, all the way to the source.
**VEGA:** In reality, that's managing risk from suppliers and components — the SolarWinds-style attack we opened with, where a trusted update carried a hidden backdoor.

*[CONTROL: SR-11 Component Authenticity]*
  what it means: Detect and prevent counterfeit components.
  why it matters: A tampered part can arrive pre-compromised; SR-11 checks what you're given is real.
**NOVA:** How do we trust the parts themselves?
**VEGA:** SR-11, component authenticity, hunts counterfeits and tampering.

*[VERBATIM] “Develop and implement anti-counterfeit policy and procedures that include the means to detect and prevent counterfeit components from entering the system;” — NIST SP 800-53r5  ·  SR-11 Component Authenticity*
**ARCHIVIST:** Develop and implement anti-counterfeit policy and procedures that include the means to detect and prevent counterfeit components from entering the system;

*[CHEAT CARD: Supply Chain Risk Management]*
  • SR-3 Supply Chain Controls and Processes — supply chain controls and processes
  • SR-5 Acquisition Strategies, Tools, and Methods — strategies for acquiring components
  • SR-8 Notification Agreements — notification agreements with suppliers
  • SR-11 Component Authenticity — detect and prevent counterfeits
  remember: “Trust the road, all the way to the source.”
**VEGA:** Your security is only as strong as your weakest supplier.

*[GUARDIAN OATH — SR] “I trust no part I cannot trace.” (SR-11)*
**VEGA:** The Caravan-Master's oath. I trust no part I cannot trace.

*[HOW IT FITS: The Forge in the RMF]*
  • CM keeps IMPLEMENTATION honest and supports MONITORING
  • SA and SR push security upstream — into building and buying
  • In practice: secure SDLC, locked-down configs, vetted suppliers
**VEGA:** The best breach is the one designed out before it's built.

*[QUIZ] A counterfeit network card arrives pre-tampered. Which control should catch it?*
  A. CM-2 Baseline Configuration
  B. SR-11 Component Authenticity (answer)
  C. MA-2 Maintenance
**NOVA:** Scenario: a tampered part in the box. Whose job is that? Pause, and answer.

*[QUIZ] Disabling unused ports and services is which control?*
  A. CM-7 Least Functionality (answer)
  B. SA-22 Unsupported Components
  C. CM-8 Inventory
**VEGA:** And shutting the doors you never use?

*[NOTEBOOK: Episode 05 — the Forge]*
  • SA builds and buys security in (SA-3, SA-8, SA-22).
  • CM keeps a known config and controls every change (CM-2, CM-7, CM-8).
  • MA guards maintenance; SR guards the supply chain (MA-2, MA-4; SR-3, SR-11).
  remember: The best breach is the one designed out before it's built.
**NOVA:** Notebook: secure how you build, configure, maintain, and source — the attacker counts on you skipping one.
**VEGA:** The forge is hardened, from source to system.
**NULL:** Then I'll take your secrets in transit, or your backups.
**VEGA:** Then we ride for the Vaults and the Lifelines.


---

# The Vaults & Lifelines  (06)
*SC · MP · CP — Protect the data and survive disaster: communications protection, media protection, contingency planning.*

*[BREACH OF THE WEEK: 2017 — A wiper erases a global shipping line overnight.]*
  Self-spreading malware destroyed tens of thousands of machines at a major shipping company. It came back only because one backup happened to be offline and out of reach during the attack.
  MITRE ATT&CK: Data Destruction · T1485
**NULL:** Every gap, every shortcut, every forgotten door — I will find it. And if I can't get in, I'll burn it down.
**VEGA:** Not tonight. Seal the roads, guard the vaults, and prepare for the dark.
**NOVA:** Prepare for the worst, you mean.
**VEGA:** Always.

*[MAP: THE VAULTS]*
**NULL:** If I can't break the walls, I'll snatch your secrets in transit, or wait for the lights to go out.
**VEGA:** Then we seal the roads, guard the vaults, and prepare for the dark.

*[TITLE: 06 — THE VAULTS & LIFELINES — Communications · Media · Contingency]*
**VEGA:** Layer six protects the data itself, and keeps the city alive through disaster.
**NARRATOR:** Three families hold the line: System & Communications Protection, Media Protection, and Contingency Planning.

*[MAP: THE VAULTS & LIFELINES]*
**NOVA:** SC, MP, and CP. The warden of the roads, the steward of scrolls, and the keeper of lifelines.

*[GUARDIAN: SC System and Communications Protection — “The Warden of Walls and Roads”]*
  guards: Fortifies the ramparts and seals the roads between districts.
  in reality: Boundary protection and cryptography that protect data in transit and at rest.
**VEGA:** The Warden of Walls and Roads, System and Communications Protection.
**VEGA:** It fortifies the ramparts and seals the roads between districts.
**VEGA:** In reality, that's boundary protection and cryptography — guarding data as it moves and where it rests.

*[PLAIN ENGLISH: System boundary]*
  meaning: The line you draw around a system: everything inside is 'your system' — the part you own, authorize, and defend. Drawing it well is one of the most consequential decisions in 800-53.
  everyday example: Like the property line and fence around a building — it defines exactly what you're responsible for guarding.
**NOVA:** What is 'the edge of the system'?
**VEGA:** Draw a line around your computers, data, and the people who run them. Inside is your system. SC-7 watches that line.

*[CONTROL: SC-7 Boundary Protection]*
  what it means: Monitor and control traffic at the system's boundaries.
  why it matters: The boundary is where outside meets inside; SC-7 decides what may cross.
**VEGA:** SC-7, boundary protection, guards the edge of the system.

*[PLAIN ENGLISH: Encryption — in transit & at rest]*
  meaning: Math that scrambles data with a secret key, so anyone who intercepts it sees gibberish. 'In transit' is data moving across a network; 'at rest' is data sitting on a disk or in a database.
  everyday example: The padlock on a web address (HTTPS) is encryption in transit; a password-locked, encrypted laptop is encryption at rest.
**NOVA:** You keep saying cryptography — what does it actually do?
**VEGA:** It locks the data. Encrypt it in transit and at rest, and a thief without your key gets nothing.

*[CONTROL: SC-8 Transmission Confidentiality and Integrity]*
  what it means: Protect data in transit — its confidentiality and integrity.
  why it matters: On the wire, encryption is what stops eavesdropping and tampering.
**NULL:** I was listening on that line...
**VEGA:** Then you heard noise. SC-8 protects data in transit, often with approved cryptography.

*[CONTROL: SC-28 Protection of Information at Rest]*
  what it means: Protect data at rest — in storage.
  why it matters: Stored data outlives the session; SC-28 keeps it encrypted and safe.
**NOVA:** And the data just sitting in storage?
**VEGA:** SC-28 protects it at rest, often with cryptography from SC-12 and SC-13.

*[DIAGRAM: The boundary decides what crosses]*
  Untrusted network → Boundary protection (SC-7) → Your system
**VEGA:** Untrusted traffic meets the boundary, and only the allowed passes through.
**NOVA:** Filter at the edge, encrypt across the wire.

*[VERBATIM] “Monitor and control communications at the external managed interfaces to the system and at key internal managed interfaces within the system;” — NIST SP 800-53r5  ·  SC-7 Boundary Protection*
**ARCHIVIST:** Monitor and control communications at the external managed interfaces to the system and at key internal managed interfaces within the system;

*[CHEAT CARD: System and Communications Protection]*
  • SC-7 Boundary Protection — control traffic at the boundary
  • SC-8 Transmission Confidentiality and Integrity — protect data in transit (often encrypted)
  • SC-13 Cryptographic Protection — use approved cryptography
  • SC-28 Protection of Information at Rest — encrypt data at rest
  remember: “Guard the edge; encrypt everywhere.”
**VEGA:** Protect data moving and still.

*[GUARDIAN OATH — SC] “Filter at the edge; cipher on the wire.” (SC-7 · SC-8 · SC-28)*
**VEGA:** The Warden's oath. Filter at the edge; cipher on the wire.

*[GUARDIAN: MP Media Protection — “The Steward of Scrolls”]*
  guards: Guards every scroll, and destroys the ones discarded.
  in reality: Protecting digital and physical media, and sanitizing it before disposal or reuse.
**VEGA:** The Steward of Scrolls, Media Protection.
**NOVA:** It guards every scroll, and destroys the ones discarded.
**VEGA:** By 'media,' NIST means storage: hard drives, SSDs, tapes, USB sticks, even printed paper. MP protects them — and wipes them before they're thrown away.

*[CONTROL: MP-6 Media Sanitization]*
  what it means: Sanitize media before disposal or reuse — truly erase it.
  why it matters: A discarded drive can still spill its data; MP-6 makes erasure final.
**VEGA:** MP-6, media sanitization, ensures deleted really means gone.
**NULL:** Your old backup drive would have told me everything.

*[CONTROL: MP-7 Media Use]*
  what it means: Restrict the use of removable media like USB drives.
  why it matters: Removable media carries malware in and data out; MP-7 controls it.
**VEGA:** And MP-7 controls removable media, the humble USB stick.

*[PLAIN ENGLISH: Reading the [brackets]]*
  meaning: NIST writes controls as templates. Text in brackets like [Assignment: organization-defined frequency] is a blank YOU fill in — every 30 days, each quarter, whatever your risk calls for. The catalog gives the requirement; you set the value.
**VEGA:** One reading tip before the next gold card. Notice the brackets in the catalog's text.
**NOVA:** So the brackets are blanks the organization fills in?
**VEGA:** Exactly. The requirement is fixed; the value is yours.

*[VERBATIM] “Sanitize [organization-defined system media] prior to disposal, release out of organizational control, or release for reuse using [organization-defined sanitization techniques and procedures] ;” — NIST SP 800-53r5  ·  MP-6 Media Sanitization*
**ARCHIVIST:** Sanitize [organization-defined system media] prior to disposal, release out of organizational control, or release for reuse using [organization-defined sanitization techniques and procedures] ;

*[CHEAT CARD: Media Protection]*
  • MP-2 Media Access — restrict who can access media
  • MP-4 Media Storage — store media securely
  • MP-6 Media Sanitization — sanitize media before disposal
  • MP-7 Media Use — control removable media
  remember: “Guard the scroll; burn the discard.”
**VEGA:** Data outlives the device. Wipe it like you mean it.

*[GUARDIAN OATH — MP] “When it's gone, it's gone for good.” (MP-6)*
**VEGA:** The Steward's oath. When it's gone, it's gone for good.

*[GUARDIAN: CP Contingency Planning — “The Keeper of Lifelines”]*
  guards: Plans for the day the towers fall, and how to rebuild.
  in reality: Backups, alternate sites, and tested plans to recover operations after a disruption.
**VEGA:** The Keeper of Lifelines, Contingency Planning.
**VEGA:** It plans for the day the towers fall, and how to rebuild.
**VEGA:** In reality, that's backups, alternate sites, and tested plans to recover operations after a disruption.

*[CONTROL: CP-9 System Backup]*
  what it means: Back up your systems and data — and be able to restore.
  why it matters: When ransomware strikes, a clean, tested backup is the way home.
**NOVA:** What saves us from ransomware?
**VEGA:** CP-9, system backup, a clean copy you can actually restore.
**VEGA:** 'Clean' is the key word — a backup kept offline or unchangeable, where ransomware can't reach it. That's what saved the shipping line we opened with.

*[CONTROL: CP-2 Contingency Plan]*
  what it means: Write and maintain a contingency plan — and CP-4 tests it.
  why it matters: An untested plan is a guess; rehearsal turns disaster into routine.
**VEGA:** CP-2 is the plan; CP-4 is the drill that proves it works.

*[VERBATIM] “Conduct backups of user-level information contained in [system components] [frequency];” — NIST SP 800-53r5  ·  CP-9 System Backup*
**ARCHIVIST:** Conduct backups of user-level information contained in [system components] [frequency];

*[CHEAT CARD: Contingency Planning]*
  • CP-2 Contingency Plan — have a contingency plan
  • CP-4 Contingency Plan Testing — test the plan
  • CP-9 System Backup — back up systems and data
  • CP-10 System Recovery and Reconstitution — recover and reconstitute
  remember: “Back it up; rehearse the recovery.”
**VEGA:** Survival is planned in advance, never improvised.

*[GUARDIAN OATH — CP] “We rehearse the dark, so we survive it.” (CP-2 · CP-4 · CP-9)*
**VEGA:** The Keeper's oath. We rehearse the dark, so we survive it.

*[HOW IT FITS: The Vaults & Lifelines in the RMF]*
  • SC and MP carry out the PROTECT function for data
  • CP delivers RECOVER — resilience when prevention fails
  • In practice: encrypt in transit and at rest, wipe media, test backups
**VEGA:** Prevention buys time. Recovery buys survival.

*[QUIZ] Ransomware encrypts your servers. What gets you back fastest?*
  A. A clean, tested backup (CP-9) (answer)
  B. A firewall rule (SC-7)
  C. A privacy notice (PT-5)
**NOVA:** Scenario: ransomware hits. What brings you home? Pause, and answer.

*[QUIZ] A surplus hard drive is sold without being wiped. Which control failed?*
  A. SC-8 Transmission
  B. MP-6 Media Sanitization (answer)
  C. CP-2 Contingency Plan
**VEGA:** And the drive that left with its secrets intact?

*[NOTEBOOK: Episode 06 — the Vaults & Lifelines]*
  • SC draws the boundary and encrypts data in transit and at rest (SC-7, SC-8, SC-28).
  • MP protects storage media and truly wipes it before disposal (MP-2, MP-6, MP-7).
  • CP backs up (clean = offline/immutable) and rehearses recovery (CP-2, CP-4, CP-9).
  remember: Prevention buys time; recovery buys survival.
**NOVA:** Notebook: lock the data moving and still — and keep a backup the attacker can't touch.
**VEGA:** Data sealed, lifelines ready. The city can take a punch.
**NULL:** Then I'll bring everything, all at once. Siege night.
**VEGA:** We'll be ready. All twenty guardians, together.


---

# Siege Night  (07)
*All 20 + RMF — Act I finale: defense in depth, the full RMF at a glance, and how 800-53 gets used in practice.*

*[TITLE: FINALE — SIEGE NIGHT — Defense in Depth · The Full Picture]*
**NULL:** Every gap, every shortcut, every forgotten door — I will find it. Tonight, I bring everything. Every vector, every door, all at once.
**VEGA:** Not tonight. Tonight, every guardian answers. Welcome to Siege Night.

*[TITLE: 07 — SIEGE NIGHT — All twenty guardians · The Risk Management Framework]*
**VEGA:** One attacker, many weapons. One city, twenty guardians. This is defense in depth.

*[MAP: THE CITY STANDS AS ONE]*
**NARRATOR:** The Null strikes everywhere at once. Watch the city answer.

*[DEFENSE IN DEPTH: The assault — repelled, vector by vector]*
  • Phishing email → AT, the trained human spots it
  • Stolen credential → IA proves identity; AC-6 limits the reach
  • Tailgating the door → PE stops the walk-in
  • Malware on a host → SI detects and cleans it
  • Wiping the logs → AU-9 protects the record
**VEGA:** Each weapon meets a guardian. No single failure ends the city.
**NULL:** One of these should have worked...

*[DEFENSE IN DEPTH: ...and still it holds]*
  • Counterfeit part → SR checks authenticity
  • Eavesdropping the wire → SC encrypts it
  • The departing insider → PS revoked the keys
  • Ransomware detonates → CP restores from clean backup
  • Unpatched crack → RA found it, SI fixed it
**VEGA:** Layered defense means no single failure ends the fight. If one layer fails, others still prevent, detect, limit, or recover.
**NOVA:** Twenty guardians, one shield.

*[DIAGRAM: The Risk Management Framework, end to end]*
  Prepare → Categorize → Select → Implement → Assess → Authorize → Monitor
**VEGA:** Here is how it all comes together, the lifecycle from 800-37.
**VEGA:** Prepare, categorize, select, implement, assess, authorize, and monitor, forever.

*[IN PRACTICE: How to actually use 800-53]*
  • 1. Categorize the system — FIPS 199, with help from SP 800-60
  • 2. Select a baseline from SP 800-53B, then tailor it
  • 3. Implement the controls in the system
  • 4. Assess them — procedures in SP 800-53A
  • 5. Authorize to operate, then 6. Monitor continuously
**NOVA:** So in the real world, where do I start?
**VEGA:** Prepare, categorize the system, select and tailor a baseline, implement, assess, authorize, and never stop watching.

*[THE COMPANIONS: Your bookshelf]*
  • SP 800-53 — the control catalog (this series)
  • SP 800-53B — the control baselines
  • SP 800-53A — how to assess the controls
  • SP 800-37 — the Risk Management Framework
  • FIPS 199 / 200 — categorize and set minimum requirements
**VEGA:** These books travel together. Know which one answers which question.

*[THE ROLL CALL: Twenty guardians, one shield — their oaths]*
  • AC: None pass unknown; none hold more than they need.
  • AU: Every footstep written; no page erased.
  • RA: I do not guess the storm; I measure it.
  • SC: Filter at the edge; cipher on the wire.
  • CP: We rehearse the dark, so we survive it.
**VEGA:** Hear the oaths together, and the whole defense fits in your hand.
**NOVA:** Twenty guardians, one shield.

*[TITLE: GUARDIAN ROLL CALL — Five questions across the whole city]*
**NOVA:** Final test. Five questions, all twenty guardians. Ready?

*[QUIZ] Which guardian proves you are who you claim, before access?*
  A. AC — Access Control
  B. IA — Identification & Authentication (answer)
  C. AU — Audit
**NOVA:** One. Who checks your identity at the gate?

*[QUIZ] Where do the Low, Moderate, and High control baselines live?*
  A. SP 800-53
  B. SP 800-53B (answer)
  C. SP 800-53A
**NOVA:** Two. Where do the baselines live?

*[QUIZ] Ransomware hits and encrypts everything. What brings you back?*
  A. CP-9 System Backup (answer)
  B. AC-6 Least Privilege
  C. AT-2 Training
**NOVA:** Three. What saves you from ransomware?

*[QUIZ] Which document tells you HOW to assess whether controls work?*
  A. SP 800-53B
  B. SP 800-53A (answer)
  C. FIPS 199
**NOVA:** Four. Which book holds the assessment procedures?

*[QUIZ] A senior official accepts the risk and lets the system operate. Which control?*
  A. CA-6 Authorization (answer)
  B. PL-2 System Plan
  C. RA-3 Risk Assessment
**NOVA:** Five. Who signs to let the system go live?

*[THE SIEGE ENDS · THE CAMPAIGN BEGINS: The siege breaks — but the war isn't won]*
  • You met all 20 families across six layers of defense
  • You can read any control: ID, Control, Discussion, Related, Enhancements
  • But knowing the guardians isn't the same as standing up a system the right way
**VEGA:** You walked every wall, every tower, every vault. The siege broke on our walls, Nova.
**NULL:** ...but I left with the blueprints. I'll be back — and next time, it won't be one city.
**NOVA:** Then how do we prove a NEW citadel is safe before we trust it with the Crown Data?
**VEGA:** That, apprentice, is a campaign. And in Act Two, you're going to lead it.

*[TITLE: ACT II AWAITS — THE CAMPAIGN — Next: standing up a real system with the Risk Management Framework]*
**NARRATOR:** The guardians are known. Now you learn to deploy them — categorize, select, implement, assess, authorize, and watch. The campaign begins in Act Two.


---

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


---

# The Campaign: the RMF  (08)
*SP 800-37r2 — Act II begins. The 7-step Risk Management Framework and how the NIST document family fits together.*

*[TITLE: ACT II — THE CAMPAIGN — Standing up a system the right way · the RMF]*
**NARRATOR:** You have met the twenty guardians. But knowing them is not the same as deploying them.
**VEGA:** You just watched Aegis Hospital secured end to end. Now we slow down and learn each step — and Nova, you're leading it.
**NOVA:** From apprentice to running the campaign. Let's begin.

*[TITLE: 08 — THE RISK MANAGEMENT FRAMEWORK — NIST SP 800-37, Revision 2]*
**VEGA:** The plan of campaign has a name: the Risk Management Framework, from 800-37.
**NOVA:** The process that tells you what to do, and in what order.

*[PLAIN ENGLISH: Framework]*
  stands for: RMF = Risk Management Framework (NIST SP 800-37)
  meaning: A repeatable, step-by-step process for managing a system's security risk — from understanding the system, to choosing and proving controls, to approving operation and watching over time.
**NOVA:** What makes the RMF a 'framework' and not just a checklist?
**VEGA:** It's the living process that ties the catalog, the baselines, and the assessments into one repeatable lifecycle.

*[DIAGRAM: Seven steps, one lifecycle]*
  Prepare → Categorize → Select → Implement → Assess → Authorize → Monitor
**VEGA:** Seven steps. Prepare, categorize, select, implement, assess, authorize, and monitor.
**NOVA:** And it's a cycle, monitoring never stops.
**VEGA:** Prepare was added in Revision 2, getting the organization and system ready first.

*[800-37 · STEPS 1-5: What each step does]*
  • Prepare — set context, roles, and risk strategy
  • Categorize — size the system's impact (FIPS 199)
  • Select — choose a control baseline (800-53B) and tailor it
  • Implement — put the controls (800-53) to work
  • Assess — verify they work (800-53A)
**VEGA:** Each step has a job, and most are guided by a supporting NIST publication.

*[800-37 · STEPS 6-7: ...and the last two]*
  • Authorize — a senior official accepts the risk (the ATO)
  • Monitor — ongoing awareness throughout the system lifecycle (800-137)
  • Then the cycle begins again as the system changes
**VEGA:** Authorize, then monitor. A system is never simply 'done.'
**NULL:** Good. Because I never stop, either.

*[THE DOCUMENT FAMILY: Your campaign bookshelf]*
  • FIPS 199 / 800-60 — categorize the system
  • FIPS 200 — the minimum security requirements
  • SP 800-53B — the control baselines
  • SP 800-53 — the control catalog (Act I)
  • SP 800-53A — how to assess; SP 800-37 — the process
**VEGA:** These books travel together. Each answers one question in the campaign.
**NOVA:** So Act One taught the controls. Act Two is how we actually use them.

*[QUIZ] How many steps are in the RMF (SP 800-37 Rev 2)?*
  A. Five
  B. Six
  C. Seven (answer)
**NOVA:** Quick check. How many steps in the framework? Pause, and answer.

*[QUIZ] Which RMF step was newly added in Revision 2?*
  A. Prepare (answer)
  B. Authorize
  C. Monitor
**VEGA:** And which step did Revision 2 add at the front?

*[RECAP: Episode 08 — remember this]*
  • The RMF (800-37r2) has 7 steps: Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor
  • Each step has a companion NIST document
  • It's a continuous lifecycle, not a one-time checklist
**VEGA:** The map is set. First stop, knowing what we're protecting.
**VEGA:** Next: categorization.


---

# Know Your Realm  (09)
*FIPS 199/200 · 800-60 — Security categorization: rating Confidentiality/Integrity/Availability, the high-water mark, minimum requirements.*

*[TITLE: 09 — KNOW YOUR REALM — Security Categorization · FIPS 199]*
**VEGA:** Before you pick defenses, you must know what you're defending, and how much it matters.
**NARRATOR:** This is categorization, and it begins with a federal standard: FIPS 199.

*[PLAIN ENGLISH: FIPS · to categorize]*
  stands for: FIPS = Federal Information Processing Standards
  meaning: FIPS are mandatory U.S. federal standards. To 'categorize' a system is to rate how serious the harm would be — Low, Moderate, or High — if its confidentiality, integrity, or availability were lost.
**NOVA:** FIPS? Categorize?
**VEGA:** FIPS — Federal Information Processing Standards, the mandatory ones. Categorizing is sizing the stakes for C, I, and A — the triad from Episode zero.

*[DIAGRAM: Three security objectives]*
  Confidentiality → Integrity → Availability
**VEGA:** FIPS 199 judges a system on three objectives.
**NOVA:** Confidentiality, Integrity, and Availability. The C-I-A triad.

*[FIPS 199 · IMPACT: Rate each at Low, Moderate, or High]*
  • Confidentiality — harm if data is disclosed
  • Integrity — harm if data is altered or destroyed
  • Availability — harm if access is disrupted
  • Each gets an impact level: Low, Moderate, or High
**VEGA:** For each objective, ask: how bad is the worst-case impact?
**VEGA:** Low, Moderate, or High.

*[THE HIGH-WATER MARK: The high-water mark]*
  • The system's overall category = the HIGHEST of the three
  • Example: Confidentiality Moderate, Integrity Low, Availability Moderate
  • ...the system is categorized MODERATE
  • One High anywhere makes the whole system High
**NOVA:** So one High pulls the whole system up?
**VEGA:** Exactly. We call it the high-water mark. The worst case wins.

*[FIPS 200 · SP 800-60: Two more companions]*
  • SP 800-60 — maps your information TYPES to impact levels
  • FIPS 200 — the minimum security requirements for federal systems
  • FIPS 200 is what mandates using SP 800-53 in the first place
**VEGA:** 800-60 helps you rate each information type.
**VEGA:** And FIPS 200 sets the floor, and points you to 800-53.

*[CONTROL: RA-2 Security Categorization]*
  what it means: Categorize the system and its information, and document the results.
  why it matters: Categorization is itself a control, RA-2, the control behind the RMF Categorize step.
**VEGA:** And the catalog has a control for exactly this: RA-2.
**ARCHIVIST:** Categorize the system and information it processes, stores, and transmits;

*[QUIZ] A system is Confidentiality=Moderate, Integrity=Low, Availability=High. Its category is?*
  A. Low
  B. Moderate
  C. High (answer)
**NOVA:** Scenario time. What's the overall category? Pause, and answer.

*[QUIZ] Which standard defines the Low / Moderate / High impact levels?*
  A. FIPS 199 (answer)
  B. SP 800-53B
  C. SP 800-37
**VEGA:** And which standard sets the impact levels themselves?

*[RECAP: Episode 09 — remember this]*
  • FIPS 199 rates Confidentiality, Integrity, Availability as Low / Moderate / High
  • Overall category = the high-water mark (the highest of the three)
  • 800-60 maps information types; FIPS 200 sets the floor and points to 800-53; RA-2 documents it
**VEGA:** We know the realm's worth. Now we choose its defenses.
**VEGA:** Next: the armory, and the baselines of 800-53B.


---

# The Armory: Baselines  (10)
*SP 800-53B — Control baselines (Low 149 / Moderate 287 / High 370 / Privacy 96) and how to tailor them with overlays.*

*[TITLE: 10 — THE ARMORY — Control Baselines & Tailoring · NIST SP 800-53B]*
**VEGA:** You know the system's worth. Now draw your loadout from the armory.
**NARRATOR:** The baselines, and the tailoring guidance, live in SP 800-53B.

*[800-53B: What is a baseline?]*
  • A pre-defined STARTING set of controls for an impact level
  • Three security baselines: Low, Moderate, High
  • Plus a separate Privacy baseline for systems that process PII
  • Your FIPS 199 level picks the SECURITY baseline: a Moderate system → Moderate baseline
**NOVA:** So a baseline is a ready-made kit?
**VEGA:** A starting kit. Matched to how much the system matters.

*[PLAIN ENGLISH: Tailoring & overlays]*
  meaning: Tailoring is adjusting the baseline to fit your system — removing what doesn't apply, adding what's missing, setting parameters, and justifying each change. An overlay is ready-made tailoring for a whole community.
**NOVA:** Tailoring? Overlay?
**VEGA:** Tailoring fits the kit to you — like Aegis Hospital dropping wireless because that app is wired-only, and adding a healthcare overlay. An overlay is shared tailoring, so you don't start from scratch.

*[DIAGRAM: The three security baselines (controls + enhancements)]*
  LOW 149 controls → MODERATE 287 controls → HIGH 370 controls
**VEGA:** Low draws 149 items. Moderate, 287. High, 370.
**VEGA:** Higher impact, more controls and enhancements, by design.

*[TAILORING: Then you TAILOR it]*
  • Scoping — drop controls that don't apply to your system
  • Compensating controls — swap in an alternative that meets the intent
  • Parameters — fill in organization-defined values (frequencies, roles)
  • Supplementation — ADD controls for risks the baseline misses
**VEGA:** A baseline is a starting point, never the finish line. You tailor it to fit.
**NULL:** I look for the control you wrongly tailored away.

*[OVERLAYS: Overlays & a key nuance]*
  • Overlays — ready-made tailored baselines for a community (cloud, classified, mission-specific)
  • The Privacy baseline (96 controls) covers systems processing PII
  • Security baselines span 18 families — Program Management (PM) is org-wide, not in them
**VEGA:** Overlays are shared tailoring, so you don't start from scratch.
**NOVA:** And remember, PM controls run across the whole organization, outside any baseline.

*[QUIZ] Where do the Low / Moderate / High baselines live?*
  A. SP 800-53 (the catalog)
  B. SP 800-53B (answer)
  C. FIPS 199
**NOVA:** Quick check. Which book holds the baselines? Pause, and answer.

*[QUIZ] Adjusting a baseline — scoping out, swapping, adding controls — is called?*
  A. Categorization
  B. Tailoring (answer)
  C. Authorization
**VEGA:** And the act of adjusting the baseline to fit your system?

*[RECAP: Episode 10 — remember this]*
  • Baselines (800-53B): Low 149, Moderate 287, High 370, Privacy 96
  • Your FIPS 199 category selects the baseline
  • Then TAILOR: scope, compensate, set parameters, supplement, apply overlays
**VEGA:** Defenses chosen and fitted. Now, do they actually work?
**VEGA:** Next: the reckoning, assessment and authorization.


---

# The Reckoning  (11)
*800-53A · 800-137 — Assessment methods (examine/interview/test), the SAR and POA&M, authorization (ATO), continuous monitoring.*

*[TITLE: 11 — THE RECKONING — Assess · Authorize · Monitor]*
**VEGA:** The walls are built. But a defense you haven't tested is only a hope.
**NARRATOR:** Now: assessment, authorization, and the watch that never ends.

*[DIAGRAM: How assessors check a control (SP 800-53A)]*
  Examine → Interview → Test
**VEGA:** 800-53A gives assessors three methods.
**NOVA:** Examine the evidence, interview the people, and test the system itself.

*[800-53A · SAR · POA&M: From assessment to decision]*
  • Assessors produce a Security Assessment Report (the SAR)
  • Open weaknesses go on a POA&M — a Plan of Action & Milestones (CA-5)
  • The POA&M tracks each gap until it's fixed
**VEGA:** The findings become a report, and every gap gets a plan to close it.

*[THE ARTIFACT CHAIN: The paperwork trail — and why it matters]*
  • Assess → the Security Assessment Report (SAR): what works, what doesn't
  • Open gaps → the POA&M: each weakness with an owner and a due date
  • SAR + plan + evidence → the authorization package the AO reviews
  • AO accepts the residual risk → the ATO: the system may operate
**VEGA:** Every step leaves a document. Together, they let a leader make an honest call.
**NOVA:** Assess, report, plan, package, authorize.

*[CONTROL: CA-2 Control Assessments]*
  what it means: Assess whether controls are implemented correctly, operate as intended, and produce the desired outcome.
  why it matters: CA-2 calls for the assessment (independent where required); 800-53A is the how-to.
**VEGA:** The catalog control behind all this is CA-2.
**ARCHIVIST:** Select the appropriate assessor or assessment team for the type of assessment to be conducted;

*[800-37 · AUTHORIZE: Authorization — the ATO]*
  • A senior leader, the authorizing official, reviews the residual risk
  • If acceptable, they grant an Authorization to Operate — the ATO (CA-6)
  • It is a documented acceptance of risk, not a guarantee of safety
**NOVA:** So someone has to own the risk and sign for it?
**VEGA:** Yes. The authorizing official grants the ATO, and owns that decision.
**NULL:** A signature... still won't stop me.

*[CONTROL: CA-7 Continuous Monitoring]*
  what it means: Keep assessing and watching the system continuously, not just once.
  why it matters: Authorization is a point-in-time risk decision; monitoring runs across the system's life to keep risk in view.
**VEGA:** Which is why the final step never ends: CA-7, continuous monitoring.
**VEGA:** SP 800-137 is the playbook for that ongoing watch.

*[QUIZ] What are the three assessment methods in SP 800-53A?*
  A. Scan, Patch, Report
  B. Examine, Interview, Test (answer)
  C. Plan, Do, Check
**NOVA:** Final stretch. Name the three assessment methods. Pause, and answer.

*[QUIZ] A senior official accepts the residual risk and lets the system run. That decision is the?*
  A. POA&M
  B. ATO (Authorization to Operate) (answer)
  C. SAR
**VEGA:** And the decision that lets the system go live?

*[QUIZ] Where are open weaknesses tracked until they're remediated?*
  A. In the SAR
  B. In a POA&M (answer)
  C. In FIPS 199
**VEGA:** And where do we track the gaps we haven't closed?

*[THE WHOLE PICTURE: The campaign, complete]*
  • Prepare → Categorize → Select → Implement → Assess → Authorize → Monitor
  • FIPS 199 + 800-60 categorize it; FIPS 200 sets the floor; 800-53B picks the baseline; 800-53 supplies the controls
  • 800-53A assesses; 800-37 runs the process; 800-137 keeps the watch
**VEGA:** Categorize, select, implement, assess, authorize, monitor. You've walked the whole campaign.
**NOVA:** From a single control... to a system that's authorized and watched for life.

*[TITLE: THE CITADEL ENDURES — CYBER CITADEL — An educational aid — always consult the NIST publications]*
**NOVA:** In Episode zero, I didn't even know what eight-hundred fifty-three was. Tonight, I'm signing for it.
**VEGA:** Then sign, Castellan — and keep the watch.
**NULL:** ...until next time.
**NOVA:** There's always a next time. That's the job. CA-7 — the watch never ends.
**NARRATOR:** Episode zero promised: protect it, and you thrive. You protected it. Now you never stop. The story was ours; the controls are real.


---


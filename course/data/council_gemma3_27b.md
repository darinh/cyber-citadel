## COUNCIL REVIEW - CYBER CITADEL: The 20 Guardians

**1) VERDICT:** APPROVE-WITH-CHANGES

**2) Top 5 Highest-Signal Improvements:**

*   **RMF Integration – Beyond the Finale:** The RMF lifecycle appearance in the finale is insufficient. *Each* family episode needs a brief (30-60 second) segment demonstrating *how* implementing controls from that family directly supports a specific RMF phase. Don't just *show* the lifecycle, *apply* it. This is the core of 800-53 usability.
*   **Control Selection Logic – Show the "Why":**  You're showcasing 3-5 flagship controls per family. Excellent. But *explicitly* explain the rationale for *those* controls being highlighted. What common scenarios drive their selection? What are the typical organizational impacts of implementing (or *not* implementing) them?  Don't just present the control; present the *decision-making process*.
*   **"The Null" – Threat Modeling Depth:** The Null as a generalized adversary is weak.  Instead of just *showing* an attack, tie each "Breach of the Week" to a specific threat actor profile (APT29, ransomware group, disgruntled insider) and a corresponding MITRE ATT&CK technique. This adds realism and ties the controls to tangible threats.
*   **Enhancements – Don't Ignore Them:** You mention enhancements, but the proposal is silent on *showing* them.  Enhancements are crucial for tailoring 800-53 to specific organizational needs. Include a brief segment in each episode demonstrating how a relevant enhancement modifies a base control.
*   **Baselines – Explicitly Address 800-53B's Impact:** While you mention 800-53B, the proposal doesn't demonstrate how the baselines affect control selection.  A dedicated segment in EP00 and recurring references in family episodes are needed to clarify how organizations use baselines to tailor the catalog.

**3) Single Biggest Risk + Mitigation:**

**Risk:** **Superficial Coverage & "Check-Box" Learning.** The gamified approach, while potentially engaging, risks becoming a memorization exercise *without* fostering genuine understanding of control implementation and the underlying security principles. Learners may be able to recite the "20 Guardians" but fail to apply 800-53 effectively in real-world scenarios.

**Mitigation:**  Prioritize practical application over pure memorization.  The RMF integration (point #1 above) is critical. Add "Implementation Challenges" segments to each episode, discussing common pitfalls and best practices for deploying the featured controls.



**4) Answers to Open Questions:**

1.  **Scope/Feasibility:**  Approve the phased approach. Templated pipeline + pilot episodes are essential to validate the concept and refine the production process.
2.  **Framing:** The Citadel framing is acceptable, but leans heavily on spatial memory. Ensure the city map is consistently used and visually reinforces the control families. A heist serial *could* be more engaging, but risks trivializing the serious nature of cybersecurity.
3.  **Accuracy Guardrails:**  The Archivist + on-screen IDs are a *minimum* requirement, not a sufficient condition.  Independent SME review of *every* script is mandatory.
4.  **TTS:** Staying fully local with Piper is acceptable *if* audio quality is prioritized. Poor audio will undermine the entire series. Rigorous testing is needed.
5.  **Biggest Risks:** Technical debt from fully local production. Ensure robust version control and backup procedures.



**5) NIST 800-53r5 Accuracy Pitfalls to Avoid:**

*   **Confusing Controls with Control Baselines:**  Learners frequently conflate the controls themselves with the baseline implementations. Emphasize that baselines are *starting points* for tailoring, not the definitive implementation.
*   **Ignoring the "Discussion" Section:** The "Discussion" section of each control provides critical context and guidance. Don't treat it as optional reading; integrate key points into the narration.
*   **Treating Enhancements as Afterthoughts:** Enhancements aren't just "nice-to-haves." They are essential for addressing specific organizational risks and compliance requirements.
*   **Overlooking Privacy Controls:**  800-53 Rev 5 integrates privacy controls throughout the catalog. Ensure these controls receive adequate coverage and are not treated as separate from security controls.
*   **Static View of Controls:** Emphasize that 800-53 is a living document. Controls are updated and revised over time. Learners should understand the importance of staying current with the latest revisions.



I expect to see a revised plan addressing these points before production begins. Don't aim for "fun" at the expense of accuracy and practical applicability. The goal is to create a genuinely useful training resource, not a flashy but ultimately ineffective video series.
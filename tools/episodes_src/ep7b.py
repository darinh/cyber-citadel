"""EP07B - The Campaign Briefing: one real system through the whole RMF.

The multi-LLM beginner review's #1 fix: a single concrete worked example. We
follow a fictional "Aegis Regional Hospital" patient-records system through every
RMF step, with a named human cast, so the abstract process in EP08-11 has a story
to hang on. All control IDs are real; baseline counts come from SP 800-53B.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

CATEGORIZE = [{"label": "Confidentiality\nMODERATE", "x": 150, "y": 470, "w": 460, "h": 160, "color": "gold"},
              {"label": "Integrity\nHIGH", "x": 730, "y": 470, "w": 460, "h": 160, "color": "red"},
              {"label": "Availability\nHIGH", "x": 1310, "y": 470, "w": 460, "h": 160, "color": "red"}]

beats = [
    L.b_title("ACT II \u00b7 BRIEFING", "THE CAMPAIGN BRIEFING",
              "One real system, end to end \u00b7 Aegis Regional Hospital",
              [["VEGA", "Before we study the campaign step by step, let's watch a real one unfold \u2014 start to finish."],
               ["NOVA", "A real system? Not the metaphor?"],
               ["VEGA", "A real system. And this time, apprentice, you're running it."]]),

    L.b_points("Meet the team",
               ["Maya \u2014 System Owner: accountable for the system day to day",
                "The CIO \u2014 Authorizing Official (AO): signs to accept the risk",
                "Raj \u2014 ISSO: the hands-on security officer for this system",
                "Sam \u2014 Privacy Officer: guards the patients' personal data",
                "Stellaris Audit Co. \u2014 the independent Assessor"],
               [["VEGA", "Security isn't done by one hero. It's a team: Maya owns the system day to day; the CIO is the authorizing official who signs for the risk; Raj is the hands-on security officer; Sam guards the patients' privacy; and an outside firm, Stellaris, assesses the work."],
                ["NOVA", "So 'doing 800-53' is really a group of people, each with a named role and hat."]],
               kicker="THE CAST \u00b7 REAL ROLES"),

    L.b_define("Information system (made concrete)",
               "Aegis Regional Hospital runs a Patient Records System: a web app plus a database, used by about 800 clinicians, hosted on-premises, holding patients' medical records.",
               [["VEGA", "Here's our system. Not 'a computer' \u2014 an app, a database, the staff who use it, and the data they protect."],
                ["NOVA", "And those records are PII \u2014 personal, and protected by law."]],
               example="Web app + database + 800 users + sensitive health records = one information system to authorize.",
               kicker="THE SYSTEM \u00b7 AEGIS HOSPITAL"),

    L.b_diagram("Step 1\u20132: Prepare, then Categorize the impact", CATEGORIZE, [],
                [["VEGA", "First, prepare \u2014 set roles and context. Then categorize: how bad is the worst case for C, I, and A?"],
                 ["VEGA", "Confidentiality, Moderate. But Integrity is High \u2014 a wrong dose could kill. Availability is High \u2014 downtime closes the ER."],
                 ["NOVA", "And the high-water mark takes the worst of the three..."],
                 ["VEGA", "So the whole system is categorized HIGH. One High pulls it all up."]]),

    L.b_points("Step 3: Select the starting controls",
               ["The HIGH security baseline from SP 800-53B \u2014 370 controls and enhancements",
                "PLUS the Privacy baseline (96) \u2014 because the system processes PII",
                "This is the starting kit, not the finished list"],
               [["VEGA", "Maya opens 800-53B and draws the HIGH baseline \u2014 and the privacy baseline, because of those patient records."],
                ["NOVA", "A starting kit, sized to the stakes."]],
               kicker="SELECT \u00b7 SP 800-53B"),

    L.b_define("Common control (inheritance)",
               "A control someone else provides for you, so you don't build it yourself. You 'inherit' it. Controls can be common (provided), system-specific (yours alone), or hybrid (shared).",
               [["NOVA", "Does Maya's team really configure every one of 370 controls?"],
                ["VEGA", "No. The data center already provides physical security, PE-3, for every tenant. Maya inherits it \u2014 that's a common control."]],
               example="PE-3 (physical access) is common (the data center). AC-6 (least privilege) is system-specific. CP-2 (contingency plan) is often hybrid.",
               kicker="REAL-WORLD NUANCE"),

    L.b_points("Step 4: Tailor the baseline to fit",
               ["Scope out only what truly doesn't apply: this app is wired-only, so AC-18 (Wireless Access) is out of its boundary",
                "Inherit PE-3 (physical access) from the data center \u2014 a common control",
                "Add controls from a healthcare (HIPAA) overlay",
                "Set parameters: AC-2 disables inactive accounts after 60 days"],
               [["VEGA", "Tailoring is fitting the kit to the system \u2014 not an excuse to delete protections."],
                ["NULL", "I look for the one control you wrongly tailored away."],
                ["VEGA", "Which is why every change is justified and written down \u2014 we drop wireless only because this system has none."]],
               kicker="TAILOR \u00b7 NOT DELETE"),

    L.b_points("Step 5: Implement the controls",
               ["IA-2: multi-factor login for all 800 clinicians",
                "SC-28: encrypt the patient database at rest",
                "SI-2: patch servers on a set schedule",
                "CP-9: a nightly backup kept offline, where ransomware can't reach it"],
               [["VEGA", "Now Raj's team puts the controls to work. The catalog says WHAT; they choose HOW."],
                ["NOVA", "Same requirement, many possible tools."]],
               kicker="IMPLEMENT \u00b7 SP 800-53"),

    L.b_points("Step 6: Assess \u2014 do they actually work?",
               ["Stellaris (independent) EXAMINES the security plan",
                "INTERVIEWS Raj and the admins",
                "TESTS the system: a vulnerability scan and a phishing simulation",
                "The findings become a Security Assessment Report \u2014 the SAR"],
               [["VEGA", "An outside assessor checks the work three ways: examine, interview, test."],
                ["NOVA", "Selecting a control isn't proof it works. Assessment is."]],
               kicker="ASSESS \u00b7 SP 800-53A"),

    L.b_define("Residual risk",
               "The risk that's left after your controls are in place. It never reaches zero \u2014 so a senior leader has to look at what remains and decide if it's acceptable.",
               [["NOVA", "What about the weaknesses the assessor found?"],
                ["VEGA", "The risk that remains \u2014 residual risk. The CIO weighs it before anyone goes live."]],
               kicker="THE WORD BEHIND AUTHORIZATION"),

    L.b_points("Step 7\u20138: Authorize, then Monitor forever",
               ["The CIO reviews the SAR, accepts the residual risk, signs a 3-year ATO",
                "12 open findings go on a POA&M \u2014 each with an owner and a due date",
                "Monitor: quarterly scans, annual reviews, re-authorize after the big upgrade",
                "A system is never simply 'done'"],
               [["VEGA", "The CIO signs the authorization to operate. Then the watch begins \u2014 and never ends."],
                ["NULL", "Good. Because neither do I."]],
               kicker="AUTHORIZE \u00b7 MONITOR"),

    L.b_notebook("The campaign, in one breath",
                 ["Categorize the system (HIGH) \u2192 select a baseline (800-53B) \u2192 tailor it to fit.",
                  "Implement the controls \u2192 assess them (examine/interview/test \u2192 SAR).",
                  "Authorize (the ATO, accepting residual risk; gaps \u2192 POA&M) \u2192 monitor forever."],
                 "One system, one team, seven steps \u2014 that's the RMF.",
                 [["NOVA", "I just watched a whole system get secured, start to finish."],
                  ["VEGA", "You did. Now we'll slow down and learn each step in depth \u2014 starting with the framework itself."]]),
]

if __name__ == "__main__":
    L.write_spec("EP7B", "the_campaign_briefing", beats, tag="WORKED EXAMPLE")

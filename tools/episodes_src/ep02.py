"""EP02 - The Watchtowers (AU, SI, IR): detect, keep integrity, respond."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

IR_LIFECYCLE = ([{"label": "Preparation", "x": 70, "y": 470, "w": 300, "h": 150, "color": "cyan"},
                 {"label": "Detection & Analysis", "x": 440, "y": 470, "w": 300, "h": 150, "color": "gold"},
                 {"label": "Containment", "x": 810, "y": 470, "w": 300, "h": 150, "color": "mint"},
                 {"label": "Eradication", "x": 1180, "y": 470, "w": 300, "h": 150, "color": "mint"},
                 {"label": "Recovery", "x": 1550, "y": 470, "w": 300, "h": 150, "color": "cyan"}],
                [[0, 1], [1, 2], [2, 3], [3, 4]])

beats = [
    L.b_coldopen("EP02",
                 [["NULL", "Every gap, every shortcut, every forgotten door \u2014 I will find it."],
                  ["VEGA", "Not tonight. Even if you slip in, you will not move unseen."],
                  ["NOVA", "Because someone's watching?"],
                  ["VEGA", "Because the watchtowers never sleep."]]),

    L.b_map("INSIDE THE WALLS", [],
            [["NULL", "I slipped a careless credential past your wall. Now I move in the shadows."],
             ["VEGA", "Shadows don't last here. The watchtowers never sleep."]]),

    L.b_section("02", "THE WATCHTOWERS", "Audit \u00b7 Integrity \u00b7 Incident Response",
                [["VEGA", "Layer two assumes someone got in. Now we see them, stop the rot, and respond."],
                 ["NARRATOR", "Three families keep watch: Audit, System Integrity, and Incident Response."]]),

    L.b_map("THE WATCHTOWERS", ["AU", "SI", "IR"],
            [["NOVA", "AU, SI, and IR. The eyes, the immune system, and the firefighters."]],
            deps=[["AU", "AC"], ["SI", "IR"]]),

    # --- AU ---
    L.b_guardian("AU",
                 [["VEGA", "The Chronicler, Audit and Accountability."],
                  ["VEGA", "It records every footstep, so no deed goes unseen."],
                  ["VEGA", "In reality, that's logging security-relevant events so you can review them and hold people accountable."]]),

    L.b_define("Audit log",
               "A timestamped record of what happened on a system \u2014 who signed in, what they touched, what changed. It is the evidence you read after something goes wrong.",
               [["NOVA", "What exactly is a 'log'?"],
                ["VEGA", "A diary the system keeps. A Windows Event Log, a syslog, a tool like Splunk \u2014 same idea."]],
               example="Like a building's sign-in sheet and camera timeline, but for a computer system."),

    L.b_control("AU-2", "Decide which events the system logs to support the audit function.",
                "You can't review what you never recorded; logging is where accountability begins.",
                [["VEGA", "AU-2 chooses what's worth logging."],
                 ["NULL", "So I'll just delete the logs when I'm done."]]),

    L.b_control("AU-9", "Protect audit information and logging tools from unauthorized change or deletion.",
                "This is what stops an intruder from erasing their own tracks.",
                [["VEGA", "Not so fast. AU-9 protects the logs themselves."],
                 ["NOVA", "So the Null can't quietly rewrite history."]]),

    L.b_quote("AU-2",
              [["ARCHIVIST", L.verbatim("AU-2")]]),

    L.b_cheatcard("AU",
                  [L.cheat_bullet("AU-2", "decide what events to log"),
                   L.cheat_bullet("AU-3", "capture enough detail in each record"),
                   L.cheat_bullet("AU-6", "review and analyze the logs"),
                   L.cheat_bullet("AU-9", "protect the logs from tampering")],
                  "\u201CLog it, protect it, read it.\u201D",
                  [["VEGA", "A log no one reads, or one that can be erased, is no log at all."]]),

    L.b_oath("AU", [["VEGA", "The Chronicler's oath. Every footstep written; no page erased."]]),

    # --- SI ---
    L.b_guardian("SI",
                 [["VEGA", "The Healer, System and Information Integrity."],
                  ["NOVA", "It finds the rot, cures the sickness, and keeps the truth true."],
                  ["VEGA", "In reality, that's patching flaws, blocking malicious code, monitoring for intrusions, and verifying nothing was tampered with."]]),

    L.b_control("SI-2", "Find, report, and fix system flaws \u2014 and patch them in good time.",
                "Unpatched flaws are the cracks attackers pour through; SI-2 seals them.",
                [["VEGA", "SI-2 is flaw remediation, the discipline of patching."]]),

    L.b_control("SI-4", "Monitor the system to detect attacks, intrusions, and unusual activity.",
                "It's the tower's spyglass, watching traffic and behavior for trouble.",
                [["VEGA", "And SI-4 watches the system for signs of an intruder."],
                 ["NULL", "Every move I make... another tower turns my way."]]),

    L.b_map("THE WATCH CATCHES A SHADOW", ["AU", "SI", "IR"],
            [["NULL", "Six days I moved in your shadows before a single tower turned."],
             ["NOVA", "Six days?!"],
             ["VEGA", "Six days \u2014 but SI-4 saw the anomaly, and AU-9 kept the logs he tripped. He got in. He did not get out clean."],
             ["NULL", "...this time."]]),

    L.b_quote("SI-2",
              [["ARCHIVIST", L.verbatim("SI-2")]]),

    L.b_cheatcard("SI",
                  [L.cheat_bullet("SI-2", "patch flaws promptly"),
                   L.cheat_bullet("SI-3", "stop malicious code"),
                   L.cheat_bullet("SI-4", "monitor for intrusions"),
                   L.cheat_bullet("SI-7", "verify software and data integrity")],
                  "\u201CPatch, detect, verify.\u201D",
                  [["VEGA", "Integrity is keeping the system clean and honest."]]),

    L.b_oath("SI", [["VEGA", "The Healer's oath. Find the rot, close the wound, keep it true."]]),

    # --- IR ---
    L.b_guardian("IR",
                 [["VEGA", "The Firewatch, Incident Response."],
                  ["VEGA", "When something burns, it sounds the alarm and contains the blaze."],
                  ["VEGA", "In reality, that's detecting, reporting, analyzing, containing, and recovering from security incidents."]]),

    L.b_define("Security incident",
               "An event that actually harms a system or its data, or breaks the rules meant to protect them \u2014 a real breach, not just a warning light.",
               [["NOVA", "When does a threat become an 'incident'?"],
                ["VEGA", "The moment it stops being hypothetical \u2014 malware runs, data leaks, a system goes down."]],
               example="A ransomware infection, a stolen laptop full of patient data, or a hijacked account."),

    L.b_control("IR-4", "Run a capability to detect, contain, eradicate, and recover from incidents.",
                "A breach is a question of when; IR-4 is having the answer rehearsed.",
                [["NOVA", "What happens the moment we spot the Null?"],
                 ["VEGA", "IR-4 takes over, handling the incident end to end."]]),

    L.b_diagram("The incident response lifecycle", IR_LIFECYCLE[0], IR_LIFECYCLE[1],
                [["VEGA", "Every incident follows a rhythm: prepare, detect, contain, eradicate, recover."],
                 ["NOVA", "And IR-8 writes the plan that makes it routine."]]),

    L.b_quote("IR-4",
              [["ARCHIVIST", L.verbatim("IR-4")]]),

    L.b_cheatcard("IR",
                  [L.cheat_bullet("IR-2", "train people for their incident roles"),
                   L.cheat_bullet("IR-4", "handle incidents end to end"),
                   L.cheat_bullet("IR-6", "report incidents to the right people"),
                   L.cheat_bullet("IR-8", "write and maintain the response plan")],
                  "\u201CPlan, detect, contain, recover.\u201D",
                  [["VEGA", "The best responders practiced before the fire."]]),

    L.b_oath("IR", [["VEGA", "The Firewatch's oath. When it burns, we are already running."]]),

    L.b_points("The Watchtowers in the RMF",
               ["AU, SI, and IR power the MONITOR step \u2014 continuous vigilance",
                "They embody the Detect and Respond security functions",
                "Protect your logs (AU-9) or the whole watch can be blinded"],
               [["VEGA", "Selecting and implementing was the wall. Watching is how you keep it."]],
               kicker="HOW IT FITS"),

    L.b_quiz("An intruder tries to delete the logs to hide. Which control blocks that?",
             ["AU-2 Event Logging", "AU-9 Protection of Audit Information", "SI-4 System Monitoring"], 1,
             [["NOVA", "Scenario: the Null deletes logs. What stops it? Pause, and answer."]]),

    L.b_quiz("Which family detects, contains, and recovers from a breach?",
             ["IR \u2014 Incident Response", "AU \u2014 Audit", "AC \u2014 Access Control"], 0,
             [["VEGA", "And who runs toward the fire?"]]),

    L.b_notebook("Episode 02 \u2014 the Watchtowers",
                 ["AU sees and remembers \u2014 and protects its own records (AU-2, AU-6, AU-9).",
                  "SI keeps the system clean and honest: patch, detect, verify (SI-2, SI-4, SI-7).",
                  "IR turns a crisis into a rehearsed routine (IR-4, IR-6, IR-8)."],
                 "Log it, protect it, read it \u2014 then run toward the fire.",
                 [["NOVA", "Notebook: assume they got in, then see them, heal the system, and answer fast."],
                  ["VEGA", "Seen, healed, and answered. The towers hold."],
                  ["NULL", "Then I'll turn your own people against you."],
                  ["VEGA", "Then we ride to the Keepers of the Pact."]]),
]

if __name__ == "__main__":
    L.write_spec("EP02", "the_watchtowers", beats, tag="EP02")

"""EP01 - The Outer Walls (AC, IA, PE). Template for family-layer episodes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

ACCESS_DIAGRAM = ([{"label": "User / Process", "x": 170, "y": 470, "w": 360, "h": 130, "color": "cyan"},
                   {"label": "Policy Decision", "x": 790, "y": 470, "w": 360, "h": 130, "color": "gold"},
                   {"label": "Enforcement Gate", "x": 1410, "y": 470, "w": 360, "h": 130, "color": "mint"}],
                  [[0, 1, "request"], [1, 2, "allow / deny"]])

beats = [
    # --- cold open: a real breach + the recurring ritual ---
    L.b_coldopen("EP01",
                 [["NULL", "Every gap, every shortcut, every forgotten door \u2014 I will find it."],
                  ["VEGA", "Not tonight. One stolen login should never be enough to end a city."],
                  ["NOVA", "So where do we begin?"],
                  ["VEGA", "Where every attacker does \u2014 at the wall."]]),

    L.b_map("AEGIS CITADEL \u2014 NIGHTFALL", [],
            [["NULL", "Every fortress has a door. I only need one careless soul to leave one open."],
             ["VEGA", "Then meet the three guardians of the gate. I'm Vega. This is the apprentice, Nova."],
             ["NOVA", "Let's walk the walls."]]),

    L.b_section("01", "THE OUTER WALLS", "Access Control \u00b7 Identity \u00b7 Physical",
                [["VEGA", "Layer one is the perimeter, who gets in, and what they may touch."],
                 ["NARRATOR", "Three families stand the wall: Access Control, Identification, and Physical."]]),

    L.b_map("THE OUTER WALLS", ["AC", "IA", "PE"],
            [["VEGA", "Three districts light up the map: AC, IA, and PE."],
             ["NOVA", "The gatekeepers of the city."]],
            deps=[["AC", "IA"], ["AC", "AU"]]),

    # --- AC ---
    L.b_guardian("AC",
                 [["VEGA", "First, the Gatekeeper, Access Control."],
                  ["VEGA", "It decides who may enter, and exactly what they may touch."],
                  ["VEGA", "In the real world, that's the policies and mechanisms deciding which users and processes may use which systems and data."]]),

    L.b_control("AC-2", "Create, manage, review, and remove accounts across their whole lifecycle.",
                "Stale or rogue accounts are a favorite way in; managing them closes that door.",
                [["NOVA", "Where does access begin?"],
                 ["VEGA", "With accounts. AC-2 governs every account from birth to deletion."]]),

    L.b_control("AC-6", "Give every user and process only the access they truly need \u2014 nothing more.",
                "If an account is stolen, least privilege limits how far the intruder can reach.",
                [["VEGA", "Then the rule that saves you again and again, AC-6, Least Privilege."],
                 ["NULL", "Less for them to give me when I take an account..."]]),

    L.b_quote("AC-6",
              [["ARCHIVIST", L.verbatim("AC-6")]]),

    L.b_diagram("How the gate decides", ACCESS_DIAGRAM[0], ACCESS_DIAGRAM[1],
                [["VEGA", "Every request runs the same path: a policy decides, and a gate enforces it."],
                 ["VEGA", "Say Alice works in payroll. Policy lets her open payroll records; the same gate blocks Bob from marketing."],
                 ["NOVA", "Decide, then enforce. AC-3 is the enforcement."]]),

    L.b_cheatcard("AC",
                  [L.cheat_bullet("AC-2", "manage the full account lifecycle"),
                   L.cheat_bullet("AC-3", "enforce approved authorizations"),
                   L.cheat_bullet("AC-6", "grant only the minimum access needed")],
                  "\u201CRight person, right door, right reason.\u201D",
                  [["VEGA", "Lock these three into memory."]]),

    L.b_oath("AC", [["VEGA", "Say the Gatekeeper's oath with me. None pass unknown; none hold more than they need."]]),

    # --- IA ---
    L.b_guardian("IA",
                 [["VEGA", "Next, the Seal-Bearer, Identification and Authentication."],
                  ["NOVA", "Access Control trusts a name. This guardian proves the name is real."]]),

    L.b_control("IA-2", "Uniquely identify and authenticate organizational users before granting access.",
                "It's the difference between 'someone' and a known, accountable person.",
                [["VEGA", "IA-2 demands proof of identity for every organizational user."],
                 ["VEGA", "Its enhancements are where multi-factor authentication lives."]]),

    L.b_define("Multi-factor authentication (MFA)",
               "Proving who you are with two or more different kinds of evidence \u2014 so one stolen password isn't enough to get in.",
               [["NOVA", "Multi-factor authentication \u2014 what is that, exactly?"],
                ["VEGA", "Two kinds of proof instead of one. It's why the pipeline breach we opened with would have failed."]],
               expand="Something you know + something you have + something you are",
               example="A password (know) plus a one-time code from your phone (have) \u2014 or a fingerprint (are)."),

    L.b_control("IA-5", "Manage authenticators \u2014 passwords, tokens, certificates \u2014 across their lifecycle.",
                "Weak or leaked credentials are a top breach vector; this control hardens them.",
                [["NOVA", "And the passwords and tokens themselves?"],
                 ["VEGA", "IA-5 manages them, strength, rotation, protection."]]),

    L.b_quote("IA-2",
              [["ARCHIVIST", L.verbatim("IA-2")]]),

    L.b_cheatcard("IA",
                  [L.cheat_bullet("IA-2", "prove who organizational users are (MFA via enhancements)"),
                   L.cheat_bullet("IA-5", "manage passwords, tokens, and certificates"),
                   L.cheat_bullet("IA-8", "authenticate non-organizational users too")],
                  "\u201CProve it, before you move it.\u201D",
                  [["VEGA", "Identity first. Always."]]),

    L.b_oath("IA", [["VEGA", "The Seal-Bearer's oath. Prove the name, or the gate stays shut."]]),

    # --- PE ---
    L.b_guardian("PE",
                 [["VEGA", "Last on the wall, the Wall-Warden, Physical and Environmental Protection."],
                  ["NULL", "Why pick a lock... when I can walk through an open door?"],
                  ["VEGA", "In reality, PE is physical access control \u2014 guards, badges, locks \u2014 plus protection from hazards like fire, power loss, and water."]]),

    L.b_control("PE-3", "Enforce who may physically enter \u2014 with guards, badges, locks, and logs.",
                "Code can't stop a person who strolls into the server room; PE can.",
                [["VEGA", "PE-3 enforces physical access at the doors themselves."],
                 ["NOVA", "Tailgating, propped doors, lost badges, this is where you stop them."]]),

    L.b_control("PE-6", "Monitor and review physical access to facilities.",
                "Watching the doors turns a break-in into an alarm, not a mystery.",
                [["VEGA", "And PE-6 watches and logs who comes and goes."]]),

    L.b_quote("PE-3",
              [["ARCHIVIST", L.verbatim("PE-3")]]),

    L.b_cheatcard("PE",
                  [L.cheat_bullet("PE-2", "authorize who may enter facilities"),
                   L.cheat_bullet("PE-3", "enforce entry at the doors"),
                   L.cheat_bullet("PE-6", "monitor and log physical access")],
                  "\u201CLock the doors \u2014 and watch them.\u201D",
                  [["VEGA", "Physical security is security."]]),

    L.b_oath("PE", [["VEGA", "And the Wall-Warden's oath. A door is a decision \u2014 and I decide."]]),

    # --- RMF tie-in ---
    L.b_points("The Outer Walls in the RMF",
               ["These families are SELECTED from a 800-53B baseline for your system",
                "Then IMPLEMENTED as technical and physical controls",
                "And ASSESSED and MONITORED by the High Council (CA, later in the series)"],
               [["VEGA", "Remember the framework? The wall is where you implement what you selected."],
                ["NOVA", "Select from the baseline, implement here, assess later."]],
               kicker="HOW IT FITS"),

    # --- quizzes ---
    L.b_quiz("Which guardian proves you are who you claim, before you pass?",
             ["AC \u2014 Access Control", "IA \u2014 Identification & Authentication", "PE \u2014 Physical"], 1,
             [["NOVA", "Guardian check. Who proves your identity? Pause, and answer."]]),

    L.b_quiz("'Only the access you truly need' is which control?",
             ["AC-2 Account Management", "AC-6 Least Privilege", "IA-5 Authenticator Management"], 1,
             [["VEGA", "And the rule that limits the blast radius?"]]),

    L.b_quiz("An intruder tailgates through a propped door into the server room. Which family should stop it?",
             ["PE \u2014 Physical", "AU \u2014 Audit", "SR \u2014 Supply Chain"], 0,
             [["NOVA", "Scenario: someone tailgates into the server room. Whose watch is that?"]]),

    # --- recap + cliffhanger ---
    L.b_notebook("Episode 01 \u2014 the Outer Walls",
                 ["AC decides who may do what (AC-2, AC-3, AC-6).",
                  "IA proves the name is real before you pass \u2014 MFA lives in IA-2's enhancements.",
                  "PE guards the physical doors and environment (PE-2, PE-3, PE-6)."],
                 "Right person, right door, right reason.",
                 [["NOVA", "Notebook: the wall is access, identity, and physical \u2014 working together."],
                  ["VEGA", "Three guardians, one wall. The perimeter holds."],
                  ["NULL", "Fine. I'll stop knocking... and start hiding."],
                  ["VEGA", "Then we'll need the watchtowers. Next time."]]),
]

if __name__ == "__main__":
    L.write_spec("EP01", "the_outer_walls", beats, tag="EP01")

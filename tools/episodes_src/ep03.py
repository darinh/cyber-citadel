"""EP03 - The Keepers of the Pact (AT, PS, PT): people and privacy."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

PRIVACY_FLOW = ([{"label": "Authority to process", "x": 110, "y": 470, "w": 360, "h": 140, "color": "gold"},
                 {"label": "Purpose + Notice", "x": 590, "y": 470, "w": 360, "h": 140, "color": "cyan"},
                 {"label": "Consent (where required)", "x": 1070, "y": 470, "w": 360, "h": 140, "color": "mint"},
                 {"label": "Lawful processing", "x": 1480, "y": 470, "w": 330, "h": 140, "color": "cyan"}],
                [[0, 1], [1, 2], [2, 3]])

beats = [
    L.b_coldopen("EP03",
                 [["NULL", "Every gap, every shortcut, every forgotten door \u2014 I will find it."],
                  ["VEGA", "Not tonight. And the easiest door of all is a person who hasn't been trained."],
                  ["NOVA", "So the people are the perimeter too?"],
                  ["VEGA", "The most-attacked one. Let's defend them."]]),

    L.b_map("THE HUMAN GATE", [],
            [["NULL", "Walls and towers? Tedious. People are so much easier to fool."],
             ["VEGA", "Which is why the strongest controls guard the people, and their data."]]),

    L.b_section("03", "THE KEEPERS OF THE PACT", "Training \u00b7 Personnel \u00b7 Privacy",
                [["VEGA", "Layer three is human. Train them, trust them carefully, and honor their data."],
                 ["NARRATOR", "Three families keep the pact: Awareness & Training, Personnel Security, and Privacy."]]),

    L.b_map("THE KEEPERS OF THE PACT", ["AT", "PS", "PT"],
            [["NOVA", "AT, PS, and PT. The teacher, the oathkeeper, and the privacy herald."]],
            deps=[["AT", "IR"], ["PS", "AC"]]),

    # --- AT ---
    L.b_guardian("AT",
                 [["VEGA", "The Drillmaster, Awareness and Training."],
                  ["VEGA", "A trained citizen spots the trick at the gate before it opens."],
                  ["VEGA", "In reality, that's security and privacy training so people recognize and resist threats like phishing."]]),

    L.b_define("Phishing",
               "A fake message \u2014 email, text, or phone call \u2014 designed to trick a person into giving up a password or clicking something harmful.",
               [["NOVA", "What is 'phishing,' exactly?"],
                ["VEGA", "Bait for people. A message that looks legitimate but is a trap \u2014 and it's how most breaches actually begin."]],
               example="An 'urgent' email that looks like IT, asking you to 'verify your password' on a lookalike page."),

    L.b_control("AT-2", "Give every user security and privacy awareness training \u2014 including phishing.",
                "People are the most-targeted control surface; awareness is the cheapest strong defense.",
                [["NOVA", "How do you stop a perfect phishing email?"],
                 ["VEGA", "You train the human. AT-2 builds that instinct in everyone \u2014 the instinct that hangs up on the kind of call we opened with."]]),

    L.b_control("AT-3", "Give people role-based training for their specific security duties.",
                "An admin, a developer, and a clerk face different risks; AT-3 tailors the lesson.",
                [["VEGA", "And AT-3 trains people for their particular role."]]),

    L.b_quote("AT-2",
              [["ARCHIVIST", L.verbatim("AT-2")]]),

    L.b_cheatcard("AT",
                  [L.cheat_bullet("AT-2", "awareness training for everyone (incl. phishing)"),
                   L.cheat_bullet("AT-3", "role-based training for specific duties"),
                   L.cheat_bullet("AT-4", "keep training records")],
                  "\u201CA trained user is a control.\u201D",
                  [["VEGA", "The cheapest firewall you own is an alert human."]]),

    L.b_oath("AT", [["VEGA", "The Drillmaster's oath. The sharpest blade is an alert mind."]]),

    # --- PS ---
    L.b_guardian("PS",
                 [["VEGA", "The Oathkeeper, Personnel Security."],
                  ["NULL", "Every guard you hire... could be mine."],
                  ["VEGA", "In reality, that's screening people, adjusting access when they move or leave, and guarding against insider risk."]]),

    L.b_control("PS-3", "Screen people before granting access \u2014 and rescreen as needed.",
                "Trust is granted, not assumed; screening is how the citadel vets its guards.",
                [["VEGA", "PS-3 screens people before they're trusted with access."]]),

    L.b_control("PS-4", "When someone leaves, revoke access and recover assets \u2014 promptly.",
                "A departing admin who keeps access is a breach waiting to happen.",
                [["NOVA", "And when a guard leaves?"],
                 ["VEGA", "PS-4 reclaims the keys, on the way out the door."]]),

    L.b_quote("PS-4",
              [["ARCHIVIST", L.verbatim("PS-4")]]),

    L.b_cheatcard("PS",
                  [L.cheat_bullet("PS-3", "screen people before access"),
                   L.cheat_bullet("PS-4", "revoke access on termination"),
                   L.cheat_bullet("PS-5", "adjust access on transfer"),
                   L.cheat_bullet("PS-7", "hold external workers to the same bar")],
                  "\u201CVet them in, and key them out.\u201D",
                  [["VEGA", "Access should follow the person, and leave when they do."]]),

    L.b_oath("PS", [["VEGA", "The Oathkeeper's oath. Trust is earned at the gate, and returned at the door."]]),

    # --- PT ---
    L.b_guardian("PT",
                 [["VEGA", "The Privacy Herald, P-T, Processing and Transparency of personal data."],
                  ["NOVA", "New in Revision 5, privacy now stands beside security."],
                  ["VEGA", "In reality, that's processing people's personal data lawfully and openly \u2014 with notice and consent where required."]]),

    L.b_define("PII",
               "Information that can identify a specific person \u2014 on its own, or combined with other data.",
               [["NOVA", "P-I-I keeps coming up."],
                ["VEGA", "Personally identifiable information \u2014 the data that points to a real human being. Privacy is about protecting it, and the person."]],
               expand="Personally Identifiable Information",
               example="A name with a Social Security number, a home address, a medical record, or an account number."),

    L.b_control("PT-2", "Have lawful authority before processing people's personal information.",
                "Privacy starts with a simple question: are we even allowed to do this?",
                [["VEGA", "PT-2 demands a documented authority to process personal data."]]),

    L.b_control("PT-5", "Tell people, clearly, how their personal information is used.",
                "Transparency is the promise behind the pact: no secret uses of personal data.",
                [["VEGA", "And PT-5 gives people honest notice of how their data is used."]]),

    L.b_diagram("The privacy pact, in order", PRIVACY_FLOW[0], PRIVACY_FLOW[1],
                [["VEGA", "Authority first, then purpose and notice, then consent where required, and process only as authorized."],
                 ["NOVA", "Permission where needed, and honesty, before the data is used."]]),

    L.b_quote("PT-2",
              [["ARCHIVIST", L.verbatim("PT-2")]]),

    L.b_cheatcard("PT",
                  [L.cheat_bullet("PT-2", "have authority to process PII"),
                   L.cheat_bullet("PT-3", "process PII only for stated purposes"),
                   L.cheat_bullet("PT-4", "get consent where required"),
                   L.cheat_bullet("PT-5", "give a clear privacy notice")],
                  "\u201CAllowed, honest, and only as promised.\u201D",
                  [["VEGA", "Security protects the data. Privacy honors the person."]]),

    L.b_oath("PT", [["VEGA", "The Privacy Herald's oath. By what right, for what purpose, with whose leave?"]]),

    L.b_points("The Keepers in the RMF",
               ["These are people and program controls, not just technical ones",
                "PT weaves privacy through the whole catalog \u2014 new in Revision 5",
                "In practice: train, screen, and process personal data lawfully and openly"],
               [["VEGA", "Not every control is a firewall. Some are a habit, a contract, a promise."]],
               kicker="HOW IT FITS"),

    L.b_quiz("A departing administrator still has their access a week later. Which control failed?",
             ["PS-4 Personnel Termination", "AT-2 Awareness Training", "PT-5 Privacy Notice"], 0,
             [["NOVA", "Scenario: a leaver kept their access. Which guardian dropped the ball?"]]),

    L.b_quiz("Which family is new in Revision 5 and governs personal-data processing?",
             ["AT \u2014 Training", "PS \u2014 Personnel", "PT \u2014 PII Processing & Transparency"], 2,
             [["VEGA", "And which guardian is the newcomer to the catalog?"]]),

    L.b_notebook("Episode 03 \u2014 the Keepers of the Pact",
                 ["AT trains the human firewall, including phishing (AT-2, AT-3, AT-4).",
                  "PS vets people in and keys them out (PS-3, PS-4, PS-5, PS-7).",
                  "PT keeps personal data (PII) lawful, honest, and as-promised (PT-2, PT-3, PT-5)."],
                 "People are the perimeter \u2014 train them, screen them, and honor their data.",
                 [["NOVA", "Notebook: not every control is a firewall \u2014 some are a habit, a contract, a promise."],
                  ["VEGA", "People kept, the pact honored."],
                  ["NULL", "Then I'll strike where no one is even looking. Your plans."],
                  ["VEGA", "Then it's time to meet the High Council."]]),
]

if __name__ == "__main__":
    L.write_spec("EP03", "the_keepers_of_the_pact", beats, tag="EP03")

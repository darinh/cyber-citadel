"""EP07 - Siege Night (finale): defense-in-depth, the RMF, and how to use 800-53."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

RMF_CYCLE = ([{"label": "Prepare", "x": 110, "y": 330, "w": 300, "h": 120, "color": "cyan"},
             {"label": "Categorize", "x": 540, "y": 330, "w": 300, "h": 120, "color": "cyan"},
             {"label": "Select", "x": 970, "y": 330, "w": 300, "h": 120, "color": "gold"},
             {"label": "Implement", "x": 1400, "y": 330, "w": 300, "h": 120, "color": "gold"},
             {"label": "Assess", "x": 1400, "y": 600, "w": 300, "h": 120, "color": "cyan"},
             {"label": "Authorize", "x": 970, "y": 600, "w": 300, "h": 120, "color": "cyan"},
             {"label": "Monitor", "x": 540, "y": 600, "w": 300, "h": 120, "color": "mint"}],
            [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]])

beats = [
    L.b_title("FINALE", "SIEGE NIGHT", "Defense in Depth \u00b7 The Full Picture",
              [["NULL", "Every gap, every shortcut, every forgotten door \u2014 I will find it. Tonight, I bring everything. Every vector, every door, all at once."],
               ["VEGA", "Not tonight. Tonight, every guardian answers. Welcome to Siege Night."]]),

    L.b_section("07", "SIEGE NIGHT", "All twenty guardians \u00b7 The Risk Management Framework",
                [["VEGA", "One attacker, many weapons. One city, twenty guardians. This is defense in depth."]]),

    L.b_map("THE CITY STANDS AS ONE", L.CITADEL_ORDER,
            [["NARRATOR", "The Null strikes everywhere at once. Watch the city answer."]],
            deps=[["AC", "IA"], ["AC", "AU"], ["IA", "AC"], ["SI", "IR"], ["AU", "IR"],
                  ["RA", "CA"], ["SA", "SR"], ["CM", "SA"], ["SC", "AC"], ["CP", "IR"]]),

    L.b_points("The assault \u2014 repelled, vector by vector",
               ["Phishing email \u2192 AT, the trained human spots it",
                "Stolen credential \u2192 IA proves identity; AC-6 limits the reach",
                "Tailgating the door \u2192 PE stops the walk-in",
                "Malware on a host \u2192 SI detects and cleans it",
                "Wiping the logs \u2192 AU-9 protects the record"],
               [["VEGA", "Each weapon meets a guardian. No single failure ends the city."],
                ["NULL", "One of these should have worked..."]],
               kicker="DEFENSE IN DEPTH"),

    L.b_points("...and still it holds",
               ["Counterfeit part \u2192 SR checks authenticity",
                "Eavesdropping the wire \u2192 SC encrypts it",
                "The departing insider \u2192 PS revoked the keys",
                "Ransomware detonates \u2192 CP restores from clean backup",
                "Unpatched crack \u2192 RA found it, SI fixed it"],
               [["VEGA", "Layered defense means no single failure ends the fight. If one layer fails, others still prevent, detect, limit, or recover."],
                ["NOVA", "Twenty guardians, one shield."]],
               kicker="DEFENSE IN DEPTH"),

    L.b_diagram("The Risk Management Framework, end to end", RMF_CYCLE[0], RMF_CYCLE[1],
                [["VEGA", "Here is how it all comes together, the lifecycle from 800-37."],
                 ["VEGA", "Prepare, categorize, select, implement, assess, authorize, and monitor, forever."]]),

    L.b_points("How to actually use 800-53",
               ["1. Categorize the system \u2014 FIPS 199, with help from SP 800-60",
                "2. Select a baseline from SP 800-53B, then tailor it",
                "3. Implement the controls in the system",
                "4. Assess them \u2014 procedures in SP 800-53A",
                "5. Authorize to operate, then 6. Monitor continuously"],
               [["NOVA", "So in the real world, where do I start?"],
                ["VEGA", "Prepare, categorize the system, select and tailor a baseline, implement, assess, authorize, and never stop watching."]],
               kicker="IN PRACTICE"),

    L.b_points("Your bookshelf",
               ["SP 800-53 \u2014 the control catalog (this series)",
                "SP 800-53B \u2014 the control baselines",
                "SP 800-53A \u2014 how to assess the controls",
                "SP 800-37 \u2014 the Risk Management Framework",
                "FIPS 199 / 200 \u2014 categorize and set minimum requirements"],
               [["VEGA", "These books travel together. Know which one answers which question."]],
               kicker="THE COMPANIONS"),

    L.b_points("Twenty guardians, one shield \u2014 their oaths",
               ["AC: None pass unknown; none hold more than they need.",
                "AU: Every footstep written; no page erased.",
                "RA: I do not guess the storm; I measure it.",
                "SC: Filter at the edge; cipher on the wire.",
                "CP: We rehearse the dark, so we survive it."],
               [["VEGA", "Hear the oaths together, and the whole defense fits in your hand."],
                ["NOVA", "Twenty guardians, one shield."]],
               kicker="THE ROLL CALL"),

    # --- Guardian Roll Call quiz ---
    L.b_section("", "GUARDIAN ROLL CALL", "Five questions across the whole city",
                [["NOVA", "Final test. Five questions, all twenty guardians. Ready?"]]),

    L.b_quiz("Which guardian proves you are who you claim, before access?",
             ["AC \u2014 Access Control", "IA \u2014 Identification & Authentication", "AU \u2014 Audit"], 1,
             [["NOVA", "One. Who checks your identity at the gate?"]]),

    L.b_quiz("Where do the Low, Moderate, and High control baselines live?",
             ["SP 800-53", "SP 800-53B", "SP 800-53A"], 1,
             [["NOVA", "Two. Where do the baselines live?"]]),

    L.b_quiz("Ransomware hits and encrypts everything. What brings you back?",
             ["CP-9 System Backup", "AC-6 Least Privilege", "AT-2 Training"], 0,
             [["NOVA", "Three. What saves you from ransomware?"]]),

    L.b_quiz("Which document tells you HOW to assess whether controls work?",
             ["SP 800-53B", "SP 800-53A", "FIPS 199"], 1,
             [["NOVA", "Four. Which book holds the assessment procedures?"]]),

    L.b_quiz("A senior official accepts the risk and lets the system operate. Which control?",
             ["CA-6 Authorization", "PL-2 System Plan", "RA-3 Risk Assessment"], 0,
             [["NOVA", "Five. Who signs to let the system go live?"]]),

    L.b_points("The siege breaks \u2014 but the war isn't won",
               ["You met all 20 families across six layers of defense",
                "You can read any control: ID, Control, Discussion, Related, Enhancements",
                "But knowing the guardians isn't the same as standing up a system the right way"],
               [["VEGA", "You walked every wall, every tower, every vault. The siege broke on our walls, Nova."],
                ["NULL", "...but I left with the blueprints. I'll be back \u2014 and next time, it won't be one city."],
                ["NOVA", "Then how do we prove a NEW citadel is safe before we trust it with the Crown Data?"],
                ["VEGA", "That, apprentice, is a campaign. And in Act Two, you're going to lead it."]],
               kicker="THE SIEGE ENDS \u00b7 THE CAMPAIGN BEGINS"),

    L.b_title("ACT II AWAITS", "THE CAMPAIGN", "Next: standing up a real system with the Risk Management Framework",
              [["NARRATOR", "The guardians are known. Now you learn to deploy them \u2014 categorize, select, implement, assess, authorize, and watch. The campaign begins in Act Two."]]),
]

if __name__ == "__main__":
    L.write_spec("EP07", "siege_night", beats, tag="FINALE")

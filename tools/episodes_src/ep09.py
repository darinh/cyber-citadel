"""EP09 - Know Your Realm: Security Categorization (FIPS 199, FIPS 200, SP 800-60)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

CIA = ([{"label": "Confidentiality", "x": 150, "y": 470, "w": 460, "h": 150, "color": "cyan"},
        {"label": "Integrity", "x": 730, "y": 470, "w": 460, "h": 150, "color": "gold"},
        {"label": "Availability", "x": 1310, "y": 470, "w": 460, "h": 150, "color": "mint"}],
       [])

beats = [
    L.b_section("09", "KNOW YOUR REALM", "Security Categorization \u00b7 FIPS 199",
                [["VEGA", "Before you pick defenses, you must know what you're defending, and how much it matters."],
                 ["NARRATOR", "This is categorization, and it begins with a federal standard: FIPS 199."]]),

    L.b_define("FIPS \u00b7 to categorize",
               "FIPS are mandatory U.S. federal standards. To 'categorize' a system is to rate how serious the harm would be \u2014 Low, Moderate, or High \u2014 if its confidentiality, integrity, or availability were lost.",
               [["NOVA", "FIPS? Categorize?"],
                ["VEGA", "FIPS \u2014 Federal Information Processing Standards, the mandatory ones. Categorizing is sizing the stakes for C, I, and A \u2014 the triad from Episode zero."]],
               expand="FIPS = Federal Information Processing Standards"),

    L.b_diagram("Three security objectives", CIA[0], CIA[1],
                [["VEGA", "FIPS 199 judges a system on three objectives."],
                 ["NOVA", "Confidentiality, Integrity, and Availability. The C-I-A triad."]]),

    L.b_points("Rate each at Low, Moderate, or High",
               ["Confidentiality \u2014 harm if data is disclosed",
                "Integrity \u2014 harm if data is altered or destroyed",
                "Availability \u2014 harm if access is disrupted",
                "Each gets an impact level: Low, Moderate, or High"],
               [["VEGA", "For each objective, ask: how bad is the worst-case impact?"],
                ["VEGA", "Low, Moderate, or High."]],
               kicker="FIPS 199 \u00b7 IMPACT"),

    L.b_points("The high-water mark",
               ["The system's overall category = the HIGHEST of the three",
                "Example: Confidentiality Moderate, Integrity Low, Availability Moderate",
                "...the system is categorized MODERATE",
                "One High anywhere makes the whole system High"],
               [["NOVA", "So one High pulls the whole system up?"],
                ["VEGA", "Exactly. We call it the high-water mark. The worst case wins."]],
               kicker="THE HIGH-WATER MARK"),

    L.b_points("Two more companions",
               ["SP 800-60 \u2014 maps your information TYPES to impact levels",
                "FIPS 200 \u2014 the minimum security requirements for federal systems",
                "FIPS 200 is what mandates using SP 800-53 in the first place"],
               [["VEGA", "800-60 helps you rate each information type."],
                ["VEGA", "And FIPS 200 sets the floor, and points you to 800-53."]],
               kicker="FIPS 200 \u00b7 SP 800-60"),

    L.b_control("RA-2", "Categorize the system and its information, and document the results.",
                "Categorization is itself a control, RA-2, the control behind the RMF Categorize step.",
                [["VEGA", "And the catalog has a control for exactly this: RA-2."],
                 ["ARCHIVIST", L.verbatim("RA-2")]]),

    L.b_quiz("A system is Confidentiality=Moderate, Integrity=Low, Availability=High. Its category is?",
             ["Low", "Moderate", "High"], 2,
             [["NOVA", "Scenario time. What's the overall category? Pause, and answer."]]),

    L.b_quiz("Which standard defines the Low / Moderate / High impact levels?",
             ["FIPS 199", "SP 800-53B", "SP 800-37"], 0,
             [["VEGA", "And which standard sets the impact levels themselves?"]]),

    L.b_points("Episode 09 \u2014 remember this",
               ["FIPS 199 rates Confidentiality, Integrity, Availability as Low / Moderate / High",
                "Overall category = the high-water mark (the highest of the three)",
                "800-60 maps information types; FIPS 200 sets the floor and points to 800-53; RA-2 documents it"],
               [["VEGA", "We know the realm's worth. Now we choose its defenses."],
                ["VEGA", "Next: the armory, and the baselines of 800-53B."]],
               kicker="RECAP"),
]

if __name__ == "__main__":
    L.write_spec("EP09", "know_your_realm", beats, tag="EP09")

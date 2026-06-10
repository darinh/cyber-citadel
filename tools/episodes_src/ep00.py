"""EP00 - The Citadel Awakens (orientation + beginner foundations).

Accurate, grounded in truth.json. This episode now front-loads the plain-English
foundations a total beginner needs (who NIST is, what an information system /
control / risk are, the CIA triad, and law-vs-catalog-vs-framework) BEFORE the
citadel tour, per the multi-LLM beginner-accessibility review.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

CIA = [{"label": "Confidentiality", "x": 150, "y": 470, "w": 460, "h": 150, "color": "cyan"},
       {"label": "Integrity", "x": 730, "y": 470, "w": 460, "h": 150, "color": "gold"},
       {"label": "Availability", "x": 1310, "y": 470, "w": 460, "h": 150, "color": "mint"}]

beats = [
    # --- title + recurring ritual ---
    L.b_title("EPISODE 00", "THE CITADEL AWAKENS",
              "Security & Privacy Controls \u00b7 NIST SP 800-53r5",
              [["NULL", "Every gap, every shortcut, every forgotten door \u2014 I will find it."],
               ["VEGA", "Not tonight. Welcome to the Aegis Citadel. I'm Vega, and I'll be your guide."],
               ["NARRATOR", "Every modern organization runs on information. Protect it, and you thrive. Lose it, and you fall."]]),

    # --- the city + name the stakes (Crown Data) + meet Nova ---
    L.b_map("AEGIS CITADEL", [],
            [["VEGA", "Picture an organization's information as a walled city. At its heart sits the Crown Data \u2014 the records, secrets, and services everyone depends on."],
             ["NULL", "I don't want your walls. I want what they guard \u2014 the Crown Data. Lose it once, and there is no second copy of trust."],
             ["NOVA", "I'm Nova \u2014 newly appointed, and honestly new to all of this. Can we start from the very beginning?"],
             ["VEGA", "We will. First, a few words everyone uses and almost no one defines."]]),

    # --- FOUNDATIONS: plain-English define cards -------------------------
    L.b_define("NIST",
               "A U.S. government lab that writes widely used security and technology guidance. It isn't a police force \u2014 but its playbooks are followed across government, and far beyond it.",
               [["NOVA", "So who writes all of this?"],
                ["VEGA", "NIST does. Think of them as the standards lab for digital defense."]],
               expand="National Institute of Standards and Technology"),

    L.b_define("Information system",
               "The people, hardware, software, networks, and data that work together to collect, store, process, or move information.",
               [["VEGA", "The thing we're protecting is an information system."],
                ["NOVA", "So... not just a computer?"],
                ["VEGA", "Far more. The people and processes count too."]],
               example="A hospital's patient-records app, a company's email, a bank's website \u2014 even the phone in your pocket."),

    L.b_define("Security control",
               "A safeguard or countermeasure you put in place to protect a system and its information \u2014 and to bring risk down.",
               [["NOVA", "And a 'control' is...?"],
                ["VEGA", "A safeguard. Something deliberate that reduces risk. NIST SP 800-53 is a giant, organized catalog of them."]],
               example="A lock on a door, a password requirement, a smoke alarm, or a backup of your files.",
               cite="NIST SP 800-53r5"),

    L.b_define("Risk",
               "How likely something bad is, multiplied by how badly it would hurt. Security is the work of lowering risk to a level you can live with.",
               [["NOVA", "Everyone keeps saying 'risk.'"],
                ["VEGA", "Risk is likelihood times impact. A threat is who or what could hurt you; a vulnerability is the weakness they'd use; risk is the chance \u2014 and the cost \u2014 if they do."]],
               example="An unlocked door (a vulnerability) plus a burglar nearby (a threat) makes a real risk of theft.",
               kicker="PLAIN ENGLISH \u00b7 THREAT \u00b7 VULNERABILITY \u00b7 RISK"),

    L.b_diagram("Three things every control protects \u2014 the C-I-A triad", CIA, [],
                [["VEGA", "Every control in the catalog serves three goals. Remember them as C-I-A."],
                 ["VEGA", "Confidentiality \u2014 keep secrets secret. Integrity \u2014 keep data correct and untampered. Availability \u2014 keep it working when you need it."],
                 ["NOVA", "Confidentiality, Integrity, Availability. The reason every guardian exists."]]),

    L.b_points("Three words people mix up",
               ["FISMA (Federal Information Security Modernization Act) \u2014 the LAW: U.S. agencies and many contractors must protect their information and systems",
                "NIST SP 800-53 \u2014 the CATALOG: the menu of controls you can put to work",
                "The RMF (SP 800-37) \u2014 the FRAMEWORK: the step-by-step process that ties it together"],
               [["NOVA", "Why does any of this exist?"],
                ["VEGA", "A law says you must protect systems. A catalog lists what you can use. A framework is the process that connects them."],
                ["VEGA", "The law is FISMA \u2014 the Federal Information Security Modernization Act. 800-53 is the catalog. The RMF is the process. Hold those three apart, and everything else clicks."]],
               kicker="LAW \u00b7 CATALOG \u00b7 FRAMEWORK"),

    L.b_define("Security vs. privacy",
               "Security protects information and systems from unauthorized access, change, or disruption. Privacy protects people from harm caused by how their personal information is handled. They overlap \u2014 but they are different goals.",
               [["NOVA", "Isn't privacy just part of security?"],
                ["VEGA", "They overlap, but they aim at different things. In Revision 5, security and privacy finally share one catalog."]],
               kicker="PLAIN ENGLISH \u00b7 TWO GOALS"),

    # --- ORIENTATION: what 800-53 is ------------------------------------
    L.b_points("What is NIST SP 800-53?",
               ["A catalog of security AND privacy controls for information systems and organizations",
                "Published by NIST; Revision 5 released in September 2020",
                "The backbone of U.S. federal security \u2014 and used widely beyond government too"],
               [["NOVA", "So this 'eight-hundred fifty-three' everyone cites \u2014 what is it, exactly?"],
                ["VEGA", "A catalog. A giant, well-organized menu of controls you put to work."]],
               kicker="ORIENTATION"),

    L.b_map("TWENTY FAMILIES, TWENTY DISTRICTS", [],
            [["VEGA", "The catalog is organized into twenty families. We'll walk them as twenty districts of the city."],
             ["VEGA", "A district isn't really a place \u2014 it's a family of related safeguards: policies, processes, and technical controls."],
             ["NOVA", "Twenty? That's a lot of ground."],
             ["VEGA", "So we'll group them into six layers of defense. By the end, you'll remember every one."]]),

    L.b_points("Anatomy of a control",
               ["Identifier, e.g., AC-6 (family plus a number)",
                "Control, the requirement itself (the 'what')",
                "Discussion, context and rationale, informative, not prescriptive",
                "Related controls, links to other controls",
                "Enhancements, optional add-ons that strengthen it, e.g., AC-6(1)",
                "References, pointers to supporting sources"],
               [["VEGA", "Every control shares the same anatomy. Learn it once, and you can read them all."],
                ["VEGA", "First the identifier, like AC-6 \u2014 the family and a number."],
                ["VEGA", "Then the control itself: the requirement, what you must actually do."],
                ["NOVA", "And the discussion explains it?"],
                ["VEGA", "It gives context and rationale \u2014 helpful, but not itself a requirement."],
                ["VEGA", "Related controls point to neighbors. Enhancements add strength \u2014 AC-6(1) is an enhancement of AC-6. References point outside the catalog."],
                ["ARCHIVIST", "Identifier. Control. Discussion. Related controls. Enhancements. References."]],
               kicker="HOW TO READ A CONTROL"),

    L.b_control("AC-6", "Give every user and process only the access they truly need \u2014 nothing more.",
                "We'll meet AC-6 again at the Outer Walls. For now, notice the shape: ID, title, meaning.",
                [["VEGA", "Here's a single control. AC-6, Least Privilege."],
                 ["NOVA", "Clean. An ID, a title, and what it means."]]),

    L.b_quote("AC-6",
              [["VEGA", "When you see a gold card, the Archivist is reading the catalog's real words \u2014 word for word."],
               ["ARCHIVIST", L.verbatim("AC-6")]]),

    L.b_define("Baseline",
               "A ready-made starting set of controls, matched to how much harm a system's failure would cause. You begin from the baseline, then adjust it to fit.",
               [["NOVA", "People keep saying 'baseline.'"],
                ["VEGA", "A starting kit of controls \u2014 Low, Moderate, or High, sized to the stakes."]],
               example="Like a 'basic, standard, or premium' security package you start from, then customize."),

    L.b_section("", "BASELINES MOVED OUT", "Low / Moderate / High now live in NIST SP 800-53B",
                [["NOVA", "Hold on \u2014 where are the Low, Moderate, and High baselines kept?"],
                 ["VEGA", "Sharp eye. In Revision 5 they moved out, into a companion book: 800-53B."],
                 ["NARRATOR", "800-53 is the catalog of controls. 800-53B holds the baselines and tailoring guidance."]]),

    L.b_diagram("Where 800-53 lives: the Risk Management Framework",
                [{"label": "Prepare", "x": 110, "y": 330, "w": 300, "h": 120, "color": "cyan"},
                 {"label": "Categorize", "x": 540, "y": 330, "w": 300, "h": 120, "color": "cyan"},
                 {"label": "Select", "x": 970, "y": 330, "w": 300, "h": 120, "color": "gold"},
                 {"label": "Implement", "x": 1400, "y": 330, "w": 300, "h": 120, "color": "gold"},
                 {"label": "Assess", "x": 1400, "y": 600, "w": 300, "h": 120, "color": "cyan"},
                 {"label": "Authorize", "x": 970, "y": 600, "w": 300, "h": 120, "color": "cyan"},
                 {"label": "Monitor", "x": 540, "y": 600, "w": 300, "h": 120, "color": "cyan"}],
                [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]],
                [["VEGA", "800-53 doesn't stand alone. It plugs into a process called the Risk Management Framework."],
                 ["VEGA", "In plain terms: prepare, decide how much the system matters, pick controls, put them in place, check they work, get a leader to approve it, then watch it forever."],
                 ["NOVA", "And the catalog is 800-53; the baselines in 800-53B help choose which controls we start with."],
                 ["VEGA", "We'll walk all seven steps in Act Two. For now, just know the catalog has a home."]]),

    L.b_points("Your guides",
               ["VEGA \u2014 your veteran guide through the Citadel",
                "NOVA \u2014 newly appointed; she asks what you're thinking",
                "THE ARCHIVIST \u2014 reads the catalog's exact words, on the gold cards",
                "THE NULL \u2014 the threats, failures, and bad shortcuts the controls help manage"],
               [["NARRATOR", "Three guides ride with you."],
                ["NULL", "...and one rides against you."]],
               kicker="THE CAST"),

    L.b_map("THE ROAD AHEAD \u2014 SIX LAYERS", [],
            [["VEGA", "Six layers lie ahead. The Outer Walls. The Watchtowers. The Keepers of the Pact."],
             ["VEGA", "The High Council. The Forge. The Vaults and Lifelines. Then the finale: Siege Night."]]),

    L.b_points("Before we ride",
               ["This series is a memory aid, not a substitute for the standard",
                "On-screen IDs and gold quotes are taken from the official catalog",
                "For real decisions, always consult NIST SP 800-53r5 and 800-53B"],
               [["NARRATOR", "One honest note before we ride out."],
                ["VEGA", "The story is ours. The control text is theirs \u2014 real, and shown on screen."]],
               kicker="DISCLAIMER"),

    L.b_quiz("In plain terms, a security 'control' is best described as:",
             ["A type of computer", "A safeguard that reduces risk", "A government agency"], 1,
             [["VEGA", "Let's make it stick. What's a control? Pause, and answer."]]),

    L.b_quiz("Where do the Low, Moderate, and High control baselines live now?",
             ["In 800-53 itself", "In NIST SP 800-53B", "In the RMF"], 1,
             [["NOVA", "Quick check. Where do the baselines live now? Pause, and answer."]]),

    L.b_quiz("How many control families does 800-53 Revision 5 have?",
             ["Twelve", "Seventeen", "Twenty"], 2,
             [["VEGA", "And how many families guard our city?"]]),

    L.b_notebook("Episode 00 \u2014 foundations",
                 ["NIST writes the guidance; an information system is people + tech + data working together.",
                  "A control is a safeguard that lowers risk (risk = likelihood \u00d7 impact); every control serves C-I-A.",
                  "FISMA is the law, 800-53 is the catalog, the RMF is the process; baselines live in 800-53B."],
                 "Law, catalog, framework \u2014 keep them apart.",
                 [["NOVA", "Notebook open. That's the whole map on one page."],
                  ["VEGA", "That's your foundation. Next, we ride for the Outer Walls."],
                  ["NULL", "I'll be waiting at the gate."]]),
]

if __name__ == "__main__":
    L.write_spec("EP00", "the_citadel_awakens", beats)

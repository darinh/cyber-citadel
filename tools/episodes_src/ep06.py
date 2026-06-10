"""EP06 - The Vaults & Lifelines (SC, MP, CP): protect data, survive disaster."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

BOUNDARY = ([{"label": "Untrusted network", "x": 150, "y": 470, "w": 360, "h": 140, "color": "red"},
             {"label": "Boundary protection (SC-7)", "x": 780, "y": 470, "w": 380, "h": 140, "color": "gold"},
             {"label": "Your system", "x": 1430, "y": 470, "w": 340, "h": 140, "color": "mint"}],
            [[0, 1, "filtered"], [1, 2, "allowed"]])

beats = [
    L.b_coldopen("EP06",
                 [["NULL", "Every gap, every shortcut, every forgotten door \u2014 I will find it. And if I can't get in, I'll burn it down."],
                  ["VEGA", "Not tonight. Seal the roads, guard the vaults, and prepare for the dark."],
                  ["NOVA", "Prepare for the worst, you mean."],
                  ["VEGA", "Always."]]),

    L.b_map("THE VAULTS", [],
            [["NULL", "If I can't break the walls, I'll snatch your secrets in transit, or wait for the lights to go out."],
             ["VEGA", "Then we seal the roads, guard the vaults, and prepare for the dark."]]),

    L.b_section("06", "THE VAULTS & LIFELINES", "Communications \u00b7 Media \u00b7 Contingency",
                [["VEGA", "Layer six protects the data itself, and keeps the city alive through disaster."],
                 ["NARRATOR", "Three families hold the line: System & Communications Protection, Media Protection, and Contingency Planning."]]),

    L.b_map("THE VAULTS & LIFELINES", ["SC", "MP", "CP"],
            [["NOVA", "SC, MP, and CP. The warden of the roads, the steward of scrolls, and the keeper of lifelines."]],
            deps=[["SC", "AC"], ["CP", "IR"]]),

    # --- SC ---
    L.b_guardian("SC",
                 [["VEGA", "The Warden of Walls and Roads, System and Communications Protection."],
                  ["VEGA", "It fortifies the ramparts and seals the roads between districts."],
                  ["VEGA", "In reality, that's boundary protection and cryptography \u2014 guarding data as it moves and where it rests."]]),

    L.b_define("System boundary",
               "The line you draw around a system: everything inside is 'your system' \u2014 the part you own, authorize, and defend. Drawing it well is one of the most consequential decisions in 800-53.",
               [["NOVA", "What is 'the edge of the system'?"],
                ["VEGA", "Draw a line around your computers, data, and the people who run them. Inside is your system. SC-7 watches that line."]],
               example="Like the property line and fence around a building \u2014 it defines exactly what you're responsible for guarding."),

    L.b_control("SC-7", "Monitor and control traffic at the system's boundaries.",
                "The boundary is where outside meets inside; SC-7 decides what may cross.",
                [["VEGA", "SC-7, boundary protection, guards the edge of the system."]]),

    L.b_define("Encryption \u2014 in transit & at rest",
               "Math that scrambles data with a secret key, so anyone who intercepts it sees gibberish. 'In transit' is data moving across a network; 'at rest' is data sitting on a disk or in a database.",
               [["NOVA", "You keep saying cryptography \u2014 what does it actually do?"],
                ["VEGA", "It locks the data. Encrypt it in transit and at rest, and a thief without your key gets nothing."]],
               example="The padlock on a web address (HTTPS) is encryption in transit; a password-locked, encrypted laptop is encryption at rest."),

    L.b_control("SC-8", "Protect data in transit \u2014 its confidentiality and integrity.",
                "On the wire, encryption is what stops eavesdropping and tampering.",
                [["NULL", "I was listening on that line..."],
                 ["VEGA", "Then you heard noise. SC-8 protects data in transit, often with approved cryptography."]]),

    L.b_control("SC-28", "Protect data at rest \u2014 in storage.",
                "Stored data outlives the session; SC-28 keeps it encrypted and safe.",
                [["NOVA", "And the data just sitting in storage?"],
                 ["VEGA", "SC-28 protects it at rest, often with cryptography from SC-12 and SC-13."]]),

    L.b_diagram("The boundary decides what crosses", BOUNDARY[0], BOUNDARY[1],
                [["VEGA", "Untrusted traffic meets the boundary, and only the allowed passes through."],
                 ["NOVA", "Filter at the edge, encrypt across the wire."]]),

    L.b_quote("SC-7",
              [["ARCHIVIST", L.verbatim("SC-7")]]),

    L.b_cheatcard("SC",
                  [L.cheat_bullet("SC-7", "control traffic at the boundary"),
                   L.cheat_bullet("SC-8", "protect data in transit (often encrypted)"),
                   L.cheat_bullet("SC-13", "use approved cryptography"),
                   L.cheat_bullet("SC-28", "encrypt data at rest")],
                  "\u201CGuard the edge; encrypt everywhere.\u201D",
                  [["VEGA", "Protect data moving and still."]]),

    L.b_oath("SC", [["VEGA", "The Warden's oath. Filter at the edge; cipher on the wire."]]),

    # --- MP ---
    L.b_guardian("MP",
                 [["VEGA", "The Steward of Scrolls, Media Protection."],
                  ["NOVA", "It guards every scroll, and destroys the ones discarded."],
                  ["VEGA", "By 'media,' NIST means storage: hard drives, SSDs, tapes, USB sticks, even printed paper. MP protects them \u2014 and wipes them before they're thrown away."]]),

    L.b_control("MP-6", "Sanitize media before disposal or reuse \u2014 truly erase it.",
                "A discarded drive can still spill its data; MP-6 makes erasure final.",
                [["VEGA", "MP-6, media sanitization, ensures deleted really means gone."],
                 ["NULL", "Your old backup drive would have told me everything."]]),

    L.b_control("MP-7", "Restrict the use of removable media like USB drives.",
                "Removable media carries malware in and data out; MP-7 controls it.",
                [["VEGA", "And MP-7 controls removable media, the humble USB stick."]]),

    L.b_define("Reading the [brackets]",
               "NIST writes controls as templates. Text in brackets like [Assignment: organization-defined frequency] is a blank YOU fill in \u2014 every 30 days, each quarter, whatever your risk calls for. The catalog gives the requirement; you set the value.",
               [["VEGA", "One reading tip before the next gold card. Notice the brackets in the catalog's text."],
                ["NOVA", "So the brackets are blanks the organization fills in?"],
                ["VEGA", "Exactly. The requirement is fixed; the value is yours."]],
               kicker="HOW TO READ A CONTROL \u00b7 PARAMETERS"),

    L.b_quote("MP-6",
              [["ARCHIVIST", L.verbatim("MP-6")]]),

    L.b_cheatcard("MP",
                  [L.cheat_bullet("MP-2", "restrict who can access media"),
                   L.cheat_bullet("MP-4", "store media securely"),
                   L.cheat_bullet("MP-6", "sanitize media before disposal"),
                   L.cheat_bullet("MP-7", "control removable media")],
                  "\u201CGuard the scroll; burn the discard.\u201D",
                  [["VEGA", "Data outlives the device. Wipe it like you mean it."]]),

    L.b_oath("MP", [["VEGA", "The Steward's oath. When it's gone, it's gone for good."]]),

    # --- CP ---
    L.b_guardian("CP",
                 [["VEGA", "The Keeper of Lifelines, Contingency Planning."],
                  ["VEGA", "It plans for the day the towers fall, and how to rebuild."],
                  ["VEGA", "In reality, that's backups, alternate sites, and tested plans to recover operations after a disruption."]]),

    L.b_control("CP-9", "Back up your systems and data \u2014 and be able to restore.",
                "When ransomware strikes, a clean, tested backup is the way home.",
                [["NOVA", "What saves us from ransomware?"],
                 ["VEGA", "CP-9, system backup, a clean copy you can actually restore."],
                 ["VEGA", "'Clean' is the key word \u2014 a backup kept offline or unchangeable, where ransomware can't reach it. That's what saved the shipping line we opened with."]]),

    L.b_control("CP-2", "Write and maintain a contingency plan \u2014 and CP-4 tests it.",
                "An untested plan is a guess; rehearsal turns disaster into routine.",
                [["VEGA", "CP-2 is the plan; CP-4 is the drill that proves it works."]]),

    L.b_quote("CP-9",
              [["ARCHIVIST", L.verbatim("CP-9")]]),

    L.b_cheatcard("CP",
                  [L.cheat_bullet("CP-2", "have a contingency plan"),
                   L.cheat_bullet("CP-4", "test the plan"),
                   L.cheat_bullet("CP-9", "back up systems and data"),
                   L.cheat_bullet("CP-10", "recover and reconstitute")],
                  "\u201CBack it up; rehearse the recovery.\u201D",
                  [["VEGA", "Survival is planned in advance, never improvised."]]),

    L.b_oath("CP", [["VEGA", "The Keeper's oath. We rehearse the dark, so we survive it."]]),

    L.b_points("The Vaults & Lifelines in the RMF",
               ["SC and MP carry out the PROTECT function for data",
                "CP delivers RECOVER \u2014 resilience when prevention fails",
                "In practice: encrypt in transit and at rest, wipe media, test backups"],
               [["VEGA", "Prevention buys time. Recovery buys survival."]],
               kicker="HOW IT FITS"),

    L.b_quiz("Ransomware encrypts your servers. What gets you back fastest?",
             ["A clean, tested backup (CP-9)", "A firewall rule (SC-7)", "A privacy notice (PT-5)"], 0,
             [["NOVA", "Scenario: ransomware hits. What brings you home? Pause, and answer."]]),

    L.b_quiz("A surplus hard drive is sold without being wiped. Which control failed?",
             ["SC-8 Transmission", "MP-6 Media Sanitization", "CP-2 Contingency Plan"], 1,
             [["VEGA", "And the drive that left with its secrets intact?"]]),

    L.b_notebook("Episode 06 \u2014 the Vaults & Lifelines",
                 ["SC draws the boundary and encrypts data in transit and at rest (SC-7, SC-8, SC-28).",
                  "MP protects storage media and truly wipes it before disposal (MP-2, MP-6, MP-7).",
                  "CP backs up (clean = offline/immutable) and rehearses recovery (CP-2, CP-4, CP-9)."],
                 "Prevention buys time; recovery buys survival.",
                 [["NOVA", "Notebook: lock the data moving and still \u2014 and keep a backup the attacker can't touch."],
                  ["VEGA", "Data sealed, lifelines ready. The city can take a punch."],
                  ["NULL", "Then I'll bring everything, all at once. Siege night."],
                  ["VEGA", "We'll be ready. All twenty guardians, together."]]),
]

if __name__ == "__main__":
    L.write_spec("EP06", "the_vaults_and_lifelines", beats, tag="EP06")

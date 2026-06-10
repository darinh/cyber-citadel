"""EP05 - The Forge (SA, CM, MA, SR): build, configure, maintain, supply."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

beats = [
    L.b_coldopen("EP05",
                 [["NULL", "Every gap, every shortcut, every forgotten door \u2014 I will find it. Or I'll have you build it for me."],
                  ["VEGA", "Not tonight. We harden the forge itself \u2014 how systems are built, configured, and supplied."],
                  ["NOVA", "Even the parts we buy?"],
                  ["VEGA", "Especially those."]]),

    L.b_map("THE FORGE", [],
            [["NULL", "Why break in, when I can be built in? A flaw here, a tampered part there..."],
             ["VEGA", "Then we harden the forge itself, where systems are made and supplied."]]),

    L.b_section("05", "THE FORGE", "Acquisition \u00b7 Configuration \u00b7 Maintenance \u00b7 Supply Chain",
                [["VEGA", "Layer five is how you build, buy, configure, maintain, and source."],
                 ["NARRATOR", "Four families work the forge: System Acquisition, Configuration Management, Maintenance, and Supply Chain Risk Management."]]),

    L.b_map("THE FORGE", ["SA", "CM", "MA", "SR"],
            [["NOVA", "SA, CM, MA, and SR. The quartermaster, the blueprint-master, the smith, and the caravan-master."]],
            deps=[["SA", "SR"], ["CM", "SA"]]),

    # --- SA ---
    L.b_guardian("SA",
                 [["VEGA", "The Quartermaster, System and Services Acquisition."],
                  ["VEGA", "It buys and builds only what can be trusted."],
                  ["VEGA", "In reality, that's building security into the development life cycle, and into the systems and services you acquire."]]),

    L.b_control("SA-8", "Apply security and privacy engineering principles when you design and build.",
                "Security bolted on later is weak; SA-8 bakes it in from the first sketch.",
                [["VEGA", "SA-8 builds security in by design, not as an afterthought."]]),

    L.b_control("SA-22", "Replace unsupported components \u2014 software past its end of life.",
                "Unsupported software gets no patches; it's a permanently open window.",
                [["NOVA", "What about software no one updates anymore?"],
                 ["VEGA", "SA-22 says replace it, or arrange alternate support. Unsupported is risk you must manage."]]),

    L.b_quote("SA-8",
              [["ARCHIVIST", L.verbatim("SA-8")]]),

    L.b_cheatcard("SA",
                  [L.cheat_bullet("SA-3", "build security into the life cycle"),
                   L.cheat_bullet("SA-4", "put security in acquisition contracts"),
                   L.cheat_bullet("SA-8", "engineer with security principles"),
                   L.cheat_bullet("SA-22", "replace unsupported components")],
                  "\u201CBuild it secure, or don't buy it.\u201D",
                  [["VEGA", "Trust is forged in, never sprinkled on."]]),

    L.b_oath("SA", [["VEGA", "The Quartermaster's oath. Built in, never sprinkled on."]]),

    # --- CM ---
    L.b_guardian("CM",
                 [["VEGA", "The Master of Blueprints, Configuration Management."],
                  ["NULL", "One quiet, undocumented change... and I have a door no one remembers."],
                  ["VEGA", "In reality, that's keeping a known, approved configuration and controlling every change, so systems stay in a trusted state."]]),

    L.b_define("Two kinds of 'baseline'",
               "Heads up: 'baseline' means two different things. A CONTROL baseline (from 800-53B) is your starting set of controls. A CONFIGURATION baseline (CM-2) is the known-good snapshot of a system's settings, versions, and components.",
               [["NOVA", "We already met 'baseline' back in Episode 00."],
                ["VEGA", "Different baseline. That was the control baseline. CM-2 is the configuration baseline \u2014 drift from it, and you have a question to answer."]],
               kicker="WORD WARNING \u00b7 TWO BASELINES"),

    L.b_control("CM-2", "Keep a known, documented baseline configuration of the system.",
                "If you don't know the 'normal,' you can't spot the tampering.",
                [["VEGA", "CM-2 holds the baseline, the master blueprint of the system."]]),

    L.b_control("CM-7", "Turn off what you don't need \u2014 least functionality.",
                "Every extra service and port is another door; CM-7 closes the unused ones.",
                [["VEGA", "CM-7 is least functionality. Computers talk on numbered channels \u2014 ports \u2014 and run background programs \u2014 services."],
                 ["NOVA", "And every one you don't need is another door."],
                 ["VEGA", "Exactly. CM-7 closes the ports and services you never use."]]),

    L.b_quote("CM-2",
              [["ARCHIVIST", L.verbatim("CM-2")]]),

    L.b_cheatcard("CM",
                  [L.cheat_bullet("CM-2", "keep a known baseline configuration"),
                   L.cheat_bullet("CM-3", "control every change"),
                   L.cheat_bullet("CM-7", "least functionality \u2014 disable the unneeded"),
                   L.cheat_bullet("CM-8", "inventory your components")],
                  "\u201CKnow normal; approve every change.\u201D",
                  [["VEGA", "A known system is a defensible system."]]),

    L.b_oath("CM", [["VEGA", "The Blueprint-Master's oath. A known system is a defended system."]]),

    # --- MA ---
    L.b_guardian("MA",
                 [["VEGA", "The Smith, Maintenance."],
                  ["NOVA", "It tends the machinery, and watches who holds the tools."],
                  ["VEGA", "In reality, that's controlled system maintenance \u2014 including safeguards for remote and third-party work."]]),

    L.b_control("MA-2", "Control and log maintenance \u2014 who, what, when, and approved.",
                "Maintenance touches the guts of a system; uncontrolled, it's a perfect cover.",
                [["VEGA", "MA-2 controls maintenance, scheduled, approved, and recorded."]]),

    L.b_control("MA-4", "Guard remote maintenance sessions tightly.",
                "A remote maintenance link is a powerful door; MA-4 keeps it locked and watched.",
                [["NULL", "Your remote support line was going to be my way in."],
                 ["VEGA", "MA-4 saw to that. Remote maintenance, tightly controlled."]]),

    L.b_quote("MA-2",
              [["ARCHIVIST", L.verbatim("MA-2")]]),

    L.b_cheatcard("MA",
                  [L.cheat_bullet("MA-2", "control and record maintenance"),
                   L.cheat_bullet("MA-4", "secure remote maintenance"),
                   L.cheat_bullet("MA-5", "vet maintenance personnel")],
                  "\u201CMind the hands on the machine.\u201D",
                  [["VEGA", "Maintenance is access. Treat it like access."]]),

    L.b_oath("MA", [["VEGA", "The Smith's oath. Every tool is a key, and I guard the keys."]]),

    # --- SR ---
    L.b_guardian("SR",
                 [["VEGA", "The Caravan-Master, Supply Chain Risk Management, new in Revision 5."],
                  ["VEGA", "It guards the roads your supplies travel, all the way to the source."],
                  ["VEGA", "In reality, that's managing risk from suppliers and components \u2014 the SolarWinds-style attack we opened with, where a trusted update carried a hidden backdoor."]]),

    L.b_control("SR-11", "Detect and prevent counterfeit components.",
                "A tampered part can arrive pre-compromised; SR-11 checks what you're given is real.",
                [["NOVA", "How do we trust the parts themselves?"],
                 ["VEGA", "SR-11, component authenticity, hunts counterfeits and tampering."]]),

    L.b_quote("SR-11",
              [["ARCHIVIST", L.verbatim("SR-11")]]),

    L.b_cheatcard("SR",
                  [L.cheat_bullet("SR-3", "supply chain controls and processes"),
                   L.cheat_bullet("SR-5", "strategies for acquiring components"),
                   L.cheat_bullet("SR-8", "notification agreements with suppliers"),
                   L.cheat_bullet("SR-11", "detect and prevent counterfeits")],
                  "\u201CTrust the road, all the way to the source.\u201D",
                  [["VEGA", "Your security is only as strong as your weakest supplier."]]),

    L.b_oath("SR", [["VEGA", "The Caravan-Master's oath. I trust no part I cannot trace."]]),

    L.b_points("The Forge in the RMF",
               ["CM keeps IMPLEMENTATION honest and supports MONITORING",
                "SA and SR push security upstream \u2014 into building and buying",
                "In practice: secure SDLC, locked-down configs, vetted suppliers"],
               [["VEGA", "The best breach is the one designed out before it's built."]],
               kicker="HOW IT FITS"),

    L.b_quiz("A counterfeit network card arrives pre-tampered. Which control should catch it?",
             ["CM-2 Baseline Configuration", "SR-11 Component Authenticity", "MA-2 Maintenance"], 1,
             [["NOVA", "Scenario: a tampered part in the box. Whose job is that? Pause, and answer."]]),

    L.b_quiz("Disabling unused ports and services is which control?",
             ["CM-7 Least Functionality", "SA-22 Unsupported Components", "CM-8 Inventory"], 0,
             [["VEGA", "And shutting the doors you never use?"]]),

    L.b_notebook("Episode 05 \u2014 the Forge",
                 ["SA builds and buys security in (SA-3, SA-8, SA-22).",
                  "CM keeps a known config and controls every change (CM-2, CM-7, CM-8).",
                  "MA guards maintenance; SR guards the supply chain (MA-2, MA-4; SR-3, SR-11)."],
                 "The best breach is the one designed out before it's built.",
                 [["NOVA", "Notebook: secure how you build, configure, maintain, and source \u2014 the attacker counts on you skipping one."],
                  ["VEGA", "The forge is hardened, from source to system."],
                  ["NULL", "Then I'll take your secrets in transit, or your backups."],
                  ["VEGA", "Then we ride for the Vaults and the Lifelines."]]),
]

if __name__ == "__main__":
    L.write_spec("EP05", "the_forge", beats, tag="EP05")

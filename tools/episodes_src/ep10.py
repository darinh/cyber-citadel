"""EP10 - The Armory: Control Baselines & Tailoring (SP 800-53B)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

BASELINES = ([{"label": "LOW\n149 controls", "x": 150, "y": 460, "w": 440, "h": 170, "color": "mint"},
              {"label": "MODERATE\n287 controls", "x": 740, "y": 460, "w": 440, "h": 170, "color": "gold"},
              {"label": "HIGH\n370 controls", "x": 1330, "y": 460, "w": 440, "h": 170, "color": "red"}],
             [[0, 1], [1, 2]])

beats = [
    L.b_section("10", "THE ARMORY", "Control Baselines & Tailoring \u00b7 NIST SP 800-53B",
                [["VEGA", "You know the system's worth. Now draw your loadout from the armory."],
                 ["NARRATOR", "The baselines, and the tailoring guidance, live in SP 800-53B."]]),

    L.b_points("What is a baseline?",
               ["A pre-defined STARTING set of controls for an impact level",
                "Three security baselines: Low, Moderate, High",
                "Plus a separate Privacy baseline for systems that process PII",
                "Your FIPS 199 level picks the SECURITY baseline: a Moderate system \u2192 Moderate baseline"],
               [["NOVA", "So a baseline is a ready-made kit?"],
                ["VEGA", "A starting kit. Matched to how much the system matters."]],
               kicker="800-53B"),

    L.b_define("Tailoring & overlays",
               "Tailoring is adjusting the baseline to fit your system \u2014 removing what doesn't apply, adding what's missing, setting parameters, and justifying each change. An overlay is ready-made tailoring for a whole community.",
               [["NOVA", "Tailoring? Overlay?"],
                ["VEGA", "Tailoring fits the kit to you \u2014 like Aegis Hospital dropping wireless because that app is wired-only, and adding a healthcare overlay. An overlay is shared tailoring, so you don't start from scratch."]],
               kicker="PLAIN ENGLISH"),

    L.b_diagram("The three security baselines (controls + enhancements)", BASELINES[0], BASELINES[1],
                [["VEGA", "Low draws 149 items. Moderate, 287. High, 370."],
                 ["VEGA", "Higher impact, more controls and enhancements, by design."]]),

    L.b_points("Then you TAILOR it",
               ["Scoping \u2014 drop controls that don't apply to your system",
                "Compensating controls \u2014 swap in an alternative that meets the intent",
                "Parameters \u2014 fill in organization-defined values (frequencies, roles)",
                "Supplementation \u2014 ADD controls for risks the baseline misses"],
               [["VEGA", "A baseline is a starting point, never the finish line. You tailor it to fit."],
                ["NULL", "I look for the control you wrongly tailored away."]],
               kicker="TAILORING"),

    L.b_points("Overlays & a key nuance",
               ["Overlays \u2014 ready-made tailored baselines for a community (cloud, classified, mission-specific)",
                "The Privacy baseline (96 controls) covers systems processing PII",
                "Security baselines span 18 families \u2014 Program Management (PM) is org-wide, not in them"],
               [["VEGA", "Overlays are shared tailoring, so you don't start from scratch."],
                ["NOVA", "And remember, PM controls run across the whole organization, outside any baseline."]],
               kicker="OVERLAYS"),

    L.b_quiz("Where do the Low / Moderate / High baselines live?",
             ["SP 800-53 (the catalog)", "SP 800-53B", "FIPS 199"], 1,
             [["NOVA", "Quick check. Which book holds the baselines? Pause, and answer."]]),

    L.b_quiz("Adjusting a baseline \u2014 scoping out, swapping, adding controls \u2014 is called?",
             ["Categorization", "Tailoring", "Authorization"], 1,
             [["VEGA", "And the act of adjusting the baseline to fit your system?"]]),

    L.b_points("Episode 10 \u2014 remember this",
               ["Baselines (800-53B): Low 149, Moderate 287, High 370, Privacy 96",
                "Your FIPS 199 category selects the baseline",
                "Then TAILOR: scope, compensate, set parameters, supplement, apply overlays"],
               [["VEGA", "Defenses chosen and fitted. Now, do they actually work?"],
                ["VEGA", "Next: the reckoning, assessment and authorization."]],
               kicker="RECAP"),
]

if __name__ == "__main__":
    L.write_spec("EP10", "the_armory_baselines", beats, tag="EP10")

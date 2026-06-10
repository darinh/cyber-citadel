"""EP08 - The Campaign Begins: the Risk Management Framework (SP 800-37r2)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

RMF = ([{"label": "Prepare", "x": 110, "y": 330, "w": 300, "h": 120, "color": "cyan"},
        {"label": "Categorize", "x": 540, "y": 330, "w": 300, "h": 120, "color": "gold"},
        {"label": "Select", "x": 970, "y": 330, "w": 300, "h": 120, "color": "gold"},
        {"label": "Implement", "x": 1400, "y": 330, "w": 300, "h": 120, "color": "mint"},
        {"label": "Assess", "x": 1400, "y": 600, "w": 300, "h": 120, "color": "gold"},
        {"label": "Authorize", "x": 970, "y": 600, "w": 300, "h": 120, "color": "gold"},
        {"label": "Monitor", "x": 540, "y": 600, "w": 300, "h": 120, "color": "cyan"}],
       [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]])

beats = [
    L.b_title("ACT II", "THE CAMPAIGN", "Standing up a system the right way \u00b7 the RMF",
              [["NARRATOR", "You have met the twenty guardians. But knowing them is not the same as deploying them."],
               ["VEGA", "You just watched Aegis Hospital secured end to end. Now we slow down and learn each step \u2014 and Nova, you're leading it."],
               ["NOVA", "From apprentice to running the campaign. Let's begin."]]),

    L.b_section("08", "THE RISK MANAGEMENT FRAMEWORK", "NIST SP 800-37, Revision 2",
                [["VEGA", "The plan of campaign has a name: the Risk Management Framework, from 800-37."],
                 ["NOVA", "The process that tells you what to do, and in what order."]]),

    L.b_define("Framework",
               "A repeatable, step-by-step process for managing a system's security risk \u2014 from understanding the system, to choosing and proving controls, to approving operation and watching over time.",
               [["NOVA", "What makes the RMF a 'framework' and not just a checklist?"],
                ["VEGA", "It's the living process that ties the catalog, the baselines, and the assessments into one repeatable lifecycle."]],
               expand="RMF = Risk Management Framework (NIST SP 800-37)"),

    L.b_diagram("Seven steps, one lifecycle", RMF[0], RMF[1],
                [["VEGA", "Seven steps. Prepare, categorize, select, implement, assess, authorize, and monitor."],
                 ["NOVA", "And it's a cycle, monitoring never stops."],
                 ["VEGA", "Prepare was added in Revision 2, getting the organization and system ready first."]]),

    L.b_points("What each step does",
               ["Prepare \u2014 set context, roles, and risk strategy",
                "Categorize \u2014 size the system's impact (FIPS 199)",
                "Select \u2014 choose a control baseline (800-53B) and tailor it",
                "Implement \u2014 put the controls (800-53) to work",
                "Assess \u2014 verify they work (800-53A)"],
               [["VEGA", "Each step has a job, and most are guided by a supporting NIST publication."]],
               kicker="800-37 \u00b7 STEPS 1-5"),

    L.b_points("...and the last two",
               ["Authorize \u2014 a senior official accepts the risk (the ATO)",
                "Monitor \u2014 ongoing awareness throughout the system lifecycle (800-137)",
                "Then the cycle begins again as the system changes"],
               [["VEGA", "Authorize, then monitor. A system is never simply 'done.'"],
                ["NULL", "Good. Because I never stop, either."]],
               kicker="800-37 \u00b7 STEPS 6-7"),

    L.b_points("Your campaign bookshelf",
               ["FIPS 199 / 800-60 \u2014 categorize the system",
                "FIPS 200 \u2014 the minimum security requirements",
                "SP 800-53B \u2014 the control baselines",
                "SP 800-53 \u2014 the control catalog (Act I)",
                "SP 800-53A \u2014 how to assess; SP 800-37 \u2014 the process"],
               [["VEGA", "These books travel together. Each answers one question in the campaign."],
                ["NOVA", "So Act One taught the controls. Act Two is how we actually use them."]],
               kicker="THE DOCUMENT FAMILY"),

    L.b_quiz("How many steps are in the RMF (SP 800-37 Rev 2)?",
             ["Five", "Six", "Seven"], 2,
             [["NOVA", "Quick check. How many steps in the framework? Pause, and answer."]]),

    L.b_quiz("Which RMF step was newly added in Revision 2?",
             ["Prepare", "Authorize", "Monitor"], 0,
             [["VEGA", "And which step did Revision 2 add at the front?"]]),

    L.b_points("Episode 08 \u2014 remember this",
               ["The RMF (800-37r2) has 7 steps: Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor",
                "Each step has a companion NIST document",
                "It's a continuous lifecycle, not a one-time checklist"],
               [["VEGA", "The map is set. First stop, knowing what we're protecting."],
                ["VEGA", "Next: categorization."]],
               kicker="RECAP"),
]

if __name__ == "__main__":
    L.write_spec("EP08", "the_campaign_rmf", beats, tag="EP08")

"""EP11 - The Reckoning: Assess, Authorize, Monitor (SP 800-53A & SP 800-137). Grand finale."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

METHODS = ([{"label": "Examine", "x": 150, "y": 470, "w": 460, "h": 150, "color": "cyan"},
            {"label": "Interview", "x": 730, "y": 470, "w": 460, "h": 150, "color": "gold"},
            {"label": "Test", "x": 1310, "y": 470, "w": 460, "h": 150, "color": "mint"}],
           [])

beats = [
    L.b_section("11", "THE RECKONING", "Assess \u00b7 Authorize \u00b7 Monitor",
                [["VEGA", "The walls are built. But a defense you haven't tested is only a hope."],
                 ["NARRATOR", "Now: assessment, authorization, and the watch that never ends."]]),

    L.b_diagram("How assessors check a control (SP 800-53A)", METHODS[0], METHODS[1],
                [["VEGA", "800-53A gives assessors three methods."],
                 ["NOVA", "Examine the evidence, interview the people, and test the system itself."]]),

    L.b_points("From assessment to decision",
               ["Assessors produce a Security Assessment Report (the SAR)",
                "Open weaknesses go on a POA&M \u2014 a Plan of Action & Milestones (CA-5)",
                "The POA&M tracks each gap until it's fixed"],
               [["VEGA", "The findings become a report, and every gap gets a plan to close it."]],
               kicker="800-53A \u00b7 SAR \u00b7 POA&M"),

    L.b_points("The paperwork trail \u2014 and why it matters",
               ["Assess \u2192 the Security Assessment Report (SAR): what works, what doesn't",
                "Open gaps \u2192 the POA&M: each weakness with an owner and a due date",
                "SAR + plan + evidence \u2192 the authorization package the AO reviews",
                "AO accepts the residual risk \u2192 the ATO: the system may operate"],
               [["VEGA", "Every step leaves a document. Together, they let a leader make an honest call."],
                ["NOVA", "Assess, report, plan, package, authorize."]],
               kicker="THE ARTIFACT CHAIN"),

    L.b_control("CA-2", "Assess whether controls are implemented correctly, operate as intended, and produce the desired outcome.",
                "CA-2 calls for the assessment (independent where required); 800-53A is the how-to.",
                [["VEGA", "The catalog control behind all this is CA-2."],
                 ["ARCHIVIST", L.verbatim("CA-2")]]),

    L.b_points("Authorization \u2014 the ATO",
               ["A senior leader, the authorizing official, reviews the residual risk",
                "If acceptable, they grant an Authorization to Operate \u2014 the ATO (CA-6)",
                "It is a documented acceptance of risk, not a guarantee of safety"],
               [["NOVA", "So someone has to own the risk and sign for it?"],
                ["VEGA", "Yes. The authorizing official grants the ATO, and owns that decision."],
                ["NULL", "A signature... still won't stop me."]],
               kicker="800-37 \u00b7 AUTHORIZE"),

    L.b_control("CA-7", "Keep assessing and watching the system continuously, not just once.",
                "Authorization is a point-in-time risk decision; monitoring runs across the system's life to keep risk in view.",
                [["VEGA", "Which is why the final step never ends: CA-7, continuous monitoring."],
                 ["VEGA", "SP 800-137 is the playbook for that ongoing watch."]]),

    L.b_quiz("What are the three assessment methods in SP 800-53A?",
             ["Scan, Patch, Report", "Examine, Interview, Test", "Plan, Do, Check"], 1,
             [["NOVA", "Final stretch. Name the three assessment methods. Pause, and answer."]]),

    L.b_quiz("A senior official accepts the residual risk and lets the system run. That decision is the?",
             ["POA&M", "ATO (Authorization to Operate)", "SAR"], 1,
             [["VEGA", "And the decision that lets the system go live?"]]),

    L.b_quiz("Where are open weaknesses tracked until they're remediated?",
             ["In the SAR", "In a POA&M", "In FIPS 199"], 1,
             [["VEGA", "And where do we track the gaps we haven't closed?"]]),

    L.b_points("The campaign, complete",
               ["Prepare \u2192 Categorize \u2192 Select \u2192 Implement \u2192 Assess \u2192 Authorize \u2192 Monitor",
                "FIPS 199 + 800-60 categorize it; FIPS 200 sets the floor; 800-53B picks the baseline; 800-53 supplies the controls",
                "800-53A assesses; 800-37 runs the process; 800-137 keeps the watch"],
               [["VEGA", "Categorize, select, implement, assess, authorize, monitor. You've walked the whole campaign."],
                ["NOVA", "From a single control... to a system that's authorized and watched for life."]],
               kicker="THE WHOLE PICTURE"),

    L.b_title("THE CITADEL ENDURES", "CYBER CITADEL",
              "An educational aid \u2014 always consult the NIST publications",
              [["NOVA", "In Episode zero, I didn't even know what eight-hundred fifty-three was. Tonight, I'm signing for it."],
               ["VEGA", "Then sign, Castellan \u2014 and keep the watch."],
               ["NULL", "...until next time."],
               ["NOVA", "There's always a next time. That's the job. CA-7 \u2014 the watch never ends."],
               ["NARRATOR", "Episode zero promised: protect it, and you thrive. You protected it. Now you never stop. The story was ours; the controls are real."]]),
]

if __name__ == "__main__":
    L.write_spec("EP11", "the_reckoning", beats, tag="FINALE")

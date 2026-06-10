"""EP04 - The High Council (RA, PL, PM, CA): govern, plan, assess, authorize."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import episode_lib as L

beats = [
    L.b_coldopen("EP04",
                 [["NULL", "Every gap, every shortcut, every forgotten door \u2014 I will find it."],
                  ["VEGA", "Not tonight. And the deepest gaps aren't in the walls \u2014 they're in the decisions above them."],
                  ["NOVA", "Decisions can be a vulnerability?"],
                  ["VEGA", "The costliest kind. Welcome to the High Council."]]),

    L.b_map("THE INNER KEEP", [],
            [["NULL", "Strike the plans, and every wall is built on sand."],
             ["VEGA", "Then it's time you met the High Council, where the realm is governed."]]),

    L.b_section("04", "THE HIGH COUNCIL", "Risk \u00b7 Planning \u00b7 Program \u00b7 Assessment",
                [["VEGA", "Layer four is governance, the decisions above any single wall."],
                 ["NARRATOR", "Four families rule the keep: Risk Assessment, Planning, Program Management, and Assessment & Authorization."]]),

    L.b_map("THE HIGH COUNCIL", ["RA", "PL", "PM", "CA"],
            [["NOVA", "RA, PL, PM, and CA. The seer, the cartographer, the steward, and the inspector."]],
            deps=[["RA", "CA"], ["PM", "PL"]]),

    # --- RA ---
    L.b_guardian("RA",
                 [["VEGA", "The Seer, Risk Assessment \u2014 though this seer never merely guesses."],
                  ["VEGA", "It doesn't read omens; it measures them: what could go wrong, how likely, and how badly."],
                  ["VEGA", "In reality, that's analyzing risk with hard evidence \u2014 vulnerability scans and threat intelligence."]]),

    L.b_control("RA-3", "Assess the risk to the system \u2014 threats, vulnerabilities, likelihood, and impact.",
                "Risk is the compass; it tells you which controls actually matter for your system.",
                [["VEGA", "RA-3 is the formal risk assessment, the basis for every choice."]]),

    L.b_control("RA-5", "Scan for vulnerabilities, and act on what you find.",
                "An unscanned, unpatched service is the unseen crack in the wall.",
                [["NOVA", "How do we find the cracks before the Null does?"],
                 ["VEGA", "RA-5, vulnerability monitoring and scanning, hunts them down."]]),

    L.b_quote("RA-5",
              [["ARCHIVIST", L.verbatim("RA-5")]]),

    L.b_cheatcard("RA",
                  [L.cheat_bullet("RA-3", "assess threats, vulnerabilities, and impact"),
                   L.cheat_bullet("RA-5", "scan for vulnerabilities and remediate"),
                   L.cheat_bullet("RA-7", "respond to the risks you find")],
                  "\u201CKnow the risk before you spend a coin.\u201D",
                  [["VEGA", "Risk first. It tells you where to spend your strength."]]),

    L.b_oath("RA", [["VEGA", "The Seer's oath. I do not guess the storm; I measure it."]]),

    # --- PL ---
    L.b_guardian("PL",
                 [["VEGA", "The Cartographer, Planning."],
                  ["NOVA", "It draws the map of the defense before the march."],
                  ["VEGA", "In reality, that's the system security and privacy plan, the rules of behavior, and the security architecture."]]),

    L.b_control("PL-2", "Write a security and privacy plan for the system \u2014 the single source of truth.",
                "The plan says what the system is, who runs it, and which controls protect it.",
                [["VEGA", "PL-2 is the system security and privacy plan, the master map."]]),

    L.b_control("PL-8", "Design a security and privacy architecture, on purpose, up front.",
                "Architecture decides where the walls go before a single stone is laid.",
                [["VEGA", "And PL-8 plans the architecture, defense by design."]]),

    L.b_quote("PL-2",
              [["ARCHIVIST", L.verbatim("PL-2")]]),

    L.b_cheatcard("PL",
                  [L.cheat_bullet("PL-2", "the system security & privacy plan"),
                   L.cheat_bullet("PL-4", "rules of behavior for users"),
                   L.cheat_bullet("PL-8", "security & privacy architecture")],
                  "\u201CPlan the map before the march.\u201D",
                  [["VEGA", "No plan, no defense, just luck."]]),

    L.b_oath("PL", [["VEGA", "The Cartographer's oath. No march without a map."]]),

    # --- PM ---
    L.b_guardian("PM",
                 [["VEGA", "The High Steward, Program Management."],
                  ["VEGA", "It governs the whole realm's defense, above any single system."],
                  ["VEGA", "In reality, that's organization-wide governance: the security and privacy program, roles, risk strategy, and resources."]]),

    L.b_control("PM-9", "Set an organization-wide strategy to manage risk.",
                "PM steers the whole program; these controls run org-wide, not per-system.",
                [["NOVA", "Who sets the strategy for everything?"],
                 ["VEGA", "PM-9, the risk management strategy for the entire organization."]]),

    L.b_points("A note on Program Management",
               ["PM controls are organization-wide, not tied to one system",
                "They are deployed independently of the Low / Moderate / High baselines",
                "Think governance: leadership, strategy, resources, and oversight"],
               [["VEGA", "Important: PM controls aren't selected per system from a baseline."],
                ["VEGA", "They run across the whole organization, all the time."]],
               kicker="ACCURACY ANCHOR"),

    L.b_quote("PM-9",
              [["ARCHIVIST", L.verbatim("PM-9")]]),

    L.b_cheatcard("PM",
                  [L.cheat_bullet("PM-2", "name the security program leadership"),
                   L.cheat_bullet("PM-9", "the organization-wide risk strategy"),
                   L.cheat_bullet("PM-11", "define mission and business processes"),
                   L.cheat_bullet("PM-31", "the continuous monitoring strategy")],
                  "\u201CGovern the whole, not just the parts.\u201D",
                  [["VEGA", "Program management is the realm thinking as one."]]),

    L.b_oath("PM", [["VEGA", "The High Steward's oath. One realm, one strategy \u2014 always."]]),

    # --- CA ---
    L.b_guardian("CA",
                 [["VEGA", "The Inspector, Assessment, Authorization, and Monitoring."],
                  ["NOVA", "It tests the defenses, and signs off before the gates open."],
                  ["VEGA", "In reality, that's assessing controls, formally authorizing a system to operate, and watching it continuously."]]),

    L.b_control("CA-6", "An authorizing official formally accepts the risk and authorizes the system to operate.",
                "Authorization is a named, accountable leader putting their signature on the risk.",
                [["VEGA", "CA-6, authorization, the authorizing official says 'I accept this risk.' The agency we opened with ran key systems without this signature."],
                 ["NULL", "A signature won't stop me."],
                 ["VEGA", "No. But it puts a name on the wall the day something does. And CA-7 keeps watching after the ink dries."]]),

    L.b_define("Authorization to Operate (ATO)",
               "A senior leader's formal, signed decision that a system's remaining risk is acceptable \u2014 so it may go live. It accepts risk; it does not guarantee safety.",
               [["NOVA", "So a real person signs for the risk?"],
                ["VEGA", "The authorizing official \u2014 a senior, accountable leader \u2014 grants the A-T-O, and owns that decision."]],
               expand="ATO = Authorization to Operate, granted by the Authorizing Official (AO)"),

    L.b_control("CA-2", "Independently assess whether the controls actually work.",
                "Selecting a control isn't enough; CA-2 checks it truly does its job.",
                [["VEGA", "CA-2 plans and runs the assessment, using procedures from companion doc 800-53A."]]),

    L.b_define("POA&M",
               "A living to-do list of every known weakness you haven't fixed yet \u2014 each with an owner and a due date. It's how honest teams drive risk down over time.",
               [["NOVA", "And the gaps we find but can't close today?"],
                ["VEGA", "They go on the POA&M. CA-5 requires it, and the authorizing official keeps an eye on it."]],
               expand="POA&M = Plan of Action & Milestones (CA-5)"),

    L.b_quote("CA-2",
              [["ARCHIVIST", L.verbatim("CA-2")]]),

    L.b_cheatcard("CA",
                  [L.cheat_bullet("CA-2", "assess that controls work (per 800-53A)"),
                   L.cheat_bullet("CA-5", "track weaknesses in a POA&M"),
                   L.cheat_bullet("CA-6", "authorize the system to operate"),
                   L.cheat_bullet("CA-7", "monitor continuously")],
                  "\u201CTest it, sign it, watch it.\u201D",
                  [["VEGA", "Assess, authorize, and never stop monitoring."]]),

    L.b_oath("CA", [["VEGA", "The Inspector's oath. Test before you trust; watch after you sign."]]),

    L.b_points("The High Council drives the RMF",
               ["RA \u2192 categorize and assess risk",
                "PL \u2192 plan; PM \u2192 govern the whole program",
                "CA \u2192 assess, authorize, and monitor the system"],
               [["VEGA", "If a layer maps onto the framework, it's this one."],
                ["NOVA", "Risk, planning, governance, and assessment, the work behind the RMF lifecycle."]],
               kicker="HOW IT FITS"),

    L.b_quiz("A new system is ready to go live. Who formally accepts the risk to operate it?",
             ["CA-6 Authorization", "RA-3 Risk Assessment", "PL-2 System Plan"], 0,
             [["NOVA", "Scenario: go-live day. Whose signature is required? Pause, and answer."]]),

    L.b_quiz("Where are known weaknesses tracked until they're fixed?",
             ["In the system plan", "In a POA&M (CA-5)", "In the audit log"], 1,
             [["VEGA", "And where do we record the gaps we haven't closed yet?"]]),

    L.b_notebook("Episode 04 \u2014 the High Council",
                 ["RA finds and ranks risk with evidence (RA-3, RA-5, RA-7).",
                  "PL plans the defense; PM governs the whole organization (PL-2, PL-8; PM-9, PM-2).",
                  "CA assesses, authorizes (the ATO), tracks gaps (POA&M), and monitors (CA-2, CA-5, CA-6, CA-7)."],
                 "Govern the whole; test it, sign it, watch it.",
                 [["NOVA", "Notebook: this layer is the brain \u2014 it decides what the walls are even for."],
                  ["VEGA", "The realm is governed. Now, to where it's all built."],
                  ["NULL", "Built? I'll poison it at the source."],
                  ["VEGA", "Then we descend to the Forge."]]),
]

if __name__ == "__main__":
    L.write_spec("EP04", "the_high_council", beats, tag="EP04")

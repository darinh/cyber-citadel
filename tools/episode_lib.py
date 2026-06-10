"""Authoring helpers for Cyber Citadel episodes.

All control facts (titles, verbatim quotes, citations) are pulled from
course/data/truth.json (the OSCAL-derived truth layer) so on-screen content is
accurate by construction. Beat builders keep episode scripts terse.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRUTH = json.loads((ROOT / "course" / "data" / "truth.json").read_text(encoding="utf-8"))

# Guardian persona + metaphor ("guards") + real-world meaning ("reality").
PERSONAS = {
 "AC": ("The Gatekeeper", "Who may enter the city, and what they may touch.",
        "Policies and mechanisms that decide which users and processes may use which systems and data."),
 "AT": ("The Drillmaster", "Trains every citizen to spot a trick at the gate.",
        "Security and privacy awareness plus role-based training so people recognize and resist threats."),
 "AU": ("The Chronicler", "Records every footstep, so no deed goes unseen.",
        "Logging security-relevant events and being able to review them and hold actors accountable."),
 "CA": ("The Inspector", "Tests the defenses and signs off before the gates open.",
        "Assessing controls, formally authorizing systems to operate, and continuously monitoring them."),
 "CM": ("The Master of Blueprints", "Keeps the master plans and forbids unsanctioned change.",
        "Baseline configurations and change control so systems stay in a known, secure state."),
 "CP": ("The Keeper of Lifelines", "Plans for the day the towers fall, and how to rebuild.",
        "Backups, alternate sites, and tested plans to recover operations after a disruption."),
 "IA": ("The Seal-Bearer", "Proves you are who you claim, before you pass.",
        "Verifying the identity of users, devices, and processes before granting access."),
 "IR": ("The Firewatch", "Sounds the alarm and contains the blaze.",
        "Detecting, reporting, analyzing, containing, and recovering from security incidents."),
 "MA": ("The Smith", "Tends the machinery, and watches who holds the tools.",
        "Controlled system maintenance, including safeguards for remote and third-party maintenance."),
 "MP": ("The Steward of Scrolls", "Guards every scroll, and destroys the ones discarded.",
        "Protecting digital and physical media, and sanitizing it before disposal or reuse."),
 "PE": ("The Wall-Warden", "Holds the physical gates, and guards against fire and flood.",
        "Physical access controls plus protection from hazards like fire, power loss, and water."),
 "PL": ("The Cartographer", "Draws the map of the defense before the march.",
        "System security and privacy plans, rules of behavior, and security architecture."),
 "PM": ("The High Steward", "Governs the whole realm's defense, above any single wall.",
        "Organization-wide governance: the security and privacy program, roles, risk strategy, and resources."),
 "PS": ("The Oathkeeper", "Vets every guard, and reclaims the keys when they leave.",
        "Screening personnel and adjusting access on transfer or termination; insider-risk safeguards."),
 "PT": ("The Privacy Herald", "Protects citizens' personal stories, and tells them how they are used.",
        "Lawful, transparent processing of personally identifiable information, with consent and notice."),
 "RA": ("The Seer", "Reads the omens: what could go wrong, and how badly.",
        "Identifying and analyzing risk, including vulnerability scanning and threat assessment."),
 "SA": ("The Quartermaster", "Buys and builds only what can be trusted.",
        "Building security into the development life cycle and into systems and services you acquire."),
 "SC": ("The Warden of Walls and Roads", "Fortifies the ramparts and seals the roads between districts.",
        "Boundary protection and cryptography that protect data in transit and at rest."),
 "SI": ("The Healer", "Finds the rot, cures the sickness, keeps the truth true.",
        "Flaw remediation, malicious-code protection, system monitoring, and integrity verification."),
 "SR": ("The Caravan-Master", "Guards the roads your supplies travel, all the way to the source.",
        "Managing risk from suppliers, components, and the supply chain: authenticity and provenance."),
}

# A varied threat per family (real threat flavor + MITRE ATT&CK tactic/technique hook).
THREATS = {
 "AC": "a stolen login walks straight through an over-privileged account (Valid Accounts, T1078)",
 "IA": "an attacker reuses a leaked password because nothing proves who they really are (T1110)",
 "PE": "a 'delivery courier' tailgates through a propped-open door into the server hall",
 "AU": "an intruder deletes the logs to erase every trace (Indicator Removal, T1070)",
 "SI": "malware slips past and quietly corrupts files (Data Manipulation, T1565)",
 "IR": "the breach is found on day ninety because no one was ready to respond",
 "AT": "a staffer clicks a flawless phishing lure (Phishing, T1566)",
 "PS": "a departing admin keeps their access and walks out with the crown jewels (Insider, T1078)",
 "PT": "personal records are used for a purpose the citizens never agreed to",
 "RA": "an unscanned, unpatched service is the unseen crack in the wall",
 "PL": "defenders improvise with no plan, and the gaps show",
 "PM": "each district defends alone because no one governs the whole realm",
 "CA": "a system goes live unassessed, its weaknesses unknown until it is too late",
 "SA": "a vendor ships software with security bolted on as an afterthought",
 "CM": "one undocumented change opens a hole no one remembers making (T1505)",
 "MA": "a remote maintenance session becomes the attacker's back door",
 "SR": "a tampered component arrives pre-compromised from a sub-supplier (Supply Chain, T1195)",
 "SC": "secrets are sniffed off an unencrypted channel (Adversary-in-the-Middle, T1557)",
 "MP": "a lost backup drive spills its data because it was never encrypted or wiped",
 "CP": "ransomware detonates and there is no clean, tested backup to restore from",
}

LAYER_FAMILIES = {
    1: ["AC", "IA", "PE"], 2: ["AU", "SI", "IR"], 3: ["AT", "PS", "PT"],
    4: ["RA", "PL", "PM", "CA"], 5: ["SA", "CM", "MA", "SR"], 6: ["SC", "MP", "CP"],
}

# Spoken, first-person guardian oaths (mnemonics) — each encodes its flagship controls.
OATHS = {
 "AC": ("None pass unknown; none hold more than they need.", "AC-3 \u00b7 AC-6"),
 "IA": ("Prove the name, or the gate stays shut.", "IA-2"),
 "PE": ("A door is a decision \u2014 and I decide.", "PE-3"),
 "AU": ("Every footstep written; no page erased.", "AU-2 \u00b7 AU-9"),
 "SI": ("Find the rot, close the wound, keep it true.", "SI-2 \u00b7 SI-4 \u00b7 SI-7"),
 "IR": ("When it burns, we are already running.", "IR-4 \u00b7 IR-8"),
 "AT": ("The sharpest blade is an alert mind.", "AT-2"),
 "PS": ("Trust is earned at the gate, and returned at the door.", "PS-3 \u00b7 PS-4"),
 "PT": ("By what right, for what purpose, with whose leave?", "PT-2 \u00b7 PT-5"),
 "RA": ("I do not guess the storm; I measure it.", "RA-3 \u00b7 RA-5"),
 "PL": ("No march without a map.", "PL-2"),
 "PM": ("One realm, one strategy \u2014 always.", "PM-1 \u00b7 PM-9"),
 "CA": ("Test before you trust; watch after you sign.", "CA-2 \u00b7 CA-6 \u00b7 CA-7"),
 "SA": ("Built in, never sprinkled on.", "SA-8"),
 "CM": ("A known system is a defended system.", "CM-2 \u00b7 CM-7"),
 "MA": ("Every tool is a key, and I guard the keys.", "MA-2 \u00b7 MA-4"),
 "SR": ("I trust no part I cannot trace.", "SR-11"),
 "SC": ("Filter at the edge; cipher on the wire.", "SC-7 \u00b7 SC-8 \u00b7 SC-28"),
 "MP": ("When it's gone, it's gone for good.", "MP-6"),
 "CP": ("We rehearse the dark, so we survive it.", "CP-2 \u00b7 CP-4 \u00b7 CP-9"),
}

# Real, public 'breach of the week' cold opens (factual, neutral framing) + MITRE ATT&CK hook.
BREACHES = {
 "EP01": {"year": "2021",
          "headline": "One old password darkens a fuel pipeline.",
          "body": "Attackers signed into a forgotten VPN account that had no second "
                  "factor, and a pipeline serving much of the U.S. East Coast went offline. "
                  "Not a zero-day \u2014 just one unguarded door.",
          "mitre": "Valid Accounts \u00b7 T1078", "teaches": "IA-2 \u00b7 AC-2"},
 "EP02": {"year": "2017",
          "headline": "A missed patch, unseen for weeks.",
          "body": "A known flaw in a public web app went unpatched. With monitoring crippled by "
                  "an expired security certificate, the intrusion ran undetected for about 76 days "
                  "while data on roughly 147 million people was taken.",
          "mitre": "Exploit Public-Facing App \u00b7 T1190", "teaches": "SI-2 \u00b7 SI-4 \u00b7 AU-6"},
 "EP03": {"year": "2020",
          "headline": "They didn't hack the computer. They called the staff.",
          "body": "Attackers phoned employees, talked their way into an internal admin tool, "
                  "and hijacked high-profile accounts. The exploit was a person, not a port.",
          "mitre": "Phishing \u00b7 T1566", "teaches": "AT-2 \u00b7 PS-3"},
 "EP04": {"year": "2015",
          "headline": "Records of millions, taken on an unauthorized system.",
          "body": "Background-investigation files on about 21 million people were stolen. "
                  "Auditors had warned for years that key systems were running without a "
                  "current authorization to operate.",
          "mitre": "Governance failure \u00b7 no valid ATO", "teaches": "CA-6 \u00b7 RA-3"},
 "EP05": {"year": "2020",
          "headline": "The malware was shipped in, signed and trusted.",
          "body": "Attackers hid a backdoor inside a routine software update from a trusted "
                  "vendor; roughly 18,000 organizations installed it themselves. They didn't "
                  "break in \u2014 they were built in.",
          "mitre": "Supply Chain Compromise \u00b7 T1195.002", "teaches": "SR-11 \u00b7 SA-8 \u00b7 CM-2"},
 "EP06": {"year": "2017",
          "headline": "A wiper erases a global shipping line overnight.",
          "body": "Self-spreading malware destroyed tens of thousands of machines at a major "
                  "shipping company. It came back only because one backup happened to be "
                  "offline and out of reach during the attack.",
          "mitre": "Data Destruction \u00b7 T1485", "teaches": "CP-9 \u00b7 CP-2"},
}

CITADEL_ORDER = ["AC", "IA", "PE", "AU", "SI", "IR", "AT", "PS", "PT",
                 "RA", "PL", "PM", "CA", "SA", "CM", "MA", "SR", "SC", "MP", "CP"]


def fam_of(cid):
    return cid.split("-")[0]


def control(cid):
    return TRUTH[fam_of(cid)]["controls"][cid]


def title(cid):
    return control(cid)["title"]


def cite(cid):
    return f"NIST SP 800-53r5  \u00b7  {cid} {title(cid)}"


def verbatim(cid, snippet=None, maxlen=300):
    """Return a verbatim excerpt of the control statement (first sentence)."""
    flat = re.sub(r"\s+", " ", control(cid)["statement"]).strip()
    if snippet:
        return snippet  # validated as substring by verify_script.py
    m = re.search(r"^(.*?[\.;:])(\s|$)", flat)
    s = m.group(1) if m else flat
    if len(s) > maxlen:
        s = flat[:maxlen].rsplit(" ", 1)[0] + "\u2026"
    return s


def fam_name(fam):
    return TRUTH[fam]["name"]


# ---- beat builders -------------------------------------------------------

def b_title(badge, title_txt, subtitle, say, kicker="A NIST SP 800-53r5 TRAINING SERIES"):
    return {"scene": "title", "kicker": kicker, "badge": badge, "title": title_txt,
            "subtitle": subtitle, "say": say, "min_seconds": 4}


def b_section(num, title_txt, subtitle, say):
    return {"scene": "section", "num": num, "title": title_txt, "subtitle": subtitle, "say": say}


def b_map(title_txt, highlight, say, deps=None, subtitle=""):
    return {"scene": "map", "title": title_txt, "highlight": highlight,
            "deps": deps or [], "subtitle": subtitle, "say": say}


def b_guardian(fam, say):
    persona, guards, reality = PERSONAS[fam]
    return {"scene": "guardian", "family": fam, "family_name": fam_name(fam),
            "persona": persona, "protects": guards, "reality": reality, "say": say}


def b_control(cid, plain, why, say):
    return {"scene": "control", "id": cid, "title": title(cid), "plain": plain, "why": why, "say": say}


def b_quote(cid, say, snippet=None):
    return {"scene": "quote", "quote": verbatim(cid, snippet), "cite": cite(cid), "say": say}


def b_diagram(title_txt, nodes, arrows, say):
    return {"scene": "diagram", "title": title_txt, "nodes": nodes, "arrows": arrows, "say": say}


def b_quiz(q, options, answer, say, min_seconds=7):
    return {"scene": "quiz", "q": q, "options": options, "answer": answer,
            "reveal": True, "say": say, "min_seconds": min_seconds}


def b_points(title_txt, bullets, say, kicker="KEY POINTS", note=""):
    return {"scene": "points", "title": title_txt, "bullets": bullets,
            "kicker": kicker, "note": note, "say": say}


def b_cheatcard(fam, bullets, mnemonic, say):
    return {"scene": "cheatcard", "family": fam, "title": fam_name(fam),
            "bullets": bullets, "mnemonic": mnemonic, "say": say}


def b_define(term, plain, say, expand=None, example=None, cite=None,
             kicker="PLAIN ENGLISH", min_seconds=6.5):
    """A beginner definition card: term, optional acronym expansion, plain meaning, example."""
    return {"scene": "define", "term": term, "expand": expand, "plain": plain,
            "example": example, "cite": cite, "kicker": kicker, "say": say,
            "min_seconds": min_seconds}


def b_coldopen(fam_or_ep, say, min_seconds=7.0):
    """A real-incident 'breach of the week' cold open (keyed by EP id in BREACHES)."""
    b = dict(BREACHES[fam_or_ep])
    b.update({"scene": "coldopen", "say": say, "min_seconds": min_seconds})
    return b


def b_oath(fam, say, min_seconds=4.5):
    oath, controls = OATHS[fam]
    return {"scene": "oath", "family": fam, "oath": oath, "controls": controls,
            "say": say, "min_seconds": min_seconds}


def b_notebook(title_txt, lines, mnemonic, say, min_seconds=5.0):
    """Nova's notebook recap page (friendly takeaways + the mnemonic)."""
    return {"scene": "notebook", "title": title_txt, "lines": lines,
            "mnemonic": mnemonic, "say": say, "min_seconds": min_seconds}


def cheat_bullet(cid, gloss):
    return f"{cid} {title(cid)} \u2014 {gloss}"


def write_spec(epid, slug, beats, tag=None):
    spec = {"id": epid, "tag": tag or epid, "slug": slug, "beats": beats}
    out = ROOT / "course" / "scripts" / f"{epid.lower()}.json"
    out.write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out} ({len(beats)} beats)")
    return out

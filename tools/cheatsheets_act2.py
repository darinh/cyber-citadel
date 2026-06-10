"""Act II process cheat sheets (RMF, categorization, baselines, assessment).

Reuses the portrait cheat-sheet style from cheatsheets.py. Facts mirror the
Act II episodes (and baseline counts come from the official 800-53B profiles).
"""
import sys
from pathlib import Path
from PIL import ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cheatsheets as C
import scene as S

INK, MUTED, GOLD = S.INK, S.MUTED, S.GOLD

SHEETS = [
    ("campaign_1_the_rmf", "The Risk Management Framework", "NIST SP 800-37, Rev 2", S.CYAN, [
        ("1 · Prepare", "Set organization + system context, roles, and risk strategy"),
        ("2 · Categorize", "Determine the impact level \u2014 FIPS 199, SP 800-60"),
        ("3 · Select", "Choose a control baseline (SP 800-53B) and tailor it"),
        ("4 · Implement", "Put the SP 800-53 controls to work"),
        ("5 · Assess", "Verify the controls work \u2014 SP 800-53A"),
        ("6 · Authorize", "An authorizing official accepts the risk \u2014 the ATO"),
        ("7 · Monitor", "Ongoing awareness across the lifecycle \u2014 SP 800-137"),
    ], "A continuous lifecycle. \u201CPrepare\u201D was added in Revision 2 (2018)."),

    ("campaign_2_categorization", "Security Categorization", "FIPS 199 / 200 \u00b7 SP 800-60", GOLD, [
        ("Confidentiality", "Impact if information is disclosed"),
        ("Integrity", "Impact if information is altered or destroyed"),
        ("Availability", "Impact if access to the system is disrupted"),
        ("Impact levels", "Rate each objective Low, Moderate, or High"),
        ("High-water mark", "System category = the HIGHEST of the three"),
        ("SP 800-60", "Maps information types to impact levels"),
        ("FIPS 200", "Minimum requirements; mandates SP 800-53 (control RA-2)"),
    ], "Example: C = Moderate, I = Low, A = High  \u2192  the system is HIGH."),

    ("campaign_3_baselines", "Baselines & Tailoring", "NIST SP 800-53B", S.MINT, [
        ("Low baseline", "149 controls + enhancements (131 base controls)"),
        ("Moderate baseline", "287 controls + enhancements (177 base)"),
        ("High baseline", "370 controls + enhancements (188 base)"),
        ("Privacy baseline", "96 controls \u2014 for systems processing PII"),
        ("Tailoring", "Scope out, use compensating controls, set parameters, supplement"),
        ("Overlays", "Ready-made tailored baselines for a community (cloud, classified)"),
    ], "Your FIPS 199 level selects the security baseline. PM is org-wide, not in baselines."),

    ("campaign_4_assess_authorize", "Assess · Authorize · Monitor", "SP 800-53A \u00b7 SP 800-137", S.MAGENTA, [
        ("Examine", "Review documents, designs, and configurations"),
        ("Interview", "Talk to the people who run the controls"),
        ("Test", "Exercise the system to observe real behavior"),
        ("SAR", "Security Assessment Report \u2014 the findings"),
        ("POA&M", "Plan of Action & Milestones \u2014 track open gaps (CA-5)"),
        ("ATO", "Authorization to Operate \u2014 accept the risk (CA-6)"),
        ("Monitor", "Continuous monitoring, never-ending watch (CA-7, SP 800-137)"),
    ], "Examine / Interview / Test are the three SP 800-53A assessment methods."),
]


def render(name, title, doc, col, rows, note):
    img = C.bg()
    d = ImageDraw.Draw(img, "RGBA")
    M = 90
    d.rectangle([0, 0, C.PW, 14], fill=col)
    S.tracked_text(d, (M, 70), "CYBER CITADEL  \u00b7  CHEAT SHEET", S.FSB(26), col, tracking=6)
    d.text((M, 150), title, font=S.FB(58), fill=INK)
    d.text((M, 232), doc, font=S.FSL(38), fill=GOLD)
    d.line([(M, 320), (C.PW - M, 320)], fill=(255, 255, 255, 40), width=2)
    y = 370
    for term, gloss in rows:
        C.rrect(d, [M, y, M + 430, y + 92], 14, col, 2, fill=(col[0] // 6, col[1] // 6, col[2] // 6, 255))
        S.draw_wrapped(d, (M + 24, y + 14), term, S.FB(34), col, 400, 1.05)
        S.draw_wrapped(d, (M + 470, y + 12), gloss, S.FSB(32), INK, C.PW - (M + 470) - M, 1.22)
        y += 112
    fy = C.PH - 200
    d.line([(M, fy), (C.PW - M, fy)], fill=(255, 255, 255, 40), width=2)
    S.tracked_text(d, (M, fy + 24), "REMEMBER", S.FSB(24), GOLD, tracking=5)
    S.draw_wrapped(d, (M, fy + 58), note, S.FSB(36), GOLD, C.PW - 2 * M, 1.2)
    d.text((M, C.PH - 70), "An educational aid \u2014 always consult the NIST publications", font=S.MONO(24), fill=MUTED)
    out = C.OUT / f"{name}.png"
    img.convert("RGB").save(out, quality=95)
    return out


if __name__ == "__main__":
    for s in SHEETS:
        print("sheet:", render(*s).name)

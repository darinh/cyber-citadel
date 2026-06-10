"""Package the course: transcripts, quizzes.json, SRT->VTT, and index.html player."""
from __future__ import annotations
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "course" / "scripts"
EPISODES = ROOT / "course" / "episodes"
TRANSCRIPTS = ROOT / "course" / "transcripts"
CHEATS = ROOT / "course" / "cheatsheets"
TRANSCRIPTS.mkdir(parents=True, exist_ok=True)

META = [
    ("ep00", "the_citadel_awakens", "00", "The Citadel Awakens", "Orientation",
     "What 800-53 is, why it exists, how to read a control, why baselines moved to 800-53B, and where it all fits in the RMF."),
    ("ep01", "the_outer_walls", "01", "The Outer Walls", "AC \u00b7 IA \u00b7 PE",
     "Who gets in, and what they may touch: access control, identity, and physical security."),
    ("ep02", "the_watchtowers", "02", "The Watchtowers", "AU \u00b7 SI \u00b7 IR",
     "See the intruder, keep the system honest, and respond: audit, integrity, incident response."),
    ("ep03", "the_keepers_of_the_pact", "03", "The Keepers of the Pact", "AT \u00b7 PS \u00b7 PT",
     "People and privacy: awareness training, personnel security, and PII processing & transparency."),
    ("ep04", "the_high_council", "04", "The High Council", "RA \u00b7 PL \u00b7 PM \u00b7 CA",
     "Govern and assess: risk assessment, planning, program management, and assessment & authorization."),
    ("ep05", "the_forge", "05", "The Forge", "SA \u00b7 CM \u00b7 MA \u00b7 SR",
     "Build, configure, maintain, and source securely, including the supply chain."),
    ("ep06", "the_vaults_and_lifelines", "06", "The Vaults & Lifelines", "SC \u00b7 MP \u00b7 CP",
     "Protect the data and survive disaster: communications protection, media protection, contingency planning."),
    ("ep07", "siege_night", "07", "Siege Night", "All 20 + RMF",
     "Act I finale: defense in depth, the full RMF at a glance, and how 800-53 gets used in practice."),
    ("ep7b", "the_campaign_briefing", "7B", "The Campaign Briefing", "Worked Example \u00b7 Aegis Hospital",
     "One real system walked end to end through the RMF \u2014 categorize, select, tailor, implement, assess, authorize, monitor \u2014 with a named human cast (System Owner, AO, ISSO, Privacy Officer, Assessor)."),
    ("ep08", "the_campaign_rmf", "08", "The Campaign: the RMF", "SP 800-37r2",
     "Act II begins. The 7-step Risk Management Framework and how the NIST document family fits together."),
    ("ep09", "know_your_realm", "09", "Know Your Realm", "FIPS 199/200 \u00b7 800-60",
     "Security categorization: rating Confidentiality/Integrity/Availability, the high-water mark, minimum requirements."),
    ("ep10", "the_armory_baselines", "10", "The Armory: Baselines", "SP 800-53B",
     "Control baselines (Low 149 / Moderate 287 / High 370 / Privacy 96) and how to tailor them with overlays."),
    ("ep11", "the_reckoning", "11", "The Reckoning", "800-53A \u00b7 800-137",
     "Assessment methods (examine/interview/test), the SAR and POA&M, authorization (ATO), continuous monitoring."),
]


def fmt_dur(sec):
    m, s = divmod(int(round(sec)), 60)
    return f"{m}:{s:02d}"


def probe(path):
    if not path.exists():
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return None


def srt_to_vtt(srt, vtt):
    txt = srt.read_text(encoding="utf-8")
    txt = re.sub(r"(\d\d:\d\d:\d\d),(\d\d\d)", r"\1.\2", txt)
    vtt.write_text("WEBVTT\n\n" + txt, encoding="utf-8")


def _onscreen(b):
    """Render a beat's ON-SCREEN text (not just spoken lines) for the transcript."""
    sc = b.get("scene"); out = []
    def head(label, txt):
        if txt:
            out.append(f"*[{label}: {txt}]*")
    if sc in ("title", "section"):
        head("TITLE", " \u2014 ".join(x for x in [b.get("badge") or b.get("num"), b.get("title"), b.get("subtitle")] if x))
    elif sc == "map":
        head("MAP", b.get("title"))
    elif sc == "guardian":
        head("GUARDIAN", f"{b.get('family')} {b.get('family_name')} \u2014 \u201C{b.get('persona')}\u201D")
        if b.get("protects"): out.append(f"  guards: {b['protects']}")
        if b.get("reality"): out.append(f"  in reality: {b['reality']}")
    elif sc == "control":
        head("CONTROL", f"{b.get('id')} {b.get('title')}")
        if b.get("plain"): out.append(f"  what it means: {b['plain']}")
        if b.get("why"): out.append(f"  why it matters: {b['why']}")
    elif sc == "quote":
        out.append(f"*[VERBATIM] \u201C{b.get('quote','')}\u201D \u2014 {b.get('cite','')}*")
    elif sc == "define":
        head("PLAIN ENGLISH", b.get("term"))
        if b.get("expand"): out.append(f"  stands for: {b['expand']}")
        if b.get("plain"): out.append(f"  meaning: {b['plain']}")
        if b.get("example"): out.append(f"  everyday example: {b['example']}")
    elif sc == "coldopen":
        head("BREACH OF THE WEEK", f"{b.get('year','')} \u2014 {b.get('headline','')}")
        if b.get("body"): out.append(f"  {b['body']}")
        if b.get("mitre"): out.append(f"  MITRE ATT&CK: {b['mitre']}")
    elif sc == "oath":
        out.append(f"*[GUARDIAN OATH \u2014 {b.get('family')}] \u201C{b.get('oath','')}\u201D ({b.get('controls','')})*")
    elif sc == "diagram":
        head("DIAGRAM", b.get("title"))
        labels = " \u2192 ".join(n.get("label", "").replace("\n", " ") for n in b.get("nodes", []))
        if labels: out.append(f"  {labels}")
    elif sc in ("points", "notebook"):
        head("NOTEBOOK" if sc == "notebook" else (b.get("kicker") or "KEY POINTS"), b.get("title"))
        for it in b.get("bullets", b.get("lines", [])):
            out.append(f"  \u2022 {it}")
        if b.get("mnemonic"): out.append(f"  remember: {b['mnemonic']}")
    elif sc == "cheatcard":
        head("CHEAT CARD", b.get("title"))
        for it in b.get("bullets", []):
            out.append(f"  \u2022 {it}")
        if b.get("mnemonic"): out.append(f"  remember: {b['mnemonic']}")
    elif sc == "quiz":
        out.append(f"*[QUIZ] {b.get('q','')}*")
        for i, opt in enumerate(b.get("options", [])):
            mark = " (answer)" if i == b.get("answer") else ""
            out.append(f"  {chr(65+i)}. {opt}{mark}")
    return out


def build_transcripts_and_quizzes():
    quizzes = []
    for epid, slug, num, title, fams, syn in META:
        sp = SCRIPTS / f"{epid}.json"
        if not sp.exists():
            continue
        spec = json.loads(sp.read_text(encoding="utf-8"))
        # transcript: on-screen text + spoken lines, beat by beat
        lines = [f"# {title}  ({num})", f"*{fams} \u2014 {syn}*", ""]
        for b in spec["beats"]:
            for ln in _onscreen(b):
                lines.append(ln)
            for sp_, tx in b.get("say", []):
                lines.append(f"**{sp_}:** {tx}")
            lines.append("")
        (TRANSCRIPTS / f"{epid}.md").write_text("\n".join(lines), encoding="utf-8")
        # quizzes
        for b in spec["beats"]:
            if b.get("scene") == "quiz":
                quizzes.append({"ep": num, "epTitle": title, "q": b["q"],
                                "options": b["options"], "answer": b["answer"]})
    (ROOT / "course" / "quizzes.json").write_text(json.dumps(quizzes, indent=1, ensure_ascii=False), encoding="utf-8")
    return quizzes


def build_manifest():
    eps = []
    for epid, slug, num, title, fams, syn in META:
        mp4 = EPISODES / f"{epid}_{slug}.mp4"
        if not mp4.exists():
            continue
        nq = 0
        cf = EPISODES / f"{epid}.cues.json"
        if cf.exists():
            try:
                nq = len(json.loads(cf.read_text(encoding="utf-8")).get("quizzes", []))
            except Exception:
                nq = 0
        eps.append({"id": epid, "num": num, "title": title, "families": fams,
                    "synopsis": syn, "video": f"course/episodes/{epid}_{slug}.mp4",
                    "cues": f"course/episodes/{epid}.cues.json", "quizzes": nq})
    (EPISODES / "manifest.json").write_text(json.dumps(eps, indent=1, ensure_ascii=False), encoding="utf-8")
    print("wrote manifest.json |", len(eps), "episodes")
    return eps


def build_index(quizzes):
    cards = []
    for epid, slug, num, title, fams, syn in META:
        mp4 = EPISODES / f"{epid}_{slug}.mp4"
        srt = EPISODES / f"{epid}_{slug}.srt"
        vtt = EPISODES / f"{epid}_{slug}.vtt"
        if srt.exists():
            srt_to_vtt(srt, vtt)
        dur = probe(mp4)
        durtxt = fmt_dur(dur) if dur else "&mdash;"
        rel = f"course/episodes/{epid}_{slug}.mp4"
        # Captions are baked into the video; do NOT attach a soft subtitle track
        # (it would double up and some players force-show track 1). VTT stays on disk.
        video = (f'<video controls preload="none" poster="">'
                 f'<source src="{rel}" type="video/mp4"></video>') if mp4.exists() else \
                '<div class="missing">video renders to this folder</div>'
        cards.append(f'''
      <article class="ep">
        <div class="epmedia">{video}</div>
        <div class="epbody">
          <div class="epnum">EP {num} &middot; <span class="fams">{fams}</span> &middot; <span class="dur">{durtxt}</span></div>
          <h3>{title}</h3>
          <p>{syn}</p>
          <a class="tx" href="course/transcripts/{epid}.md">Transcript</a>
        </div>
      </article>''')

    sheets = sorted([p.name for p in CHEATS.glob("*.png")])
    chips = "".join(f'<a class="sheet" href="course/cheatsheets/{n}"><img loading="lazy" src="course/cheatsheets/{n}" alt="{n}"></a>' for n in sheets)

    html = TEMPLATE
    html = html.replace("/*CARDS*/", "".join(cards))
    html = html.replace("/*SHEETS*/", chips)
    html = html.replace("/*QUIZ*/", json.dumps(quizzes, ensure_ascii=False))
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("wrote index.html  |", len(cards), "episodes,", len(sheets), "cheat sheets,", len(quizzes), "quiz questions")
    # link check: every local src/href must resolve from repo root
    missing = []
    for m in re.finditer(r'(?:src|href)="([^"#:]+)"', html):
        ref = m.group(1)
        if ref.startswith("http") or ref.startswith("data:"):
            continue
        if not (ROOT / ref).exists():
            missing.append(ref)
    if missing:
        print("  !! BROKEN LINKS:", sorted(set(missing)))
    else:
        print("  link check: all local references resolve \u2713")


TEMPLATE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cyber Citadel &mdash; NIST SP 800-53r5 Training</title>
<style>
:root{--bg:#080b1e;--bg2:#101636;--ink:#e8ecff;--mut:#8a93c2;--cy:#38e1ff;--go:#ffc857;--mg:#ff3cac;--mint:#5eead4}
*{box-sizing:border-box}body{margin:0;font-family:'Segoe UI',system-ui,Arial,sans-serif;background:linear-gradient(180deg,#080b1e,#101636);color:var(--ink);line-height:1.55}
a{color:var(--cy);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
header.hero{padding:70px 0 30px;text-align:center;border-bottom:1px solid #ffffff18}
.kick{letter-spacing:.35em;color:var(--mg);font-weight:700;font-size:14px}
h1{font-size:64px;margin:.15em 0;letter-spacing:.04em;text-shadow:0 0 30px #38e1ff55}
.sub{color:var(--mut);font-size:22px}
.disc{margin:18px auto 0;max-width:760px;color:var(--mut);font-size:14px;background:#ffffff0a;border:1px solid #ffffff14;border-radius:12px;padding:12px 16px}
section{padding:46px 0}h2{font-size:30px;letter-spacing:.02em;border-left:4px solid var(--cy);padding-left:14px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:24px}
@media(max-width:820px){.grid{grid-template-columns:1fr}h1{font-size:42px}}
.ep{background:#0e142f;border:1px solid #ffffff14;border-radius:16px;overflow:hidden;display:flex;flex-direction:column}
.epmedia{background:#05071a;aspect-ratio:16/9}.epmedia video{width:100%;height:100%;display:block;background:#05071a}
.missing{display:flex;align-items:center;justify-content:center;height:100%;color:var(--mut);font-size:14px}
.epbody{padding:16px 18px 20px}.epnum{color:var(--cy);font-size:13px;letter-spacing:.08em;font-weight:700}
.fams{color:var(--go)}.dur{color:var(--mut)}
.ep h3{margin:.3em 0 .2em;font-size:23px}.ep p{color:var(--mut);font-size:15px;margin:.2em 0 .8em}
.tx{font-size:13px;letter-spacing:.05em}
.sheets{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}
.sheet{width:128px;border:1px solid #ffffff14;border-radius:8px;overflow:hidden;background:#0e142f}
.sheet img{width:100%;display:block}
.map{display:block;max-width:760px;margin:22px auto 0;border:1px solid #ffffff14;border-radius:14px}
.quiz{background:#0e142f;border:1px solid #ffffff14;border-radius:16px;padding:22px;margin-top:20px}
.q{margin:0 0 10px;font-size:19px}.opt{display:block;width:100%;text-align:left;margin:7px 0;padding:12px 16px;border-radius:10px;border:1px solid #2a3257;background:#121937;color:var(--ink);font-size:15px;cursor:pointer}
.opt:hover{border-color:var(--cy)}.opt.ok{border-color:var(--mint);background:#10312b}.opt.no{border-color:var(--mg);background:#311022}
.qmeta{color:var(--cy);font-size:12px;letter-spacing:.08em;font-weight:700}
.navbtns{display:flex;justify-content:space-between;margin-top:14px}.navbtns button{background:#1a2350;color:var(--ink);border:1px solid #2a3257;border-radius:10px;padding:10px 18px;cursor:pointer}
footer{padding:50px 0;text-align:center;color:var(--mut);border-top:1px solid #ffffff18}
.layers{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}
@media(max-width:820px){.layers{grid-template-columns:1fr}}
.layer{background:#0e142f;border:1px solid #ffffff14;border-radius:12px;padding:14px 16px}
.layer b{color:var(--cy)}.layer .f{color:var(--go);font-family:Consolas,monospace}
</style></head><body>
<header class="hero"><div class="wrap">
  <div class="kick">A NIST SP 800-53r5 TRAINING SERIES</div>
  <h1>CYBER CITADEL</h1>
  <div class="sub">The Twenty Guardians &mdash; learn federal security &amp; privacy controls the fun way</div>
  <p style="margin:22px 0 6px"><a href="watch.html" style="display:inline-block;background:var(--cy);color:#04121a;font-weight:700;padding:14px 34px;border-radius:12px;font-size:18px">&#9654;&nbsp; Launch the interactive course</a></p>
  <div class="disc">An educational aid that dramatizes NIST SP 800-53 Revision 5 (and the wider Risk Management Framework) as a besieged digital city. On-screen control IDs, titles, and gold quotes are taken verbatim from the official catalog. This is <b>not</b> a substitute for the standard &mdash; always consult the NIST publications for real decisions.</div>
</div></header>

<section class="wrap"><h2>Watch the series</h2>
  <div class="grid">/*CARDS*/</div>
</section>

<section class="wrap"><h2>The map &mdash; six layers, twenty guardians</h2>
  <img class="map" src="course/cheatsheets/00_MASTER_the_twenty_guardians.png" alt="The twenty guardians">
  <div class="layers">
    <div class="layer"><b>1 &middot; Outer Walls</b><br><span class="f">AC IA PE</span><br>Who gets in</div>
    <div class="layer"><b>2 &middot; Watchtowers</b><br><span class="f">AU SI IR</span><br>See &amp; respond</div>
    <div class="layer"><b>3 &middot; Keepers of the Pact</b><br><span class="f">AT PS PT</span><br>People &amp; privacy</div>
    <div class="layer"><b>4 &middot; High Council</b><br><span class="f">RA PL PM CA</span><br>Govern &amp; assess</div>
    <div class="layer"><b>5 &middot; The Forge</b><br><span class="f">SA CM MA SR</span><br>Build &amp; supply</div>
    <div class="layer"><b>6 &middot; Vaults &amp; Lifelines</b><br><span class="f">SC MP CP</span><br>Protect &amp; recover</div>
  </div>
</section>

<section class="wrap"><h2>Cheat sheets &mdash; one page per family</h2>
  <div class="sheets">/*SHEETS*/</div>
</section>

<section class="wrap"><h2>Guardian Roll Call &mdash; test yourself</h2>
  <div class="quiz" id="quiz">
    <div class="qmeta" id="qmeta"></div>
    <p class="q" id="qtext"></p>
    <div id="qopts"></div>
    <div class="navbtns"><button onclick="prevQ()">&larr; Prev</button>
      <span id="score" style="align-self:center;color:var(--mut)"></span>
      <button onclick="nextQ()">Next &rarr;</button></div>
  </div>
</section>

<footer class="wrap">Cyber Citadel &middot; a locally-produced training series &middot; the story is ours, the controls are real.<br>
Always consult <a href="https://doi.org/10.6028/NIST.SP.800-53r5">NIST SP 800-53r5</a> and SP 800-53B.</footer>

<script>
const QZ=/*QUIZ*/;let qi=0,correct=0,seen=0,done={},answered=false;
function render(){const q=QZ[qi];document.getElementById('qmeta').textContent='EP '+q.ep+' \u00b7 '+q.epTitle+'  ('+(qi+1)+'/'+QZ.length+')';
document.getElementById('qtext').textContent=q.q;const o=document.getElementById('qopts');o.innerHTML='';answered=false;
q.options.forEach((opt,i)=>{const b=document.createElement('button');b.className='opt';b.textContent=String.fromCharCode(65+i)+'.  '+opt;
b.onclick=()=>{if(answered)return;answered=true;if(!done[qi]){done[qi]=1;seen++;if(i===q.answer)correct++;}[...o.children].forEach((c,j)=>{if(j===q.answer)c.classList.add('ok');else if(j===i)c.classList.add('no');});
document.getElementById('score').textContent=(i===q.answer?'Correct!':'Answer: '+String.fromCharCode(65+q.answer))+'   \u00b7   Score '+correct+'/'+seen;};o.appendChild(b);});
document.getElementById('score').textContent='Score '+correct+'/'+seen;}
function nextQ(){qi=(qi+1)%QZ.length;render();}function prevQ(){qi=(qi-1+QZ.length)%QZ.length;render();}
render();
// Captions are baked into the videos; force every soft text track OFF (defensive).
function killTracks(v){try{const t=v.textTracks||[];for(let i=0;i<t.length;i++)t[i].mode='disabled';}catch(e){}}
document.querySelectorAll('video').forEach(v=>{killTracks(v);v.addEventListener('loadedmetadata',()=>killTracks(v));v.addEventListener('play',()=>killTracks(v));});
</script>
</body></html>"""


if __name__ == "__main__":
    qz = build_transcripts_and_quizzes()
    build_manifest()
    build_index(qz)

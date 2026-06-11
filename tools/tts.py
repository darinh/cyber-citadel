"""Piper TTS engine with acronym/ID pronunciation pre-processing + loudness
normalization + per-character voice effects. Produces normalized 22050 Hz mono
WAVs the episode assembler stitches together.

Council-mandated: pronounce NIST/CISO/RMF/control-IDs correctly; normalize loudness.
The pre-processor is applied ONLY to spoken narration, never to on-screen text.
"""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICES = ROOT / "tools" / "voices"

# Character -> piper voice model
SPEAKER_VOICE = {
    "NARRATOR": "en_GB-alan-medium",
    "VEGA": "en_US-ryan-high",
    "NOVA": "en_US-amy-medium",
    "ARCHIVIST": "en_US-lessac-medium",
    "NULL": "en_US-hfc_male-medium",
    "HERALD": "en_GB-jenny_dioco-medium",
}
# Per-speaker pace (piper length-scale; >1 = slower) and ffmpeg post-effect.
SPEAKER_LENGTH = {"ARCHIVIST": 1.06, "NULL": 1.12, "NARRATOR": 1.0,
                  "VEGA": 0.98, "NOVA": 1.0, "HERALD": 1.0}

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def n2w(n: int) -> str:
    n = int(n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])
    if n < 1000:
        return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + n2w(n % 100))
    return str(n)

ACRONYMS = {
    "NIST": "nisst", "FISMA": "fizmuh", "FedRAMP": "fed ramp", "CISO": "see-so",
    "OSCAL": "oss-cal", "FIPS": "fips", "RMF": "R-M-F", "PII": "P-I-I",
    "POA&M": "po-a-and-em", "SIEM": "sim", "MFA": "M-F-A", "VPN": "V-P-N",
    "ATT&CK": "attack", "MITRE": "MY-ter", "SP": "S-P", "IoT": "I-O-T",
    "USB": "U-S-B", "DNS": "D-N-S", "TLS": "T-L-S", "PKI": "P-K-I",
    "APT": "A-P-T", "SDLC": "S-D-L-C", "ID": "I-D",
}

# Document number forms (process before generic patterns). No "dash"; numbers
# use spaces (hyphens are converted to spaces at the end of preprocess anyway).
DOC_FORMS = [
    (re.compile(r"\b800-53r5\b"), "eight hundred fifty three, revision five"),
    (re.compile(r"\b800-53B\b"), "eight hundred fifty three B"),
    (re.compile(r"\b800-53A\b"), "eight hundred fifty three A"),
    (re.compile(r"\b800-53\b"), "eight hundred fifty three"),
    (re.compile(r"\b800-37r2\b"), "eight hundred thirty seven, revision two"),
    (re.compile(r"\b800-37\b"), "eight hundred thirty seven"),
    (re.compile(r"\b800-30\b"), "eight hundred thirty"),
    (re.compile(r"\b800-39\b"), "eight hundred thirty nine"),
    (re.compile(r"\b800-18\b"), "eight hundred eighteen"),
    (re.compile(r"\b800-60\b"), "eight hundred sixty"),
    (re.compile(r"\b800-137\b"), "eight hundred one thirty seven"),
    (re.compile(r"\b800-160\b"), "eight hundred one sixty"),
    (re.compile(r"\b800-171\b"), "eight hundred one seventy one"),
    (re.compile(r"\bFIPS\s*199\b"), "fips one ninety nine"),
    (re.compile(r"\bFIPS\s*200\b"), "fips two hundred"),
]

# Phonetic spelling of the 20 family codes so TTS says the letters correctly.
FAMILY_SAY = {
    "AC": "ay see", "AT": "ay tee", "AU": "ay you", "CA": "see ay", "CM": "see em",
    "CP": "see pee", "IA": "eye ay", "IR": "eye are", "MA": "em ay", "MP": "em pee",
    "PE": "pee ee", "PL": "pee el", "PM": "pee em", "PS": "pee ess", "PT": "pee tee",
    "RA": "are ay", "SA": "ess ay", "SC": "ess see", "SI": "ess eye", "SR": "ess are",
}

ID_RE = re.compile(r"\b([A-Z]{2})-(\d{1,2})(?:\((\d{1,2})\))?")


def _id_repl(m):
    fam = FAMILY_SAY.get(m.group(1), " ".join(m.group(1)))
    out = f"{fam} {n2w(m.group(2))}"
    if m.group(3):
        out += f", enhancement {n2w(m.group(3))}"
    return out


def preprocess(text: str) -> str:
    """Make narration text speakable. Applies to spoken lines only."""
    for rx, rep in DOC_FORMS:
        text = rx.sub(rep, text)
    text = ID_RE.sub(_id_repl, text)            # AC-6 -> "ay see six"
    for ac, rep in ACRONYMS.items():
        text = re.sub(r"\b" + re.escape(ac) + r"\b", rep, text)
    # Lowercase ALL-CAPS *emphasis* words (HIGH, WHAT, HOW, LOW, MODERATE...) so the model
    # SAYS them instead of spelling them letter-by-letter. Real acronyms/codes are protected
    # (already substituted above, or in KEEP) so they're unaffected.
    _KEEP = set(ACRONYMS) | set(FAMILY_SAY) | {
        "SP", "SAR", "ATO", "POA", "PII", "MFA", "VPN", "DNS", "TLS", "PKI", "APT",
        "SDLC", "FIPS", "CISO", "NIST", "FISMA", "RMF", "OSCAL", "IOT", "USB", "ID"}
    text = re.sub(r"\b[A-Z][A-Z]+\b",
                  lambda m: m.group(0) if m.group(0) in _KEEP else m.group(0).capitalize(), text)
    # Rev N -> revision N
    text = re.sub(r"\bRev\.?\s*(\d)\b", lambda m: "revision " + n2w(m.group(1)), text)
    text = text.replace(" — ", ", ").replace("—", ", ").replace(" – ", ", ")
    text = text.replace("-", " ")               # any remaining hyphens -> spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def piper_raw(speaker: str, text: str, out_wav: Path):
    voice = SPEAKER_VOICE.get(speaker, "en_US-lessac-medium")
    model = VOICES / f"{voice}.onnx"
    ls = SPEAKER_LENGTH.get(speaker, 1.0)
    p = subprocess.run([sys.executable, "-m", "piper", "-m", str(model),
                        "-f", str(out_wav), "--length-scale", str(ls)],
                       input=preprocess(text).encode("utf-8"),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if p.returncode != 0 or not out_wav.exists():
        raise RuntimeError(f"piper failed for {speaker}: {text[:60]}")


def _effect_chain(speaker: str) -> str:
    base = "loudnorm=I=-16:TP=-1.5:LRA=11"
    if speaker == "NULL":
        # menacing: pitch down, echo, lowpass
        return ("asetrate=22050*0.86,aresample=22050,atempo=1.0,"
                "aecho=0.8:0.85:55:0.35,lowpass=f=3400," + base)
    if speaker == "ARCHIVIST":
        return "highpass=f=90," + base
    return base


def synth_line(speaker: str, text: str, out_wav: Path) -> float:
    """Synthesize + normalize a single line. Returns duration in seconds."""
    out_wav = Path(out_wav)
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_wav.with_suffix(".raw.wav")
    piper_raw(speaker, text, tmp)
    _run(["ffmpeg", "-y", "-i", str(tmp), "-ar", "22050", "-ac", "1",
          "-af", _effect_chain(speaker), str(out_wav)])
    tmp.unlink(missing_ok=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration", "-of", "csv=p=0", str(out_wav)],
                         capture_output=True, text=True).stdout.strip()
    return float(dur)


if __name__ == "__main__":
    # Quick demo: synthesize a short multi-voice exchange for a listening test.
    tmp = ROOT / "tools" / "_tmp" / "ttstest"
    lines = [
        ("NARRATOR", "Welcome to the Cyber Citadel, a training series on NIST SP 800-53r5."),
        ("VEGA", "I'm Vega. Twenty guardians defend this city. First up: AC-6, Least Privilege."),
        ("NOVA", "So that's giving people only the access they actually need?"),
        ("ARCHIVIST", "Employ the principle of least privilege, allowing only authorized accesses."),
        ("NULL", "Your walls will fall. I am the Null."),
    ]
    for i, (sp, tx) in enumerate(lines):
        print(f"[{sp}] pre> {preprocess(tx)}")
        d = synth_line(sp, tx, tmp / f"{i:02d}_{sp}.wav")
        print(f"   -> {d:.2f}s")
    print("wrote test wavs to", tmp)

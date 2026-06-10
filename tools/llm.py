"""Reusable local-LLM (ollama) caller used for drafting + adversarial review.

Usage:
  from llm import ask
  text = ask("gpt-oss:120b", prompt, system="...", temperature=0.7)
"""
import json
import sys
import urllib.request

OLLAMA = "http://localhost:11434/api/generate"


def ask(model: str, prompt: str, system: str = "", temperature: float = 0.7,
        num_ctx: int = 8192, timeout: int = 1800) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {"temperature": temperature, "num_ctx": num_ctx},
    }
    req = urllib.request.Request(
        OLLAMA, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data.get("response", "")


if __name__ == "__main__":
    # CLI: python llm.py <model> <promptfile> [systemfile] [outfile]
    model = sys.argv[1]
    prompt = open(sys.argv[2], encoding="utf-8").read()
    system = open(sys.argv[3], encoding="utf-8").read() if len(sys.argv) > 3 and sys.argv[3] != "-" else ""
    out = ask(model, prompt, system=system)
    if len(sys.argv) > 4:
        open(sys.argv[4], "w", encoding="utf-8").write(out)
        print(f"wrote {sys.argv[4]} ({len(out)} chars)")
    else:
        print(out)

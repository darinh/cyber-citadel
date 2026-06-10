"""Expression variants via IP-Adapter Plus (Apache-2.0) anchored on each character's
EXISTING base portrait, so the established design is preserved (CLIP image conditioning)
while the prompt varies only the expression. License-clean: tencent IP-Adapter (Apache-2.0),
h94 weights (Apache-2.0), SDXL base (OpenRAIL++-M). No InsightFace.

Run in the SDXL venv:  .\.venv_img\Scripts\python.exe tools\gen_avatar_ipa.py [NAME ...]
"""
import sys
from pathlib import Path
import torch
from PIL import Image
from diffusers import StableDiffusionXLPipeline, DDIMScheduler

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_avatars as G

IPA = Path(__file__).resolve().parent / "_ipa"
ENC = IPA / "models" / "image_encoder"          # ViT-H (1280-dim) for the _vit-h adapter
CKPT = IPA / "sdxl_models" / "ip-adapter-plus_sdxl_vit-h.safetensors"

STYLE = (", anime style, flat cel shading, simple clean shading, bold clean lineart, "
         "head and shoulders bust portrait, centered, dark teal background, single character")
NEG = ("text, watermark, multiple people, extra limbs, deformed, blurry, lowres, "
       "photorealistic, 3d render, painterly, heavy rendering, realistic skin, nsfw, "
       "different character, neutral expression")

# per-character expression prompts (identity comes from the reference image, not the text)
EXPR = {
    "VEGA": {
        "explain": "a man with a clear warm friendly smile, mouth open speaking, kind eyes, explaining",
        "ask": "a man with a thoughtful curious look, one eyebrow raised high, head tilted, questioning",
    },
    "NOVA": {
        "curious": "a young woman with a gentle soft smile, bright wide attentive eyes, eager and curious",
        "ask": "a young woman asking a question, both eyebrows raised high, mouth open mid-question, inquisitive",
        "aha": "a young woman with a big open joyful grin showing teeth, eyes wide with delight, thrilled aha moment",
    },
}
SCALE = 0.72   # identity strength; lower = more expression freedom
SEED = 42


def main(names):
    from ip_adapter import IPAdapterPlusXL
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16,
        scheduler=DDIMScheduler.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0", subfolder="scheduler"),
        add_watermarker=False, variant="fp16", use_safetensors=True).to("cuda")
    ip = IPAdapterPlusXL(pipe, str(ENC), str(CKPT), "cuda", num_tokens=16)
    for name in names:
        ref = Image.open(G.OUT / f"{name}.png").convert("RGB").resize((1024, 1024))
        for expr, desc in EXPR[name].items():
            imgs = ip.generate(pil_image=ref, num_samples=1, num_inference_steps=30,
                               seed=SEED, prompt=desc + STYLE, negative_prompt=NEG,
                               scale=SCALE, guidance_scale=8.0, width=1024, height=1024)
            imgs[0].save(G.OUT / f"{name}_{expr}.png")
            print(f"ipa expr: {name}_{expr}")
    print("done ->", G.OUT)


if __name__ == "__main__":
    main(sys.argv[1:] or ["NOVA"])

"""Generate anime-style character portraits with SDXL (runs in .venv_img).

One bust portrait per persona, consistent style + fixed seeds. Saved to
course/art/avatars/raw/<NAME>.png; framed into avatar cards by make_avatars.py.
Run:  .\.venv_img\Scripts\python.exe tools\gen_avatars.py
"""
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline

OUT = Path(__file__).resolve().parent.parent / "course" / "art" / "avatars" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

STYLE = (", anime style character portrait, head and shoulders bust, centered, "
         "clean cel shading, dramatic rim lighting, dark teal studio background, "
         "highly detailed, crisp, single character, looking at viewer")
NEG = ("text, words, letters, watermark, signature, logo, multiple people, crowd, "
       "extra limbs, extra fingers, deformed, mutated, blurry, lowres, photorealistic, "
       "3d render, nsfw, full body, weapon")

CHARS = {
    "VEGA": (1101, "a confident veteran cybersecurity officer, man in his thirties, short "
             "silver-blue hair, navy tactical uniform with glowing cyan accents, calm determined expression"),
    "NOVA": (1102, "a young eager apprentice officer, woman in her early twenties, short tousled "
             "auburn hair, teal jacket with gold trim, bright curious hopeful expression"),
    "ARCHIVIST": (1103, "a wise archivist scholar, woman, round glasses, dark hooded robe with glowing "
                  "golden circuit embroidery, serene knowing expression, soft gold light"),
    "NULL": (1104, "a shadowy hooded cyber antagonist, face mostly hidden in shadow, glowing magenta "
             "eyes, dark cloak with faint red glitch effects, menacing ominous"),
    "NARRATOR": (1105, "a dignified herald narrator, older man, deep blue cloak, subtle gold circuitry "
                 "mask on forehead, calm authoritative presence, soft blue light"),
}


def main():
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda")
    pipe.set_progress_bar_config(disable=True)
    for name, (seed, desc) in CHARS.items():
        g = torch.Generator("cuda").manual_seed(seed)
        img = pipe(desc + STYLE, negative_prompt=NEG, width=1024, height=1024,
                   num_inference_steps=34, guidance_scale=7.0, generator=g).images[0]
        img.save(OUT / f"{name}.png")
        print("avatar:", name)
    print("done ->", OUT)


if __name__ == "__main__":
    main()

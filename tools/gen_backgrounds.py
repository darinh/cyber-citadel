"""Generate atmospheric 'cyber-castle' backgrounds with SDXL (runs in .venv_img).

HYBRID approach (council-endorsed): AI makes only dark, text-free, character-free
BACKGROUNDS; the designed UI + sigils stay on top. Saves to course/art/backgrounds/.
Run with:  .\.venv_img\Scripts\python.exe tools\gen_backgrounds.py
"""
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline

OUT = Path(__file__).resolve().parent.parent / "course" / "art" / "backgrounds"
OUT.mkdir(parents=True, exist_ok=True)

STYLE = ", dark moody concept art, deep navy background, high contrast, volumetric fog, cinematic rim lighting, depth of field, 16:9, no text, no characters"
NEG = "text, words, letters, numbers, watermark, signature, people, person, face, hands, ui, border, frame, bright, washed out, low quality, jpeg artifacts, busy, cluttered"

SCENES = {
    "citadel": "a colossal dark cyber fortress citadel on a hill at night, glowing cyan circuit ramparts, distant gold lights",
    "walls": "a fortified digital gate, faint cyan energy barrier, towering dark ramparts, atmospheric haze",
    "watch": "tall watchtowers above a dark data-city, faint teal scanning light beams in fog",
    "people": "a vast dim archive hall of faintly glowing data shelves, warm gold ambient light",
    "council": "a dark high council chamber, faint holographic blue maps floating, violet ambient glow",
    "forge": "a dark industrial forge with dim server racks and supply conduits, faint orange and cyan embers",
    "vault": "a deep underground data vault, dark blast doors, faint magenta and cyan glowing cores",
    "network": "an abstract dark void with a faint constellation of cyan and gold light nodes, depth of field",
}


def main():
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16, variant="fp16", use_safetensors=True)
    pipe = pipe.to("cuda")
    pipe.set_progress_bar_config(disable=True)
    for i, (name, prompt) in enumerate(SCENES.items()):
        g = torch.Generator("cuda").manual_seed(1000 + i)
        img = pipe(prompt + STYLE, negative_prompt=NEG, width=1344, height=768,
                   num_inference_steps=30, guidance_scale=6.5, generator=g).images[0]
        p = OUT / f"{name}.png"
        img.save(p)
        print("bg:", p.name)
    print("done ->", OUT)


if __name__ == "__main__":
    main()

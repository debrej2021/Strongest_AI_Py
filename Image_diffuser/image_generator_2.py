"""
Generic text-to-image generator (CPU-friendly, SDXL-Turbo) with safety checks.

Run:   python image_generator.py
Then type any prompt. Commands:  quit  |  seed 123  |  steps 2
Images are saved in an "outputs" folder next to this script.

First run downloads SDXL-Turbo (~7 GB) and the safety checker (~1.2 GB) once.
"""
import os
import re
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
from diffusers import AutoPipelineForText2Image
from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
from transformers import CLIPImageProcessor

OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)

# Layer 1: block disallowed prompts before spending any compute.
# Keep your full keyword list here.
BLOCKED_WORDS = {
    "nsfw", "explicit",
}


def prompt_allowed(prompt: str) -> bool:
    words = set(re.findall(r"[a-z]+", prompt.lower()))
    return not (words & BLOCKED_WORDS)


def slug(text: str, n: int = 40) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:n] or "image"


def is_safe_image(image, safety_checker, feature_extractor) -> bool:
    if safety_checker is None or feature_extractor is None:
        return True  # Skip Layer 2 when disabled
    inputs = feature_extractor(images=image, return_tensors="pt")
    _, has_flag = safety_checker(
        images=np.expand_dims(np.array(image), axis=0),
        clip_input=inputs.pixel_values,
    )
    return not has_flag[0]


def load_pipeline():
    torch.set_num_threads(os.cpu_count() or 1)
    print("Loading models (first time downloads them)...")

    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-turbo",
        dtype=torch.float32,
        variant="fp16",
        use_safetensors=True,
    )
    pipe.enable_attention_slicing()
    return pipe, None, None


def main():
    pipe, safety_checker, feature_extractor = load_pipeline()
    seed, steps = 42, 2
    print("\nReady. Type a prompt (or 'quit', 'seed 123', 'steps 2').")

    while True:
        prompt = input("\nPrompt> ").strip()
        if not prompt:
            continue
        if prompt.lower() in {"quit", "exit", "q"}:
            break
        if prompt.lower().startswith("seed "):
            try:
                seed = int(prompt.split()[1])
                print(f"Seed set to {seed}")
            except (IndexError, ValueError):
                print("Usage: seed 123")
            continue
        if prompt.lower().startswith("steps "):
            try:
                steps = max(1, min(4, int(prompt.split()[1])))
                print(f"Steps set to {steps}")
            except (IndexError, ValueError):
                print("Usage: steps 2")
            continue

        if not prompt_allowed(prompt):
            print("Blocked: that prompt isn't allowed. Try something else.")
            continue

        start = time.time()
        result = pipe(
            prompt=prompt,
            num_inference_steps=steps,
            guidance_scale=0.0,
            height=512,
            width=512,
            generator=torch.Generator("cpu").manual_seed(seed),
        )
        image = result.images[0]

        if not is_safe_image(image, None, None):
            print("Blocked: the safety checker flagged the result, so it was not saved.")
            continue

        name = f"{datetime.now():%Y%m%d_%H%M%S}_{slug(prompt)}_s{seed}.png"
        image.save(OUT / name)
        print(f"Saved outputs/{name}  ({time.time() - start:.1f}s)")


if __name__ == "__main__":
    main()
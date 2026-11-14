"""
Generic text-to-image generator (CPU-friendly, SD-Turbo) with safety checks.

Run:   python image_generator.py
Then type any prompt. Commands:  quit  |  seed 123  |  steps 2
Images are saved in an "outputs" folder next to this script.

First run also downloads the safety-checker model (~1.2 GB, one time).
"""
import os
import re
import time
from datetime import datetime
from pathlib import Path

import torch
from diffusers import AutoPipelineForText2Image
from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
from transformers import CLIPImageProcessor

OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)

# Layer 1: block clearly disallowed prompts before spending any compute.
BLOCKED_WORDS = {
    "nude", "naked", "nsfw", "sex", "gore", "beheading","porn",
    "child", "kid", "minor", "teen", "schoolgirl",
}


def prompt_allowed(prompt: str) -> bool:
    words = set(re.findall(r"[a-z]+", prompt.lower()))
    return not (words & BLOCKED_WORDS)


def slug(text: str, n: int = 40) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:n] or "image"


def load_pipeline():
    torch.set_num_threads(os.cpu_count())
    print("Loading models (first time downloads them)...")
    # Layer 2: the standard Stable Diffusion safety checker inspects every
    # finished image and blacks it out if it detects unsafe content.
    # safety_checker = StableDiffusionSafetyChecker.from_pretrained(
    #     "CompVis/stable-diffusion-safety-checker"
    # )
    # feature_extractor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch32")
    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sd-turbo",
        dtype=torch.float32,       # CPU needs float32
        local_files_only=True
        # safety_checker=False,
        # feature_extractor=None,
    )
    pipe.enable_attention_slicing()
    return pipe


def main():
    pipe = load_pipeline()
    seed, steps = 42, 1
    print("\nReady. Type a prompt (or 'quit', 'seed 123', 'steps 2').")

    while True:
        prompt = input("\nPrompt> ").strip()
        if not prompt:
            continue
        if prompt.lower() in {"quit", "exit", "q"}:
            break
        if prompt.lower().startswith("seed "):
            seed = int(prompt.split()[1]); print(f"Seed set to {seed}"); continue
        if prompt.lower().startswith("steps "):
            steps = max(1, min(4, int(prompt.split()[1]))); print(f"Steps set to {steps}"); continue

        if not prompt_allowed(prompt):
            print("Blocked: that prompt isn't allowed. Try something else.")
            continue

        start = time.time()
        result = pipe(
            prompt=prompt,
            num_inference_steps=steps,
            guidance_scale=0.0,
            height=512, width=512,
            generator=torch.Generator("cpu").manual_seed(seed),
        )
        if result.nsfw_content_detected and result.nsfw_content_detected[0]:
            print("Blocked: the safety checker flagged the result, so it was not saved.")
            continue

        name = f"{datetime.now():%Y%m%d_%H%M%S}_{slug(prompt)}_s{seed}.png"
        result.images[0].save(OUT / name)
        print(f"Saved outputs/{name}  ({time.time() - start:.1f}s)")


if __name__ == "__main__":
    main()

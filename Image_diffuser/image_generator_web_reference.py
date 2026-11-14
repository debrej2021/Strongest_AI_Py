"""
CPU-friendly DreamShaper-8-LCM generator with optional web-lookup enrichment
and safety-check hooks (Layer 2 disabled via None).

Run:   python image_generator_web_reference.py
Commands:
  <any prompt>       -> generate directly from your prompt
  web <topic>        -> look up <topic> on Wikipedia first, then generate
  seed 123 | steps 6 -> change seed or denoising steps (1-8)
  quit               -> exit
"""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
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
        return True  # Layer 2 inactive when None is passed
    inputs = feature_extractor(images=image, return_tensors="pt")
    _, has_flag = safety_checker(
        images=np.expand_dims(np.array(image), axis=0),
        clip_input=inputs.pixel_values,
    )
    return not has_flag[0]


def fetch_web_context(topic: str, max_chars: int = 220) -> str:
    """Fetch a short summary from Wikipedia to enrich the image prompt."""
    encoded = urllib.parse.quote(topic.strip().replace(" ", "_"))
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
    req = urllib.request.Request(url, headers={"User-Agent": "ImageAgentDemo/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        summary = (data.get("extract") or "").strip()
        if summary:
            return summary[:max_chars].rsplit(" ", 1)[0]
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        pass
    return ""


def load_pipeline():
    torch.set_num_threads(os.cpu_count() or 1)
    print("Loading models (first time downloads them)...")

    pipe = AutoPipelineForText2Image.from_pretrained(
        "Lykon/dreamshaper-8-lcm",
        dtype=torch.float32,
        safety_checker=None,
    )
    pipe.enable_attention_slicing()
    return pipe, None, None


def main():
    pipe, safety_checker, feature_extractor = load_pipeline()
    seed, steps = 42, 4
    print("\nReady. Type a prompt, 'web <topic>', 'seed 123', 'steps 6', or 'quit'.")

    while True:
        raw_input = input("\nPrompt> ").strip()
        if not raw_input:
            continue
        if raw_input.lower() in {"quit", "exit", "q"}:
            break
        if raw_input.lower().startswith("seed "):
            try:
                seed = int(raw_input.split()[1])
                print(f"Seed set to {seed}")
            except (IndexError, ValueError):
                print("Usage: seed 123")
            continue
        if raw_input.lower().startswith("steps "):
            try:
                steps = max(1, min(8, int(raw_input.split()[1])))
                print(f"Steps set to {steps}")
            except (IndexError, ValueError):
                print("Usage: steps 6")
            continue

        if not prompt_allowed(raw_input):
            print("Blocked: that prompt isn't allowed. Try something else.")
            continue

        prompt = raw_input
        if raw_input.lower().startswith("web "):
            topic = raw_input[4:].strip()
            context = fetch_web_context(topic)
            if context:
                prompt = f"{topic}, {context}"
                print(f"Web context added: {context}")
            else:
                prompt = topic
                print("No web summary found; using topic directly.")

        if not prompt_allowed(prompt):
            print("Blocked: enriched prompt isn't allowed. Try something else.")
            continue

        start = time.time()
        result = pipe(
            prompt=prompt,
            num_inference_steps=steps,
            guidance_scale=1.5,
            height=512,
            width=512,
            generator=torch.Generator("cpu").manual_seed(seed),
        )
        image = result.images[0]

        if not is_safe_image(image, None, None):
            print("Blocked: the safety checker flagged the result, so it was not saved.")
            continue

        name = f"{datetime.now():%Y%m%d_%H%M%S}_{slug(raw_input)}_s{seed}.png"
        image.save(OUT / name)
        print(f"Saved outputs/{name}  ({time.time() - start:.1f}s)")


if __name__ == "__main__":
    main()
"""
Diffusion noise demo: add noise to an image step by step, then remove it.
Saves before / noisy / after images in the SAME folder as this script.

Run:  pip install numpy pillow
      python diffusion_noise_demo.py              # uses a generated sample image
      python diffusion_noise_demo.py my_photo.jpg # uses your own image
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent      # "root folder" = where this script lives
STEPS = 50                                  # number of noising steps
BETA = 0.05                                 # how much noise is added per step


def sample_image(size=256):
    """Make a simple test picture (sun, hill, sky) so no download is needed."""
    img = Image.new("RGB", (size, size), (135, 206, 235))          # sky
    d = ImageDraw.Draw(img)
    d.ellipse((160, 30, 220, 90), fill=(255, 215, 0))               # sun
    d.ellipse((-60, 150, 320, 420), fill=(34, 139, 34))             # hill
    d.rectangle((60, 120, 120, 180), fill=(178, 34, 34))            # house
    d.polygon([(50, 120), (90, 85), (130, 120)], fill=(90, 50, 20)) # roof
    return img


def to_array(img):
    # Pixels 0..255 -> floats -1..1 (the range diffusion models work in)
    return np.asarray(img, dtype=np.float32) / 127.5 - 1.0


def to_image(arr):
    arr = np.clip((arr + 1.0) * 127.5, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def main():
    rng = np.random.default_rng(42)
    img = Image.open(sys.argv[1]).convert("RGB").resize((256, 256)) if len(sys.argv) > 1 else sample_image()

    x0 = to_array(img)
    img.save(OUT / "01_before.png")

    # ---- Forward process: add a little Gaussian noise at every step ----
    x = x0.copy()
    noises = []
    snapshots = {}
    for t in range(1, STEPS + 1):
        noise = rng.standard_normal(x.shape).astype(np.float32)
        noises.append(noise)
        x = np.sqrt(1 - BETA) * x + np.sqrt(BETA) * noise
        if t in (5, 15, 50):
            snapshots[t] = x.copy()
            to_image(x).save(OUT / f"02_noisy_step_{t:02d}.png")

    # ---- Reverse process: remove the noise step by step ----
    # A real model PREDICTS the noise; here we "cheat" and use the true noise,
    # to show that knowing the noise is enough to rebuild the picture.
    for noise in reversed(noises):
        x = (x - np.sqrt(BETA) * noise) / np.sqrt(1 - BETA)
    to_image(x).save(OUT / "03_after_denoised.png")

    # ---- One side-by-side strip for notes ----
    frames = [img, to_image(snapshots[5]), to_image(snapshots[15]), to_image(snapshots[50]), to_image(x)]
    labels = ["before", "step 5", "step 15", "step 50 (almost static)", "after"]
    strip = Image.new("RGB", (256 * len(frames), 280), "white")
    d = ImageDraw.Draw(strip)
    for i, (f, label) in enumerate(zip(frames, labels)):
        strip.paste(f, (256 * i, 0))
        d.text((256 * i + 8, 262), label, fill="black")
    strip.save(OUT / "00_diffusion_strip.png")

    print("Saved to:", OUT)
    for p in sorted(OUT.glob("0*.png")):
        print("  ", p.name)


if __name__ == "__main__":
    main()

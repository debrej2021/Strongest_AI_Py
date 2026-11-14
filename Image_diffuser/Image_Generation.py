# pip install torch diffusers transformers accelerate
import torch
from diffusers import AutoPipelineForText2Image

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
dtype = torch.float32 if device == "cpu" else torch.float16

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sd-turbo", torch_dtype=dtype
).to(device)

image = pipe(
    prompt="a majestic elephant walking through tall grass at sunset, photorealistic",
    num_inference_steps=4,     # turbo models need only 1-4 denoising steps
    guidance_scale=0.0,        # turbo models are trained without guidance
    generator=torch.Generator("cpu").manual_seed(42),  # same seed = same image
).images[0]

image.save("elephant.png")
print("Saved elephant.png")
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import uuid

# Use GPU if available, else CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load Stable Diffusion model
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
pipe.to(device)

# Generate image from prompt
prompt = "a futuristic city skyline at sunset, ultra realistic, 4k"
image = pipe(prompt).images[0]

# Save output image
output_path = f"static/outputs/{uuid.uuid4()}.png"
image.save(output_path)
print(f"Image saved to {output_path}")

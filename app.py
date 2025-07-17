from flask import Flask, request, jsonify, render_template
from diffusers import StableDiffusionPipeline
import torch
import os
import uuid

app = Flask(__name__)

# Load Stable Diffusion model once at startup
device = "cuda" if torch.cuda.is_available() else "cpu"

if device == "cpu":
    print("⚠ Running on CPU. Generation may be slow (30–60s per image). A CUDA-enabled GPU is recommended.")
else:
    print("✅ Running on GPU (CUDA enabled).")

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
pipe.to(device)

@app.route("/")
def index():
    # Pass device info to the HTML page
    return render_template("index.html", device=device)

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form["prompt"]
    image = pipe(prompt).images[0]

    # Create safe filename: first 6 words + UUID
    safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (" ", "_")).rstrip()
    safe_prompt = "_".join(safe_prompt.split()[:6])

    # Save generated image
    if not os.path.exists("static/outputs"):
        os.makedirs("static/outputs")

    image_path = f"static/outputs/{safe_prompt}_{uuid.uuid4()}.png"
    image.save(image_path)

    return jsonify({"image_url": image_path})

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch
import json
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

print("⏳ Loading BLIP-2 FLAN-T5 model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-flan-t5-xl",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
).to(device)

print("✅ BLIP-2 FLAN-T5 model loaded.")

@app.route("/caption", methods=["POST"])
def caption_image():
    print("⚡ /caption endpoint hit")

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    user_prompt = request.form.get("prompt", "").strip()
    mode = request.form.get("mode", "default")

    print("📸 Received file:", image_file.filename)
    print("✍️ Prompt mode:", mode)
    print("📝 User custom prompt:", user_prompt if user_prompt else "[None]")

    if user_prompt:
        prompt = user_prompt
    elif mode == "poetic":
        prompt = "Describe this image in the form of a beautiful poem."
    elif mode == "philosophical":
        prompt = "What philosophical idea does this image express?"
    elif mode == "humorous":
        prompt = "Describe this image with a sense of humor or a joke."
    elif mode == "cinematic":
        prompt = "Describe this image as if it's a scene from a dramatic movie."
    else:
        prompt = "Describe this image."

    try:
        image = Image.open(image_file).convert("RGB")
        inputs = processor(images=image, text=prompt, return_tensors="pt").to(device)

        with torch.no_grad():
            output_ids = model.generate(**inputs, max_new_tokens=100)

        caption = processor.batch_decode(output_ids, skip_special_tokens=True)[0]
        print("✅ Caption generated:", caption)
        return app.response_class(
                response=json.dumps({"caption": caption.strip()}),
                status=200,
               mimetype='application/json'
      )

    except Exception as e:
        print("❌ Error:", e)
        return app.response_class(
            response=json.dumps({"error": str(e)}),
            status=500,
            mimetype='application/json'
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)

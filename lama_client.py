# lama_client.py
import json
import requests
import io
from PIL import Image
import numpy as np
import cv2



def send_to_lama(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    import json

    url = "http://127.0.0.1:8080/inpaint"

    image = image.astype(np.uint8)
    mask = mask.astype(np.uint8)
    pil_image = Image.fromarray(image)
    pil_mask = Image.fromarray(mask, mode="L")

    print("🖼️ image.shape:", image.shape)
    print("🎭 mask.shape:", mask.shape)
    print("⚪ Non-zero mask pixels:", np.count_nonzero(mask))

    image_bytes = image_to_bytes(pil_image)
    mask_bytes = image_to_bytes(pil_mask)

    with open("debug_image.png", "wb") as f:
        f.write(image_bytes)
    with open("debug_mask.png", "wb") as f:
        f.write(mask_bytes)

    files = {
        "image": ("image.png", io.BytesIO(image_bytes), "image/png"),
        "mask": ("mask.png", io.BytesIO(mask_bytes), "image/png")
    }

    payload = {
        "prompt": "",
        "model": "lama",  # Required
        "strength": 1,
        "num_inference_steps": 25,
        "guidance_scale": 7.5,
        "seed": 42
    }

    try:
        response = requests.post(url, files=files, json=payload)  # ✅ Correct usage
        print("🧾 Full response text from LaMa:", response.text[:300])
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        raise

    with open("lama_debug_response.png", "wb") as f:
        f.write(response.content)

    try:
        result_image = Image.open(io.BytesIO(response.content)).convert("RGB")
    except Exception as e:
        print("❌ Failed to load returned image:", e)
        raise Exception("LaMa returned invalid image.")

    result_np = np.array(result_image)
    if result_np.size == 0:
        raise Exception("LaMa returned empty result image.")

    return cv2.cvtColor(result_np, cv2.COLOR_RGB2BGR)



def image_to_bytes(pil_img: Image.Image) -> bytes:
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return buf.getvalue()

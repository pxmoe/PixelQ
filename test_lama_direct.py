import requests
import numpy as np
import cv2
import io
from PIL import Image

# Step 1: Create dummy 1024x1024 image and mask
image_np = np.full((1024, 1024, 3), 255, dtype=np.uint8)  # White image
mask_np = np.zeros((1024, 1024), dtype=np.uint8)
cv2.circle(mask_np, (512, 512), 100, 255, -1)  # White circle in center

# Step 2: Convert image and mask to PNG bytes
def np_to_png_bytes(arr, mode):
    img = Image.fromarray(arr, mode=mode)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

image_bytes = np_to_png_bytes(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB), "RGB")
mask_bytes = np_to_png_bytes(mask_np, "L")

# Step 3: Send to LaMa-cleaner
url = "http://127.0.0.1:8080/inpaint"
files = {
    "image": ("image.png", io.BytesIO(image_bytes), "image/png"),
    "mask": ("mask.png", io.BytesIO(mask_bytes), "image/png"),
}

response = requests.post(url, files=files)

# Step 4: Handle result
if response.status_code == 200:
    with open("lama_result.png", "wb") as f:
        f.write(response.content)
    print("✅ Success! Saved to lama_result.png")
else:
    print("❌ Failed:", response.status_code)
    print(response.text)

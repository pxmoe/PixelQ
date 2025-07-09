# 📸 PixIQ - Smart Image Editing Tools

PixIQ is a modern web-based tool suite designed to help users perform essential image tasks like resizing, compressing, converting formats, AI caption generation, and (coming soon) watermark removal. Built with Flask and JavaScript, it delivers functionality and a clean UI optimized for monetization and user growth.

---

## ✨ Features

* 📐 **Resize Images** – Change dimensions easily
* 📉 **Compress Images** – Reduce image size while maintaining quality
* 🔁 **Convert Formats** – Convert between JPG, PNG, and WebP
* 🧠 **AI Image Captioning** – Auto-generate captions using your own image + optional prompt
* 🧼 **Watermark Remover** *(Coming Soon)* – Canvas-based mask + AI-powered inpainting
* 🔐 **User Auth** – Login, Signup & Google OAuth
* 💰 **AdSense Layout Ready** – Layout optimized for AdSense left/right banners

---

## 📁 Project Structure

```bash
pixiq/
├── app.py                  # Flask backend
├── caption_server.py       # AI captioning backend (optional to run separately)
├── lama_client.py          # Inpainting bridge for watermark removal
├── public/                 # All frontend HTML/CSS/JS assets
│   ├── dashboard.html
│   ├── login.html
│   ├── signup.html
│   ├── style.css
│   ├── script.js
│   ├── assets/
│   └── background.mp4
├── uploads/                # Uploaded files (auto-created)
├── processed/              # Inpainted results (auto-created)
├── models/ (ignored)       # Heavy AI models - not tracked in Git
├── requirements.txt        # Python dependencies
├── Procfile                # For Render/Heroku deployment
├── .gitignore              # Ignore unnecessary files
└── README.md               # This file
```

---

## ⚙️ Installation

```bash
# Clone this repo
https://github.com/pxmoe/PixelQ.git
cd PixelQ

# (Optional) create venv
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

---

## 🚀 Deployment

PixIQ supports both **frontend-only** and **full backend** deployment:

### 🔥 Render (Flask full stack)

* Add `Procfile` with:

  ```
  web: python app.py
  ```
* Add environment variables for OAuth (optional)
* Deploy repo on Render with Python environment

### 🌐 GitHub Pages (Frontend only)

* Upload `public/` folder
* Use static hosting for non-AI features (resize, compress, convert)

### 🔁 Vercel / Netlify (Frontend only)

* Connect public folder
* Works without Python features

---

## 🧠 AI Models

* Inpainting: Inpaint-Anything (via `lama_client.py`)
* Captioning: Custom model server (`caption_server.py`)

> **Note**: Large model files (`models/`) and virtual envs are `.gitignore`d.

---

## 👨‍💻 Team & Credits

Built with 💻 by:

* **Perclat (Hassan)**
* **Moeez**

GitHub: [github.com/pxmoe](https://github.com/pxmoe)

---

## 📜 License

MIT License. See [LICENSE](./LICENSE) file.

---

## ✅ To-Do / Coming Soon

* [ ] Finalize watermark removal with SAM + SD
* [ ] Integrate Firebase or Supabase auth (optional)
* [ ] Add persistent caption generation history
* [ ] Full deployment with Render + custom domain

---

Let us know what feature you want next!

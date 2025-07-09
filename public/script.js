function showTab(tabId) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
}

function downloadImage(dataUrl, filename) {
  const link = document.createElement("a");
  link.href = dataUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// ---------------- IMAGE TOOLS ----------------

function resizeImage() {
  const input = document.getElementById("resizeInput").files[0];
  const width = parseInt(document.getElementById("resizeWidth").value);
  const height = parseInt(document.getElementById("resizeHeight").value);
  if (!input || !width || !height) return alert("Provide image and dimensions.");

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      canvas.getContext("2d").drawImage(img, 0, 0, width, height);
      downloadImage(canvas.toDataURL("image/jpeg"), "resized.jpg");
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(input);
}

function compressImage() {
  const input = document.getElementById("compressInput").files[0];
  if (!input) return alert("Upload an image");

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = img.width;
      canvas.height = img.height;
      canvas.getContext("2d").drawImage(img, 0, 0);
      downloadImage(canvas.toDataURL("image/jpeg", 0.5), "compressed.jpg");
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(input);
}

function convertImage() {
  const input = document.getElementById("convertInput").files[0];
  const format = document.getElementById("formatType").value;
  if (!input || !format) return alert("Select file and format");

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = img.width;
      canvas.height = img.height;
      canvas.getContext("2d").drawImage(img, 0, 0);
      const url = canvas.toDataURL(format);
      document.getElementById("convertResult").innerHTML = `<img src="${url}" style="max-width:100%;">`;
      downloadImage(url, "converted." + format.split("/")[1]);
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(input);
}

function generateCaption() {
  const file = document.getElementById("aiImageInput").files[0];
  const prompt = document.getElementById("userPrompt").value;
  const resultBox = document.getElementById("aiCaptionResult");
  if (!file) return (resultBox.textContent = "Upload an image first.");

  const formData = new FormData();
  formData.append("image", file);
  if (prompt) formData.append("prompt", prompt);
  resultBox.textContent = "⏳ Generating...";

  fetch("/api/caption", {
    method: "POST",
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      resultBox.textContent = data.caption || "❌ Failed to generate caption.";
    })
    .catch(err => {
      console.error(err);
      resultBox.textContent = "❌ Server error.";
    });
}

// ---------------- MASK DRAWING + WATERMARK ----------------

let drawing = false;
const canvas = document.getElementById("maskCanvas");
const ctx = canvas.getContext("2d");
const preview = document.getElementById("imagePreview");

document.getElementById("wmFile").addEventListener("change", function () {
  const file = this.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function (e) {
    const img = new Image();
    img.onload = function () {
      // Set image preview
      preview.src = img.src;
      preview.style.display = "block";
      preview.width = img.width;
      preview.height = img.height;

      // Match canvas size to image
      canvas.width = img.width;
      canvas.height = img.height;

      // Clear and fill canvas with transparent black
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);

  // Hide result and download from previous run
  document.getElementById("wmPreview").style.display = "none";
  document.getElementById("wmDownload").style.display = "none";
});

// Mouse events for drawing
canvas.addEventListener("mousedown", () => drawing = true);
canvas.addEventListener("mouseup", () => drawing = false);
canvas.addEventListener("mouseleave", () => drawing = false);

canvas.addEventListener("mousemove", function (e) {
  if (!drawing) return;

  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;

  const x = (e.clientX - rect.left) * scaleX;
  const y = (e.clientY - rect.top) * scaleY;

  ctx.fillStyle = "white";
  ctx.beginPath();
  ctx.arc(x, y, 10, 0, Math.PI * 2);
  ctx.fill();
});

async function removeWatermark() {
  const input = document.getElementById("wmFile").files[0];
  const resultBox = document.getElementById("wmResult");
  const resultImage = document.getElementById("wmPreview");
  const downloadLink = document.getElementById("wmDownload");

  if (!input) {
    alert("Please select a file.");
    return;
  }

  const maskBlob = await new Promise(resolve => canvas.toBlob(resolve, "image/png"));
  const formData = new FormData();
  formData.append("file", input);
  formData.append("mask", maskBlob);

  resultBox.textContent = "Processing...";

  try {
    const res = await fetch("/remove_watermark_lama", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      resultBox.textContent = "❌ Error: " + (await res.text());
      return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);

    resultImage.src = url;
    resultImage.style.display = "block";
    downloadLink.href = url;
    downloadLink.style.display = "inline-block";
    resultBox.textContent = "";
  } catch (err) {
    console.error(err);
    resultBox.textContent = "❌ Failed to process.";
  }
}

// ---------------- ADS & INIT ----------------

function toggleAd() {
  const ad = document.getElementById("ad");
  ad.style.display = ad.style.display === "none" ? "block" : "none";
}

function notifyComingSoon() {
    const emailInput = document.querySelector(".notify-input");
    const msg = document.getElementById("notifyMsg");
    const email = emailInput.value.trim();

    if (!email || !email.includes("@")) {
      msg.textContent = "❌ Please enter a valid email.";
      msg.style.color = "#ff6b6b";
      return;
    }

    msg.textContent = "✅ You'll be notified when it's ready!";
    msg.style.color = "#00e676";
    emailInput.value = "";
  }

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("resizeButton")?.addEventListener("click", resizeImage);
  document.getElementById("compressButton")?.addEventListener("click", compressImage);
  document.getElementById("convertButton")?.addEventListener("click", convertImage);
  document.getElementById("generateCaptionButton")?.addEventListener("click", generateCaption);
  document.getElementById("removeWatermarkButton")?.addEventListener("click", removeWatermark);
  document.getElementById("toggleAdButton")?.addEventListener("click", toggleAd);
});

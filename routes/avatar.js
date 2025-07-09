const express = require("express");
const multer = require("multer");
const fetch = require("node-fetch");
require("dotenv").config();

const router = express.Router();
const upload = multer({ storage: multer.memoryStorage() });

router.post("/", upload.single("image"), async (req, res) => {
  try {
    const imageData = `data:${req.file.mimetype};base64,${req.file.buffer.toString("base64")}`;

    const response = await fetch("https://api.replicate.com/v1/predictions", {
      method: "POST",
      headers: {
        Authorization: `Token ${process.env.REPLICATE_API_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        version: "replace-this-with-your-avatar-model-version",
        input: { image: imageData }
      }),
    });

    const data = await response.json();
    if (!data || !data.output) throw new Error("Avatar generation failed");

    res.json({ avatarUrl: data.output });
  } catch (err) {
    console.error("Avatar error:", err);
    res.status(500).json({ error: "Avatar generation failed" });
  }
});

module.exports = router;

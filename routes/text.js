const express = require('express');
const router = express.Router();
const multer = require('multer');
const fs = require('fs');
const axios = require('axios');
const path = require('path');

const upload = multer({ dest: 'uploads/' });

router.post('/caption', upload.single('image'), async (req, res) => {
  try {
    const filePath = path.join(__dirname, '..', req.file.path);
    const formData = new FormData();
    formData.append('image', fs.createReadStream(filePath));

    const response = await axios.post('http://localhost:5001/caption', formData, {
      headers: formData.getHeaders()
    });

    fs.unlinkSync(filePath); // Cleanup uploaded file
    res.json({ caption: response.data.caption });

  } catch (error) {
    console.error('❌ Caption error:', error.message);
    res.status(500).json({ error: 'Failed to generate caption' });
  }
});

module.exports = router;

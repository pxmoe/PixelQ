const express = require('express');
const cors = require('cors');
const app = express();
const textRoutes = require('./routes/text');
const path = require('path');

app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/api', textRoutes); // 👈 API routes

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});

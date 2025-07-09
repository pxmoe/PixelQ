# Use official Python base
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# System dependencies (Tesseract + FFmpeg if used)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Honcho for Procfile management
RUN pip install honcho

# Expose Flask port
EXPOSE 8080

# Start both servers
CMD ["honcho", "start"]


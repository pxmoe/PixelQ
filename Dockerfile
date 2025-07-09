# Use an official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Honcho (Procfile runner)
RUN pip install honcho

# Expose the default Flask port
EXPOSE 8080

# Set the default command
CMD ["honcho", "start"]

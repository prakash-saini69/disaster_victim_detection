FROM python:3.9-slim-bookworm

WORKDIR /app

# 1. Install system dependencies
# 'awscli' is good for debugging
# 'libgl1...' and 'libglib...' are REQUIRED for cv2 (OpenCV) to work
RUN apt-get update && apt-get install -y \
    awscli \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Copy source code
COPY . /app

# 3. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 4. Start the App
CMD ["python3", "app.py"]
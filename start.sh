#!/bin/bash

# Cập nhật hệ thống và cài đặt Tesseract OCR
apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Cài đặt backend (Python)
pip install --no-cache-dir -r ./requirements.txt

# Cài đặt frontend (React)
cd frontend
npm install
npm run build
cd ..

# Chạy server backend
# uvicorn backend.main:app --host 0.0.0.0 --port 10000

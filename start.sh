#!/bin/bash
# Cài đặt Tesseract OCR
apt-get update && apt-get install -y tesseract-ocr

# Cài đặt thư viện Python
pip install -r requirements.txt

# Build frontend
cd frontend
npm install && npm run build
cd ..

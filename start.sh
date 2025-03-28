#!/bin/bash
cd frontend
npm install && npm run build  # Build frontend
cd ..
apt-get update && apt-get install -y tesseract-ocr
uvicorn backend.main:app --host 0.0.0.0 --port 10000  # Chạy backend

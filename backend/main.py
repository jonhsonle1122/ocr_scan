from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

# Đường dẫn đến tesseract nếu chạy trên Windows (Cập nhật theo hệ thống của bạn)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.get("/extract-text/")
async def extract_text(url: str = Query(..., description="URL của trang web cần quét")):
    """
    API lấy danh sách ảnh từ <figure class='wp-block-image size-full'>, 
    tải ảnh về và trích xuất nội dung bằng OCR (Tesseract).
    """
    try:
        # Gửi request lấy HTML từ trang web
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        
        if response.status_code != 200:
            return {"error": f"Không thể truy cập trang web. Mã lỗi: {response.status_code}"}
        
        # Parse HTML bằng BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Tìm các thẻ <figure> có class tương ứng
        figures = soup.find_all("figure", class_="wp-block-image size-full")
        image_texts = {}

        for figure in figures:
            img_tag = figure.find("img", src=True)
            if img_tag:
                # Lấy thuộc tính data-src nếu có, nếu không thì lấy src
                image_src = img_tag.get("data-src") or img_tag.get("src")
                
                # Tải ảnh về
                img_response = requests.get(image_src)
                if img_response.status_code == 200:
                    img = Image.open(BytesIO(img_response.content))

                    # Chuyển ảnh sang grayscale để tăng hiệu suất OCR
                    img = img.convert("L")

                    # Nhận diện văn bản từ ảnh
                    text = pytesseract.image_to_string(img, lang="eng+vie")  # Hỗ trợ tiếng Anh + Việt Nam

                    # Lưu kết quả
                    image_texts[image_src] = text.strip()
        
        return {"results": image_texts}

    except Exception as e:
        return {"error": str(e)}

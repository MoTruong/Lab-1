from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from model import Translator


print("Đang tải model...")
translator = Translator("./config.yaml")
print("Model đã được tải thành công!")

app = FastAPI(
    title  = "English to Vietnamese Translation API",
    description="Web API dịch văn bản từ tiếng Anh sang tiếng Việt sử dụng mô hình Helsinki-NLP/opus-mt-en-vi từ Hugging Face"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "English to Vietnamese Translation API",
        "description": "API dịch văn bản tiếng Anh sang tiếng Việt sử dụng Helsinki-NLP/opus-mt-en-vi.",
        "model": "Helsinki-NLP/opus-mt-en-vi",
        "endpoints": {
            "GET /": "Thông tin giới thiệu API",
            "GET /health": "Kiểm tra trạng thái hệ thống",
            "POST /generate": "Dịch văn bản từ tiếng Anh sang tiếng Việt"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model_loaded": True,
        "model": "Helsinki-NLP/opus-mt-en-vi",
    }


@app.post("/generate")
async def translate(
    message: str = Query(..., min_length=1, max_length=512, description="Văn bản tiếng Anh cần dịch")
):
    if not message.strip():
        raise HTTPException(status_code=422, detail="Tham số 'message' không được để trống.")

    try:
        result = translator(message.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi trong quá trình dịch: {str(e)}")

    return {
        "source_language": "English",
        "target_language": "Vietnamese",
        "original": message.strip(),
        "translated": result
    }

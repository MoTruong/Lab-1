# English to Vietnamese Translation API

> **Tư Duy Tính Toán — Bài thực hành số 1: Application Programming Interface**

---

## Thông tin sinh viên

| Trường        | Thông tin              |
|---------------|------------------------|
| Họ và tên     | *Phạm Minh Trường* |
| MSSV          | *24120485*          |
| Lớp           | *24CTT3*           |
| Giảng viên TH | Lê Đức Khoan           |

---

## Mô hình sử dụng

| Thông tin    | Chi tiết                                                                                                           |
|--------------|--------------------------------------------------------------------------------------------------------------------|
| Tên mô hình  | `Helsinki-NLP/opus-mt-en-vi`                                                                                       |
| Hugging Face | [https://huggingface.co/Helsinki-NLP/opus-mt-en-vi](https://huggingface.co/Helsinki-NLP/opus-mt-en-vi)             |
| Loại tác vụ  | Machine Translation — dịch máy (Anh → Việt)                                                                        |
| Kiến trúc    | MarianMT (Encoder-Decoder Transformer)                                                                             |
| Kích thước   | ~298 MB — chạy tốt trên CPU, không cần GPU                                                                         |

---

## Mô tả hệ thống

API nhận một đoạn văn bản tiếng Anh và trả về bản dịch tiếng Việt tương ứng. Hệ thống xây dựng bằng **FastAPI** và sử dụng mô hình **Helsinki-NLP/opus-mt-en-vi** — một mô hình dịch máy MarianMT được huấn luyện trên tập ngữ liệu OPUS, chuyên biệt cho cặp ngôn ngữ Anh–Việt.

---

## Cấu trúc source code

```
translate-api/
├── main.py          # FastAPI application
├── model.py         # Class Translator
├── config.yaml      # Cấu hình đường dẫn model
├── test_api.py      # Script kiểm thử API bằng requests
├── requirements.txt # Danh sách thư viện
└── README.md        # Tài liệu hướng dẫn (file này)
```

---

## Hướng dẫn cài đặt thư viện

```bash
# 1. Clone repository
git clone https://github.com/MoTruong/translation-api.git
cd translation-api

# 2. (Khuyến nghị) Tạo virtual environment
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# 3. Cài đặt thư viện
pip install -r requirements.txt
```

> Lần chạy đầu tiên sẽ tự tải model (~298 MB) từ Hugging Face về cache.

---

## Hướng dẫn chạy chương trình

```bash
uvicorn main:app --reload
```

Server khởi động tại `http://127.0.0.1:8000`

---

## Hướng dẫn gọi API

### Tổng quan endpoints

| Method | Endpoint      | Mô tả                                |
|--------|---------------|--------------------------------------|
| GET    | `/`           | Thông tin giới thiệu API             |
| GET    | `/health`     | Kiểm tra trạng thái hệ thống         |
| POST    | `/generate`  | Dịch văn bản từ tiếng Anh sang Việt  |

> `/generate` nhận body param `message` (string, bắt buộc, 1–512 ký tự).

---

### `GET /`

**Request:**
```bash
curl http://127.0.0.1:8000/
```

**Response:**
```json
{
  "name": "English to Vietnamese Translation API",
  "description": "API dịch văn bản tiếng Anh sang tiếng Việt sử dụng Helsinki-NLP/opus-mt-en-vi.",
  "model": "Helsinki-NLP/opus-mt-en-vi",
  "endpoints": {
    "GET /": "Thông tin giới thiệu API",
    "GET /health": "Kiểm tra trạng thái hệ thống",
    "POST /generate": "Dịch văn bản từ tiếng Anh sang tiếng Việt"
  }
}
```

---

### `GET /health`

**Request:**
```bash
curl http://127.0.0.1:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "model": "Helsinki-NLP/opus-mt-en-vi"
}
```

---

### `POST /generate`

**Tham số:**

| Tên       | Kiểu   | Bắt buộc | Mô tả                              |
|-----------|--------|----------|------------------------------------|
| `message` | string | ✅        | Văn bản tiếng Anh cần dịch (1–512 ký tự) |

---

#### Ví dụ 1 

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/generate?message=Hello%2C%20how%20are%20you%3F"
```

**Response:**
```json
{
  "source_language": "English",
  "target_language": "Vietnamese",
  "original": "Hello, how are you?",
  "translated": "Xin chào, bạn có khỏe không?"
}
```

---

#### Ví dụ 2 

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/generate?message=Artificial%20intelligence%20is%20transforming%20the%20world."
```

**Response:**
```json
{
  "source_language": "English",
  "target_language": "Vietnamese",
  "original": "Artificial intelligence is transforming the world.",
  "translated": "Trí tuệ nhân tạo đang chuyển đổi thế giới."
}
```

---

#### Ví dụ 3 

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/generate?message=Vietnam%20is%20a%20beautiful%20country%20with%20rich%20culture,%20stunning%20landscapes,%20and%20delicious%20food."
```

**Response:**
```json
{
  "source_language": "English",
  "target_language": "Vietnamese",
  "original": "Vietnam is a beautiful country with rich culture, stunning landscapes, and delicious food.",
  "translated": "Việt Nam là một đất nước tươi đẹp với nền văn hóa phong phú, phong cảnh tuyệt đẹp và ẩm thực ngon miệng."
}
```

---

#### Ví dụ lỗi — Thiếu tham số (422)

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/generate
```

**Response (422):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "message"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

---

## Chạy kiểm thử

```bash
# Đảm bảo server đang chạy trước
python test_api.py
```

---

## Gọi API qua Python (requests)

```python
import requests

API_URL = "http://127.0.0.1:8000/generate"
params = {"message": "Hello, how are you?"}

response = requests.post(API_URL, params=params)
print(response.json())
# {
#   "source_language": "English",
#   "target_language": "Vietnamese",
#   "original": "Hello, how are you?",
#   "translated": "Xin chào, bạn có khỏe không?"
# }
```

---

## Video demo

> 🎬 **Link video:** <https://youtu.be/8nZSlD8Asec>

---

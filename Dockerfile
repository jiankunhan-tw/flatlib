FROM python:3.10-slim

# 安裝套件
RUN pip install --no-cache-dir flatlib uvicorn fastapi

# 工作資料夾
WORKDIR /app

# 複製全部檔案
COPY . /app

# 執行 FastAPI 應用
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]

FROM python:3.10

# 安裝必要工具與依賴
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 套件
RUN pip install --no-cache-dir flatlib uvicorn fastapi

# 設定工作目錄
WORKDIR /app

# 複製本地檔案進容器
COPY . /app

# 啟動 FastAPI 服務
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]

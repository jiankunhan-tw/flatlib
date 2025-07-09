FROM python:3.10

# 安裝必要工具（可略）
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製所有檔案進容器
COPY . .

# 安裝 Python 套件（從你自己的 requirements.txt）
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 開放埠口
EXPOSE 80

# 啟動 FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

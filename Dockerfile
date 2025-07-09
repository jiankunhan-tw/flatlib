FROM python:3.10

# 安裝必要工具（可略）
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製所有檔案進容器
COPY . .

# 安裝 Python 套件
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 開放埠口（跟 Zeabur 對應）
EXPOSE 8080

# 啟動 FastAPI（❗改這裡的 port）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

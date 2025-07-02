FROM python:3.10

# 安裝必要套件
RUN pip install --upgrade pip

# 複製程式碼
WORKDIR /app
COPY . /app

# 安裝依賴（含 flatlib）
RUN pip install -r requirements.txt

# 啟動服務（這行你可調整）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]

FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 關鍵：給 start.sh 執行權限
RUN chmod +x start.sh

# 設定啟動腳本
CMD ["./start.sh"]

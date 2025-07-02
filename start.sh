#!/bin/bash

# 安裝依賴套件
pip install -r requirements.txt

# 啟動 FastAPI 應用
uvicorn main:app --host 0.0.0.0 --port 8000

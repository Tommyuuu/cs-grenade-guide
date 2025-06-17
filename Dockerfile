# 使用官方 Python 基底映像
FROM python:3.10-slim

# 建立工作目錄
WORKDIR /app

# 複製後端程式與安裝套件
COPY backend/ /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 複製前端編譯後的靜態資源
COPY frontend/dist /app/frontend/dist

# 啟用 port 8080（GCP 預設）
EXPOSE 8080

# 使用 gunicorn 啟動 Flask
CMD ["gunicorn", "-k", "eventlet", "-b", "0.0.0.0:8080", "app:app"]
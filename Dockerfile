FROM node:18-alpine AS build-stage
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
# 複製前端所有原始碼並執行編譯
COPY frontend/ ./
RUN npm run build 


# 使用官方 Python 基底映像
FROM python:3.10-slim
# 建立工作目錄
WORKDIR /app

# 複製後端程式與安裝套件
COPY backend/ /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn eventlet

COPY --from=build-stage /app/frontend/dist /app/dist
# Render 預設使用 PORT=10000
EXPOSE 10000

# 使用 Gunicorn 啟動 Flask
CMD ["gunicorn", "-k", "eventlet", "-b", "0.0.0.0:10000", "app:app"]

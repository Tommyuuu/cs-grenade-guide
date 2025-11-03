# ---------- 前端建置階段 ----------
FROM node:18 AS frontend-build
WORKDIR /frontend

# 安裝前端依賴並打包 Vue
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# ---------- 後端建置階段 ----------
FROM python:3.10-slim AS backend
WORKDIR /app

# 安裝後端依賴
COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 複製後端程式
COPY backend/ /app

# 複製前端打包好的 dist 到 Flask 目錄
COPY --from=frontend-build /frontend/dist /app/frontend/dist

# Render 預設使用 PORT=10000
EXPOSE 10000

# 使用 Gunicorn 啟動 Flask
CMD ["gunicorn", "-k", "eventlet", "-b", "0.0.0.0:10000", "app:app"]

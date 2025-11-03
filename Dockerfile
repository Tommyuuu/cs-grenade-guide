# ---------- 前端建置階段 ----------
FROM node:18 AS frontend-build
WORKDIR /frontend

# 安裝依賴並打包 Vue 前端
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

# 將前端打包結果放入 Flask 專案中
COPY --from=frontend-build /frontend/dist /app/frontend/dist

# 啟用 port（Render 自動使用 10000）
EXPOSE 10000

# 啟動 Flask (Gunicorn + Eventlet for SocketIO)
CMD ["gunicorn", "-k", "eventlet", "-b", "0.0.0.0:10000", "app:app"]

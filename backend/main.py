from app import app, socketio

# GCP 會從這裡啟動你的應用
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)

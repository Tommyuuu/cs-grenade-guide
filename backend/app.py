from flask import Flask, jsonify, request, session,  send_from_directory
from flask_cors import CORS
import db
import flask_socketio 
import datetime
import os

app=Flask(__name__)
socketio = flask_socketio.SocketIO(app, cors_allowed_origins="*")
CORS(app, supports_credentials=True)  # 讓前端可以連到後端
app.secret_key = os.environ.get('SECRET_KEY', 'default-insecure-key')  # 設定 session 用
app.config.update({
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'None',  # 或 'None'（跨網域時）
    'SESSION_COOKIE_SECURE': True     # 上線部署時請改 True
})

"""
# 假資料（模擬）
data={
    "Dust2":{
        'smoke': [
            {
            'name': 'Mid Doors',
            'x': 365,
            'y': 288,
            'methods': [
                { 'name': '出生點-1', 'video_url': '/video/中門煙-1.mp4' },
                { 'name': '出生點-2', 'video_url': '/video/中門煙-2.mp4' },
                { 'name': '暗道', 'video_url': '/video/中門煙-暗道.mp4' },
                { 'name' : '出生快煙', 'video_url': 'https://www.youtube.com/shorts/RMrGCAM0XvY'},
            ]
            },
            
            {
            'name': 'CT',
            'x': 397,
            'y': 199,
            'methods': [
                { 'name': 'CT煙-3種', 'video_url': '/video/CT煙-3種.mp4' },
            ]
            },
            
            {
            'name': 'A Short-1',
            'x': 536,
            'y': 189,
            'methods': [
                { 'name': 'A小2顆煙', 'video_url': 'https://www.youtube.com/shorts/_clJSFumTSI' }
            ]
            },

            {
            'name': 'B door',
            'x': 208,
            'y': 185,
            'methods': [
                { 'name': '各位置B門煙-T', 'video_url': 'https://www.youtube.com/shorts/k1LJqxa0rpw' },
                { 'name': 'rush快煙', 'video_url': '/video/B門煙.mp4' }
            ]
            },

            {
            'name': 'A long - CT',
            'x': 693,
            'y': 308,
            'methods': [
                { 'name': '頂住煙', 'video_url': '/video/A大煙-CT.mp4' },
            ]
            },

            {
            'name': 'B site',
            'x': 175,
            'y': 92,
            'methods': [
                { 'name': 'retake道具-研究生', 'video_url': 'https://www.youtube.com/shorts/zJXrcH7Hgck' },
                { 'name': 'B點爆彈-研究生', 'video_url': 'https://www.youtube.com/shorts/8v0o5eJnduA' }
            ]
            },

            {
            'name': 'A long - T',
            'x': 648,
            'y': 193,
            'methods': [
                { 'name': 'A大進攻', 'video_url': 'https://www.youtube.com/shorts/3Z7ZaGAB6v4' }
            ]
            }
        ],


        'flash': [
            {
            'name': 'Mid Doors',
            'x': 365,
            'y': 288,
            'methods': [
                { 'name': '中門閃', 'video_url': '/video/中門閃.mp4' },
            ]
            },

            {
            'name': 'A long - CT',
            'x': 693,
            'y': 308,
            'methods': [
                { 'name': 'YT雙人反清閃-2點', 'video_url': 'https://www.youtube.com/shorts/7SNZwcKdwwY' },
                { 'name': '雙人反清閃-A小', 'video_url': '/video/A大雙人反清閃.mp4' },
            ]
            },

            {
            'name': 'A Short- Flash',
            'x': 505,
            'y': 310,
            'methods': [
                { 'name': 'A小自助閃-研究生', 'video_url': 'https://www.youtube.com/shorts/LjOuiRVKTiw' },
                { 'name': 'A小自助閃-CT', 'video_url': '/video/A小自助閃-CT.mp4' },
                { 'name': 'A小自助閃-T', 'video_url': '/video/A小自助閃-T.mp4' },

            ]
            },

            {
            'name': 'B1',
            'x': 315,
            'y': 327,
            'methods': [
                { 'name': 'B1反清閃-CT', 'video_url': '/video/B1反清閃-CT.mp4' },
                { 'name': 'B1自助閃', 'video_url': '/video/B1自助閃.mp4' },
            ]
            },

            {
            'name': '匪口',
            'x': 453,
            'y': 510,
            'methods': [
                { 'name': '中路前壓閃', 'video_url': '/video/中路前壓閃.mp4' }
            ]
            }

        ],

        'molotov': [
            {
            'name': 'A Site',
            'x': 637,
            'y': 135,
            'methods': [
                { 'name': 'A大包火', 'video_url': '/video/A大包火.mp4' },
                { 'name': 'A小進攻火', 'video_url': '/video/A小進攻火.mp4' },
                { 'name': 'A回防火', 'video_url': '/video/A回防火.mp4' },
                { 'name': 'A點+電梯火', 'video_url': '/video/A點+電梯火.mp4' }

            ]
            },

            {
            'name': 'Blue Car',
            'x': 749,
            'y': 209,
            'methods': [
                { 'name': '藍車火', 'video_url': '/video/藍車火.mp4' }
            ]
            },

        ]
    },
    "Mirage": {
        "Flash": {
            "A Site": "https://example.com/a_site_flash.mp4"
        }
    }
}
pending_methods =[
    {'map': 'Dust2', 'grenade_type': 'smoke', 'point_name': 'A long - CT', 'x': 693, 'y': 308, 
     'method': {'name': '11', 'video_url': 'https://www.youtube.com/shorts/-LhZUFHWUhI'}, 'id': 1},
    {'map': 'Dust2', 'grenade_type': 'smoke', 'point_name': 'A long - CT', 'x': 693, 'y': 308, 
     'method': {'name': '22', 'video_url': 'https://www.youtube.com/shorts/wubnNIWhfNw'}, 'id': 2},
    {'map': 'Dust2', 'grenade_type': 'flash', 'point_name': 'Mid Doors', 'x': 365, 'y': 288, 
     'method': {'name': '33', 'video_url': 'https://www.youtube.com/shorts/i9DE62rGvlk'}, 'id': 3},
    {'map': 'Dust2', 'grenade_type': 'smoke', 'point_name': 'A long - CT', 'x': 693, 'y': 308, 
     'method': {'name': '44', 'video_url': 'https://www.youtube.com/shorts/5QOLi7ReCZ8'}, 'id': 4},
    {'map': 'Dust2', 'grenade_type': 'smoke', 'point_name': 'Mid Doors', 'x': 365, 'y': 288, 
     'method': {'name': '55', 'video_url': 'https://www.youtube.com/shorts/GAdZqStE4SQ'}, 'id': 5},
    {'map': 'Dust2', 'grenade_type': 'smoke', 'point_name': 'A long - CT', 'x': 693, 'y': 308, 
     'method': {'name': '66', 'video_url': 'https://www.youtube.com/shorts/u784rWPHOLU'}, 'id': 6},
    {'map': 'Dust2', 'grenade_type': 'smoke', 'point_name': 'A long - CT', 'x': 693, 'y': 308, 
     'method': {'name': '77', 'video_url': 'https://www.youtube.com/shorts/SAbDQN0192M'}, 'id': 7},
    {'map': 'Dust2', 'grenade_type': 'flash', 'point_name': 'A long - CT', 'x': 693, 'y': 308, 
     'method': {'name': '88', 'video_url': 'https://www.youtube.com/shorts/oOWhc1wWIAQ'}, 'id': 8},
    {'map': 'Dust2', 'grenade_type': 'smoke', 'point_name': 'Mid Doors', 'x': 365, 'y': 288, 
     'method': {'name': '99', 'video_url': 'https://www.youtube.com/shorts/y5U33TLteeI'}, 'id': 9},
    {'map': 'Dust2', 'grenade_type': 'flash', 'point_name': 'A long - CT', 'x': 693, 'y': 308, 
     'method': {'name': '1010', 'video_url': 'https://www.youtube.com/shorts/LVTZ2iHV2HU'}, 'id': 10},
    {'map': 'Dust2', 'grenade_type': 'smoke', 'point_name': 'Mid Doors', 'x': 365, 'y': 288, 
     'method': {'name': '1111', 'video_url': 'https://www.youtube.com/shorts/zB9zfD37ESo'}, 'id': 11},
    {'map': 'Dust2', 'grenade_type': 'flash', 'point_name': 'A long - CT', 'x': 693, 'y': 308, 
     'method': {'name': '1212', 'video_url': 'https://www.youtube.com/shorts/VhHgd1O22pY'}, 'id': 12},
     ]
next_id = 13
users = {
    "admin": {"password": "1234", "role": "admin"},
    "user1": {"password": "abc", "role": "user"}
}
"""
@socketio.on('join')
def on_join(data):
    room = data['map']
    flask_socketio.join_room(room)

    # 傳回最近10則訊息
    history = db.get_n_message(data['map'],10)
    for msg in reversed(history):
        flask_socketio.emit('chat', {
            'username': msg['username'],
            'message': msg['message'],
            'timestamp': msg['timestamp'].isoformat()
        })

@socketio.on('chat')
def on_chat(data):
    room = data['map']
    msg = {
        "map": room,
        "username": data['username'],
        "message": data['message'],
        "timestamp": datetime.datetime.utcnow()
    }
    db.insert_msg(msg)
    flask_socketio.emit('chat', {
        "username": msg['username'],
        "message": msg['message'],
        "timestamp": msg['timestamp'].isoformat()
    }, to=room)

# 📌 回傳某地圖中某道具類型的所有點位資訊
@app.route('/maps/<map_name>/<grenade_type>/points')
def get_grenade_points(map_name, grenade_type):
    points = db.point(map_name, grenade_type)
    return jsonify(points)

# 新增方法（給使用者用）
@app.route('/submit_method', methods=['POST'])
def submit_method():
    data = request.json
    new_id=db.insert_pending_method(data)
    return jsonify({"status": "pending", "message": "等待審核", "id": new_id}), 200

# 取得所有待審核丟法
@app.route('/pending_methods', methods=['GET'])
def get_pending():
    return jsonify(db.get_all_pending())

# 分頁取得 pending 方法
@app.route('/pending_methods_paginated', methods=['GET'])
def get_pending_paginated():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    return jsonify(db.get_pending_pag(page, size))

#登入系統
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user=db.get_user_by_credentials(username, password)
    if user:
        session['username'] = user['username']
        session['role'] = user['role']
        print('login',session)
        return jsonify(success=True, username=username, role=user['role'])
    return jsonify(success=False)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify(success=True)

@app.route('/me', methods=['GET'])
def get_current_user():
    print('me',session)
    if 'username' in session:
        return jsonify(success=True, username=session['username'], role=session.get('role'))
    return jsonify(success=False)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    su = db.insert_user(username, password)
    if su:
        return jsonify(success=True)
    return jsonify(success=False)


# 查看單筆候選丟法內容
@app.route('/get_single_pending/<string:name>', methods=['GET'])
def get_single_pending(name):
    item = db.get_pending_by_name(name)
    if item:
        return jsonify(item)
    return jsonify({"error": "not found"}), 404


#同意審核
@app.route('/approve/<int:throw_id>', methods=['POST'])
def approve_throw(throw_id):
    success= db.approve_method_by_id(throw_id)
    if success:
        return jsonify({"message": "approved and added to main data"})
    return jsonify({"error": "miss"}), 404 
#拒絕審核
@app.route('/reject/<int:throw_id>', methods=['POST'])
def reject_throw(throw_id):
    rej=db.reject_method_by_id(throw_id)
    if rej:
        return jsonify({"message": "rejected"})
    return jsonify({"error": "not found"}), 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    vue_dist_path = os.path.join(os.path.dirname(__file__), 'frontend/dist')
    print("vue_dist_path = ", os.path.abspath(vue_dist_path))
    print("index.html exists?", os.path.exists(os.path.join(vue_dist_path, 'index.html')))
    
    if path != "" and os.path.exists(os.path.join(vue_dist_path, path)):
        return send_from_directory(vue_dist_path, path)
    else:
        return send_from_directory(vue_dist_path, 'index.html')



if __name__ == '__main__':
    #db.initialize_data()
    #app.run(debug=True)
    socketio.run(app, host='0.0.0.0', port=8080)

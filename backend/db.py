# db.py
from pymongo.mongo_client import MongoClient

# 從環境變數讀取 Mongo URI（Render 將設定 MONGO_URI）
uri = "mongodb+srv://csplay27212win:cstommy0847@cluster0.f67rdr8.mongodb.net/"
# Create a new client and connect to the server
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["cs_grenade_guide"]

# Collections
grenades_col = db["grenades"]
pending_col = db["pending_methods"]
users_col = db["users"]
chat_col = db["chat_messages"]
"""訊息格式
{
  "map": "Dust2",                  // 對應的地圖名
  "username": "user1",             // 使用者名稱
  "message": "這個點太神啦",       // 訊息內容
  "timestamp": "2025-06-13T02:00"  // 時間戳（UTC或ISO格式）
}"""

# --- Initial Dummy Data Loader ---
# Only run once to initialize the database

def get_n_message(map,n): #傳回最近n則訊息
    return(list(chat_col.find({"map": map}).sort("timestamp", -1).limit(n)))
def insert_msg(msg):
    chat_col.insert_one(msg)
    count = chat_col.count_documents({"map": msg["map"]})
    if count >50:
        # 留最新 50 筆
        oldest = chat_col.find({"map": msg["map"]}).sort("timestamp", 1).limit(count - 20)
        for old in oldest:
            chat_col.delete_one({"_id": old["_id"]})


def insert_user(username, password):
    if users_col.find_one({'username':username}):
        return 0
    users_col.insert_one({'username':username,'password':password,'role':'user'})
    return 1
        

def initialize_data():
    from bson.objectid import ObjectId

    # Skip if data already exists
    if users_col.count_documents({}) > 0:
        print("ℹ️ 資料已存在，略過初始化")
        return
    grenades_col.create_index("map", unique=True)
    users_col.create_index("username", unique=True)
    chat_col.create_index("map")
    chat_col.create_index("timestamp") 

    # Users
    users_col.insert_many([
        {"username": "admin", "password": "1234", "role": "admin"},
        {"username": "user1", "password": "abc", "role": "user"},
    ])

    # Pending throws
    pending = [
        {'map': 'Dust2', 'grenade_type': 'smoke', 'point_name': 'A long - CT', 'x': 693, 'y': 308,
         'method': {'name': '11', 'video_url': 'https://www.youtube.com/shorts/-LhZUFHWUhI'}, 'id': 1},
        {'map': 'Dust2', 'grenade_type': 'smoke', 'point_name': 'A long - CT', 'x': 693, 'y': 308,
         'method': {'name': '22', 'video_url': 'https://www.youtube.com/shorts/wubnNIWhfNw'}, 'id': 2},
        {'map': 'Dust2', 'grenade_type': 'flash', 'point_name': 'Mid Doors', 'x': 365, 'y': 288,
         'method': {'name': '33', 'video_url': 'https://www.youtube.com/shorts/i9DE62rGvlk'}, 'id': 3},
        # ... 可依需要擴充
    ]
    pending_col.insert_many(pending)

    # Main grenade data
    grenades_col.insert_one({
        "map": "Dust2",
        "grenades":{
            "smoke": [
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
            }
    })
    maps= ['Mirage','Inferno','Anubis','Ancient','Nuke','Train']
    grenades_col.insert_many([
    {
        "map": name,
        "grenades": {
            "smoke": [],
            "flash": [],
            "molotov": []
        }
    } for name in maps
])

def point(map_name, grenade_type):
    doc = grenades_col.find_one({"map": map_name})
    return doc["grenades"].get(grenade_type, []) if doc else []

def get_all_pending():
    return list(pending_col.find({}, {"_id": 0}))

def get_pending_by_name(name):
    return pending_col.find_one({"method.name": name}, {"_id": 0})

def insert_pending_method(data):
    existing = pending_col.find_one(sort=[("id", -1)])
    next_id = existing["id"] + 1 if existing else 1
    data["id"] = next_id
    pending_col.insert_one(data)
    return next_id

def get_pending_pag(page, size):
    total = pending_col.count_documents({})
    data = list(
        pending_col.find({}, {"_id": 0})
        .skip((page - 1) * size)
        .limit(size)
    )
    return {"total": total, "page": page, "size": size, "data": data}

def approve_method_by_id(throw_id):
    item = pending_col.find_one({"id": throw_id})
    if not item:
        return False, "not found"

    doc = grenades_col.find_one({"map": item["map"]})
    if not doc:
        return False, "map not found"

    grenade_type = item["grenade_type"]
    target_points = doc.get("grenades", {}).get(grenade_type, [])

    for point in target_points:
        if point["name"] == item["point_name"]:
            point["methods"].append(item["method"])
            break
    else:
        # 沒有這個點位，新增一個
        target_points.append({
            "name": item["point_name"],
            "x": item["x"],
            "y": item["y"],
            "methods": [item["method"]]
        })

    grenades_col.update_one(
        {"map": item["map"]},
        {"$set": {f"grenades.{grenade_type}": target_points}}
    )
    pending_col.delete_one({"id": throw_id})
    return True, "approved"


def reject_method_by_id(throw_id):
    result = pending_col.delete_one({"id": throw_id})
    return result.deleted_count > 0


def get_user_by_credentials(username, password):
    return users_col.find_one({"username": username, "password": password}, {"_id": 0})



# --- Run initialization when script is run directly ---


import json
import os

DATA_FILE = "data/subs.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def abone_ekle(chat_id, username):
    data = load_data()
    chat_id = str(chat_id)
    if chat_id not in data:
        data[chat_id] = []
    if username not in data[chat_id]:
        data[chat_id].append(username)
        save_data(data)
        return True
    return False

def abone_sil(chat_id, username):
    data = load_data()
    chat_id = str(chat_id)
    if chat_id in data and username in data[chat_id]:
        data[chat_id].remove(username)
        save_data(data)
        return True
    return False

def abonelik_listesi(chat_id):
    data = load_data()
    return data.get(str(chat_id), [])

def get_all_subscriptions():
    return load_data()

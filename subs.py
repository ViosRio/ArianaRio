import json
import os
from subs import abone_ekle, abone_sil, abonelik_listesi

SUBS_FILE = "data/subs.json"

# Dosya var mı kontrolü
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(SUBS_FILE):
    with open(SUBS_FILE, "w") as f:
        json.dump({}, f)

# JSON oku
def load_subs():
    with open(SUBS_FILE, "r") as f:
        return json.load(f)

# JSON kaydet
def save_subs(data):
    with open(SUBS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Abonelik ekle
def abone_ekle(chat_id, username):
    data = load_subs()
    str_id = str(chat_id)
    if str_id not in data:
        data[str_id] = []
    if username not in data[str_id]:
        data[str_id].append(username)
        save_subs(data)
        return True
    return False

# Abonelik sil
def abone_sil(chat_id, username):
    data = load_subs()
    str_id = str(chat_id)
    if str_id in data and username in data[str_id]:
        data[str_id].remove(username)
        if not data[str_id]:
            del data[str_id]
        save_subs(data)
        return True
    return False

# Belirli kullanıcının abonelik listesi
def abonelik_listesi(chat_id):
    data = load_subs()
    return data.get(str(chat_id), [])

# Tüm abonelikler (checker için)
def tum_abonelikler():
    return load_subs()

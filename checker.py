import json
import os

DOSYA_YOLU = "subs.json"

def abone_ekle(user_id, username):
    user_id = str(user_id)
    try:
        if not os.path.exists(DOSYA_YOLU):
            with open(DOSYA_YOLU, "w") as f:
                json.dump({}, f)

        with open(DOSYA_YOLU, "r+") as f:
            data = json.load(f)
            if user_id not in data:
                data[user_id] = []
            if username not in data[user_id]:
                data[user_id].append(username)
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                return True
            return False
    except Exception as e:
        print(f"Hata (abone_ekle): {e}")
        return False

def abone_sil(user_id, username):
    user_id = str(user_id)
    try:
        if not os.path.exists(DOSYA_YOLU):
            return False

        with open(DOSYA_YOLU, "r+") as f:
            data = json.load(f)
            if user_id in data and username in data[user_id]:
                data[user_id].remove(username)
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                return True
            return False
    except Exception as e:
        print(f"Hata (abone_sil): {e}")
        return False

def abonelik_listesi(user_id):
    user_id = str(user_id)
    try:
        if not os.path.exists(DOSYA_YOLU):
            return []
        with open(DOSYA_YOLU, "r") as f:
            data = json.load(f)
            return data.get(user_id, [])
    except Exception as e:
        print(f"Hata (abonelik_listesi): {e}")
        return []

import os

SUBS_PATH = "data/subs.py"

def _load_subs():
    try:
        if not os.path.exists(SUBS_PATH):
            with open(SUBS_PATH, "w") as f:
                f.write("subs = {}\n")
        from data import subs as data  # içeriği import et
        return data.subs
    except Exception as e:
        print(f"Hata (subs yükleme): {e}")
        return {}

def _save_subs(data):
    try:
        with open(SUBS_PATH, "w") as f:
            f.write("subs = " + repr(data) + "\n")
    except Exception as e:
        print(f"Hata (subs kaydetme): {e}")

def abone_ekle(user_id, username):
    user_id = str(user_id)
    data = _load_subs()
    if user_id not in data:
        data[user_id] = []
    if username not in data[user_id]:
        data[user_id].append(username)
        _save_subs(data)
        return True
    return False

def abone_sil(user_id, username):
    user_id = str(user_id)
    data = _load_subs()
    if user_id in data and username in data[user_id]:
        data[user_id].remove(username)
        _save_subs(data)
        return True
    return False

def abonelik_listesi(user_id):
    user_id = str(user_id)
    data = _load_subs()
    return data.get(user_id, [])

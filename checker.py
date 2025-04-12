# checker.py
abonelikler = {}  # {chat_id: [username1, username2, ...]}

def abone_ekle(chat_id, username):
    if chat_id not in abonelikler:
        abonelikler[chat_id] = []
    if username in abonelikler[chat_id]:
        return False
    abonelikler[chat_id].append(username)
    return True

def abone_sil(chat_id, username):
    if chat_id in abonelikler and username in abonelikler[chat_id]:
        abonelikler[chat_id].remove(username)
        return True
    return False

def abonelik_listesi(chat_id):
    return abonelikler.get(chat_id, [])

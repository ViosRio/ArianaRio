import os
import json
import time
import instaloader
import requests

BOT_TOKEN = "TELEGRAM_BOT_TOKENIN"
CHAT_ID = "8141229305"

loader = instaloader.Instaloader()
last_posts = {}

def abone_ekle(user_id, username):
    subs = load_subs()
    if user_id not in subs:
        subs[user_id] = []
    if username not in subs[user_id]:
        subs[user_id].append(username)
        save_subs(subs)
        return True
    return False

def abone_sil(user_id, username):
    subs = load_subs()
    if user_id in subs and username in subs[user_id]:
        subs[user_id].remove(username)
        save_subs(subs)
        return True
    return False

def abonelik_listesi(user_id):
    subs = load_subs()
    return subs.get(user_id, [])

def load_subs():
    if not os.path.exists("subs.json"):
        return {}
    with open("subs.json", "r") as f:
        return json.load(f)

def save_subs(subs):
    with open("subs.json", "w") as f:
        json.dump(subs, f, indent=2)

def get_last_post(username):
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        posts = profile.get_posts()
        post = next(posts, None)
        if post:
            media_id = str(post.mediaid)
            caption = post.caption or "Açıklama yok."
            media_url = post.url
            return media_id, caption, media_url
    except Exception as e:
        print(f"[{username}] Post alınamadı: {e}")
    return None, None, None

def send_telegram_message(caption, image_url):
    try:
        message = f"**Yeni Gönderi**:\n\n{caption}"
        data = {
            "chat_id": CHAT_ID,
            "caption": message,
            "parse_mode": "Markdown"
        }

        files = {}
        if image_url:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                files["photo"] = response.raw

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data=data,
            files=files if files else None
        )

    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

def check_loop():
    print("[!] Takip başlatıldı. Çıkmak için Ctrl+C.")
    while True:
        try:
            subs = load_subs()
            for user_id, usernames in subs.items():
                for username in usernames:
                    post_id, caption, image = get_last_post(username)
                    if post_id:
                        if username not in last_posts or post_id != last_posts[username]:
                            print(f"[{username}] Yeni gönderi tespit edildi.")
                            send_telegram_message(f"{username}: {caption}", image)
                            last_posts[username] = post_id
        except Exception as e:
            print(f"Genel hata: {e}")
        time.sleep(120)

if __name__ == "__main__":
    check_loop()

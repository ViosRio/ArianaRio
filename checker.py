# checker.py
import json
import time
import requests
from instagrapi import Client
from datetime import datetime
import os

BOT_TOKEN = "TELEGRAM_BOT_TOKENIN"
CHAT_ID = "SAHIP_CHAT_ID"  # Ya da kullanıcıya özel log sistemi

cl = Client()
cl.login("INSTAGRAM_KULLANICI", "SIFRE")  # Gerekirse çevresel değişken yaparız

last_posts = {}

def get_last_post(username):
    try:
        user_id = cl.user_id_from_username(username)
        posts = cl.user_medias(user_id, 1)
        if posts:
            return posts[0].id, posts[0].caption_text, posts[0].thumbnail_url
    except Exception as e:
        print(f"[{username}] Post alınamadı: {e}")
    return None, None, None

def load_subs():
    if not os.path.exists("subs.json"):
        return {}
    with open("subs.json", "r") as f:
        return json.load(f)

def send_telegram_message(caption, image_url):
    try:
        message = f"**Yeni Gönderi**:\n\n{caption}"
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", data={
            "chat_id": CHAT_ID,
            "caption": message,
            "parse_mode": "Markdown"
        }, files={"photo": requests.get(image_url, stream=True).raw})
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

def check_loop():
    while True:
        subs = load_subs()
        for user_id, usernames in subs.items():
            for username in usernames:
                post_id, caption, image = get_last_post(username)
                if post_id and username in last_posts:
                    if post_id != last_posts[username]:
                        print(f"Yeni post bulundu: {username}")
                        send_telegram_message(f"{username}: {caption}", image)
                last_posts[username] = post_id
        time.sleep(120)  # 2 dakikada bir kontrol

if __name__ == "__main__":
    check_loop()

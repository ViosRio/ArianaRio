import json
import requests
import instaloader
import telebot
from telebot import types
from checker import abone_ekle, abone_sil, abonelik_listesi

# Telegram bot token
TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# Instagram giriş
INSTAGRAM_USERNAME = "YOUR_USERNAME"
INSTAGRAM_PASSWORD = "YOUR_PASSWORD"
loader = instaloader.Instaloader()

try:
    loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    print("Instagram oturumu açıldı.")
except Exception as e:
    print(f"Giriş hatası: {e}")

# /start
@bot.message_handler(commands=["start"])
def start_handler(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("♂️ SAHİP", url="https://t.me/ViosCeo"),
        types.InlineKeyboardButton("🗨️ KANAL", url="https://t.me/ViosTeam"),
        types.InlineKeyboardButton("📕 Komutlar", callback_data="help")
    )
    bot.send_message(message.chat.id,
        "Merhaba! Ben Instagram analiz botuyum.\n"
        "Gizli profilleri analiz edebilmem için onları takip etmen gerekiyor.",
        reply_markup=keyboard
    )

# /rave
@bot.message_handler(commands=["rave"])
def rave_handler(message):
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "Kullanım: /rave kullanıcıadı")

    username = args[1]
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        caption = (
            f"**{profile.full_name}** (@{profile.username})\n"
            f"Takipçi: {profile.followers}\n"
            f"Takip: {profile.followees}\n"
            f"Gönderi: {profile.mediacount}\n"
            f"Biyografi: {profile.biography}"
        )
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("📸 Story", callback_data=f"story_{username}"),
            types.InlineKeyboardButton("📕 Medya", callback_data=f"media_{username}"),
            types.InlineKeyboardButton("👥 Takipçiler", callback_data=f"followers_{username}"),
            types.InlineKeyboardButton("👤 Takip Ettikleri", callback_data=f"following_{username}"),
            types.InlineKeyboardButton("🔰 Abonelik", callback_data=f"abone|{username}")
        )
        bot.send_photo(message.chat.id, profile.profile_pic_url, caption=caption,
                       parse_mode="Markdown", reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {e}")

# Callback
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data

    if data == "help":
        bot.send_message(call.message.chat.id,
            "Komutlar:\n"
            "/story kullanıcıadı - Hikayeleri gösterir\n\n"
            "/rave kullanıcıadı - Profil analiz eder\n\n"
            "/save link - Gönderi indirir\n\n"
            "/hashtag etiket - Hashtag kazıyıcısı\n\n"
            "/abonelik kullanıcıadı - Abone ol\n\n"
            "/abonelik_iptal kullanıcıadı - Abonelikten çık\n\n"
            "/aboneliklerim - Abonelik listeni gösterir"
        )

    elif data.startswith("abone|"):
        username = data.split("|")[1]
        user_id = str(call.from_user.id)
        try:
            with open("subs.json", "r+") as f:
                try:
                    subs = json.load(f)
                except:
                    subs = {}
                if user_id not in subs:
                    subs[user_id] = []
                if username not in subs[user_id]:
                    subs[user_id].append(username)
                    f.seek(0)
                    json.dump(subs, f, indent=4)
                    f.truncate()
                    bot.answer_callback_query(call.id, "Abonelik eklendi.")
                else:
                    bot.answer_callback_query(call.id, "Zaten abonesin.")
        except Exception as e:
            bot.answer_callback_query(call.id, f"Hata: {e}")

# Abonelikler
@bot.message_handler(commands=["abonelik"])
def abonelik_ekle_handler(message):
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "kullanım: \n\n [ /abonelik cerenlovely ]")
    username = args[1]
    if abone_ekle(message.chat.id, username):
        bot.reply_to(message, f"✅DURUM \n\n {username} kullanıcısına Abone Olundu.")
    else:
        bot.reply_to(message, f"{username} zaten listende.")

@bot.message_handler(commands=["abonelik_iptal"])
def abonelik_iptal_handler(message):
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "kullanım: \n\n [ /abonelik_iptal cerenlovely ]")
    username = args[1]
    if abone_sil(message.chat.id, username):
        bot.reply_to(message, f"{username} aboneliğin iptal edildi.")
    else:
        bot.reply_to(message, f"{username} listende yok.")

@bot.message_handler(commands=["aboneliklerim"])
def abonelik_listesi_handler(message):
    abonelikler = abonelik_listesi(message.chat.id)
    if abonelikler:
        liste = "\n".join([f"• {a}" for a in abonelikler])
        bot.reply_to(message, f"Aboneliklerin:\n{liste}")
    else:
        bot.reply_to(message, "Hiçbir kullanıcıya abone değilsin.")

# /hashtag
@bot.message_handler(commands=["hashtag"])
def hashtag_handler(message):
    tag = message.text.replace("/hashtag", "").strip()
    if not tag:
        return bot.reply_to(message, "Hashtag belirtmedin.")
    
    try:
        url = f"https://cerenyaep.serv00.net/client/app/tokplus/data.php?explore={tag}"
        r = requests.get(url)
        if r.status_code == 200 and r.text.strip():
            blocks = r.text.strip().split('<hr>')
            result = "\n\n———\n\n".join(["\n".join(b.split("<br>")).strip() for b in blocks])
            bot.reply_to(message, f"**#{tag}** hakkında:\n\n{result}", parse_mode="Markdown")
        else:
            bot.reply_to(message, "Sonuç bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

# Başlat
print("Bot çalışıyor...")
bot.polling(none_stop=True)

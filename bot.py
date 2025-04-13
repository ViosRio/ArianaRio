import requests
import instaloader
import telebot
from telebot import types
from checker import abone_ekle, abone_sil, abonelik_listesi

# Telegram bot token
TOKEN = "{BOT_TOKEN}"  # Buraya Telegram botunuzun tokenını ekleyin
bot = telebot.TeleBot(TOKEN)

# Instagram kullanıcı bilgileri
INSTAGRAM_USERNAME = "{USERNAME}"  # Kendi Instagram kullanıcı adınızı buraya yazın
INSTAGRAM_PASSWORD = "{PASSWORD}"  # Kendi Instagram şifrenizi buraya yazın

# Instaloader ile oturum açma
loader = instaloader.Instaloader()
try:
    loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    print("Instagram oturumu başarıyla açıldı.")
except Exception as e:
    print(f"Instagram oturumu açılırken bir hata oluştu: {str(e)}")

# /start komutu
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text="♂️ SAHİP", url="https://t.me/ViosCeo")
    button2 = types.InlineKeyboardButton(text="🗨️ KANAL", url="https://t.me/ViosTeam")
    button3 = types.InlineKeyboardButton(text="📕 Komutlar", callback_data="help")

    keyboard.add(button1, button2, button3)

    bot.reply_to(
        message,
        "Merhaba! Ben İnstagram Analiz Botuyum. Gizli profilleri sadece takip ettiğiniz sürece analiz edebilirim.\n\n"
        "Aşağıdaki butonları kullanarak daha fazla bilgi alabilirsin:",
        reply_markup=keyboard
    )

# /rave komutu - Profil analizi
# bot.py içindeki /rave komutu kısmına ekle:
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.message_handler(commands=['rave'])
def rave_command(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Kullanım: /rave kullanıcıadı")
        return

    username = args[1]
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        caption = f"""
**{profile.full_name}** (@{profile.username})
Takipçi: {profile.followers}
Takip: {profile.followees}
Gönderi: {profile.mediacount}
Biyografi: {profile.biography}
"""
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("🔰 Abonelik", callback_data=f"abone|{username}")
        keyboard.add(button)

        bot.send_photo(
            chat_id=message.chat.id,
            photo=profile.profile_pic_url,
            caption=caption,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")
        # Profil resmi URL'si
        profile_picture_url = profile.get_profile_pic_url()

        # Butonlar
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text="📸 Story", callback_data=f"story_{username}")
        button2 = types.InlineKeyboardButton(text="📕 Medya", callback_data=f"media_{username}")
        button3 = types.InlineKeyboardButton(text="👥 Takipçiler", callback_data=f"followers_{username}")
        button4 = types.InlineKeyboardButton(text="👤 Takip Ettikleri", callback_data=f"following_{username}")
        button5 = types.InlineKeyboardButton(text="🔰 Abonelik", callback_data=f"subs_{username}")


        keyboard.add(button1, button2, button3, button4, button5)

        # Profil resmi ve bilgi mesajı
        bot.send_photo(
            message.chat.id,
            profile_picture_url,
            caption=info,
            reply_markup=keyboard
        )

    except Exception as e:
        bot.reply_to(message, f"Profil analizi yapılamadı: {str(e)}")

# Abonelik işlemleri
@bot.on_callback_query()
def callback_handler(_, query):
    data = query.data
    if data.startswith("abone|"):
        username = data.split("|")[1]
        user_id = str(query.from_user.id)
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
                query.answer("Abonelik başarıyla eklendi!")
            else:
                query.answer("Zaten abonesin!")

@bot.message_handler(commands=['abonelik'])
def abonelik_ekle(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Kullanıcı adı belirtmedin kanka. Örnek: /abonelik mehmet")
        return
    username = args[1].strip()
    if abone_ekle(message.chat.id, username):
        bot.reply_to(message, f"{username} kullanıcısına başarıyla abone olundu.")
    else:
        bot.reply_to(message, f"Zaten {username} kullanıcısına abonesin.")

# /abonelik_iptal komutu
@bot.message_handler(commands=['abonelik_iptal'])
def abonelikten_cik(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Kullanıcı adı belirtmedin kanka. Örnek: /abonelik_iptal mehmet")
        return
    username = args[1].strip()
    if abone_sil(message.chat.id, username):
        bot.reply_to(message, f"{username} kullanıcısının aboneliği iptal edildi.")
    else:
        bot.reply_to(message, f"{username} kullanıcısına zaten abone değilsin.")

# /aboneliklerim komutu
@bot.message_handler(commands=['aboneliklerim'])
def abonelik_listesi_goster(message):
    abonelikler = abonelik_listesi(message.chat.id)
    if abonelikler:
        joined = "\n".join(f"• {u}" for u in abonelikler)
        bot.reply_to(message, f"Şu anda abone olduğun profiller:\n\n{joined}")
    else:
        bot.reply_to(message, "Hiçbir kullanıcıya abone değilsin.")

# Yardım mesajı
@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_message(call):
    help_text = (
        "Komutlar:\n"
        "[1] /story : Belirtilen kullanıcı Adının Hikayelerini İndirir.\n\n"
        "[2] /rave : Belirtilen Profil Hakkında Analiz Yapar.\n\n"
        "[3] /save : Bir Gönderi Bağlantısından Medya İndirir.\n\n"
        "[4] /hashtag : Hastag Kazıyıcısıdır Etiketlere Göz At \n\n"
        "Not: Gizli Profillerden Veri Çekebilmek İçin Takip Etmelisiniz."
    )
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, help_text)

# /hashtag komutu - Hashtag ile API'den veri alma
@bot.message_handler(commands=['hashtag'])
def hashtag_search(message):
    hashtag = message.text.replace("/hashtag", "").strip()
    if not hashtag:
        bot.reply_to(message, "Lütfen bir hashtag girin.")
        return

    url = f"https://cerenyaep.serv00.net/client/app/tokplus/data.php?explore={hashtag}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text.strip()
            if content:
                # Her video bloğunu ayır
                items = content.split('<hr>')
                formatted = []
                for item in items:
                    lines = item.strip().split('<br>')
                    block = []
                    for line in lines:
                        line = line.strip()
                        if line:
                            block.append(line)
                    if block:
                        formatted.append("\n".join(block))

                final_result = "\n\n———\n\n".join(formatted)
                bot.reply_to(message, f"Hashtag **{hashtag}** ile ilgili sonuçlar:\n\n{final_result}", parse_mode="Markdown")
            else:
                bot.reply_to(message, "Veri bulunamadı veya içerik boş.")
        else:
            bot.reply_to(message, "API'ye erişim sağlanamadı. Tekrar dene kanki.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")

# Bot başlatma
print("Bot çalışıyor...")
bot.polling(none_stop=True, interval=0, timeout=60)

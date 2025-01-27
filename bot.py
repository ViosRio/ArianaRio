import request
import instaloader
import telebot
from telebot import types

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
@bot.message_handler(commands=['rave'])
def profile_analysis(message):
    username = message.text.replace("/rave", "").strip()
    if not username:
        bot.reply_to(message, "Lütfen analiz için bir kullanıcı adı yazın!")
        return

    bot.reply_to(message, f"{username} adlı kullanıcı için analiz yapılıyor...")

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        
        # Profil bilgilerini alıyoruz
        info = (
            f"Kullanıcı: {profile.username}\n"
            f"Ad: {profile.full_name}\n"
            f"Biyografi: {profile.biography}\n"
            f"Takipçi Sayısı: {profile.followers}\n"
            f"Takip Ettikleri: {profile.followees}\n"
            f"Gönderiler: {profile.mediacount}\n"
            f"Hesap Gizli mi?: {'Evet' if profile.is_private else 'Hayır'}\n"
        )

        # Profil resmi URL'si
        profile_picture_url = profile.get_profile_pic_url()

        # Butonlar
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text="📸 Story", callback_data=f"story_{username}")
        button2 = types.InlineKeyboardButton(text="📕 Medya", callback_data=f"media_{username}")
        button3 = types.InlineKeyboardButton(text="👥 Takipçiler", callback_data=f"followers_{username}")
        button4 = types.InlineKeyboardButton(text="👤 Takip Ettikleri", callback_data=f"following_{username}")

        keyboard.add(button1, button2, button3, button4)

        # Profil resmi ve bilgi mesajı
        bot.send_photo(
            message.chat.id,
            profile_picture_url,
            caption=info,
            reply_markup=keyboard
        )

    except Exception as e:
        bot.reply_to(message, f"Profil analizi yapılamadı: {str(e)}")

# Yardım mesajı
@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_message(call):
    help_text = (
        "Komutlar:\n"
        "/story - Belirtilen kullanıcı adının hikayelerini indirir.\n"
        "/rave - Belirtilen profil hakkında analiz yapar.\n"
        "/save - Bir gönderi bağlantısından medya indirir.\n\n"
        "Not: Gizli profillerden veri çekebilmek için takip etmelisiniz."
    )
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, help_text)

# Bot başlatma
print("Bot çalışıyor...")
bot.polling(none_stop=True, interval=0, timeout=60)

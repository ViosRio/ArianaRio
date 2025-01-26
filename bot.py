import instaloader
import telebot
from telebot import types

# Telegram bot token
TOKEN = "{BOT_TOKEN}"  # Buraya Telegram botunuzun tokenını ekleyin
bot = telebot.TeleBot(TOKEN)

# Instagram kullanıcı bilgileri
INSTAGRAM_USERNAME = "your_instagram_username"  # Kendi Instagram kullanıcı adınızı buraya yazın
INSTAGRAM_PASSWORD = "your_instagram_password"  # Kendi Instagram şifrenizi buraya yazın

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

# /story komutu - Hikaye indirme
@bot.message_handler(commands=['story'])
def download_story(message):
    username = message.text.replace("/story", "").strip()
    if not username:
        bot.reply_to(message, "Lütfen bir kullanıcı adı belirtin!")
        return

    bot.reply_to(message, f"{username} adlı kullanıcının hikayeleri indiriliyor...")

    try:
        loader.download_stories(usernames=[username], filename_target=f"./stories/{username}")
        bot.reply_to(message, f"{username} adlı kullanıcının hikayeleri başarıyla indirildi!")
    except Exception as e:
        bot.reply_to(message, f"Hikaye indirilemedi: {str(e)}")

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
        info = (
            f"Kullanıcı: {profile.username}\n"
            f"Ad: {profile.full_name}\n"
            f"Biyografi: {profile.biography}\n"
            f"Takipçi Sayısı: {profile.followers}\n"
            f"Takip Ettikleri: {profile.followees}\n"
            f"Gönderiler: {profile.mediacount}\n"
            f"Hesap Gizli mi?: {'Evet' if profile.is_private else 'Hayır'}\n"
        )
        bot.reply_to(message, info)
    except Exception as e:
        bot.reply_to(message, f"Profil analizi yapılamadı: {str(e)}")

# /save komutu - Gönderi indirme
@bot.message_handler(commands=['save'])
def download_post(message):
    post_url = message.text.replace("/save", "").strip()
    if not post_url:
        bot.reply_to(message, "Lütfen bir gönderi bağlantısı paylaşın!")
        return

    bot.reply_to(message, "Medya indiriliyor...")

    try:
        post = instaloader.Post.from_shortcode(loader.context, post_url.split("/")[-2])
        loader.download_post(post, target="posts")
        bot.reply_to(message, "Gönderi başarıyla indirildi!")
    except Exception as e:
        bot.reply_to(message, f"Medya indirilemedi: {str(e)}")

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

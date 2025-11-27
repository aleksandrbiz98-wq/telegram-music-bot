import telebot
import yt_dlp

bot = telebot.TeleBot("ТОКЕН_ОТ_БОТА")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Отправь название песни — я найду и скачаю её в MP3!")

@bot.message_handler(func=lambda m: True)
def music(message):
    query = message.text
    bot.send_message(message.chat.id, "Ищу музыку...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        filename = ydl.prepare_filename(info['entries'][0]).replace(".webm", ".mp3")

    with open(filename, "rb") as audio:
        bot.send_audio(message.chat.id, audio)

bot.polling()

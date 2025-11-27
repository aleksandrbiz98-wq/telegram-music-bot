import telebot
from yt_dlp import YoutubeDL

# Токен Telegram бота
TOKEN = "ТВОЙ_ТОКЕН_ОТ_БОТА"
bot = telebot.TeleBot(TOKEN)

# Опции yt-dlp с cookies
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # сохраняет в папку downloads
    'cookies': 'cookies.txt',  # путь к файлу cookies
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Создаем папку downloads, если нет
import os
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def download_audio(message):
    query = message.text
    bot.send_message(message.chat.id, f"Ищу аудио по запросу: {query}")

    try:
        # Поиск на YouTube
        with YoutubeDL({'quiet': True}) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = result['webpage_url']

        # Скачиваем аудио
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        filename = f"downloads/{result['title']}.mp3"
        # Отправка аудио пользователю
        with open(filename, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, title=result['title'])

    except Exc

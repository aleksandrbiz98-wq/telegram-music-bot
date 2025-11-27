import os
import telebot
from yt_dlp import YoutubeDL
from tempfile import NamedTemporaryFile

# Получаем токен из переменной окружения Render
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Настройки yt-dlp для скачивания аудио
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'noplaylist': True
}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Отправь название песни, и я пришлю тебе аудио с YouTube.")

# Обработка текстовых сообщений (поиск музыки)
@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    bot.send_message(message.chat.id, f"Ищу аудио для: {query} ...")

    # Используем yt-dlp для поиска на YouTube
    with YoutubeDL({'quiet': True}) as ydl:
        try:
            # Поиск и получение первого видео
            result = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = result['webpage_url']
        except Exception as e:
            bot.send_message(message.chat.id, f"Не удалось найти видео: {e}")
            return

    # Скачивание аудио во временный файл
    try:
        with YoutubeDL(ydl_opts) as ydl:
            temp_file = NamedTemporaryFile(delete=False, suffix='.mp3')
            ydl.download([url])
            # Найдётся скачанный mp3 (yt-dlp создаёт файл в текущей папке)
            # Для простоты, используем название видео
            filename = f"{result['title']}.mp3"
            os.rename(result['title'] + ".mp3", temp_file.name)
            # Отправка пользователю
            with open(temp_file.name, 'rb') as audio:
                bot.send_audio(message.chat.id, audio, title=result['title'])
            os.remove(temp_file.name)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при скачивании: {e}")

# Запуск бота
bot.polling(none_stop=True)

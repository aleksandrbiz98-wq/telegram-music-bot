import os
import asyncio
from aiogram import Bot, Dispatcher, types
from yt_dlp import YoutubeDL

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def search_music(message: types.Message):
    query = message.text

    ydl_opts_search = {"quiet": True, "skip_download": True, "extract_flat": "in_playlist"}
    with YoutubeDL(ydl_opts_search) as ydl:
        result = ydl.extract_info(f"ytsearch1:{query}", download=False)
        if not result.get("entries"):
            await message.reply("Ничего не найдено 😔")
            return
        video = result["entries"][0]

    url = f"https://www.youtube.com/watch?v={video['id']}"
    await message.reply(f"Скачиваю аудио:\n{video['title']}")

    ydl_opts_download = {
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        "quiet": True,
    }

    with YoutubeDL(ydl_opts_download) as ydl:
        ydl.download([url])

    await message.answer_audio(types.InputFile("audio.mp3"))
    os.remove("audio.mp3")

if __name__ == "__main__":
    asyncio.run(dp.start_polling())

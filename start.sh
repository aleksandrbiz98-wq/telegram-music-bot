#!/bin/bash
# Обновляем пакеты и устанавливаем ffmpeg
apt-get update
apt-get install -y ffmpeg

# Запускаем бота
python bot.py

#!/bin/bash
echo "Running start.sh"
which ffmpeg || echo "ffmpeg not found"
apt-get update
apt-get install -y ffmpeg
python bot.py

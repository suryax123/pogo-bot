import schedule
import time
import os
import re
import subprocess
import telebot
from keep_alive import keep_alive
from threading import Thread

keep_alive()

TOKEN = "8460070207:AAGYRIx5-Y2bI8qfPUNpYfJBv_QnVowPM0k"
CHAT_ID = "7830761325"   # Replace with your Telegram chat ID

bot = telebot.TeleBot(TOKEN)
STREAM_URL = "https://m3umergers.xyz/artl/artl.ts?id=a02p"
OUTPUT_FILE = "pogo_multitrack.mp4"

# Detect all audio tracks
def get_all_audio_tracks(stream_url):
    cmd = ["ffmpeg", "-i", stream_url]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    ffmpeg_output = result.stderr + result.stdout
    matches = []
    for match in re.findall(r"Stream #0:(\d+).*Audio.*\((.*?)\)", ffmpeg_output):
        track_index = int(match[0])
        matches.append(track_index)
    return matches

# Record and send video
def record_pogo():
    audio_tracks = get_all_audio_tracks(STREAM_URL)
    if not audio_tracks:
        print("No audio tracks found!")
        return

    map_cmd = " ".join([f"-map 0:a:{i}" for i in audio_tracks])
    ffmpeg_cmd = f'ffmpeg -i "{STREAM_URL}" -map 0:v:0 {map_cmd} -t 00:01:00 -c copy "{OUTPUT_FILE}"'
    print("Recording with command:", ffmpeg_cmd)
    os.system(ffmpeg_cmd)

    # Send video to Telegram chat
    try:
        with open(OUTPUT_FILE, "rb") as video:
            bot.send_video(CHAT_ID, video)
        print("Video sent successfully!")
    except Exception as e:
        print("Failed to send video:", e)

# Schedule recordings
schedule.every().day.at("06:00").do(record_pogo)
schedule.every().day.at("22:55").do(record_pogo)

# Simple bot command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Pogo bot is running!")

Thread(target=bot.polling).start()

while True:
    schedule.run_pending()
    time.sleep(1)

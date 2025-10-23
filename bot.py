import os
import time
import subprocess
import telebot
from datetime import datetime
import schedule

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

def record_video():
    url = "https://m3umergers.xyz/artl/artl.ts?id=a02p"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = f"record_{timestamp}.mp4"
    cmd = [
        "ffmpeg", "-i", url,
        "-map", "0:v:0", "-map", "0:a:2",
        "-t", "00:02:00", "-c", "copy", output
    ]
    subprocess.run(cmd)
    with open(output, "rb") as video:
        bot.send_video(CHAT_ID, video)
    os.remove(output)

# Schedule times (6–7 AM & 10:55 PM–12 AM)
schedule.every().day.at("06:00").do(record_video)
schedule.every().day.at("22:55").do(record_video)

print("✅ Scheduler started successfully...")

while True:
    schedule.run_pending()
    time.sleep(10)

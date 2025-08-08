import telebot
import schedule
import time
import threading
from datetime import datetime

BOT_TOKEN = "8231704674:AAFc3-ZqU47Ba-ytura8atk6FcZJ2G6wL3Q"
USER_ID = 5949872528  # Replace with your own ID

bot = telebot.TeleBot(BOT_TOKEN)
tasks = []

@bot.message_handler(func=lambda message: message.chat.id == USER_ID)
def handle_task(message):
    task_text = message.text.strip()
    if task_text:
        tasks.append(task_text)
        bot.reply_to(message, f"Task saved for tomorrow: {task_text}")

def send_polls():
    global tasks
    if tasks:
        for task in tasks:
            bot.send_poll(USER_ID, f"{task}?", ["Yes", "No"], is_anonymous=False)
        tasks = []  # clear after sending

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Schedule job for 8 AM every day
schedule.every().day.at("08:30").do(send_polls)

# Start scheduler in background
threading.Thread(target=schedule_checker, daemon=True).start()

print("Bot is running...")
bot.infinity_polling()


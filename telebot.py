import psutil
from typing import Final

import requests
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import signal
import sys

TOKEN = "7096939476:AAGhtV5dKp8kwUtKxNjYob4zhwQ6UXf28tw"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"
BOT_USERNAME: Final = "@ServerStatusMCYQ_bot"
chat_id = "700351178"  # Replace with your group chat ID


async def start_command(update: Update):
    await update.message.reply_text("Hello! Thanks for talking to my bot")


async def help_command(update: Update):
    await update.message.reply_text("Hello! Type something so I can respond")


async def custom_command(update: Update):
    await update.message.reply_text("Custom Command")


def handle_response(text: str) -> str:
    # Your function code here
    processed: str = text.lower()  # Change all input to lower case so if else can detect
    if "hello" in text:
        return "Heyy cutie!"
    if "minecraft" in text:
        return "I love playing!"
    if "status" in text:
        return check_if_process_running("javaw.exe")
    if "info" in text:
        return pc_info()
    if "awake" in text:
        return "I am wide awake!!"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type  # inform on group chat or private chat
    text: str = update.message.text

    print(f'user ({update.message.chat.id}) in {message_type}): "{text}"')

    # Check if text processing is working correctly
    processed_text = text.lower()
    print("Processed text:", processed_text)

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()  # strip for no whitespaces
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot:", response)
    print("Bot: Replying with message:", response)
    await context.bot.send_message(chat_id=update.message.chat_id, text=response)


def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


##
def list_running_processes():  # List out all running processes in the system
    processes = psutil.process_iter()
    for process in processes:
        print(f"Process name: {process.name()} | PID: {process.pid}")


def check_if_process_running(process_name):  # Check if a certain process is running
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return "The Server is running!"
    return "❌The Server is offline now!❌"


def check_running_first(process_name):  # Run first time only!!
    command_message = (
        "Available Tele Commands\n"
        "- @me status\n"
        "  To check the status of the server\n\n"
        "- @me info\n"
        "  Display server hardware usuage\n\n"
        "- @me awake\n"
        "  Check if tele bot is awake and running"
    )
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return "🔛𝗺𝗰.𝘆𝘂𝗮𝗻𝗾𝗶𝗻𝗴.𝘀𝗶𝘁𝗲 is 𝗢𝗡𝗟𝗜𝗡𝗘🔛\n\n" + command_message
    return "❌𝗺𝗰.𝘆𝘂𝗮𝗻𝗾𝗶𝗻𝗴.𝘀𝗶𝘁𝗲 is offline.❌ Please check again later\n\n" + command_message


def pc_info():  # List system's important data
    cpu_usage = f"CPU usage: {psutil.cpu_percent()}%"
    total_memory = f"Total memory: {psutil.virtual_memory().total / 1024 / 1024:.2f} MB"
    available_memory = f"Available memory: {psutil.virtual_memory().available / 1024 / 1024:.2f} MB"
    memory_usage = f"Memory usage: {psutil.virtual_memory().percent}%"

    return f"{cpu_usage}\n{total_memory}\n{available_memory}\n{memory_usage}"


def cleanup_function(signum, frame):  # This function will be called when the script is stopped
    close_script = (
        "The bot has fallen asleep and will not respond."
    )
    send_message(chat_id="-1002114816980", text=close_script)
    time.sleep(3)
    send_message(chat_id="-1002114816980", text="🥱😴💤")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, cleanup_function)  # Ctrl+C
    signal.signal(signal.SIGTERM, cleanup_function)  # Termination signal

    send_message(chat_id="-1002114816980", text=check_running_first("javaw.exe"))

    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)
    print("Polling...")
    app.run_polling(poll_interval=3)

import subprocess, timeout_decorator
from timeout_decorator import TimeoutError
import os


import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

BOT_TOKEN = "499748172:AAF-GpIxh7qojA93_XBMKC0PD2sWtpy2Pus"
bot = telegram.Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text="I'm a Python bot, please write python code to me!")


@timeout_decorator.timeout(30, use_signals=False, exception_message="Time out!",)
def run_code(f, update):
        process = subprocess.Popen(['python', os.getcwd() + '/' + f.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = process.communicate()
        bot.send_message(chat_id=update.message.chat_id, text=out[0] + out[1])


def echo(bot, update):
    f = open(update.message.from_user.name,"w+")
    f.write(update.message.text)
    f.flush()
    f.close()
    temp = update.message.text.encode('utf-8')
    check_str = "os."
    if (temp.find(check_str) == -1):
        try:
            run_code(f, update)
        except TimeoutError:
            bot.send_message(chat_id=update.message.chat_id, text="Your program worked too long!")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, you used forbidden command '" + check_str + "'")
    os.remove(os.getcwd() + '/' + f.name)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


echo_handler = MessageHandler(Filters.text, echo)
unknown_handler = MessageHandler(Filters.command, unknown)
start_handler = CommandHandler('start', start)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(unknown_handler)


updater.start_polling()

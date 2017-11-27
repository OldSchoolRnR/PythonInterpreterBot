import subprocess

import os
import telegram
#from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

BOT_TOKEN = "499748172:AAF-GpIxh7qojA93_XBMKC0PD2sWtpy2Pus"
bot = telegram.Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    f = open(update.message.from_user.name,"w+")
    f.write(update.message.text)
    f.flush()
    f.close()
    #update.message.text
    #update.message.from_user.name
    process = subprocess.Popen(['python', os.getcwd() + '/'+f.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = process.communicate()
    bot.send_message(chat_id=update.message.chat_id, text=out[0]+out[1])
    os.remove( os.getcwd() + '/'+f.name)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


echo_handler = MessageHandler(Filters.text, echo)
unknown_handler = MessageHandler(Filters.command, unknown)
start_handler = CommandHandler('start', start)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(unknown_handler)


updater.start_polling()

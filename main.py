import subprocess
import timeout_decorator
from timeout_decorator import TimeoutError
import os, re
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import bot_token

stop_all=False

BOT_TOKEN = bot_token.BOT_TOKEN
bot = telegram.Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a Python bot, please write python code to me!")


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This bot have 2 modes. Work on real time mode and without it. For work in real time mode type \"REAL_TIME_PROGRAM\" (without brackets) and your code from a new line. If you don't need this - just type your code.")


def proc(f, update, real_time):
    for path in run_code(f, real_time, update):
        pass
        # bot.send_message(chat_id=update.message.chat_id, text=path.encode("utf-8"))


def echo(bot, update):
    global stop_all
    f = open(update.message.from_user.name, "w+")

    #Check for os and real time

    temp = update.message.text.encode('utf-8')
    if (temp.startswith("REAL_TIME_PROGRAM")):
        temp = temp[17:]
        real_time = True
    else:
        real_time = False

    f.write(temp)
    f.flush()
    f.close()
    if (re.search(r'^(import\sos)|(import\s.+\sos(\s.+|$))', temp, flags=re.MULTILINE) == None):
        try:
            run_code(f, real_time, update)
        except TimeoutError:
            stop_all = True
            bot.send_message(chat_id=update.message.chat_id, text="Your program worked too long!")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, you used forbidden command '" + "os." + "'")
    os.remove(os.getcwd() + '/' + f.name)
    stop_all = False


@timeout_decorator.timeout(10, use_signals=False)
def run_code(f, real_time, update):
    process = subprocess.Popen(['python', os.getcwd() + '/' + f.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if real_time:
        while not stop_all:
            line = process.stdout.readline().rstrip()
            if not line and process.stderr:
                line = process.stderr.readline().rstrip()

            if not line:
                break

            bot.send_message(chat_id=update.message.chat_id, text=line.encode("utf-8"))
    else:
        stdout, stderr = process.communicate()

        bot.send_message(chat_id=update.message.chat_id, text=stdout.encode("utf-8")+stderr.encode("utf-8"))



def stop(bot, update):
    global stop_all
    stop_all = True
    bot.send_message(chat_id=update.message.chat_id, text="You stopped your program.")


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


echo_handler = MessageHandler(Filters.text, echo)
unknown_handler = MessageHandler(Filters.command, unknown)
start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
help_handler = CommandHandler('help', help)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(unknown_handler)


updater.start_polling()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import random
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)

ans_list = ["El dotor Bisman tenia digamo contra la presidenta y lo que dijo, tenia todo confirmado todo cierto",
 "él sea estaba apuesto a todo",
 "o sea que puso el pan sobre la mesa, al pan pan, al vino vino, sobre las cartas la mesa",
 "con mucha verdad, nada de mentira entonces y por eso lo mandaron a asesinar",
 "Yo quiero que se aclare justicia para Discman",
 "o sea a él lo assssesinaron, o sea lo mandaron a asesinar",
 "yo soy magre y agüela",
 "yo estoy acá presente pidiendo justicia para Bisman",
 "como chi o como no",
 "como como?",
 "yo estoy en silencio y pa hacer un homenaje a Bisman",
 "porque mataron a un fiscal",
 "se podía hablar y arreglar las cosas hasta que se sepa todas las cosas y no mandar matar",
 "Jorge Dib soy yo",
 "Un argentino, viva la patria. 1810-2015. El pueblo quiere saber. Salvemos la república",
 "Lo que aquí he expresado el sentimiento de un argentino de 65 años",
 "dentro de la ley todo, fuera de la ley nada",
 "Aquellos que tenemos como yo mi edad",
 "lo menos que merece un ser humano por mas bronca que se tenga es decir 'descanse en paz' porque todos salimos de una madre",
 "lamentablemente no soy doctor, no soy abogado, no soy penalista",
 "simplemente soy un ser humano autodidáctico",
 "hay transplante de todo menos de cerebro, pero yo pienso",
 "me encuentro con tristes realidades",
 "yo soy argentino, hujo de argentino y nieto de árabes",
 "me encantó porque es como si me hubieran matado un hijo a mi",
 "muy buenmozo, un encanto de persona. Ojalá lo hubiera conocido en vida",
 "hermoso hermoso, me encanta"]

key_list = ["Nisman", "Bisman", "nisman", "bisman", "cartas", "mesa", "NISMAN", "BISMAN", "Doctora",
"Sobre las cartas", "sobre las cartas", "apuesto a todo", "todo confirmado", "Doctor", "doctor", "dotor", "dotora", "Dotora"]

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    answer = ""
    ok = False
    for k in key_list:
        if k in update.message.text:
            answer = random.choice(ans_list)
            ok = True
    if ok:
        update.message.reply_text(answer)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    run(updater)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
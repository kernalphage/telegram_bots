#!/usr/bin/python3
import bot_secrets

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import logging
import re
import urllib
from wikihow import getwikihow

updater = Updater(token=bot_secrets.PAGING_BOT_KEY)
dispatcher = updater.dispatcher

logging = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



def iama(bot, update, args):
    query = args[0]
    bot.sendMessage(chat_id=update.message.chat_id,text="poof you're a {}".format(query))

print("Starting listening...")

imgHandler = CommandHandler('iama', iama,pass_args=True)
dispatcher.add_handler(imgHandler)

print("waiting...")

updater.start_polling()
updater.idle()

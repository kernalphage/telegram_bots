#!/usr/bin/python3
key="No Key here NOSIREE"
print("Importing...")
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import logging
import re
import urllib
from wikihow import getwikihow

updater = Updater(token=key)
dispatcher = updater.dispatcher

logging = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def getURL(query):
    if not query:
        return
    match = re_image.search(query)
    if( match ):
        img, top, bottom = [urllib.parse.quote(x) for x in match.groups() ]
        url =  "http://urlme.me/{}/{}/{}.jpg".format(img,top,bottom)
        return url
    raise ArgumentError ("Query was incorrect")

def imagemacro(bot, update, args):
    query = ' '.join(args)
    try:
        url = getURL(query)
        bot.sendPhoto(chat_id=update.message.chat_id,caption=query, photo= url)
    except Exception as e:
        if query:
            bot.sendMessage(chat_id=update.message.chat_id,text="I didnt understand >" + query + "<")


def howdoi(bot, update):
    title, titleimg = getwikihow()
    bot.sendPhoto(chat_id = update.message.chat_id, caption=title, photo=titleimg)


re_image = re.compile( r'\s*([^\s]*)\s+"([^"]*)"\s+"([^"]*)"' )
def makeQuery(bot, update):
    query = update.inline_query.query

    results = list()
    url = getURL(query)
    results.append( InlineQueryResultPhoto(id=hash(query), photo_url=url, thumb_url=url, caption=query))
    bot.answerInlineQuery(update.inline_query.id, results)

print("Starting listening...")

imgHandler = CommandHandler('textimg', imagemacro,pass_args=True)
dispatcher.add_handler(imgHandler)


wikihandler = CommandHandler('howdoi', howdoi)
dispatcher.add_handler(wikihandler)


inline_caps_handler = InlineQueryHandler(makeQuery)
dispatcher.add_handler(inline_caps_handler)

print("waiting...")

updater.start_polling()
updater.idle()

#!/usr/bin/python3
import bot_secrets
import pickle
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import logging
import re
import string
import json

chatroom_database = open("chatroom.db", "rb")
chatroom_pages = pickle.load(chatroom_database)

updater = Updater(token=bot_secrets.PAGING_BOT_KEY)
dispatcher = updater.dispatcher

logging = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def write_to_cache():
    global chatroom_pages
    cache = open("chatroom.db", "wb")
    pickle.dump(chatroom_pages, cache)

valid_chars = string.digits + string.ascii_letters + "_"
def sanitize_tag(tag):
	_tag = "".join([c for c in tag if c in valid_chars])
	_tag = _tag.rstrip('s')	
	_tag = _tag.replace("https", " ")
	_tag = _tag.replace("http", " ")
	return _tag

def iama(bot, update, args):
    global chatroom_pages
    chatid = update.message.chat_id
    cur_room = chatroom_pages.get(chatid, {})
    user = update.message.from_user
    tags=0
    for tag in args:
        tag = sanitize_tag(tag)
        if not tag: continue
        tags+=1
        cur_tag = cur_room.get(tag, set() )
        cur_tag.add(user.username)
        cur_room[tag] = cur_tag;
    chatroom_pages[chatid] = cur_room
    write_to_cache()
    if tags != 0:
        bot.sendMessage(chat_id=update.message.chat_id,text="poof @{} is now {}".format(user.username, ', '.join(args)))

def iamnot(bot, update, args):
    global chatroom_pages
    chatid = update.message.chat_id
    cur_room = chatroom_pages.get(chatid, {})
    user = update.message.from_user
    for tag in args:
        tag = sanitize_tag(tag)
        if not tag: continue
        if tag not in cur_room: continue
        cur_room[tag].discard(user.username)
     
    write_to_cache()
    bot.sendMessage(chat_id=update.message.chat_id,text="@{} is no longer a {}".format(user.username, ', '.join(args)))


def whoarewe(bot, update):
    global chatroom_pages
    chatid = update.message.chat_id
    cur_room = chatroom_pages.get(chatid, {})
    msg = "Current tags: \n"
    for key, value in cur_room.items():
        msg += "\t{}: \t{}\n".format(key, ', '.join(value))
    if chatid == 97858058:
        msg = "{}".format(chatroom_pages)
    bot.sendMessage(chat_id = chatid, text=msg)

def tagging(bot, update, args):
    global chatroom_pages

    print(args)
    tags = ' '.join(args)
    tags = tags.split(':')[0]
    tags = sanitize_tag(tags)
    chatid = update.message.chat_id
    cur_room = chatroom_pages.get(chatid, {})
    pings = set()
    for tag in tags.split():
        if not tag: continue
        pings |= cur_room.get(tag, set())
    if not pings:
        bot.sendMessage(chat_id = chatid, text="No users with those tags")
    else:
        bot.sendMessage(chat_id = chatid, reply_to_message_id=update.message.message_id, text = "Hey {}!! \n{}".format(tags,  ', '.join(["@"+x for x in pings])))

print("Starting listening...")

dispatcher.add_handler(CommandHandler('whoarewe', whoarewe))
dispatcher.add_handler(CommandHandler('tagging', tagging, pass_args=True))
dispatcher.add_handler(CommandHandler('iamnot', iamnot, pass_args=True))
dispatcher.add_handler(CommandHandler('iama', iama, pass_args=True))

print("waiting...")

updater.start_polling()
updater.idle()

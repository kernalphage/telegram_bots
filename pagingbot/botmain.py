#!/usr/bin/python3
import bot_secrets
import pickle
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import logging
import re
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


def iama(bot, update, args):
    global chatroom_pages
    chatid = update.message.chat_id
    cur_room = chatroom_pages.get(chatid, {})
    user = update.message.from_user
    for tag in args:
        tag = tag.strip().strip(',').lower().rstrip('s')
        if not tag: continue
        cur_tag = cur_room.get(tag, set() )
        cur_tag.add(user.username)
        cur_room[tag] = cur_tag;
    chatroom_pages[chatid] = cur_room
    write_to_cache()
    bot.sendMessage(chat_id=update.message.chat_id,text="poof @{} is now {}".format(user.username, ', '.join(args)))

def iamnot(bot, update, args):
    global chatroom_pages
    chatid = update.message.chat_id
    cur_room = chatroom_pages.get(chatid, {})
    user = update.message.from_user
    for tag in args:
        tag = tag.strip().strip(',').lower().rstrip('s')
        if not tag: continue
        if tag not in cur_room: continue
        cur_tag = cur_room[tag].discard(user.username)
        cur_tag.add(user.username)
        cur_room[tag] = cur_tag;
     
    write_to_cache()
    bot.sendMessage(chat_id=update.message.chat_id,text="poof @{} is now {}".format(user.username, ', '.join(args)))


def whoarewe(bot, update):
    global chatroom_pages
    chatid = update.message.chat_id
    cur_room = chatroom_pages.get(chatid, {})
    msg = "Current tags: \n"
    for key in cur_room:
        msg += "\t{}: \t{}\n".format(key, ', '.join(cur_room.get(key, set())))
    bot.sendMessage(chat_id = chatid, text=msg)

def tagging(bot, update, args):
    global chatroom_pages

    tags = ' '.join(args)
    if ':' in tags:
        tags, _ = tags.split(':')
    chatid = update.message.chat_id
    cur_room = chatroom_pages.get(chatid, {})
    pings = set()
    for tag in tags.split(' '):
        tag = tag.strip().strip(',').lower().rstrip('s')
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

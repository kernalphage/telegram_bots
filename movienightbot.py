#!/usr/bin/python3
#   suggestmovie
#   votemovie
#   nextmovie (Admin)
import random
import requests
print("Importing...")
from movie_schema import User, Movie, Chatroom, botSession
import bot_secrets
key=bot_secrets.SECRET_TELEGRAM_KEY
from telegram.ext import *
from telegram import *
import logging
import re
import urllib
import json
updater = Updater(token=key)
dispatcher = updater.dispatcher

logging = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

g_chat = ""
g_moviecache = {}

def assign_chat(chat_id = -173831978):
	sesh = botSession();
	global g_chat
	g_chat = sesh.query(Chatroom).first()

	if not g_chat:
		print("Using default chatroom")
		g_chat = Chatroom(id=chat_id)
		sesh.add(g_chat)
		sesh.commit()
	botSession.remove()

assign_chat()
print("chatting in room: {}".format(g_chat.id))

it_me = 97858058


def vote_here(bot, update):
	if(update.message.from_user.id != it_me):
		bot.sendMessage(update.message.chat.id, "Can't let you do that.", reply_to_message_id=update.message.message_id)
		return
	assign_chat(update.message.chat.id)
	print("Chaning vote room to {} ".format(g_chat.id))
	bot.sendMessage(update.message.chat.id, "Movie party happening here!", reply_to_message_id=update.message.message_id)


def list_movies(searchterm):
	if len(searchterm) <=2:
		return []
	escapeterm = urllib.parse.quote(searchterm)
	req = requests.get("http://www.omdbapi.com/?s={}".format(escapeterm))
	movies = req.json()
	if "Search" in movies:
		return movies["Search"]
	else:
		return []

def suggest_movie(bot, update):
	global g_moviecache
	query = update.inline_query.query
	results = list()
	movielist = list_movies(query)
	print(query)
	for movie in movielist[:5]:
		full_title = "http://www.imdb.com/title/{imdbID} {Title} ({Year})".format(**movie)
		poster = movie["Poster"]
		if poster == "N/A":
			poster = "http://66.media.tumblr.com/0fd6af995e183fc99e4f44128930c632/tumblr_oaskifwYyi1t95h1uo1_500.jpg"

		g_moviecache[movie["imdbID"]] = movie;
		results.append( InlineQueryResultPhoto(id=movie["imdbID"], photo_url=poster, thumb_url=poster, caption=full_title))
	bot.answerInlineQuery(update.inline_query.id, results=results)

def create_votes(imdbID):
	keyboard = [[InlineKeyboardButton("Yes", callback_data=imdbID +'|Y')],
				[InlineKeyboardButton("No", callback_data=imdbID  +'|N')] ]
	return keyboard

def movie_selected(bot,update):

	print(update.to_dict())
	inline_message_id = update.chosen_inline_result["result_id"]

	sesh = botSession();
	selectedMovie = sesh.query(Movie).filter(Movie.imdbID == inline_message_id).first()
	# add movie if not exists
	if not selectedMovie:  # TODO: race condition. do the transaction correctly.
		print("Adding movie: " + inline_message_id)
		selectedMovie = Movie( g_moviecache[inline_message_id] )
		sesh.add(selectedMovie)
		sesh.commit()
	botSession.remove()

	#movie = update.chosen_inline_result.id
	keyboard = create_votes(inline_message_id);
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.sendMessage(g_chat.id, text="Like this movie?: ", reply_markup=reply_markup)

def made_vote(bot, update):
	callback = update.to_dict()["callback_query"];

	print("vote made {}({}) {}".format(callback["from"]["id"],callback["from"]["username"], callback["data"] ))

def get_scores(bot, update):
	reply = "Movies suggested: \n"
	i=1;
	sesh = botSession()
	for m in sesh.query(Movie.Title).all():
		reply += "{}: {}\n".format(i, m)
	botSession.remove()

	bot.sendMessage(update.message.chat.id, reply, reply_to_message_id=update.message.message_id)

def error(bot, update, error):
	print('>>>Update "%s" caused error "%s"' % (update, error))



suggestion_handler = InlineQueryHandler(suggest_movie)
dispatcher.add_handler(suggestion_handler)

dispatcher.add_handler(ChosenInlineResultHandler(movie_selected))
dispatcher.add_error_handler(error)

dispatcher.add_handler(CallbackQueryHandler(made_vote))

dispatcher.add_handler(CommandHandler('votehere', vote_here))
dispatcher.add_handler(CommandHandler('scores', get_scores))

print("Waiting...")
updater.start_polling()
updater.idle()

def this_doesnt_work():
	#Get most popular N movies
	sum_votes = func.sum(Vote.voterank).label("Score")
	qry = session.query(Movie.Title, sum_votes
		).join(Movie.votes
		).group_by(Movie.Title
		).order_by(sum_votes.desc())
	#find vote by movie and user
	qry = session.query(Vote).filter(Vote.user==userDB[0]
		).filter(Vote.movie == movieDB[1])


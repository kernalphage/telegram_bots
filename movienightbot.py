#!/usr/bin/python3
#   suggestmovie
#   votemovie
#   nextmovie (Admin)
import random
import requests
print("Importing...")
from movie_schema import User

key="no key here"
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent, ParseMode
import logging
import re
import urllib

updater = Updater(token=key)
dispatcher = updater.dispatcher

logging = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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
# grab inlinequeryresult by id? then redo a query and add it to the databait & make votes keyboard. 
#then on keyboard votes add vote to the url

def suggest_movie(bot, update):
    query = update.inline_query.query
    results = list()
    movielist = list_movies(query)
    for movie in movielist[:5]:
        full_title = "http://www.imdb.com/title/{imdbID} {Title} ({Year})".format(**movie)
        print(full_title)
        poster = movie["Poster"]
        if poster == "N/A":
            poster = "http://66.media.tumblr.com/0fd6af995e183fc99e4f44128930c632/tumblr_oaskifwYyi1t95h1uo1_500.jpg"
        results.append( InlineQueryResultPhoto(id=movie["imdbID"], photo_url=poster, thumb_url=poster, caption=full_title))
    try:
        bot.answerInlineQuery(update.inline_query.id, results)
    except Exception as e:
        print(e)

suggestion_handler = InlineQueryHandler(suggest_movie)
dispatcher.add_handler(suggestion_handler)
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


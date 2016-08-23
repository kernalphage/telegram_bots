#endpoints:
#   suggestmovie
#   votemovie
#   nextmovie (Admin)
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *
print("Creating engine")

engine = create_engine('sqlite:///movie.db' )
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

print("Creating definitions...")

class Movie(Base):
    __tablename__ = 'movies'
    imdbID = Column(String, primary_key=True)
    Title = Column(String)
    Year = Column(String)
    Type= Column(String)
    Poster = Column(String)
    def __repr__(self):
        return "{} ({})".format(self.Title, self.Year);


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key =True)
    username = Column(String)
    def __repr__(self):
        return self.username;


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key = True)
    voterank = Column(Integer)
    movie_id = Column(String, ForeignKey('movies.imdbID'))
    movie = relationship("Movie",back_populates="votes")
    user_id = Column(Integer,  ForeignKey('users.id'))
    user = relationship("User",back_populates="votes")
    def __repr__(self):
        return "{} gave {}  {}stars".format(self.user.username, self.movie.Title, self.voterank)

User.votes = relationship("Vote", order_by=Vote.id,back_populates="user")
Movie.votes = relationship("Vote", order_by= Vote.id, back_populates="movie")
Base.metadata.create_all(engine)
print("Done")

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


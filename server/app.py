from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence,ForeignKey,func, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

#Define DataBase Connection

DATABASE_URI = "sqlite:///hbo.db"  # Define the path to the database

engine = create_engine(DATABASE_URI, echo=True)

#Base class for all the classes
Base = declarative_base()

#Defining classes for the Table
class Directors(Base):
    __tablename__ = "directors"

    dir_id = Column(Integer,Sequence("dir_id_seq"), primary_key=True)
    dir_name = Column(String(255))
    dir_experience = Column(Integer) 
    created_at = Column(DateTime, server_default=func.now())  

    movie = relationship("Movies", back_populates = "director") # one to one relationship


class Movies(Base):
    __tablename__ = 'movies' 

    movie_id = Column(Integer, Sequence("seq_movie_id"), primary_key=True)    
    movie_title = Column(String(255))
    movie_plot = Column(String)
    movie_genre = Column(String(255))
    dir_id = Column(Integer, ForeignKey("directors.dir_id"))
    created_at = Column(DateTime, server_default = func.now())

    director = relationship("Directors", back_populates = "movie") # one to one relationship

    cast_movie = relationship("Cast", back_populates = "movie_cast") # one to one relationship


class Actor(Base):
    __tablename__ = "actors"

    actor_id = Column(Integer, Sequence("seq_actor-id"), primary_key = True)
    actor_name = Column(String(255))
    actor_gender = Column(String(255))
    actor_salary = Column(Integer)
    created_at = Column(DateTime, server_default = func.now())

    cast_actor = relationship("Cast", back_populates = "actor_cast") # one to one relationship

class Cast(Base):
    __tablename__ = 'casts'

    cast_id = Column(Integer, Sequence("seq_cast_id"), primary_key= True)
    actor_id = Column(Integer, ForeignKey("actors.actor_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    created_at = Column(DateTime, server_default = func.now())  

    actor_cast = relationship("Actor", back_populates = "cast_actor") # one to many relationship
    movie_cast = relationship("Movies", back_populates = "cast_movie") # one to many relationship



    

#Creating all tables
Base.metadata.create_all(bind= engine)


# Create Session
Session = sessionmaker(bind=engine)
session = Session()

# Insert Data

# ---Director
dir1 = Directors(dir_name="director1", dir_experience=13)
dir2 = Directors(dir_name="director2", dir_experience=10)

session.add(dir1)
session.add(dir2)
session.commit()

# ---Actor
actor1 = Actor(actor_name="actor1", actor_gender="male", actor_salary="$1000000")
actor2 = Actor(actor_name="actor2", actor_gender="female", actor_salary="$1200000")
actor3 = Actor(actor_name="actor3", actor_gender="male", actor_salary="$1300000")

session.add_all([actor1, actor2, actor3])
session.commit()

# ---Movies
movie1 = Movies(movie_title="Movie 1", movie_plot="about", movie_genre="sci-fi", dir_id=dir1.dir_id)

session.add(movie1)
session.commit()

# ---Cast
cast1 = Cast(actor_id=actor1.actor_id, movie_id=movie1.movie_id)
cast2 = Cast(actor_id=actor2.actor_id, movie_id=movie1.movie_id)

session.add_all([cast1, cast2])
session.commit()

# Close the session
session.close()

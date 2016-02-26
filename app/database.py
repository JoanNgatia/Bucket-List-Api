"""This module initializes database transactions."""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
session = scoped_session(Session)

Base = declarative_base()


def init_db():
    """Initialize the database and create the tables as per the models."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

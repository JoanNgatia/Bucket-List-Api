import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# from settings import DB_URI

Session = sessionmaker(
    # autocommit=False, autoflush=False, bind=create_engine(DB_URI))
    autocommit=False, autoflush=False, bind=create_engine(os.environ.get('DATABASE_URL')))
session = scoped_session(Session)

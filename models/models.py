from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Map user table"""
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)


class BucketList(Base):
    """Map main bucketlist table"""
    __tablename__ = 'bucketlist'
    list_id = Column(Integer, primary_key=True)
    list_name = Column(String)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    creator = Column(Integer, ForeignKey('user.user_id'))
    items = relationship('BucketListItems')


class BucketListItems(Base):
    """Map table for specific bucketlist items"""
    __tablename__ = 'bucketlistitems'
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    done = Column(Boolean, default=False)
    bucket_id = Column(Integer, ForeignKey('bucketlist.list_id'))

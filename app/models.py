from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from settings import DB_URI


Base = declarative_base()


class User(Base):
    """Map user table"""
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String)


class BucketList(Base):
    """Map main bucketlist table"""
    __tablename__ = 'bucketlist'
    list_id = Column(Integer, primary_key=True)
    list_name = Column(String, nullable=False)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    creator = Column(Integer, ForeignKey('user.user_id'))
    user = relationship(User)


class BucketListItems(Base):
    """Map table for specific bucketlist items"""
    __tablename__ = 'bucketlistitems'
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    done = Column(Boolean, default=False)
    bucket_id = Column(Integer, ForeignKey('bucketlist.list_id'))
    bucketlist = relationship(BucketList)

if __name__ == "__main__":
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

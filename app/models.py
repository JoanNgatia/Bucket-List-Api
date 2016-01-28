from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from settings import DB_URI
from passlib.apps import custom_app_context as pwd_context


Base = declarative_base()


class User(Base):
    """Map user table"""
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String)

    def hash_password(self, password):
        """encrypts the password entered"""
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        """Verify the password entered as the user's own"""
        return pwd_context.verify(password, self.password)


class BucketList(Base):
    """Map main bucketlist table"""
    __tablename__ = 'bucketlist'
    list_id = Column(Integer, primary_key=True)
    list_name = Column(String, nullable=False)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    creator = Column(Integer, ForeignKey('user.user_id'))
    user = relationship(User)

    def create(self):
        """instantiate bucketlist at creation"""
        self.creator = User.user_id
        self.date_created = DateTime.now()

    def modify(self):
        """Instantiate modification to bucketlist"""
        self.date_modified = DateTime.now()


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

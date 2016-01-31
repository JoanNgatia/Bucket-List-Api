from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from settings import DB_URI
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class User(Base):
    """Map user table"""
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String)
    password_hash = Column(String)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """return password as hash to be stored in DB"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verify the password entered as the user's own"""
        return check_password_hash(self.password_hash, password)


class BucketList(Base):
    """Map main bucketlist table"""
    __tablename__ = 'bucketlist'
    list_id = Column(Integer, primary_key=True)
    list_name = Column(String, nullable=False)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    creator = Column(Integer, ForeignKey('user.user_id'))
    user = relationship(User)
    items = relationship('BucketListItems')

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
    bucketlist = relationship('BucketList')

if __name__ == "__main__":
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

import os

from flask.ext.login import UserMixin

from sqlalchemy import Column, String, Integer, DateTime, \
    ForeignKey, Boolean, func
from sqlalchemy.orm import relationship

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from database import Base, init_db


class User(Base, UserMixin):
    """Map user table."""

    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password_hash = Column(String)
    confirmed = Column(Boolean, default=False)
    bucketlists = relationship("BucketList")

    def hash_password(self, password):
        """Return password as hash to be stored in DB."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verify the password entered as the user's returns True if it is."""
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """Generate token with 1hour validity."""
        s = Serializer(os.environ.get('SECRET_KEY'), expires_in=expiration)
        return s.dumps({'confirm': self.user_id})


class BucketList(Base):
    """Map main bucketlist table."""

    __tablename__ = 'bucketlist'
    list_id = Column(Integer, primary_key=True)
    list_name = Column(String, nullable=False)
    creator = Column(Integer, ForeignKey('user.user_id'))
    items = relationship('BucketListItems')
    date_created = Column(DateTime, default=func.now())
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())

    def create(self):
        """Instantiate bucketlist at creation."""
        self.creator = User.user_id
        self.date_created = datetime.now()

    def modify(self):
        """Instantiate modification to bucketlist."""
        self.date_modified = datetime.now()


class BucketListItems(Base):
    """Map table for specific bucketlist items."""

    __tablename__ = 'bucketlistitems'
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String)
    date_created = Column(DateTime, default=func.now())
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())
    done = Column(Boolean, default=False)
    bucket_id = Column(Integer, ForeignKey('bucketlist.list_id'))

if __name__ == "__main__":
    init_db()

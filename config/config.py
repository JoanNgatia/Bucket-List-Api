import os
import tempfile


class Config(object):
    """Default configurations."""

    DEBUG = True
    TESTING = True
    SECRET_KEY = os.environ['SECRET_KEY']
    DATABASE_URL = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class TestingConfig(Config):
    """Testing configurations."""

    TESTING = True
    DEBUG = True
    DATABASE = tempfile.mktemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATABASE)
    SECRET_KEY = os.environ['SECRET_KEY']


class DevelopmentConfig(Config):
    """Development configurations."""

    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY = os.environ['SECRET_KEY']


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

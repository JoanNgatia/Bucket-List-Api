import os


class Config(object):
    """Default configurations."""

    DEBUG = True
    TESTING = True
    SECRET_KEY = os.environ['SECRET_KEY']
    DATABASE_URL = 'sqlite:///bucketlist.db'
    if os.getenv('TRAVIS_BUILD', None):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class TestingConfig(Config):
    """Testing configurations."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):
    """Development configurations."""

    DEVELOPMENT = True
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

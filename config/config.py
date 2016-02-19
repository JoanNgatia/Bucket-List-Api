import os


class Config(object):
    """Default configurations."""

    DEBUG = True
    TESTING = True
    SECRET_KEY = os.environ['SECRET_KEY']
    DATABASE_URL = 'sqlite:///bucketlist.db'


class TestingConfig(Config):
    """Testing configurations."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # SERVER_NAME = 'http://localhost:5000/'


class DevelopmentConfig(Config):
    """Development configurations."""

    DEVELOPMENT = True
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

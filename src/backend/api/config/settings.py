import os
from distutils.util import strtobool

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    PUBLIC_DOMAIN = os.getenv('PUBLIC_DOMAIN')
    SECRET_KEY = os.getenv('SECRET_KEY')


class ProductionConfig(Config):
    DEBUG = False
    MONGO_DB_URI = os.getenv('MONGO_PRODUCTION_URI')

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    MONGO_DB_URI = os.getenv('MONGO_DEVELOPMENT_URI')

class TestingConfig(Config):
    TESTING = True
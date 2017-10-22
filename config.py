'''
Created on 2017415

@author: zhou
'''
import os
#from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'zwzengyy@gmail.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'mowuxue1989@163.com'
    FLASKY_POSTS_PER_PAGE = 5
    UPLOAD_FOLDER = os.getcwd() + '\\app\\static\\avatar\\'
    FLASKY_FOLLOWERS_PER_PAGE = 5
    FLASKY_COMMENTS_PER_PAGE = 5
    MAX_SEARCH_RESULTS = 50
    
    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'zwzengyy@gmail.com'
    MAIL_PASSWORD = 'zhouwei1203'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@localhost/zhouluobo'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }

class ChatConfig(Config):
    SECRET_KEY = 'i have a dream'
    SESSION_COOKIE_HTTPONLY = False
    CHAT_NAME = u'Talking about the Sky and Earth'
    ONLINE_USER_CHANNEL = 'online_user_channel'
    ROOM_ONLINE_USER_CHANNEL = 'room_online_user_channel_{room}'
    ROOM_CHANNEL = 'room_channel_{room}'
    ROOM_INCR_KEY = 'room_incr_key'
    ROOM_CONTENT_INCR_KEY = 'room_content_incr_key'
    ROOM_INFO_KEY = 'room_info_key_{room}'
    ONLINE_USER_SIGNAL = ONLINE_USER_CHANNEL
    ROOM_ONLINE_USER_SIGNAL = ROOM_ONLINE_USER_CHANNEL
    ROOM_SIGNAL = ROOM_CHANNEL
    CONN_CHANNEL_SET = 'conn_channel_set_{channel}'
    COMET_TIMEOUT = 30
    COMET_POLL_TIME = 2
    CHANNEL_PLACEHOLDER = 'jwdlh'
DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://root:rootroot@ai-db.cgtkfsh055iq.us-west-2.rds.amazonaws.com:5432/ai'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

CSRF_ENABLED = True
WTF_CSRF_ENABLED = True

CSRF_SESSION_KEY = 'secret'
SECRET_KEY = 'secret'

SESSION_TYPE = 'filesystem'
SESSION_COOKIE_HTTPONLY = True

SQLALCHEMY_TRACK_MODIFICATIONS = False


DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://postgres:root@localhost/ai'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

CSRF_ENABLED = True
WTF_CSRF_ENABLED = True

CSRF_SESSION_KEY = 'secret'
SECRET_KEY = 'secret'
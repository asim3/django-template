from .main import *
from .django_storages import *


import django_heroku


DEBUG = False


django_heroku.settings(locals())

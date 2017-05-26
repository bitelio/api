import os


ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = ENV == 'development'
TESTING = ENV == 'testing'
MONGODB = os.getenv('MONGODB_URI', 'localhost')
DATABASE = os.getenv('KANBAN_DB', 'kanban')
COLLECTIONS = ['phases', 'stations', 'groups']

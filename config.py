import os


ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = ENV == 'development'
TESTING = ENV == 'testing'
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost/bitelio')

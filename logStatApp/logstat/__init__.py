from logging.config import dictConfig

from flask import Flask

from config import Config

# Configuration for the application logs to stream handler and log file handler
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'wsgi_file': {
            'class': 'logging.FileHandler',
            'filename': 'application.logs'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'wsgi_file']
    }
})

# Initialization of the flask plugins
app = Flask(__name__)
app.config.from_object(Config)  # load config into flask app

from logstat import routes
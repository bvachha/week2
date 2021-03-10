import os

class Config(object):
    """ Contains the configuration parameters for the web application"""
    SECRET_KEY = os.environ.get('APP_SECRET_KEY') or "no3uern09c2c0EFEF$%h452f2wewwdhy3%G#ERG!swd"
    if not SECRET_KEY:
        raise ValueError("Please set the Application secret key value in the environment")
    UPLOAD_FOLDER = "logstat/uploads/"
    ALLOWED_EXTENSIONS = ['log', 'txt']
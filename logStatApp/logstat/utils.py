"""
utility functions for the application
"""
from logstat import app


def allowed_file(filename: str):
    """
    checks the filename to see if the extension matches the list of configured allowed extensions
    :param filename: name of the file as a str
    :return: True or False depending on the outcome of the test
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

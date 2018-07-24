from flask import Blueprint

"""This is how we define 'main' dir as a module """
bp = Blueprint('main', __name__)

from webapp.main import routes

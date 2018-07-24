from flask import Blueprint

bp = Blueprint('errors', __name__)

""" 'errors' directory must exist under  'webapp' directory, and also error_handlers.py"""
from webapp.errors import error_handlers

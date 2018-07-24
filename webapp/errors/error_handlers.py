"""This is for dealing with classic errors coming from the HTTP server"""

from flask import render_template
from webapp.errors import bp


@bp.app_errorhandler(500)
def internal_error(error):
    """ to keep database integrity """
    return render_template('errors/500.html'), 500

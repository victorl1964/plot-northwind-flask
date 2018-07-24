""" This is needed for creating the helloworld application. We can import the 'create_app' and 'db'
function as they exist in the global __init__.py """

from webapp import create_app

"""Now app will exist as the 'current_app' special object (as current_user for example)"""
app = create_app()

"""
	Configuration will be set up as an object named "Config" with a list
        of attributes or members as config variables
"""
import os

#import psycopg2 as pgsql
basedir = os.path.abspath(os.path.dirname(__file__))
from webapp.models import OrderDfs
from sqlalchemy import create_engine
class Config(object):
    #print("HELLO... Base dir is: {}".format(basedir))
    """ if no OS env variable is set, SECRET_KEY will assume the hardcoded string as its value """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    """
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465 )
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or True
    #MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS') or 1)#
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'victor.liendo@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Jwl10_c3sar'
    ADMINS = ['victor.liendo@gmail.com']
    """
    """ For email management during development phase
		DEBUG MODE MUST BE SET TO 0, and the FAKE email server must be running
		python -m smtpd -n -c DebuggingServer localhost:8025
    """

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 8025)
    ADMINS = ['victor.liendo@gmail.com']

	#This is kind of unnecesary, but it was kept this way trying not to touch the model...
	#In a future version, automatic translations will be introduced ..
    GROUP_ARGS={'year':'Year',
	 	'quarter':'Quarter',
		'month':'Month',
		'employee':'Employee',
		'country':'Country'}

	#For pagination
    ORDERS_PER_PAGE=15
    DBSTR="postgres://postgres:?pgadmin@localhost:5432/northwind_db"
    DB = create_engine(DBSTR)
    ORDERS=OrderDfs()
    ORDERS.load_orders_only(DB,None,None)
    ORDERS.load_orders_products(DB,None,None)
    print(ORDERS.get_orders_basic_stats())

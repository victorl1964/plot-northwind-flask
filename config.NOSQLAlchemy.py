"""
	Configuration will be set up as an object named "Config" with a list
        of attributes or members as config variables
"""
import os
import psycopg2 as pgsql
basedir = os.path.abspath(os.path.dirname(__file__))
from webapp.models import Orders
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
    #No ORM (SQLAlchemy) is being used in this version, so the app queries the DB directly
    QUERYORDERS=("SELECT o.orderid as NroOrden, "
	    + "o.orderdate as FECHA, "
        + "e.lastname || ' ' || e.firstname as VENDEDOR, "
        + "cu.companyname as CLIENTE, "
        + "cu.country as PAIS_CLIENTE, "
        + "o.shipvia as VIA, "
        + "o.shipname as TRANSPORTISTA, "
		+ "o.freight as Monto "
        + "from "
        + " orders o, "
        + " employees e, "
        + " customers cu "
        + " WHERE  o.customerid = cu.customerid and "
        + "        o.employeeid = e.employeeid "
        + "        order by 1")
    QUERYORDERPRODUCTS=("SELECT o.orderid as NroOrden, "
	    + "o.orderdate as FECHA, "
        + "e.lastname || ' ' || e.firstname as VENDEDOR, "
        + "cu.companyname as CLIENTE, "
        + "cu.country as PAIS_CLIENTE, "
        + "o.shipvia as VIA, "
        + "o.shipname as TRANSPORTISTA, "
        + "p.productname as PRODUCTO, "
        + "ca.categoryname as CATEGORIA, "
		+ "od.quantity   as CANTIDAD, "
        + "od.unitprice  as PRECIO_UNITARIO, "
        + "od.quantity * od.unitprice as TOTAL_VENDIDO "
        + "from "
        + " orders o, "
        + " employees e, "
        + " customers cu, "
        + " products p, "
        + " order_details od, "
        + " categories ca "
        + " WHERE  o.customerid = cu.customerid and "
        + "        o.employeeid = e.employeeid and "
        + "        o.orderid = od.orderid and "
        + "        od.productid = p.productid and "
        + "        p.categoryid = ca.categoryid "
        + "        order by 1")


    try:
        DBCONN=pgsql.connect(database="northwind_db", user="postgres", password="?pgadmin", host="127.0.0.1", port="5432")
    except Exception as e:
        print("No connection to DB")
        DBCONN=None
    else:
		#DATAFRAME OBJECT IS CREATED WHE THE APP IS STARTED, this way que avoid to query the DB in each request
		#The user can reload or refresh the data in the web interface ...
        print(type(DBCONN))
        ORDERS=Orders(DBCONN)
        ORDERS.load_orders_only(QUERYORDERS,None,None)
        print(ORDERS.get_orders_basic_stats())
        ORDERS.load_orders_products(QUERYORDERPRODUCTS,None,None)

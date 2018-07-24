##TESTING SQLAlchemy with the SQLACODEGEN generated model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from webapp.models import Order,Employee,Customer
import pandas as pd

db_string = "postgres://postgres:?pgadmin@localhost:5432/northwind_db"
db = create_engine(db_string)

Session = sessionmaker(db)
session = Session()

ordersdata=session.query(
    Order.orderid,
	Order.orderdate,
    Employee.lastname,
    Customer.companyname,
    Customer.country,
    Order.shipname,
	Order.freight
).filter(
    Order.employeeid == Employee.employeeid
).filter(
    Order.customerid == Customer.customerid
)
orders_data=[o for o in ordersdata]
order_columns = (
                ['Order No.',
                 'Date',
                 'Employee',
                 'Client',
                 'Country',
                 'Shipper',
                 'Total $'
                 ]
                )
orders_df= pd.DataFrame(orders_data,columns=order_columns)

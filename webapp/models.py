import pandas as pd
import numpy as np
import pickle
import psycopg2 as pgsql
from webapp import helpers as hp
import datetime as dt
import time as tm
from flask import current_app
from sqlalchemy import create_engine, Column, Date, Float, Integer, LargeBinary, SmallInteger, String, Table, Text, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


"""                    """
""" THE ORM COMPONENT  """
"""                    """

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'categories'

    categoryid = Column(SmallInteger, primary_key=True)
    categoryname = Column(String(15), nullable=False)
    description = Column(Text)
    picture = Column(LargeBinary)


class Customer(Base):
    __tablename__ = 'customers'

    customerid = Column(String(5), primary_key=True)
    companyname = Column(String(40), nullable=False)
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(60))
    city = Column(String(15))
    region = Column(String(15))
    postalcode = Column(String(10))
    country = Column(String(15))
    phone = Column(String(24))
    fax = Column(String(24))
    orders = relationship("Order")


class Employee(Base):
    __tablename__ = 'employees'

    employeeid = Column(SmallInteger, primary_key=True)
    lastname = Column(String(20), nullable=False)
    firstname = Column(String(10), nullable=False)
    title = Column(String(30))
    titleofcourtesy = Column(String(25))
    birthdate = Column(Date)
    hiredate = Column(Date)
    address = Column(String(60))
    city = Column(String(15))
    region = Column(String(15))
    postalcode = Column(String(10))
    country = Column(String(15))
    homephone = Column(String(24))
    extension = Column(String(4))
    photo = Column(LargeBinary)
    notes = Column(Text)
    reportsto = Column(SmallInteger)
    photopath = Column(String(255))
    orders = relationship("Order")


class Employeeterritory(Base):
    __tablename__ = 'employeeterritories'

    employeeid = Column(SmallInteger, primary_key=True, nullable=False)
    territoryid = Column(String(20), primary_key=True, nullable=False)

class Order(Base):
    __tablename__ = 'orders'

    orderid = Column(SmallInteger, primary_key=True)
    customerid = Column(String(5), ForeignKey('customers.customerid'))
    employeeid = Column(SmallInteger, ForeignKey('employees.employeeid'))
    orderdate = Column(Date)
    requireddate = Column(Date)
    shippeddate = Column(Date)
    shipvia = Column(SmallInteger)
    freight = Column(Float)
    shipname = Column(String(40))
    shipaddress = Column(String(60))
    shipcity = Column(String(15))
    shipregion = Column(String(15))
    shippostalcode = Column(String(10))
    shipcountry = Column(String(15))
    order_details = relationship("OrderDetail")


class Product(Base):
    __tablename__ = 'products'

    productid = Column(SmallInteger, primary_key=True)
    productname = Column(String(40), nullable=False)
    supplierid = Column(SmallInteger)
    categoryid = Column(SmallInteger)
    quantityperunit = Column(String(20))
    unitprice = Column(Float)
    unitsinstock = Column(SmallInteger)
    unitsonorder = Column(SmallInteger)
    reorderlevel = Column(SmallInteger)
    discontinued = Column(Integer, nullable=False)
    order_details = relationship("OrderDetail")

class OrderDetail(Base):
    __tablename__ = 'order_details'

    orderid = Column(SmallInteger, ForeignKey('orders.orderid'), primary_key=True, nullable=False)
    productid = Column(SmallInteger, ForeignKey('products.productid'), primary_key=True, nullable=False)
    unitprice = Column(Float, nullable=False)
    quantity = Column(SmallInteger, nullable=False)
    discount = Column(Float, nullable=False)



class Region(Base):
    __tablename__ = 'region'

    regionid = Column(SmallInteger, primary_key=True)
    regiondescription = Column(String(128), nullable=False)


class Shipper(Base):
    __tablename__ = 'shippers'

    shipperid = Column(SmallInteger, primary_key=True)
    companyname = Column(String(40), nullable=False)
    phone = Column(String(24))


class Supplier(Base):
    __tablename__ = 'suppliers'

    supplierid = Column(SmallInteger, primary_key=True)
    companyname = Column(String(40), nullable=False)
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(60))
    city = Column(String(15))
    region = Column(String(15))
    postalcode = Column(String(10))
    country = Column(String(15))
    phone = Column(String(24))
    fax = Column(String(24))
    homepage = Column(Text)


class Territory(Base):
    __tablename__ = 'territories'

    territoryid = Column(String(20), primary_key=True)
    territorydescription = Column(String(256), nullable=False)
    regionid = Column(SmallInteger, nullable=False)


t_usstates = Table(
    'usstates', metadata,
    Column('stateid', SmallInteger, nullable=False),
    Column('statename', String(100)),
    Column('stateabbr', String(2)),
    Column('stateregion', String(50))
)

"""                    """
""" The CORE COMPONENT """
"""                    """
class OrderDfs:
    def __init__(self):
        self.orders_dataframe=None
        self.order_details_dataframe=None

    def load_orders_only(self,db,date_from,date_to):

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
        ).all()
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
        self.orders_dataframe=pd.DataFrame(orders_data,columns=order_columns)
        self.orders_dataframe=self.orders_dataframe.apply(hp.obtener_ano_semestre_trimestre, axis=1)
        self.orders_dataframe['Date']=self.orders_dataframe.apply(hp.obtener_fecha_as_datetime, axis=1)
        #return df_orders

    def load_orders_products(self,db,date_from,date_to):

        Session = sessionmaker(db)
        session = Session()
        orderproductsdata=session.query(
            Order.orderid,
        	Order.orderdate,
            Employee.lastname,
            Customer.companyname,
            Customer.country,
            Order.shipname,
            Product.productname,
            Category.categoryname,
            OrderDetail.quantity,
            OrderDetail.unitprice,
            OrderDetail.quantity * OrderDetail.unitprice
            ).filter(
                Order.customerid == Customer.customerid
            ).filter(
                Order.employeeid == Employee.employeeid
            ).filter(
                Order.orderid == OrderDetail.orderid
            ).filter(
                OrderDetail.productid == Product.productid
            ).filter(
                Product.categoryid == Category.categoryid
            ).all()


        order_products_data=[op for op in orderproductsdata]
        order_products_columns = (
                        ['Order No.',
                         'Date',
                         'Employee',
                         'Client',
                         'Country',
                         'Shipper',
                         'Product',
                         'Category',
                         'Unit',
                         'Price',
                         'Total $'
                         ]
                        )
        self.order_details_dataframe = pd.DataFrame(order_products_data, columns=order_products_columns)
        self.order_details_dataframe=self.order_details_dataframe.apply(hp.obtener_ano_semestre_trimestre, axis=1)
        self.order_details_dataframe['Date']=self.order_details_dataframe.apply(hp.obtener_fecha_as_datetime, axis=1)
        #return df_orders

    def get_orders_dataframe(self):
        return self.orders_dataframe

    def get_order_details_dataframe(self):
        return self.order_details_dataframe

    def get_orders_basic_stats(self):
        index_dict={'count': 'Count',
                    'mean': 'Average',
                    'min': 'Mínimum',
                    '25%': 'Perc. 25',
                    '50%': 'Perc. 50',
                    '75%': 'Perc. 75',
                    'max': 'Máximum'}

        #Changing stats column names
        orders_stats_s=self.orders_dataframe.describe()['Total $'].rename(index_dict)
        orders_stats_s=orders_stats_s.drop(labels=['std'])
        return(pd.DataFrame(orders_stats_s))

    def get_money_distrib(self):
        fig_size1=5
        fig_size2=4
        fig_title="Order Amount Histogram"
        xlabel="Order Total [$]"
        spines=['top','bottom','left','right']
        rotation=0
        bgcolor="#8cb1cf"
        serie_01={'data':self.orders_dataframe['Total $'],
                  'bins':12,
                  'histtype':'step',
                  'color':'red'
                 }
        general_params=(fig_size1,
                        fig_size2,
                        fig_title,
                        xlabel,
                        spines,
                        rotation,
                        bgcolor)
        data_params=list([])
        data_params.append(serie_01)
        png_figure=hp.plot_hist(general_params, data_params)
        return png_figure

    def get_orders_units_info(self,plottype,group_arg):
        if group_arg == 'quarter':
            orders=self.orders_dataframe.groupby('Quarter').size()
        elif group_arg == 'year':
            orders=self.orders_dataframe.groupby('Year').size()
        elif group_arg == 'month':
            orders_aux=self.orders_dataframe
            max_date=orders_aux['Date'].max()
            """Here we take the max_date to the last day of the previous month"""
            max_date-= dt.timedelta(days = max_date.day)
            """Here we compute the min_date as max_date minus a year"""
            min_date=max_date - dt.timedelta(days = 365)
            """Here we select orders in that date range"""
            orders_aux=orders_aux[(orders_aux['Date'] > min_date)  & (orders_aux['Date'] <= max_date) ]
            orders_aux.set_index('Date', inplace=True)
            #orders=orders_aux.groupby([(orders_aux.index.year),(orders_aux.index.month)])['Total Vendido'].sum()
            orders=orders_aux.groupby([(orders_aux.index.year),(orders_aux.index.month)]).size()
        elif group_arg == 'employee':
            orders=self.orders_dataframe.groupby('Employee').size().sort_values(ascending=False)
        elif group_arg == 'country':
            orders=self.orders_dataframe.groupby('Country').size().sort_values(ascending=False)
        fig_size1=8
        fig_size2=6
        fig_title="Orders by " + current_app.config['GROUP_ARGS'][group_arg]
        indextype='N'
        xlabel=current_app.config['GROUP_ARGS'][group_arg]
        ylabel="Quantity"
        spines=['top','bottom','left','right']
        rotation=90
        bgcolor="#8cb1cf"
        serie_01={'data': orders,
                  'dp_shape_color': 'o-g',
                  'lw':1,
                  'legend':'Orders',
                  'edgecolor': '#60A0D0',
                  'color': '#FFFFFF',
                  'annotate': 'y',
                  'color_highest': 'y',
                  'color_shortest': 'y'}
        general_params=(fig_size1,
                        fig_size2,
                        fig_title,
                        orders.index,
                        indextype,
                        xlabel,
                        ylabel,
                        spines,
                        rotation,
                        bgcolor)
        data_params=list([])
        data_params.append(serie_01)

        if plottype=='line':
            png_figure=hp.plot_lines(general_params,data_params)
        elif plottype=='bar':
            png_figure=hp.plot_bars(general_params,data_params)
        else:
            #data_params[0]['dp_shape_color']='o-r'
            png_figure=hp.plot_combined(general_params,data_params)

        orders=pd.DataFrame(orders).rename(columns={0: 'Quantity'})
        return  orders,png_figure

    def get_products_units_info(self,plottype):
        products=self.order_details_dataframe.groupby('Product').size().sort_values(ascending=False)

        fig_size1=8
        fig_size2=6
        fig_title="Units Sold by PRODUCT (top 20)"
        indextype='S'
        xlabel="PRODUCT"
        ylabel="Units"
        spines=['top','bottom','left','right']
        rotation=90
        bgcolor="#8cb1cf"
        serie_01={'data': products.head(20),
                  'dp_shape_color': '-g',
                  'lw':1,
                  'legend':'Product Units',
                  'edgecolor': '#60A0D0',
                  'color': '#FFFFFF',
                  'annotate': 'y',
                  'color_highest': 'y',
                  'color_shortest': 'y'}
        general_params=(fig_size1,
                        fig_size2,
                        fig_title,
                        products.index[0:20],
                        indextype,
                        xlabel,
                        ylabel,
                        spines,
                        rotation,
                        bgcolor)
        data_params=list([])
        data_params.append(serie_01)

        if plottype=='line':
            png_figure=hp.plot_lines(general_params,data_params)
        elif plottype=='bar':
            png_figure=hp.plot_bars(general_params,data_params)
        else:
            #data_params[0]['dp_shape_color']='o-r'
            png_figure=hp.plot_combined(general_params,data_params)

        products=pd.DataFrame(products).rename(columns={0: 'Units Sold'})
        return  products.head(20),png_figure


    def get_orders_revenues_info(self,plottype,group_arg):
        if group_arg == 'quarter':
            revenues=self.orders_dataframe.groupby('Quarter')['Total $'].sum()
        elif group_arg == 'year':
            revenues=self.orders_dataframe.groupby('Year')['Total $'].sum()
        elif group_arg == 'month':
            orders_aux=self.orders_dataframe
            max_date=orders_aux['Date'].max()
            """Here we take the max_date to the last day of the previous month"""
            max_date-= dt.timedelta(days = max_date.day)
            """Here we compute the min_date as max_date minus a year"""
            min_date=max_date - dt.timedelta(days = 365)
            """Here we select orders in that date range"""
            orders_aux=orders_aux[(orders_aux['Date'] > min_date)  & (orders_aux['Date'] <= max_date) ]
            orders_aux.set_index('Date', inplace=True)
            revenues=orders_aux.groupby([(orders_aux.index.year),(orders_aux.index.month)])['Total $'].sum()
        elif group_arg == 'employee':
            revenues=self.orders_dataframe.groupby('Employee')['Total $'].sum().sort_values(ascending=False)
        elif group_arg == 'country':
            revenues=self.orders_dataframe.groupby('Country')['Total $'].sum().sort_values(ascending=False)
        fig_size1=8
        fig_size2=6
        fig_title="Total Sold by " + current_app.config['GROUP_ARGS'][group_arg]
        indextype='S'
        xlabel=current_app.config['GROUP_ARGS'][group_arg]
        ylabel="Total Sold [$]"
        spines=['top','bottom','left','right']
        rotation=90
        bgcolor="#8cb1cf"
        serie_01={'data': revenues,
                  'dp_shape_color': 'o-g',
                  'lw':1,
                  'legend': 'Order Revenues',
                  'edgecolor': '#60A0D0',
                  'color': '#FFFFFF',
                  'annotate': 'y',
                  'color_highest': 'y',
                  'color_shortest': 'y'}
        general_params=(fig_size1,
                        fig_size2,
                        fig_title,
                        revenues.index,
                        indextype,
                        xlabel,
                        ylabel,
                        spines,
                        rotation,
                        bgcolor)
        data_params=list([])
        data_params.append(serie_01)

        if plottype=='line':
            png_figure=hp.plot_lines(general_params,data_params)
        elif plottype=='bar':
            png_figure=hp.plot_bars(general_params,data_params)
        else:
            #data_params[0]['dp_shape_color']='o-r'
            png_figure=hp.plot_combined(general_params,data_params)

        revenues=pd.DataFrame(revenues).rename(columns={0: 'Total Sold'})
        return  revenues,png_figure

    def get_products_revenues_info(self,plottype):
        revenues=self.order_details_dataframe.groupby('Product')['Total $'].sum().sort_values(ascending=False)

        fig_size1=8
        fig_size2=6
        fig_title="Total Sold by PRODUCT (top 20)"
        indextype='S'
        xlabel="PRODUCT"
        ylabel="Total Sold [$]"
        spines=['top','bottom','left','right']
        rotation=90
        bgcolor="#8cb1cf"
        serie_01={'data': revenues.head(20),
                  'dp_shape_color': '-g',
                  'lw':1,
                  'legend':'Product Revenues',
                  'edgecolor': '#60A0D0',
                  'color': '#FFFFFF',
                  'annotate': 'f',
                  'color_highest': 'y',
                  'color_shortest': 'y'}
        general_params=(fig_size1,
                        fig_size2,
                        fig_title,
                        revenues.index[0:20],
                        indextype,
                        xlabel,
                        ylabel,
                        spines,
                        rotation,
                        bgcolor)
        data_params=list([])
        data_params.append(serie_01)

        if plottype=='line':
            png_figure=hp.plot_lines(general_params,data_params)
        elif plottype=='bar':
            png_figure=hp.plot_bars(general_params,data_params)
        else:
            #data_params[0]['dp_shape_color']='o-r'
            png_figure=hp.plot_combined(general_params,data_params)

        revenues=pd.DataFrame(revenues).rename(columns={0: 'Total Sold'})
        return  revenues.head(20),png_figure

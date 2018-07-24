# coding: utf-8
from sqlalchemy import Column, Date, Float, Integer, LargeBinary, SmallInteger, String, Table, Text, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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

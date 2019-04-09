from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///DataBase.db', echo=True)
Base = declarative_base()

class JuniorForm(Base):

	__tablename__ = "JuniorForm"

	id = Column(Integer, primary_key=True)
	Name = Column(String)
	Part = Column(String)
	Phone = Column(Integer)
	Email = Column(String)
	Time = Column(String)
	Option = Column(String)
	Payment = Column(String)

class SeniorForm(Base):

	__tablename__ = "SeniorForm"

	id = Column(Integer, primary_key=True)
	Name = Column(String)
	Part = Column(String)
	Phone = Column(Integer)
	Email = Column(String)
	Time = Column(String)
	Option = Column(String)
	Payment = Column(String)

class User(Base):

	__tablename__ = "User"

	Username = Column(String, primary_key=True)
	Password = Column(String, primary_key=True)
	PhoneNO = Column(Integer, primary_key=True)
	Email = Column(String, primary_key=True)

class OEM(Base):

	__tablename__ = "OEM"

	id = Column(Integer, primary_key=True)
	Name = Column(String)
	Phone = Column(Integer)
	Email = Column(String)
	Pname = Column(String)
	Price = Column(Integer)
	Option = Column(String)

class Admin(Base):

	__tablename__ = "Admin"

	AdminName = Column(String, primary_key=True)
	AdminPassword = Column(String, primary_key=True)

class Image(Base):

	__tablename__ = "Image"

	ImageName = Column(String, primary_key=True)


def __init__(self, Username, Password, PhoneNO, Email, Pname, Price, ImageName, Name, Phone, Option):

	self.Username = Username
	self.Password = Password
	self.PhoneNO = PhoneNO
	self.Email = Email
	self.Pname = Pname
	self.Price = Price
	self.ImageName = ImageName
	self.Name = Name
	self.Phone = Phone
	self.Option = Option

# create tables
Base.metadata.create_all(engine)
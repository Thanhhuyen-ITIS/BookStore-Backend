from sqlalchemy import Column, Integer, String, ForeignKey, BLOB, Float, Text
from sqlalchemy.orm import relationship

from config.database import Base
from sqlalchemy.types import DATE, DATETIME


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20))

class User(Base):
    __tablename__ = 'user'
    username = Column(String(45), primary_key=True)
    email = Column(String(45), nullable=False)
    password = Column(String(200), nullable=False)
    name = Column(String(45))
    gender = Column(String(10))
    id_role = Column(Integer, ForeignKey('role.id'), default=2)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    category = Column(String(100), nullable=False)


class Book (Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100))
    about = Column(String(500))
    id_category = Column(Integer, ForeignKey('category.id'))
    release_date = Column(DATE)
    picture = Column(Text(4294967295), nullable=False)
    page = Column(Integer)
    quatity_sold = Column(Integer, default=0)
    cost = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)

class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), ForeignKey('user.username'), nullable=False)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    count = Column(Integer, nullable=False, default=1)


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(100), nullable=False)


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), ForeignKey('user.username'))
    name = Column(String(100))
    address = Column(String(1000))
    id_book = Column(Integer, ForeignKey('book.id'))
    quantity = Column(Integer)
    total_price = Column(Integer)
    order_date = Column(DATE)

    id_status = Column(Integer, default=1)





class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), ForeignKey('user.username'))
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    star = Column(Integer, nullable=False)
    comment = Column(String(300))

class Comment(Base):
    __tablename__  = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), ForeignKey('user.username'))
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    comment = Column(String(300), nullable=False)




from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'produto'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    inventory = Column(Integer)
    
    def __repr__(self):
       return "<User(name='%s')>" % (self.name)
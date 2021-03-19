from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Seller(Base):
    __tablename__ = 'vendedor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
       return "<User(name='%s')>" % (self.name)
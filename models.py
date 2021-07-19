from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sneaker(Base):
  '''
      description: Sneaker description
  '''
  __tablename__ = 'sneakers'

  id = Column(Integer, primary_key=True)
  name = Column(String())
  brand = Column(String())
  release_date = Column(String())
  sku = Column(String())

  def __init__(self, name, brand, release_date, sku):
    self.name = name
    self.brand = brand
    self.release_date = release_date
    self.sku = sku

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def serialize(self):
    return {
        'id': self.id,
        'name': self.name,
        'brand': self.brand,
        'release_date': self.release_date,
        'sku': self.sku
    }

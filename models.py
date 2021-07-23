from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Sneaker(Base):
  '''
      description: Sneakers
  '''
  __tablename__ = 'sneakers'

  id = Column(Integer, primary_key=True)
  name = Column(String())
  brand = Column(String())
  sku = Column(String())
  colorway = Column(String())
  gender = Column(String())
  release_year = Column(Integer())
  release_date = Column(String())
  retail_price = Column(BigInteger())
  estimated_market_value = Column(BigInteger())
  story = Column(String())
  image = relationship("Image", back_populates="sneaker", uselist=False, cascade="all, delete")
  links = relationship("Link", back_populates="sneaker", uselist=False, cascade="all, delete")
  source_id = Column(Integer, ForeignKey('sources.id'))
  source = relationship("Source", back_populates="sneaker")
  id_in_source = Column(String())

  def __init__(self, **kwargs):
    super(Sneaker, self).__init__(**kwargs)

  def __repr__(self):
    return f"<id { self.id }, name { self.name }, sku { self.sku }, id_in_source { self.id_in_source }>"

  def serialize(self):
    return {
        'id': self.id,
        'name': self.name,
        'brand': self.brand,
        'sku': self.sku,
        'colorway': self.colorway,
        'gender': self.gender,
        'release_year': self.release_year,
        'release_date': self.release_date,
        'retail_price': self.retail_price,
        'estimated_market_value': self.estimated_market_value,
        'story': self.story,
        'image': self.image.serialize(),
        'links': self.links.serialize(),
        'source': self.source.serialize(),
        'id_in_source': self.id_in_source,
    }


class Image(Base):
  '''
    description: Images
  '''
  __tablename__ = 'images'

  id = Column(Integer, primary_key=True)
  original = Column(String())
  small = Column(String())
  thumbnail = Column(String())
  sneaker_id = Column(Integer, ForeignKey('sneakers.id'))
  sneaker = relationship("Sneaker", back_populates="image")

  def __init__(self, **kwargs):
    super(Image, self).__init__(**kwargs)

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def serialize(self):
    return {
        'original': self.original,
        'small': self.small,
        'thumbnail': self.thumbnail,
    }


class Link(Base):
  '''
    description: Links
  '''
  __tablename__ = 'links'

  id = Column(Integer, primary_key=True)
  stockx = Column(String())
  goat = Column(String())
  flight_club = Column(String())
  sneaker_id = Column(Integer, ForeignKey('sneakers.id'))
  sneaker = relationship("Sneaker", back_populates="links")

  def __init__(self, **kwargs):
    super(Link, self).__init__(**kwargs)

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def serialize(self):
    return {
        'stockx': self.stockx,
        'goat': self.goat,
        'flight_club': self.flight_club,
    }


class Source(Base):
  '''
    description: Source
  '''
  __tablename__ = 'sources'

  id = Column(Integer, primary_key=True)
  name = Column(String())
  sneaker = relationship("Sneaker", back_populates="source")

  def __init__(self, **kwargs):
    super(Source, self).__init__(**kwargs)

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def serialize(self):
    return {
        'name': self.name,
    }

from app import db

class Sneaker(db.Model):
  __tablename__ = 'sneakers'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  brand = db.Column(db.String())
  release_date = db.Column(db.String())

  def __init__(self, name, brand, release_date):
    self.name = name
    self.brand = brand
    self.release_date = release_date

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'brand': self.brand,
      'release_date': self.release_date
    }
import os
import unittest

from app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base, Sneaker, Image, Link, Source


class BaseCase(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()

    load_dotenv()  # take environment variables from .env
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    self.session = Session()

  def tearDown(self):
    # Delete Database collections after the test is complete
    sneakers = self.session.query(Sneaker).all()
    for sneaker in sneakers:
      self.session.delete(sneaker)

    sources = self.session.query(Source).all()
    for source in sources:
      self.session.delete(source)

    self.session.commit()

  def create_sneaker(self):
    sneaker_payload = {
        "_id": "1234567890",
        "sku": "CW5814-001",
        "brand": "Nike",
        "name": "Nike Free Run Trail Black Anthracite",
        "colorway": "Black/Anthracite-White",
        "gender": "men",
        "releaseYear": 2021,
        "releaseDate": "2021-08-01",
        "retailPrice": 110,
        "estimatedMarketValue": 87,
        "story": "",
        "image": {
            "original": "https://image.goat.com/attachments/product_template_pictures/images/056/696/892/original/CW5814_001.png.png",
            "small": "https://image.goat.com/750/attachments/product_template_pictures/images/056/696/892/original/CW5814_001.png.png",
            "thumbnail": "https://image.goat.com/400/attachments/product_template_pictures/images/056/696/892/original/CW5814_001.png.png"
        },
        "links": {
            "stockx": "https://stockx.com/nike-free-run-trail-black-anthracite",
            "goat": " https://goat.com/sneakers/free-run-trail-black-white-cw5814-001",
            "flightClub": " https://flightclub.com/free-run-trail-black-white-cw5814-001"
        }
    }

    source = Source(
        name='test'
    )

    image = Image(
        original=sneaker_payload['image']['original'],
        small=sneaker_payload['image']['small'],
        thumbnail=sneaker_payload['image']['thumbnail'],
    )

    links = Link(
        stockx=sneaker_payload['links']['stockx'],
        goat=sneaker_payload['links']['goat'],
        flight_club=sneaker_payload['links']['flightClub'],
    )

    sneaker = Sneaker(
        name=sneaker_payload['name'],
        brand=sneaker_payload['brand'],
        sku=sneaker_payload['sku'],
        colorway=sneaker_payload['colorway'],
        gender=sneaker_payload['gender'],
        release_year=sneaker_payload['releaseYear'],
        release_date=sneaker_payload['releaseDate'],
        retail_price=sneaker_payload['retailPrice'],
        estimated_market_value=sneaker_payload['estimatedMarketValue'],
        story=sneaker_payload['story'],
        image=image,
        links=links,
        source=source,
        id_in_source=sneaker_payload['_id'],
    )

    self.session.add(source)
    self.session.add(image)
    self.session.add(links)
    self.session.commit()
    self.session.add(sneaker)
    self.session.commit()

    return sneaker_payload

import os
import json
import httpx
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Sneaker, Image, Link, Source

sneakers_file = 'thesneakerdatabase.json'
sneakers_url = 'https://www.thesneakerdatabase.com/api/getData?brand=Nike'
sneakers_headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Accept': '*/*',
    'Origin': 'https://thesneakerdatabase.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://thesneakerdatabase.com/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7'
}
load_dotenv()  # take environment variables from .env
database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()


def get_sneakers_from_url():
  response = httpx.get(sneakers_url, headers=sneakers_headers)
  return response.json()['data']


def get_sneakers_from_file(file):
  with open(f"./{ file }") as json_file:
    return json.load(json_file)['data']


def get_or_create_sneaker(sneaker, source):
  instance = session.query(Sneaker).filter_by(sku=sneaker['sku']).one_or_none()
  if instance:
    return True
  else:
    image = Image(
        original=sneaker['image']['original'],
        small=sneaker['image']['small'],
        thumbnail=sneaker['image']['thumbnail'],
    )

    links = Link(
        stockx=sneaker['links']['stockx'],
        goat=sneaker['links']['goat'],
        flight_club=sneaker['links']['flightClub'],
    )

    instance = Sneaker(
        name=sneaker['name'],
        brand=sneaker['brand'],
        sku=sneaker['sku'],
        colorway=sneaker['colorway'],
        gender=sneaker['gender'],
        release_year=sneaker['releaseYear'],
        release_date=sneaker['releaseDate'],
        retail_price=sneaker['retailPrice'],
        estimated_market_value=sneaker['estimatedMarketValue'],
        story=sneaker['story'],
        image=image,
        links=links,
        source=source,
        id_in_source=sneaker['_id'],
    )

    try:
      session.add(image)
      session.add(links)
      session.commit()
      session.add(instance)
      session.commit()
      print(f"{ sneaker['name'] } created")
      return True
    # The actual exception depends on the specific database so we catch all exceptions.
    # This is similar to the official documentation:
    # https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
    except Exception as e:
      print(f"get_or_create error: { str(e) }")
      session.rollback()
      return False


def get_or_create_source():
  instance = session.query(Source).filter_by(name='thesneakerdatabase.com').one_or_none()
  if instance:
    return instance
  else:
    instance = Source(
        name='thesneakerdatabase.com'
    )
    try:
      session.add(instance)
      session.commit()
      return instance
    except Exception as e:
      print(f"get_or_create_source error: { str(e) }")
      session.rollback()
      raise e


def save_to_db(sneakers):
  source = get_or_create_source()
  # for sneaker in sneakers:
  for sneaker in sneakers[:10]:
    # print(f"sneaker: { sneaker['name'] }", end='')
    new_sneaker = get_or_create_sneaker(sneaker, source)
    # if new_sneaker:
    #   print(f" - success")
    # else:
    #   print(f" - fail")
    if not new_sneaker:
      print(f"{ sneaker['name'] } - fail")


def count_in_db():
  sneakers = session.query(Sneaker).all()
  return len(sneakers)


def handler(event, context):
  if os.path.exists(f"./{ sneakers_file }"):
    print(f"load snekers from { sneakers_file }")
    sneakers = get_sneakers_from_file(sneakers_file)
  else:
    print('getting sneakers from url ...')
    sneakers = get_sneakers_from_url()

  print('saving sneakers in db ...')
  save_to_db(sneakers)
  print(f"count of sneakers in db: { count_in_db() }")


if __name__ == '__main__':
  handler({}, {})

import json
from models import Base, Sneaker

api_path = '/v1/sneakers'
headers = {"Content-Type": "application/json"}


def test_create_sneaker_success(client, dbsession):
  payload = {
      "sku": "ABC123",
      "brand": "Nike",
      "name": "Nike Super Waffle",
      "colorway": "White",
      "gender": "men",
      "release_year": 2099,
      "release_date": "2099-01-01",
      "retail_price": 100,
      "estimated_market_value": 0,
      "story": "",
      "image": {
          "original": "none at the moment",
          "small": "none at the moment",
          "thumbnail": "none at the moment"
      },
      "links": {
          "stockx": "none at the moment",
          "goat": "none at the moment",
          "flight_club": "none at the moment"
      }
  }

  response = client.post(api_path, headers=headers, data=json.dumps(payload))
  new_sneaker_id = response.json['items'][0]['id']
  sneaker = dbsession.query(Sneaker).filter_by(id=new_sneaker_id).one_or_none()

  assert response.status_code == 201
  assert sneaker.name == payload['name']
  assert sneaker.sku == payload['sku']
  assert sneaker.source.name == 'Sneakers API'
  assert sneaker.id_in_source == str(sneaker.id)


# def test_create_sneaker_missing_fields(client):
#   payload = json.dumps({
#       "email": "paurakh011@gmail.com",
#       "password": "mycoolpassword"
#   })

#   response = client.post(api_path, headers=headers, data=payload)

#   assert ...

#   # create sneaker via API
#   # check response is 400
#   # check response error array contains missing fields

# CHECK SKU ALREADY EXIST

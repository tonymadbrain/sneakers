import json
from models import Sneaker

api_path = '/v1/sneakers'
headers = {"Content-Type": "application/json"}


def test_empty_response(client, dbsession):
  response = client.get(api_path)
  expected = {
      'items': [],
      'errors': []
  }

  assert response.status_code == 200
  assert response.json == expected


def test_sneakers_response(client, sneaker):
  response = client.get(api_path)
  added_sneaker = response.json['items'][0]

  assert sneaker['name'] == added_sneaker['name']
  assert sneaker['sku'] == added_sneaker['sku']
  assert sneaker['_id'] == added_sneaker['id_in_source']
  assert len(response.json['items']) == 1
  assert response.status_code == 200


def test_sneakers_by_id_response(client, sneaker):
  response = client.get(api_path)
  added_sneaker_id = response.json['items'][0]['id']

  response = client.get(f"{ api_path }/{ added_sneaker_id }")
  added_sneaker = response.json['items'][0]

  assert 'test' == added_sneaker['source']['name']
  assert sneaker['name'] == added_sneaker['name']
  assert response.status_code == 200


def test_nonexistent_sneaker_response(client, sneaker):
  response = client.get(api_path)
  added_sneaker_id = response.json['items'][0]['id']

  response = client.get(f"{ api_path }/{ added_sneaker_id + 1 }")
  expected = {'items': [], 'errors': ['Sneaker not found']}
  assert response.status_code == 404
  assert response.json == expected


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

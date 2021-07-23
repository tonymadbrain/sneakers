def test_index(client):
  response = client.get('/')

  expected = 'Welcome to Sneakers API!<br />Endpoints:<br /> - GET /v1/sneakers<br /> - GET /v1/sneakers/$id'

  assert response.status_code == 200
  assert expected == response.get_data(as_text=True)


def test_empty_response(client, dbsession):
  response = client.get('/v1/sneakers')

  assert response.status_code == 200
  assert response.json == []


def test_sneakers_response(client, sneaker):
  response = client.get('/v1/sneakers')
  added_sneaker = response.json[0]

  assert sneaker['name'] == added_sneaker['name']
  assert sneaker['sku'] == added_sneaker['sku']
  assert sneaker['_id'] == added_sneaker['id_in_source']
  assert len(response.json) == 1
  assert response.status_code == 200


def test_sneakers_by_id_response(client, sneaker):
  response = client.get('/v1/sneakers')
  added_sneaker_id = response.json[0]['id']

  response = client.get(f"/v1/sneakers/{ added_sneaker_id }")
  added_sneaker = response.json

  assert sneaker['name'] == added_sneaker['name']
  assert response.status_code == 200


def test_non_existent_sneaker_response(client, sneaker):
  response = client.get('/v1/sneakers')
  added_sneaker_id = response.json[0]['id']

  response = client.get(f"/v1/sneakers/{ added_sneaker_id + 1 }")

  assert response.status_code == 404

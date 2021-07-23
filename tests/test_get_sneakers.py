api_path = '/v1/sneakers'


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

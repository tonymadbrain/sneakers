def test_index(client):
  response = client.get('/')

  expected = 'Welcome to Sneakers API!<br />Endpoints:<br /> - GET /v1/sneakers<br /> - GET /v1/sneakers/$id'

  assert response.status_code == 200
  assert expected == response.get_data(as_text=True)


def test_nonexistent(client):
  response = client.get('/nonexistent_endpoint')

  expected = {'items': [], 'errors': ['Not found']}
  assert response.status_code == 404
  assert response.json == expected


def test_not_allowed(client):
  response = client.post('/')

  expected = {'items': [], 'errors': ['Method not allowed']}
  assert response.status_code == 405
  assert response.json == expected

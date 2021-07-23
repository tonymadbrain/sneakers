def test_index(client):
  response = client.get('/')

  expected = 'Welcome to Sneakers API!<br />Endpoints:<br /> - GET /v1/sneakers<br /> - GET /v1/sneakers/$id'

  assert response.status_code == 200
  assert expected == response.get_data(as_text=True)

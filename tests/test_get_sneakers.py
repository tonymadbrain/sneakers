import unittest
import json

from tests.base_case import BaseCase


class TestGetSneakers(BaseCase):

  def test_empty_response(self):
    response = self.app.get('/v1/sneakers')
    self.assertListEqual(response.json, [])
    self.assertEqual(response.status_code, 200)

  def test_sneakers_response(self):
    # Given
    sneaker_payload = self.create_sneaker()

    # When
    response = self.app.get('/v1/sneakers')
    added_sneaker = response.json[0]

    # Then
    self.assertEqual(sneaker_payload['name'], added_sneaker['name'])
    self.assertEqual(sneaker_payload['sku'], added_sneaker['sku'])
    self.assertEqual(sneaker_payload['_id'], added_sneaker['id_in_source'])
    self.assertEqual(1, len(response.json))
    self.assertEqual(200, response.status_code)

  def test_sneakers_by_id_response(self):
    # Given
    sneaker_payload = self.create_sneaker()
    response = self.app.get('/v1/sneakers')
    added_sneaker_id = response.json[0]['id']

    # When
    response = self.app.get(f"/v1/sneakers/{ added_sneaker_id }")
    added_sneaker = response.json

    # Then
    self.assertEqual(sneaker_payload['name'], added_sneaker['name'])
    self.assertEqual(200, response.status_code)

  def test_non_existent_sneaker_response(self):
    # Given
    self.create_sneaker()
    response = self.app.get('/v1/sneakers')
    added_sneaker_id = response.json[0]['id']

    # When
    response = self.app.get(f"/v1/sneakers/{ added_sneaker_id + 1 }")

    # Then
    self.assertEqual(404, response.status_code)

#!/usr/bin/python3
"""Testing review endpoint"""
import unittest
from app import create_app
import uuid

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        email = f"{uuid.uuid4()}@something.com"
        user_response = self.client.post('api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": email
        })
        self.user = user_response.get_json()["id"]
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place for testing reviews",
            "price": 50.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.user,
            "amenities": []
        })
        self.place = place_response.get_json()["id"]

    def test_create_review(self):
        response = self.client.post('api/v1/reviews/', json={
            "text": "Lovely place",
            "rating": 4,
            "user_id": self.user,
            "place_id": self.place
            })
        self.assertEqual(response.status_code, 201)

    def test_review_invalid_data(self):
        response = self.client.post('api/v1/reviews/', json={
            "text": "",
            "rating": 0,
            "user_id": "ofobabo-nfbafbabbf-akfibfau-gsgs",
            "place_id": "ofobabo-nfbafbabbf-akfibfau-gsgs"
        })
if __name__ == '__main__':
    unittest.main(verbosity=2)

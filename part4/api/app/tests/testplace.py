#!/usr/bin/python3
"""Testing place endpoint"""
import uuid
import unittest
from app import create_app
from flask_jwt_extended import create_access_token

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        email = f"john-{uuid.uuid4()}@example.com"

        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": email,
            "password": "password123"
        })
        
        self.user_id = user_response.get_json()["id"]
        self.token = create_access_token(identity=self.user_id)
    def test_create_place(self):
        response = self.client.post('/api/v1/places/', 
            headers={"Authorization": f"Bearer {self.token}"},
            json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.00,
            "latitude": 37.7749,
            "longitude": -122.4194
            })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_data(self):
        response = self.client.post('/api/v1/places/',
            headers={"Authorization": f"Bearer {self.token}"},                         
            json={
            "title": "",
            "description": "",
            "price": -1,
            "latitude": 190,
            "longitude": -190
            })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main(verbosity=2)

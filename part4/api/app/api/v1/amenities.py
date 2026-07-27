#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields, marshal
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})
amenity_response = api.model('AmenityResponse', {
    'id': fields.String,
    'name': fields.String,
})
@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validation=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        try:
            amenity = facade.create_amenity(amenity_data)
            return marshal(amenity, amenity_response), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    @api.marshal_list_with(amenity_response)
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return amenities, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {'error': 'Amenity not found'}, 404
        return marshal(amenity, amenity_response),  200

    @api.expect(amenity_model, validation=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {'error': 'Amenity not found'}, 404
        try:
            amenity_data = api.payload
            facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return {"message": "Amenity updated successfully"}, 200

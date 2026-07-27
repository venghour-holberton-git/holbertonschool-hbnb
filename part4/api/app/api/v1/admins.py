#!/usr/bin/python3

from app.services import facade
from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt
from app.extensions import bcrypt
from app.api.v1.reviews import review_model

api = Namespace('admin', description='Admin operations')

review_modify = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'password': fields.String(required=True, description='User password'),
    'email': fields.String(required=True, description='Email of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_response = api.model('AmenityResponse', {
    'id': fields.String,
    'name': fields.String
})

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @api.expect(user_model)
    @api.response(400, "Invalid input data")
    @api.response(200, "User updated successfully")
    @api.response(404, "user not found")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def put(self, user_id):

        user_data = api.payload
        """No data"""
        if not user_data:
            return {"error": "Invalid input data"}, 400
        
        first_name = user_data.get("first_name")
        if first_name is not None and not isinstance(first_name, str):
            return {"error": "Invalid first name"}, 400
        
        last_name = user_data.get("last_name")
        if last_name is not None and not isinstance(last_name, str):
            return {"error": "Invalid last name"}, 400
        
        email = user_data.get("email")
        if email is not None: 
            if not isinstance(email, str) or "@" not in email:
                return {"error": "Invalid email"}, 400

        user = facade.get_user(user_id)
        """ID was not found, wrong or missing"""
        if not user:
            return {"error": "user not found"}, 404

        current_user = get_jwt()
        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
            
        existing_user = facade.get_user_by_email(email)
        if email:
            # Check if email is already in use
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        if 'password'in user_data:
            if user_data['password'] == "":
                return {"error": "empty password"}, 400
            user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

        facade.update_users(user_id, user_data)
        return {"message": "User updated successfully"}, 200

@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(user_model, validation=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):

        user_data = api.payload
        """No data"""
        if not user_data:
            return {"error": "No data provided"}, 400

        current_user = get_jwt()
        """Admin verification"""
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return {
            "id": new_user.id,
            "message": "User created successfully"
        }, 201


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model, validation=True)
    @api.response(400, "Invalid input data")
    @api.response(201, "Amenity successfully created")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):

        amenity_data = api.payload
        """No data"""
        if not amenity_data:
            return {"error": "Invalid input data"}, 400

        current_user = get_jwt()
        """If not admin validation"""
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to create a new amenity
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return marshal(new_amenity, amenity_response), 201

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def put(self, amenity_id):

        amenity_data = api.payload
        """No data"""
        if not amenity_data:
            return {"error": "Invalid input data"}, 400

        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {"error": "Amenity not found"}, 404

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return {"message": "Amenity updated successfully"}, 200

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def put(self, place_id):

        place_data = api.payload
        place_data.pop("owner_id",None)
        """No data"""
        if not place_data:
            return {"error": "Invalid input data"}, 400

        current_user = get_jwt()
        # Set is_admin default to False if not exists

        is_admin = current_user.get('is_admin', False)
        if not is_admin:
            return {'error': 'Unauthorized action'}, 403

        place = facade.get_place(place_id)
        if place is None:
            return {"error": "place not found"}, 404
        try:
            updated_place = facade.update_place(place_id, place_data)
            """Update fail"""   
            if not updated_place:
                return {"error": "update failed"}, 400
        except Exception as e:
            return {"error": str(e)}, 400
        return {"message": "Place updated successfully"}, 200

@api.route('/places/<place_id>')
class AdminPlaceDelete(Resource):
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        found_place = facade.get_place(place_id)
        if found_place is None:
            return {"error": "place not found"}, 404
        
        try:
            facade.delete_place(place_id)
            return {'success': 'Place successfully deleted'}, 200
        except ValueError as e:
            return {'error': str(e)}, 404
        
@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @jwt_required()
    @api.expect(review_modify)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        
        review_data = api.payload
        """No data"""
        if not review_data:
            return {"error": "Invalid input data"}, 400

        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        found_review = facade.get_review(review_id)
        if found_review is None:
            return {"error": "review not found"}, 404
        
        try:
            review = facade.update_review(review_id, review_data)
            if not review:
                return {'error': "Update Failed"}, 400
        except ValueError as e:
            return {"error": str(e)}, 400

        return {'success': "Review update"}, 200
    
@api.route('/reviews/<review_id>')
class AdminReviewDelete(Resource):
    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, "Admin privileges required")
    def delete(self, review_id):
        """Delete a review"""
        
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        found_review = facade.get_review(review_id)
        if found_review is None:
            return {"error": "review not found"}, 404
        
        try:
            facade.delete_review(review_id)
            return {'success': 'Review successfully deleted'}, 200
        except ValueError as e:
            return {'error': str(e)}, 404
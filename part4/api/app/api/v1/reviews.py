from flask_restx import Namespace, Resource, fields, marshal
from app.services import facade
from app.models.review import Review
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_output = api.model('Review_out', {
    'id': fields.String,
    'text': fields.String,
    'rating': fields.Integer,
    'user_id': fields.String(attribute="user.id"),
    'place_id': fields.String
    })

review_list_output = api.model('Review List Output', {
    'id': fields.String,
    'text': fields.String,
    'rating': fields.Integer,
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validation=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        place = facade.get_place(review_data.get("place_id"))
        if place is None:
            return {"error": "Place not found"}, 400

        user = facade.get_user(get_jwt_identity())

        if get_jwt_identity() == place.owner.id:
            return {"error": "Review can't be created by the place owner"}, 400
        for review in place.reviews:
            if review.user.id == get_jwt_identity():
                return {"error": "Only one review is allowed per place"}, 400

        fields = ["text", "rating"]
        review_params = {f:review_data[f] for f in fields}
        review_params["place_id"] = place.id
        review_params["user"] = user
        review_params["user_id"] = get_jwt_identity()
        try:
            new_review = facade.create_review(review_params)
            place.add_review(new_review)
            return marshal(new_review, review_output), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_list_output)
    def get(self):
        """Retrieve a list of all reviews"""
        review_list = facade.get_all_reviews()
        return review_list, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @jwt_required()
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review == None:
            return {'error': 'Review not found'}, 404
        return marshal(review, review_output), 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        founded_review = facade.get_review(review_id)
        if get_jwt_identity() != founded_review.user.id:
            return {"error": "Users can only modify reviews they created"}, 403
        review = facade.update_review(review_id, review_data)
        if not review:
            return {'error': "review is not found"}, 400

        return {'success': "Review update"}, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        founded_review = facade.get_review(review_id)
        if get_jwt_identity() != founded_review.user.id:
            return {"error": "Users can only delete reviews they created"}, 403
        try:
            facade.delete_review(review_id)
            return {'success': 'Review successfully deleted'}, 200
        except ValueError as e:
            return {'error': str(e)}, 404

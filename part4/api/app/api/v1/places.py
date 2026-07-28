from flask_restx import Namespace, Resource, fields, marshal
from app.services import facade
from app.models.place import Place
from app.api.v1.reviews import review_model, review_list_output
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})
place_id_model = api.model(
    'place_id',
    {
        "id": fields.String,
        "title": fields.String,
        "description": fields.String,
        "price": fields.Float,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "owner": fields.Nested(user_model),
        "amenities": fields.List(fields.Nested(amenity_model)),
        "reviews": fields.List(fields.Nested(review_model))
    }
)
place_post_model = api.model(
    'place_most',
    {
        "id": fields.String,
        "title": fields.String,
        "price": fields.Float,
        "description": fields.String,
        "price": fields.Float,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "owner_id": fields.String(attribute="owner.id")
    }
)

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validation=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        data = api.payload
        user = facade.get_user(get_jwt_identity())
        if user == None:
            return {"message": "no user found"}, 400
        try:
            params_field = ["title", "description", "price", "latitude", "longitude"]
            place_params = {p_f:data[p_f] for p_f in params_field}
            place_params["owner_id"] = user.id
            new_place = facade.create_place(place_params)
        except Exception as e:
            return {"error": str(e)}, 400
        return marshal(new_place, place_post_model) , 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        data = facade.get_all_places()
        if not all(isinstance(p, Place) for p in data):
            raise TypeError("This is a place list")
        fields = ["id", "title", "price", "latitude", "longitude"]
        res_dic = [{field: d.__dict__[field] for field in fields} for d in data]
        return res_dic, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @jwt_required()
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_with(place_id_model)
    def get(self, place_id):
        """Get place details by ID"""
        data = facade.get_place(place_id)
        if data == None:
            return {"error": "Place dose not exist"}, 200
        return data, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload

        """ prevent client from change owner_id of the place """
        data.pop("owner_id",None)

        try:
            founded_place = facade.get_place(place_id)
            if founded_place is None:
                return {"error": "place not found"}, 404
            if founded_place.owner_id != get_jwt_identity():
                return {"error": "only owner of the place is allowed to modify"}, 403
            is_updated = facade.update_place(place_id, data)
            if not is_updated:
                return {"error": "place not found"}, 404
            return {"message": "success"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "place not found"}, 400
        reviews = place.reviews
        if not reviews or len(reviews) == 0:
            return {"message": "no review found"}, 200

        return marshal(reviews, review_list_output), 200

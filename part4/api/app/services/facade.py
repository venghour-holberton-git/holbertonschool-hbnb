#!/usr/bin/python3

from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.services.repositories.user_repository import UserRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.extensions import db

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()  # Switched to SQLAlchemyRepository
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # User related methods
    def create_user(self, user_data):
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        email = user_data.get("email")

        if not all([first_name, last_name]) or not all(isinstance(x, str) for x in [first_name, last_name]):
            raise ValueError("Invalid name fields")

        if not email or not isinstance(email, str) or "@" not in email:
            raise ValueError("Invalid email")

        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_users(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)
    # Amenities related methods
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")

        if any(char.isdigit() for char in name):
            raise ValueError("Cannot input numbers")
        if not name or not isinstance(name, str):
            raise ValueError("Invalid amenity name")

        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        name = amenity_data.get("name")

        if not name or not isinstance(name, str):
            raise ValueError("Invalid name input")
        if any(char.isdigit() for char in name):
            raise ValueError("Cannot input numbers")
        return self.amenity_repo.update(amenity_id, amenity_data)

    # Place realted methods
    def create_place(self, place_data):
        if not isinstance(place_data["price"], float):
            raise TypeError("price data need to be of type float")
        if place_data["price"] < 0:
            raise ValueError("price need to be positive number")
        if place_data["latitude"] < -90 or place_data["latitude"] > 90:
            raise ValueError("latitude must be between -90 and 90")
        if place_data["longitude"] < -180 or place_data["longitude"] > 180:
            raise ValueError("longitude must be between -180 and 180")
        place_data.pop("reviews", None)
        place_data.pop("amenities", None)
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        if place_data["title"] == "":
            raise ValueError("empty title")
        if not isinstance(place_data["price"], float):
            raise TypeError("price data need to be of type float")
        if place_data["price"] < 0:
            raise ValueError("price need to be positive number")
        if place_data["latitude"] < -90 or place_data["latitude"] > 90:
            raise ValueError("latitude must be between -90 and 90")
        if place_data["longitude"] < -180 or place_data["longitude"] > 180:
            raise ValueError("longitude must be between -180 and 180")
        if not self.place_repo.get(place_id):
            return False
        if place_data["amenities"] is not None:
            available_amenities = self.get_all_amenities()
            amenities = [amenity for amenity in available_amenities if amenity.name in place_data["amenities"]]
            place_data["amenities"] = amenities
        place_data.pop("reviews", None)
        
        self.place_repo.update(place_id, place_data)
        return True
    
    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        
        if not place:
            raise ValueError("Place not found")
        
        self.place_repo.delete(place_id)
        return place
    
    # Review realated methods
    def create_review(self, review_data):
        if review_data["rating"] < 1 or review_data["rating"] > 5:
            raise ValueError("Rating should be between 1 and 5")

        review = Review(**review_data)

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get(place_id)

    def update_review(self, review_id, review_data):
        if review_data["rating"] < 1 or review_data["rating"] > 5:
            raise ValueError("Rating should be between 1 and 5")
        if not self.review_repo.get(review_id):
            return False
        
        review_data.pop("place_id", None)
        self.review_repo.update(review_id, review_data)
        return True

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)

        if not review:
            raise ValueError("Review not found")

        self.review_repo.delete(review_id)
        return review

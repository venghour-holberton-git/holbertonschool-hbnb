from app.models.base_model import BaseModel
from app.extensions import db
from app.models.place_amenity_associtation import place_amenity_association

class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(254), nullable = False)
    price = db.Column(db.Float, nullable = False)
    latitude = db.Column(db.Float, nullable = False)
    longitude = db.Column(db.Float, nullable = False)
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable = False)
    owner = db.relationship("User", back_populates="places")
    reviews = db.relationship("Review", backref='places', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity_association, lazy='subquery',
                                 backref=db.backref('places', lazy=True))

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

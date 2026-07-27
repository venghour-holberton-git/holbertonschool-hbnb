from app.extensions import db

place_amenity_association = db.Table(
    "place_amenity",
    db.Column("place_id", db.ForeignKey('places.id'), primary_key=True),
    db.Column("amenity_id", db.ForeignKey('amenities.id'), primary_key=True)
)

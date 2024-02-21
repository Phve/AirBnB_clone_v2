#!/usr/bin/python3
"""Defines the Place class."""

from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

association_table = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True, nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """Represents a Place for the HBNB project."""
    __tablename__ = "places"

    def __init__(self, *args, **kwargs):
        """Initialize Place object."""
        super().__init__(*args, **kwargs)
        if storage_type == 'db':
            self.city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
            self.user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
            self.name = Column(String(128), nullable=False)
            self.description = Column(String(1024))
            self.number_rooms = Column(Integer, default=0)
            self.number_bathrooms = Column(Integer, default=0)
            self.max_guest = Column(Integer, default=0)
            self.price_by_night = Column(Integer, default=0)
            self.latitude = Column(Float)
            self.longitude = Column(Float)
            self.reviews = relationship("Review", backref="place", cascade="all, delete, delete-orphan")
            self.amenities = relationship("Amenity", secondary=association_table, viewonly=False, backref="place_amenities")
        else:
            self.city_id = ""
            self.user_id = ""
            self.name = ""
            self.description = ""
            self.number_rooms = 0
            self.number_bathrooms = 0
            self.max_guest = 0
            self.price_by_night = 0
            self.latitude = 0.0
            self.longitude = 0.0
            self.amenity_ids = []

    if storage_type != 'db':
        @property
        def reviews(self):
            """Get a list of all linked Reviews."""
            review_list = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Get/set linked Amenities."""
            amenity_list = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)

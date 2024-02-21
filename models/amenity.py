#!/usr/bin/python3
"""Defines the Amenity class."""

from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """Represents an Amenity for the HBNB project."""

    __tablename__ = "amenities"

    def __init__(self, *args, **kwargs):
        """Initialize Amenity object."""
        super().__init__(*args, **kwargs)
        if storage_type == 'db':
            self.name = Column(String(128), nullable=False)
        else:
            self.name = ""


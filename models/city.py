#!/usr/bin/python3
"""Defines the City class."""

from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """Represents a city for the HBNB project."""

    __tablename__ = "cities"

    def __init__(self, *args, **kwargs):
        """Initialize City object."""
        super().__init__(*args, **kwargs)
        if storage_type == 'db':
            self.name = Column(String(128), nullable=False)
            self.state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
            self.places = relationship("Place", backref="cities", cascade="all, delete, delete-orphan")
        else:
            self.name = ''
            self.state_id = ''

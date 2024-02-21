#!/usr/bin/python3
"""Defines the State class."""

from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """Represents a state for the HBNB project."""

    __tablename__ = "states"

    def __init__(self, *args, **kwargs):
        """Initialize State object."""
        super().__init__(*args, **kwargs)
        if storage_type == 'db':
            self.name = Column(String(128), nullable=False)
            self.cities = relationship('City', backref='state', cascade='all, delete, delete-orphan')
        else:
            self.name = ''

    if storage_type != 'db':
        @property
        def cities(self):
            """Get a list of all linked cities."""
            from models import storage
            related_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    related_cities.append(city)
            return related_cities

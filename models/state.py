#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='all, delete')

    @property
    def cities(self):
        """getter that returns list of cities"""
        from models import storage
        city_list = []
        all_cities = storage.all(City).values()

        for city in all_cities:
            if self.id == city.state_id:
                city_list.append(city)

        return city_list

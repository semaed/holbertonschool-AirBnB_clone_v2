""" This module defines a class that manages database storage fro hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


username = os.getenv('HBNB_MYSQL_USER')
passwd = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
db = os.getenv('HBNB_MYSQL_DB')
env = os.getenv('HBNB_ENV')


class DBStorage:
    """
    This class manages storage of hbnb models to SQL
    """
    __engine = None
    __session = None
    __classes = [Amenity, City, Place, Review, State, User]

    def __init__(self):
        """ Constructor for the class DBStorage """
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@/{}".format(username, passwd, host, db), pool_pre_ping=True)

    if env == 'test':
        Base.MetaData.drop_all()

    def all(self, cls=None):
        """ Returns objects in dictionary format """
        dict = {}
        if cls in self.__classes:
            results = DBStorage.__session.query(cls)
            for result in results:
                key = "{}.{}".format(result.__class__.__name__, result.id)
                dict[key] = result

        if cls is None:
            for cls in self.__classess__:
                results = DBStorage.__session.query(cls)
                for result in results:
                    key = "{}:{}".format(result.__class__.__name__, result.id)
                    dict[key] = result

        return dict

    def new(self, obj):
        """ Adds new object to current db session """
        DBStorage.__session.add(obj)

    def save(self):
        """ Commits all changes of current db session """
        DBStorage.__session.commit()

    def delete(self, obj=None):
        """ Deletes from current db session if not none """
        DBStorage.__session.delete(obj)

    def reload(self):
        """ Creates current db session """
        Base.metadata.create_all(self.__engine)
        sessions = sessionmaker(bind=self.engine, expire_on_commit=False)
        Session = scoped_session(sessions)
        DBStorage.__session = Session()

    def close(self):
        """ Close Session """
        DBStorage.__session.close()

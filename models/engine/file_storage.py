#!/usr/bin/python3
"""
FileStorage module for serializing and deserializing JSON files
"""

import json
from os import path

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    FileStorage class that serializes and deserializes JSON files
    """

    FILE_PATH = "file.json"
    OBJECTS = {}

    CLASS_DICT = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def all(self):
        """Returns the dictionary of objects in memory"""
        return self.OBJECTS

    def new(self, obj):
        """Sets in OBJECTS the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.OBJECTS[key] = obj

    def save(self):
        """Serializes OBJECTS to the JSON file (path: FILE_PATH)"""
        serialized_objects = {}
        for key, obj in self.OBJECTS.items():
            serialized_objects[key] = obj.to_dict()

        with open(self.FILE_PATH, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """
        Deserializes the JSON file to OBJECTS.
        Only if the JSON file (FILE_PATH) exists; otherwise, do nothing.
        If the file does not exist, no exception should be raised.
        """
        if path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r', encoding="utf-8") as file:
                serialized_objects = json.load(file)
                for key, obj_data in serialized_objects.items():
                    class_name, obj_id = key.split('.')
                    obj_class = globals()[class_name]
                    obj_instance = obj_class(**obj_data)
                    self.OBJECTS[key] = obj_instance

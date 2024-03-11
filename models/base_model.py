#!/usr/bin/python3

import uuid
from datetime import datetime
import models


class BaseModel:
    """All functions in BaseModel class"""

    TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, *args, **kwargs):
        """Create a new BaseModel with time."""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ["created_at", "updated_at"]:
                        value = datetime.strptime(value, self.TIME_FORMAT)
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def to_dict(self):
        """Making the dictionary for user"""
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = obj_dict["created_at"].isoformat()
        obj_dict["updated_at"] = obj_dict["updated_at"].isoformat()
        return obj_dict

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()
        models.storage.new(self)

    def __str__(self):
        """Should print: {[<class name>] (<self.id>) <self.__dict__>}"""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

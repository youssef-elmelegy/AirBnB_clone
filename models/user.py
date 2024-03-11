#!/usr/bin/python3
"""User's class for BaseModel"""

from models.base_model import BaseModel


class User(BaseModel):
    """Super User class"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

#!/usr/bin/python3

"""my command line interpreter"""

import cmd
import re
from models.base_model import BaseModel
from models.user import User
from models import storage
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.place import Place


class HBNBCommand(cmd.Cmd):
    """
    A simple command line interpreter
    The simple_shell will cry after this
    """

    CLASSES = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    prompt = "(hbnb) "

    def __init__(self):
        super().__init__()

    def do_create(self, line):
        """Creates a new user Syntax: create <class_name>"""
        arg = line.split()
        if not arg:
            print("** class name missing **")
            return
        try:
            class_name = arg[0]
            object = self.CLASSES[class_name]()
            object.save()
            print(object.id)
        except KeyError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Prints the string representation."""
        args = line.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes the class if it exists"""
        args = line.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, line):
        """ Deletes an instance."""
        arg = line.split()

        if not arg:
            print([str(obj) for obj in storage.all().values()])
        elif arg[0] not in self.CLASSES:
            print("** class doesn't exist **")
        else:
            class_name = arg[0]
            instances = [
                str(obj) for key, obj in storage.all().items()
                if key.startswith(class_name + '.')
            ]
            print(instances)

    def do_update(self, line):
        """Update name of the user"""
        arg = line.split()
        if not arg:
            print("** class name missing **")
            return

        rexe = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s(".*"|[^"]\S*)?)?)?)?'
        match = re.search(rexe, line)

        if not match:
            print("** invalid command format **")
            return

        classname, uid, attribute, value = match.groups()

        if classname not in self.CLASSES:
            print("** class doesn't exist **")
            return
        elif not uid:
            print("** instance id missing **")
            return

        Key = f"{classname}.{uid}"
        if Key not in storage.all():
            print("** no instance found **")
            return
        elif not attribute:
            print("** attribute name missing **")
            return
        elif not value:
            print("** value missing **")
            return

        obj = storage.all()[Key]
        setattr(obj, attribute, value)

        storage.all()[Key].save()

    def do_EOF(self, line):
        """End Of File Handle (Ctrl + d)."""
        print()
        return True

    def emptyline(self):
        """Empty line handle."""
        pass

    def default(self, line):
        """if there is no match will print error word."""
        print(f"Unrecognized command: {line}.\
                Type 'help' for assistance.\n")


if __name__ == '__main__':
    HBNBCommand().cmdloop()

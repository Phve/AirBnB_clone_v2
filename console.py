import cmd
from shlex import split
from models import storage
from datetime import datetime

class MyConsole(cmd.Cmd):
    prompt = "(myconsole) "
    supported_classes = {"BaseModel", "User", "State", "City", "Amenity", "Place", "Review"}

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_quit(self, arg):
        """Quit the console"""
        return True

    def do_EOF(self, arg):
        """Handle EOF (Ctrl+D)"""
        print()
        return True

    def do_create(self, arg):
        """Create a new instance of a class"""
        try:
            args = split(arg)
            if not args:
                raise SyntaxError("Class name is missing.")
            class_name = args[0]
            if class_name not in self.supported_classes:
                raise ValueError("Invalid class name.")
            kwargs = {}
            for pair in args[1:]:
                key, value = pair.split("=")
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    value = eval(value)
                kwargs[key] = value
            new_instance = eval(class_name)(**kwargs)
            storage.new(new_instance)
            storage.save()
            print(new_instance.id)
        except SyntaxError as e:
            print("** Syntax error: {} **".format(e))
        except ValueError as e:
            print("** Value error: {} **".format(e))

    def do_show(self, arg):
        """Show the string representation of an instance"""
        try:
            args = split(arg)
            if len(args) != 2:
                raise SyntaxError("Usage: show <class> <id>")
            class_name, obj_id = args
            if class_name not in self.supported_classes:
                raise ValueError("Invalid class name.")
            key = "{}.{}".format(class_name, obj_id)
            obj = storage.all().get(key)
            if obj:
                print(obj)
            else:
                print("** No instance found **")
        except SyntaxError as e:
            print("** Syntax error: {} **".format(e))
        except ValueError as e:
            print("** Value error: {} **".format(e))

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id"""
        try:
            args = split(arg)
            if len(args) != 2:
                raise SyntaxError("Usage: destroy <class> <id>")
            class_name, obj_id = args
            if class_name not in self.supported_classes:
                raise ValueError("Invalid class name.")
            key = "{}.{}".format(class_name, obj_id)
            objects = storage.all()
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** No instance found **")
        except SyntaxError as e:
            print("** Syntax error: {} **".format(e))
        except ValueError as e:
            print("** Value error: {} **".format(e))

    def do_all(self, arg):
        """Display string representations of all instances of a class"""
        try:
            if arg:
                if arg not in self.supported_classes:
                    raise ValueError("Invalid class name.")
                objs = [str(obj) for obj in storage.all(arg).values()]
            else:
                objs = [str(obj) for obj in storage.all().values()]
            print(objs)
        except ValueError as e:
            print("** Value error: {} **".format(e))

    def do_update(self, arg):
        """Update an instance by adding or updating attribute"""
        try:
            args = split(arg)
            if len(args) < 3:
                raise SyntaxError("Usage: update <class> <id> <key=value>")
            class_name, obj_id = args[:2]
            if class_name not in self.supported_classes:
                raise ValueError("Invalid class name.")
            key = "{}.{}".format(class_name, obj_id)
            objects = storage.all()
            if key not in objects:
                print("** No instance found **")
                return
            obj = objects[key]
            for pair in args[2:]:
                key, value = pair.split("=")
                if hasattr(obj, key):
                    if value[0] == '"':
                        value = value.strip('"').replace("_", " ")
                    else:
                        value = eval(value)
                    setattr(obj, key, value)
                else:
                    print("** Attribute '{}' not found **".format(key))
                    return
            obj.save()
        except SyntaxError as e:
            print("** Syntax error: {} **".format(e))
        except ValueError as e:
            print("** Value error: {} **".format(e))

if __name__ == "__main__":
    MyConsole().cmdloop()

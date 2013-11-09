import pkgutil
import inspect

from viper.common.abstracts import Module

def load_modules():
    # Import modules package.
    import modules

    plugins = dict()

    # Walk recursively throug hall modules and packages.
    for loader, module_name, ispkg in pkgutil.walk_packages(modules.__path__, modules.__name__ + '.'):
        # If current item is a package, skip.
        if ispkg:
            continue

        # Try to import the module, otherwise skip.
        try:
            module = __import__(module_name, globals(), locals(), ['dummy'], -1)
        except ImportError as e:
            continue

        # Walk through all members of currently imported modules.
        for member_name, member_object in inspect.getmembers(module):
            # Check if current member is a class.
            if inspect.isclass(member_object):
                # Yield the class if it's a subclass of Module.
                if issubclass(member_object, Module) and member_object is not Module:
                    plugins[member_object.cmd] = dict(obj=member_object, description=member_object.description)

    return plugins

__modules__ = load_modules()
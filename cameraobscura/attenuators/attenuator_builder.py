
# python standard library
import os
import importlib
import inspect

# this package
from cameraobscura import CameraobscuraError
from attenuator import Attenuator

def is_attenuator(instance):
    """
    A function to see if the imported module item is a sub-class of Attenuator

    :param:

     - `instance`: an object to check

    :return: True if instance sub-classes `Attenuator`, False otherwise
    """
    # the 'inspect.isclass(instance)' call is there so that if there's
    # stuff in the modules that lack a `__base__` attribute it won't
    # raise an AttributeError
    return (inspect.isclass(instance) and instance.__base__ is Attenuator)

def get_definitions():
    """
    Imports class definitions for `Attenuator` sub-classes

    :return: dict of (name (lower-cased): class definition object)
    """
    definitions = {}
    if __name__ == '__builtin__':
        return definitions

    # directory is the path to this directory
    directory = os.path.dirname(__file__)
    
    # filenames is a generator of python files in this directory
    filenames  = (name for name in os.listdir(directory) if name.endswith('.pyc'))
    #basenames_extensions is a generator of (basename, ext) tuples for the python files
    # so basename is the filename without '.py' (and no path either)
    basenames_extensions = (os.path.splitext(name) for name in filenames)

    # modules is a generator of modules represented by the python files
    # `__package__` is 'cameraobscura.attenuators'
    modules =  (importlib.import_module('.'.join((__package__, base)))
                for base, extension in basenames_extensions)

    for module in modules:
        members = inspect.getmembers(module, predicate=is_attenuator)
        # members is a list of all Attenuator sub-classes in the module
        # so it could possibly have more than one member
        for member in members:
            name, definition = member
            # the AdeptNCustomPath is returning an incorrect name for some reason
            # so the __name__ variable is used instead of the returned 'name'
            definitions[definition.__name__.lower()] = definition
    return definitions
# end get_definitions

class AttenuatorBuilder(object):
    """
    Builds attenuator objects
    """
    _attenuators = {}
    definitions = get_definitions()
    
    @classmethod
    def GetAttenuator(cls, attenuator_type, ip_address):
        """
        Check what *type* of attenuator is needed and return an instance
        of that type. Use the collection of already created instances
        to avoid duplication.
        
        :param:
         - `attenuator_type`: Name of class to control attenuator, e.g. "MockAttenuator"
         - `ip_address`: attenuator's IP or hostname

        :return: Attenuator object
        :raise: CameraObscura error if the `attenuator_type` is unknown
        """        
        type_lower = attenuator_type.lower()
        check = (type_lower, ip_address)

        if check not in AttenuatorBuilder._attenuators:
            try:
                new_attenuator = cls.definitions[type_lower](ip_address)
            except KeyError as error:
                print(error)
                raise CameraobscuraError("'{0}' attenuator not implemented (or mis-named)".format(attenuator_type))
            AttenuatorBuilder._attenuators[check] = new_attenuator
        return AttenuatorBuilder._attenuators[check]
# end AttenuatorBuilder
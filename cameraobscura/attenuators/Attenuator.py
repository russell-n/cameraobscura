
# python standard library
from abc import ABCMeta, abstractmethod
import logging

# this package
from cameraobscura import CameraobscuraError

class Attenuator(object):
    """
    Abstract Base Class - should not be instantiated. Instead attenuators
    should be implemented when they are needed, inheriting from this class
    and overriding these methods. (No data or methods are inherited except hostname and logger.)
    """
    __metaclass__ = ABCMeta
    def __init__(self, hostname):
        """
        Attenuator Constructor

        :param:

         - `hostname`: IP address or resolvable network name for attenuator
        """
        # provide a logger to children
        super(Attenuator, self).__init__()
        self._logger = None
        self.hostname = hostname
        return

    @property
    def logger(self):
        """
        :return: A logging object.
        """
        if self._logger is None:
            self._logger = logging.getLogger("{0}.{1}".format(self.__module__,
                                  self.__class__.__name__))
        return self._logger

    @abstractmethod
    def routes(self,route):
        return 

    @abstractmethod
    def getAttenuation(self, routes):
        return 

    @abstractmethod
    def setAttenuation(self, value, routes):
        return 

    @abstractmethod
    def getAttenMax(self, routes):
        return
# end class Attenuator

class AttenuatorError(CameraobscuraError):
    """
    An Exception for fatal attenuator errors
    """
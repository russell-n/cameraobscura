
import logging
import logging.handlers

DOT_JOIN = "{0}.{1}"

class BaseClass(object):
    """
    A base-class to provide logging for all its children
    """
    def __init__(self):
        self._logger = None
        return

    @property
    def logger(self):
        """
        A python Logger.
        """
        if self._logger is None:
            self._logger = logging.getLogger(DOT_JOIN.format(self.__module__,
                                                             self.__class__.__name__))
        return self._logger
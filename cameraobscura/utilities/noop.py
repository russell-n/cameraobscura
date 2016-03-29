
# python standard library
import logging

class NoOp(object):
    """
    A class to do nothing
    """
    def __init__(self, noop_name, *args, **kwargs):
        """
        NoOp constructor. Pass in anything you want, it just gets logged.

        :param:

         - `noop_name`: An identifier used in the logging as the class name
        """
        super(NoOp, self).__init__()
        self._logger = None
        self.noop_name = noop_name
        self.logger.debug("NoOp created for {0}".format(noop_name))
        self.logger.debug("args= {0}".format(args))
        self.logger.debug("kwargs= {0}".format(kwargs))
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


    def __call__(self, *args, **kwargs):
        """
        Does nothing but log arguments
        """
        self.logger.debug("{2} Called with args={0}, kwargs={1}".format(args,
                                                                    kwargs,
                                                                    self.noop_name))
        return

    def __getattr__(self, name):
        """
        Just logs the arguments
        """
        self.logger.debug("'{0}.{1}' called ".format(self.noop_name,
                                                     name))
        return self
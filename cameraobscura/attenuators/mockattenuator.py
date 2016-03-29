
from attenuator import Attenuator

class MockAttenuatorConstants(object):
    """
    a holder of constants (mostly to make testing easier)
    """
    __slots__ = ()
    # class name
    class_name = 'MockAttenuator'
    # methods
    routes = 'routes'
    getAttenuation = 'getAttenuation'
    setAttenuation = 'setAttenuation'
    getAttenMax = 'getAttenMax'

    # arguments
    # there is both a method and common parameter named 'routes'
    value='value'
    route = 'route'
    attenuation_max = 1000

LOG_STRING = "Method: {m} called with arguments: {a}"

class MockAttenuator(Attenuator):
    """
    Concrete implementation that does nothing
    """
    def __init__(self, *args, **kwargs):
        super(MockAttenuator, self).__init__(*args, **kwargs)
        self.attenuation = 0
        return

    def log_call(self, method, **kwargs):
        """
        Logs method calls (info-level)
        """
        self.logger.info(LOG_STRING.format(m=method,
                                           a=kwargs))
        return
    
    def routes(self, route=None):
        self.log_call(MockAttenuatorConstants.routes, route=route)
        return 

    def getAttenuation(self, routes=None):
        self.log_call(MockAttenuatorConstants.getAttenuation,
                      routes=routes)
        return self.attenuation

    def setAttenuation(self, value, routes=None):
        self.log_call(MockAttenuatorConstants.setAttenuation, value=value, routes=routes)
        self.attenuation = value
        return 

    def getAttenMax(self, routes=None):
        self.log_call(MockAttenuatorConstants.getAttenMax, routes=routes)
        return MockAttenuatorConstants.attenuation_max
# end class MockAttenuator
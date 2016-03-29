
# python standard library
import telnetlib
import socket
import time

# this package
from Attenuator import Attenuator, AttenuatorError
from cameraobscura import CameraobscuraError

def handleattenuatorerrors(method,  *args, **kwargs):
    """
    Function to use as a method decorator (expects ``self`` as one of the arguments) to catch connection errors

    Also expects that the object has connection and logger attributes

    :param:

     - `method`: method instance
    """
    def wrapped(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except (socket.error, EOFError) as error:
            message = "{e}: Error with connection to {c}".format(c=self.connection,
                                                                 e=type(error))
            self.logger.error(message)
            raise CameraobscuraError(message)
    return wrapped

defaultPort = 10001  # What TCP port the attenuator's XPort is listening on.
retryWait = 5   # How long to wait before retrying a connection
NEWLINE = '\n'

NUM_CHANNELS, MAX_ATTENUATION, MIN_STEP_SIZE = range(3)
if __name__ == '__builtin__':
    # this should only get printed when creating the documentation
    print("   defaultPort,{0},TCP port attenuator's XPort is listening on".format(defaultPort))
    print("   retryWait,{0},Seconds before retrying connection".format(retryWait))

class WeinschelP(Attenuator):
    """
    Controls Weinschel attenuators over a telnet connection.

    The ports affected by each function are supplied as a list of strings.
    These strings can be port numbers or predefined port groups.
    See the route() method for a list of port groups.

    By default, operations are done on the first group of two ports.
    ** NOTE: may want to supply default ports from init.

    To help with using a persistent telnet session, the _retrytelnet function
    is provided to retry the connection if it fails. This really should only
    be used on writes to the connection.

    If an error occurs then this throws an AttenuatorError exception.

    """
    def __init__(self, *args, **kwargs):
        """
        WeinschelP Constructor

        :param:

         - `hostname`: Device IP or resolvable hostname
        """
        super(WeinschelP, self).__init__(*args, **kwargs)
        self._connection = None

        self._device_info = None
        self._numChannels = None
        self._maxAttenuation = None
        self._minStepSize = None
        self._routetable = None
        return

    @property
    def connection(self):
        """
        A telnet connection to the attenuator

        :return: opened connection 
        """
        if self._connection is None:
            self._connection = telnetlib.Telnet(self.hostname, defaultPort)
        return self._connection

    @property
    def device_info(self):
        """
        This was created to get rid of the _getDeviceInfo side-effect in the constructor
        :return: triple of (<number of channels>, <max attenuation>, <min step size>)
        """
        if self._device_info is None:
            self._device_info = self._getDeviceInfo()
        return self._device_info

    @property
    def numChannels(self):
        """
        :return: number of channels (from device_info)
        """
        if self._numChannels is None:
            self._numChannels = self.device_info[NUM_CHANNELS]
        return self._numChannels

    @property
    def maxAttenuation(self):
        """
        :return: maximum allowed attenuation
        """
        if self._maxAttenuation is None:
            self._maxAttenuation = self.device_info[MAX_ATTENUATION]
        return self._maxAttenuation

    @property
    def minStepSize(self):
        """
        :return: minimum allowed step-size
        """
        if self._minStepSize is None:
            self._minStepSize = self.device_info[MIN_STEP_SIZE]
        return self._minStepSize

    @property
    def routetable(self):
        """
        Builds the predefined list of routes based on the
        number of channels a device has.

        Right now this includes a list of individual ports, and
        groups of even numbers of ports up to 8.

        e.g. a four-port attenuator would have the following routes
        "1" -> [1]
        "2" -> [2]
        "3" -> [3]
        "4" -> [4]
        "2x1" -> [1,2]
        "2x2" -> [3,4]
        "4x1" -> [1,2,3,4]

        :return: output of buildRouteTable (whatever that is)
        """
        if self._routetable is None:
            self._routetable = {}

            for cn in range(1, self.numChannels + 1):
                self._routetable[str(cn)] = [cn]
            
            for n in range(2, 10, 2):
                # cn and nbys? are we paying for variable names by the letter?
                nbys = [range(1, self.numChannels + 1)[i:i + n] for i in range(0, self.numChannels, n)]
                groupNum = 1
                for cns in nbys:
                    if len(cns) == n:
                        self._routetable["{}x{}".format(n, groupNum)] = cns
                        groupNum += 1
        return self._routetable

    def __del__(self):
        """
        Destructor

        :postcondition: self._connection is closed
        """
        self.close()
        return

    def routes(self, route=""):
        """
        Handles predefined routes in the device.
        At the moment the list of routes is just a list of channels.

        Without an argument returns the list of routes and what channel
        they are mapped to.

        With an argument returns the channel list for a named route.

        :param:

         - `route`: A key for the self.routetable dictionary (side-effect of buildRouteTable)
         
        :return: entire route table or route within routetable
        :raise: AttenuatorError if route given but not in the route-table 
        """
        if len(route) == 0:
            return self.routetable

        try:
            return self.routetable[route]
        except KeyError as error:
            self.logger.error(error)
            raise AttenuatorError("Route {0} does not exist.".format(route))

    def setAttenuation(self, attenuation, routes=["1","2","3","4"]):
        """
        Sets the attenuation of a set of routes.

        :param:

         - `attenuation`: the attenuation value to set
         - `routes`: list of routes (see _portsAffected)

        :returns: float - the attenuation the routes have been set to.
        :raise: AttenuationError for mismatched values of failure to set attenuation
        """
        ports = self._portsAffected(routes)
        cmd = "; ".join(map(lambda p: "CHAN {}; ATTN {}\n".format(p, attenuation), ports))
        self._retry_write(cmd)

        attns = self.getAttenuation(routes)

        if attns.count(attns[0]) != len(attns):
            raise AttenuatorError("Mismatched values ({})".format(attns))

        if attns[0] != attenuation:
            raise AttenuatorError("Attenuator did not set to {}, instead is at {}".format(attenuation,
                                                                                          attns[0]))
        return attns[0]

    @handleattenuatorerrors
    def getAttenuation(self, routes=["2x1"]):
        """
        Gets the attenuation of a set of routes.

        :param:

         - `routes`: list of 'routes' (see _buildRouteTable)

        :rtype: Float
        :returns: The attenuation of each route.
        :raise: AttenuationError on socket error, end-of file, wrong count of routes returned
        """
        allattns = []

        for route in routes:
            ports = self._portsAffected([route])
            
            # cmd is a string of ';' separated command strings
            # cmd = '; '.join(["CHAN {c}; ATTN?".format(c=p) for p in ports])            
            cmd = "; ".join(map(lambda p: "CHAN {}; ATTN?\n".format(p), ports))
            self._retry_write(cmd)
            matchText = self.connection.read_until(NEWLINE)

            attns = map(float, matchText.split(";"))
            if attns.count(attns[0]) != len(attns):
                raise AttenuatorError("Mismatched values ({}) on route {}".format(attns, route))

            allattns.append(float(attns[0]))

        if len(allattns) != len(routes):
            raise AttenuatorError("Error in number of routes returned ({})".format(allattns))
        return allattns

    def getAttenMax(self, port=0):
        """
        A getter method (!) to get _maxAttenuation
        """
        return self.maxAttenuation

    def _portsAffected(self, routes):
        """
        Given a list of routes this returns the set of ports that the
        routes cover.

        :param:

         - `routes`: list of routes (see buildRouteTable)

        :returns: A list of (integer) ports.
        """
        portList = map(self.routes, routes)
        return list(set(sum(portList, [])))

    @handleattenuatorerrors
    def _getDeviceInfo(self):
        """
        Gets the number of channels, maximum attenuation, and minimum step size
        for the device.

        The number of channels is found by switching to increasingly large channel
        numbers until an error is reported.

        The step size is determined after a device reset. Per the user manual step sizes
        are set to the device resolution after a reset.

        The maximum attenuation is also found by reading the attenuation of a channel
        after device reset. This is an empirical observation, so this assumption should
        be checked with Weinschel.

        :returns: (int,float,float) Number of channels, Maximum attenuation, Minimum step size
        :raise: AttenuatorError on socket error or end-of-file error
        """
        currentChannel = 0
        channelExists = True

        while channelExists:
            currentChannel += 1
            self.connection.write("*CLS; CHAN {}; *ESR?\n".format(currentChannel))
            matchText = self.connection.read_until(NEWLINE)
            self.connection.write("*CLS\n")

            if int(matchText) & 32:
                channelExists = False

        self.connection.write("*RST; *WAI; CHAN 1; STEPSIZE?\n")
        minStep = self.connection.read_until(NEWLINE)

        self.connection.write( "ATTN?\n")
        maxAtten = self.connection.read_until(NEWLINE)
        return (currentChannel - 1), float(maxAtten), float(minStep)

    def _retry_write(self, param):
        """
        Writes the `param` to the telnet connection.
        If the function fails then sleep for retryWait seconds and try it
        again. Subsequent failure causes an exception.

        :param:

        - `param`: string to write to telnet connection
        """
        try:
            self.connection.write(param)
        except AttenuatorError as error:
            self.logger.error(error)
            self.logger.info("closing the telnet connection")
            self.close()
            self.logger.info("Sleeping for {0} seconds.".format(retryWait))
            time.sleep(retryWait)
            self.connection.write(param)
        return 

    def close(self):
        """
        Closes the telnet connection and sets it to  None

        :postcondition: If connection was open it is closed and set to None
        """
        if self._connection is not None:
            self._connection.close()
            self._connection = None
        return
# end WeinschelP
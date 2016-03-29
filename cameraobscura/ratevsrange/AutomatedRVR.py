
"""
Using new Attenuator Library to automate
Attenuation steps.

Author: Russell Miller
04/06/2011
"""

# python standard library
import time
import shutil
import os
import re
import ConfigParser
import socket
import logging

# third-party
from theape.infrastructure.composite import TheComposite

# this package
from cameraobscura import BOLD, RESET, BLUE, RED
from cameraobscura import NoOp
from cameraobscura import CameraobscuraError
from cameraobscura.commands.iperf.Iperf import Iperf
from cameraobscura.commands.iperf.iperfsettings import IperfConstants
import cameraobscura.hosts.host
from cameraobscura.attenuators.AttenuatorFactory import AttenuatorFactory
from cameraobscura.attenuators.Attenuator import AttenuatorError

from cameraobscura.utilities.configurationadapter import ConfigurationAdapter
from rvrconfiguration import RVRConfiguration, TrafficEnum
from stepiterator import StepIterator
from cameraobscura.utilities.query import QueryBuilder, Query

from cameraobscura.utilities.dump import TheDump
from cameraobscura.commands.ping.pingbuilder import PingBuilder

class AutomatedRVREnum(object):
    """
    A holder of special constants for the Test method
    """
    __slots__ = ()
    upstream = IperfConstants.up
    downstream = IperfConstants.down
    
    # for the query
    attenuation = 'attenuation'
    dut_upstream = "DUT TX (upstream)"
    server_upstream = "Server RX (upstream)"
    dut_downstream = 'DUT RX (downstream)'
    server_downstream = 'Server TX (downstream)'

FOLDER_TIMESTAMP = "_%Y_%m_%d_%a_%H:%M"
FOUR_DECIMALS = '{0:0.4f}'
DOT_JOIN = "{0}.{1}"
RECOVERY_TIME = 20
BOLD_RED = BOLD + RED
BOLD_BLUE = BOLD + BLUE
BOLD_RESET = BOLD + "{0}" + RESET
BOLD_BLUE_RESET = BOLD_BLUE + "{0}" + RESET
BOLD_RED_RESET = BOLD_RED + "{0}" + RESET
ZERO = 0
WRITEABLE = 'w'
DIRECTION_MAP = {TrafficEnum.upstream:(AutomatedRVREnum.upstream,),
                 TrafficEnum.both:(AutomatedRVREnum.upstream,
                                   AutomatedRVREnum.downstream),
                 TrafficEnum.downstream:(AutomatedRVREnum.downstream,)}

# for the data-file headers
IPERF_FIELDS = {AutomatedRVREnum.upstream:
                [AutomatedRVREnum.attenuation,
                 AutomatedRVREnum.dut_upstream,
                 AutomatedRVREnum.server_upstream],
                AutomatedRVREnum.downstream:
                [AutomatedRVREnum.attenuation,
                 AutomatedRVREnum.dut_downstream,
                 AutomatedRVREnum.server_downstream]}

class Test(object):
    """
    Test object. Specific steps of each rate vs. range test.
    This should be loaded by its TestManager and
    that should be loaded by the QueueManager.
    """
    def __init__(self, config):
        """
        Start loggers, set up SSH connections and attenuator.

        :param:
        
         - `config`: ConfigParser object or ConfigurationAdapter -- holds all settings values
        """
        super(Test, self).__init__()
        self._logger = None
        self._configuration = None
        #parameter kept as 'config' for backwards compatibility
        self.configuration = config

        self._result_location = None
        self._ping = None

        self._maximum_attenuation = None
        
        self._dut = None
        self._server = None        
        self._iperf = None
        self._attenuator = None
        self._attenuations = None

        self._dump = None
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

    @property
    def ping(self):
        """
        a Ping object to ping from dut to traffic server
        """
        if self._ping is None and self.configuration.ping is not None:
            if self.configuration.ping.target is None:
                # take the server as the default
                self.configuration.ping.target = self.server.TestInterface
            self._ping = PingBuilder(connection=self.dut,
                                     configuration=self.configuration.ping).product
        return self._ping

    @property
    def attenuations(self):
        """
        An iterator of attenuations
        """
        if self._attenuations is None:
            self._attenuations = StepIterator(start=self.configuration.attenuation.start,
                                              stop=self.maximum_attenuation,
                                              step_sizes=self.configuration.attenuation.step_sizes,
                                              step_change_thresholds=self.configuration.attenuation.step_change_thresholds,
                                              step_list=self.configuration.attenuation.step_list,
                                              reversal_limit=self.configuration.attenuation.reversal_limit)
            self.logger.debug('step iterator built with "{0}"'.format(self._attenuations))
            self._attenuations.check_rep()
        return self._attenuations
        
    @property
    def maximum_attenuation(self):
        """
        The stopping condition for the RunTest while loop

        Uses the minimum of RVRConfiguration.maximum_attenuation and attenuator.getAttenMax()

        :return: integer value for largest attenuation to run
        """
        if self._maximum_attenuation is None:
            self._maximum_attenuation = min(self.configuration.attenuation.stop,
                                            self.attenuator.getAttenMax())
        return self._maximum_attenuation
    
    @property
    def configuration(self):
        """
        an RVRConfiguration

        :return: RVRConfiguration 
        """
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        """
        Creates an RVRConfiguration out of the configuration

        :param:

         - `configuration`: a ConfigParser, ConfigurationAdapter, or RVRConfiguration

        :postcondition: self._configuration is an RVRConfiguration
        """
        if isinstance(configuration, RVRConfiguration):
            self._configuration = configuration
        elif isinstance(configuration, ConfigurationAdapter):
            self._configuration = RVRConfiguration(configuration)
        elif isinstance(configuration, ConfigParser.ConfigParser):
            configuration = ConfigurationAdapter(configuration)
            self._configuration = RVRConfiguration(configuration)
        else:
            # allow duck-typed substitutes
            self._configuration = configuration
        return
                                   
    @property
    def dut(self):
        """
        create dut for iperf

        :return: HostSSH Connected to the DUT
        """
        if self._dut is None:
            self._dut = cameraobscura.hosts.host.TheHost(hostname=self.configuration.dut.control_ip,
                                                      username=self.configuration.dut.username,
                                                      password=self.configuration.dut.password,
                                                      test_interface=self.configuration.dut.test_ip,
                                                      prefix=self.configuration.dut.prefix,
                                                      timeout=self.configuration.dut.timeout,
                                                      operating_system=self.configuration.dut.operating_system,
                                                      connection_type=self.configuration.dut.connection_type,
                                                      **self.configuration.dut.kwargs)
        return self._dut

    @property
    def server(self):
        """
        Connection to the server

        :return: HostSSH connected to the server's control ip
        """
        if self._server is None:
            self._server = cameraobscura.hosts.host.TheHost(hostname=self.configuration.server.control_ip,
                                                         username=self.configuration.server.username,
                                                         password=self.configuration.server.password,
                                                         test_interface=self.configuration.server.test_ip,
                                                         prefix=self.configuration.server.prefix,
                                                         timeout=self.configuration.server.timeout,
                                                         operating_system=self.configuration.server.operating_system,
                                                         connection_type=self.configuration.server.connection_type,
                                                         **self.configuration.server.kwargs)
        return self._server

    @property
    def iperf(self):
        """
        An iperf runner

        :return: built Iperf instance
        """
        if self._iperf is None:
            self._iperf = Iperf(dut=self.dut,
                                traffic_server=self.server,
                client_settings=self.configuration.traffic.client_settings,
                server_settings=self.configuration.traffic.server_settings)
        return self._iperf
            
    @property
    def attenuator(self):
        """
        The attenuator
        """
        if self._attenuator is None:
            self.logger.info("Initializing attenuator.")
            self._attenuator = AttenuatorFactory.GetAttenuator(self.configuration.attenuation.name,
                                                               self.configuration.attenuation.control_ip)
        return self._attenuator

    @property
    def result_location(self):
        """
        Name of the folder with a time stamp added

        :return: folder name
        """
        if self._result_location is None:
            self._result_location = self.configuration.other.result_location
            if "{timestamp}" in self.result_location:
                self._result_location.format(timestamp=time.strftime(FOLDER_TIMESTAMP))
            if not os.path.isdir(self._result_location):
                os.makedirs(self._result_location)
        return self._result_location

    @property
    def dump(self):
        """
        Creates a Composite with command dumps to call after the testing is done

        :return: Dump Composite or NoOp if configuration.dump was not created
        """
        if self._dump is None:
            if self.configuration.dump is not None:
                components = []
                path = os.path.join(self.result_location, 'dump')
                if not os.path.isdir(path):
                    os.makedirs(path)
                for index, field in enumerate(self.configuration.dump.fields):
                    filename = os.path.join(path, "{0}.txt".format(field))
                    components.append(TheDump(command=self.configuration.dump.commands[index],
                                              connection=self.dut,
                                              identifier=field,
                                              filename=filename,
                                              timeout=self.configuration.dump.timeout)
                    )
                self._dump = TheComposite(components=components)
            else:
                self._dump = NoOp(noop_name='TheDump')
        return self._dump

    def save_configuration(self, filename='automated_rvr.ini'):
        """
        Saves a copy of the configuration to a file in the results-location.

        :param:

         -`filename`: name (without folder path) to use for the file
        """
        out_name = os.path.join(self.result_location, filename)
        with open(out_name, WRITEABLE) as writeable_file:
            self.configuration.configuration.write(writeable_file)
        return

    def connected(self, raise_error=False):
        """
        If the user didn't set the [attenuation] ping option to false, client pings server

        :param:

         - `raise_error`: If True, raise exception
        :return: True if pinged within timeout, False otherwise

        :raise: CameraobscuraError if not connected and raise_error
        """
        if not self.ping:
            # not testing -- vacuously True
            self.logger.info("'ping' option not set, not testing connection")
            return True

        self.logger.info(BOLD_BLUE_RESET.format("** Checking DUT --> Server Connection **" ))
        try:
            success = self.ping()
        except CameraobscuraError as error:
            success = False
        
        if not success:
            msg = BOLD_RED_RESET.format("Connection between DUT {0} and server {1} failed".format(self.dut,
                                                                                                  self.server.TestInterface))
            self.logger.error(msg)
        if not success and raise_error:
            raise CameraobscuraError("Connection Between DUT and Server not established")
        return success

    def get_querier(self, direction):
        """
        Creates a Query object with an file based on filename

        :param:

         - `direction`: token to add to filename

        :return: Query object to query the dut or NoOp if configuration.query was not created
        """
        path = os.path.join(self.result_location, 'compiled_data')
        if self.configuration.query is None:
            filename = 'data.csv'
            new_query = Query(output_filename=None,
                              fields=IPERF_FIELDS[direction],
                              commands={})
        else:
            filename = self.configuration.query.filename
            new_query = QueryBuilder(connection=self.dut,
                                     configuration=self.configuration.query).product
            # add attenuation and iperf data columns
            # this turns out to be a dangerous point --
            # the QueryBuilder is getting the actual lists from the configuration
            # not copies of the lists. so it's a new query, but not a new 'fields' list
            if AutomatedRVREnum.attenuation not in new_query.fields:
                    new_query.fields.extend(IPERF_FIELDS[direction])
            
        if not os.path.isdir(path):
            os.makedirs(path)
        filename = os.path.join(path,
                                "{0}_{1}".format(direction,
                                filename))
            
        # an ugly bit added to let the user add something to the filename
        new_query.output_filename = filename
            
        try:
            new_query.check_rep()
        except AssertionError as error:
            self.logger.error(error)
            raise CameraobscuraError("Something's wrong with the Query configuration: {0}".format(new_query))
        return new_query
        
    def __call__(self):
        """
        A wrapper for RunTest to do up-link or down-link tests, or both.
        If doing both it attempts to allow lag time for reconnecting between
        the two.

        Once up-link/down-link test(s) is/are complete, uses the IperfParse
        library to create the final result file.

        :return: (bool, str) Success/Failure and possibly an error message.
        :raise: CameraobscuraError if Dut can't ping server
        """
        self.save_configuration()
        directions = DIRECTION_MAP[self.configuration.traffic.direction]
        # log the iperf version
        for connection in (self.dut, self.server):
            self.logger.info("{0} --  {1}".format(connection, self.iperf.version(connection)))
            
        for not_first_test, direction in enumerate(directions):
            print
            self.attenuations.reset()
            
            # *** this next call is where most of the interesting things happen
            self.RunTest(direction)
            # ***
            
            if 0 < not_first_test < len(directions) - 1:
                # take a break then check the connection
                self.logger.info(BOLD_BLUE_RESET.format("Sleeping for {0} seconds to let the system"
                                                        " recover it's state.".format(self.configuration.other.recovery_time)))
                time.sleep(self.configuration.other.recovery_time)
                self.connected(raise_error=True)

        # dumps whatever was configured to dump
        self.logger.info(BOLD_BLUE_RESET.format("**** Dumping Device Info ****"))
        self.dump()
        # close the clients so the files will be closed
        self.dut.close()
        self.server.close()
        
        # parse the test results for the average throughput
        traffic_type = 'tcp'
        if self.iperf.udp:
            traffic_type = 'udp'
        path = os.path.join(self.result_location, 'raw_iperf')

        # uplink and/or downlink complete
        self.logger.info(BOLD_RESET.format("**** Test completed ****"))
        return True, "Test completed."

    def RunTest(self, direction):
        """
        Each test will go through these steps:

         - Set initial attenuation
         - Go into the control loop (see below)
         - Exit control loop when attenuation reaches max value
         - Set attenuation to zero

        The control loop:

         - Verify connection with a ping test
         - Run iperf traffic for specified duration
         - Save Results
         - Increase Attenuation

        :param:

         - `direction`: direction for the traffic (up or down)
        """
        # this data stuff needs to be separated out, the method is way too long
        # setup csv
        save_device_data = self.get_querier(direction)
        if direction == AutomatedRVREnum.downstream:
            # Server -> DUT
            fields = (AutomatedRVREnum.attenuation,
                      AutomatedRVREnum.dut_downstream,
                      AutomatedRVREnum.server_downstream)
        else:
            # DUT -> Server
            fields = (AutomatedRVREnum.attenuation,
                      AutomatedRVREnum.dut_upstream,
                      AutomatedRVREnum.server_upstream)
            
        self.logger.info(BOLD_RESET.format("**** Beginning {0} Rate vs Range Test ****"
                              "".format(direction.capitalize())))

        lost_connection = False
        for attenuation_index, attenuation in enumerate(self.attenuations):
            print()
            self.logger.info(BOLD_BLUE_RESET.format("*** Setting Attenuation to {0} ***".format(attenuation)))
            self.attenuator.setAttenuation(attenuation)
            if lost_connection:
                lost_connection = False
                timeout = self.configuration.other.recovery_time
                self.logger.info("Sleeping for {0} seconds to recover".format(timeout))
                time.sleep(timeout)
            # Verify there is a connection between the dut and server
            if not self.connected(raise_error=attenuation==self.attenuations.start):
                # aaiiiieeeeeee!
                lost_connection = True
                if not self.attenuations.reverse():
                    message = "Stopping {0} test".format(direction)
                else:
                    message = "Reversed Attenuation Direction"
                self.logger.info(BOLD_RED_RESET.format("**** Lost connection between dut and server --"
                                                       " {0} ****".format(message)))
                continue

            self.logger.info(BOLD_BLUE_RESET.format( "*** Running the Iperf Session ***"))
            path = os.path.join(self.result_location, 'raw_iperf')
            if not os.path.isdir(path):
                os.makedirs(path)
            filename = os.path.join(path, "attenuation_{a:03}_dut_{d}{t}.iperf".format(a=attenuation,
                                                                                       d="{0}@{1}".format(self.dut.username,
                                                                                                          self.dut.hostname),
                                                                                                          t=time.strftime(FOLDER_TIMESTAMP)))
            try:
                self.iperf(direction, filename)                
                self.logger.info(BOLD_BLUE_RESET.format("*** Saving the Device Data ***"))
                # fields are attenuation, dut data, server data
                if direction == AutomatedRVREnum.downstream:
                    # DUT (server) <- TPC (client)
                    data = (attenuation, self.iperf.server_summary,
                            self.iperf.client_summary)
                else:
                    # DUT (client) -> TPC (server)
                    data = (attenuation, self.iperf.client_summary,
                            self.iperf.server_summary)
                # fields defined at the top of this method

                save_device_data(dict(zip(fields, data)))

            except socket.error as error:
                self.logger.info(error)
                if self.attenuations.reverse():
                    self.logger.info('socket error reached -- reversing attenuation direction')
                lost_connection = True                

        # Putting attenuation at zero, to help the next test... :)
        # Why is the AttenuatorError not trapped here?
        self.attenuator.setAttenuation(ZERO)

        msg = "Completed {0} test.".format(direction)
        self.logger.info(BOLD_RESET.format("**** " + msg + " ****"))
        return True, msg

    def reset(self):
        """
        Sets some properties back to None (but not the configuration)
        """
        self.logger.debug("resetting the properties to None")
        self._attenuations = None
        self._maximum_attenuation = None
        self._ping = None
        self._dut = None
        self._server = None
        self._attenuator = None
        self._dump = None
        self._query = None
        return
# end Class Test

from __future__ import print_function

# python standard library
import sys
import abc
from abc import abstractproperty, abstractmethod
from types import IntType
import textwrap
import ConfigParser
import logging

# this package
from cameraobscura import CameraobscuraError

from cameraobscura.commands.iperf.Iperf import IperfConfiguration
from cameraobscura.commands.iperf.iperfsettings import IperfConstants
from cameraobscura.commands.iperf.iperfsettings import  IperfClientSettings, IperfServerSettings

from cameraobscura.hosts.host import HostConfiguration

from cameraobscura.attenuators.AttenuatorFactory import get_definitions
attenuation_definitions = get_definitions()

from cameraobscura.utilities.configurationadapter import ConfigurationError

from cameraobscura.common.baseconfiguration import BaseConfiguration
from cameraobscura.utilities.query import QueryEnum, QueryConfiguration
from cameraobscura.utilities.dump import DumpConstants, DumpConfiguration

from cameraobscura.commands.ping.pingconfiguration import PingConfigurationConstants, PingConfiguration

UNDERSCORE = '_'
ONE = 1
FIRST = 0
LAST = -1

class AttenuationEnum(object):
    """
    Constants for the [attenuation] section
    """
    __slots__ = ()
    section = 'attenuation'

    # options
    stop = 'stop'
    name ='name'
    control_ip = 'control_ip'
    interface = 'interface'
    start = 'start'
    step_sizes = 'step_sizes'
    step = 'step'
    step_list = 'step_list'
    reversal_limit = 'reversal_limit'
    step_change_thresholds = 'step_change_thresholds'
    stepchange = 'stepchange'
    
    # defaults
    default_attenuator = 'WeinschelP'
    default_start = 0
    default_reversal_limit = 0
    default_stop = sys.maxint
    default_step_sizes = [1]

    # constants
    delimiter = ' '

    
ATTENUATION_LOG_STRING = '[attenuation] {0} = {1}'

class DutEnum(object):
    """
    Holder of constants for the DUT
    """
    __slots__ = ()
    section = 'dut'

class ServerEnum(object):
    """
    Holder of constants for the server
    """
    __slots__ = ()
    section = 'server'

class OtherEnum(object):
    """
    Holder of constants for the other section
    """
    __slots__ = ()
    section = 'other'

    # options
    result_location = 'result_location'
    test_name = 'test_name'
    ping ='ping'
    repetitions = 'repetitions'
    recovery_time = 'recovery_time'

    #defaults
    default_result_location = 'output_folder'
    default_test_name = 'rate_vs_range'
    default_repetitions = 1
    default_recovery_time = 10

class TrafficEnum(object):
    """
    A holder of iperf traffic constant    
    """
    __slots__ = ()
    section = 'iperf'
    old_section = 'traffic'

    # directions
    upstream = IperfConstants.up
    downstream = IperfConstants.down
    both = 'both'

    # options
    direction = 'direction'

    # defaults
    default_direction = both

    false = 'no false off'.split()

def optionalsection(method,  *args, **kwargs):
    """
    function to use as a method decorator (expects ``self`` as one of the arguments)

    Also expects that the object has logger attributes

    :param:

     - `method`: method instance
    """
    def wrapped(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except ConfigParser.NoSectionError as error:
            self.logger.debug(error)
    return wrapped

class RVRConfiguration(object):
    """
    A holder of the RVR Configuration
    """
    def __init__(self, configuration):
        """
        RVRConfiguration constructor

        :param:

         - `configuration`: a ConfigurationAdapter with the configuration
        """
        super(RVRConfiguration, self).__init__()
        self.configuration = configuration
        self._attenuation = None
        self._other = None
        
        self._dut = None
        self._server = None       

        self._traffic = None
        self._query = None

        self._dump = None
        self._ping = None
        self._logger = None
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
    def attenuation(self):
        """
        An Attenuation Section Configuration
        """
        if self._attenuation is None:
            try:
                self._attenuation = AttenuationConfiguration(configuration=self.configuration)
                self.logger.debug(str(self._attenuation))
                self._attenuation.check_rep()
            except ConfigurationError as error:
                print(self._attenuation.example)
                raise CameraobscuraError(error)
        return self._attenuation

    @property
    def dump(self):
        """
        A dump-composite configuration

        :return: DumpConfiguration or None
        """
        if self._dump is None:
            if self.configuration.has_section(DumpConstants.section):
                self._dump = DumpConfiguration(configuration=self.configuration)
                self.logger.debug(str(self._dump))
                self._dump.check_rep()
        return self._dump

    @property
    def ping(self):
        """
        A ping configuration
        """
        if self._ping is None:
            if self.configuration.has_section(PingConfigurationConstants.section):
                self._ping =PingConfiguration(configuration=self.configuration)
                self.logger.debug(str(self._ping))
                self._ping.check_rep()
        return self._ping
    
    @property
    def query(self):
        """
        A Query configuration

        :return: QueryConfiguration or None if not given
        """
        if self._query is None:
            if self.configuration.has_section(QueryEnum.section):
                self._query = QueryConfiguration(configuration=self.configuration)
                self.logger.debug(str(self._query))
                self._query.check_rep()
        return self._query

    @property
    def dut(self):
        """
        The client's configuration
        """
        if self._dut is None:
            self._dut = HostConfiguration(configuration=self.configuration,
                                            section=DutEnum.section)
            self.logger.debug(str(self._dut))
            self._dut.check_rep()
        return self._dut

    @property
    def server(self):
        """
        The server's configuration
        """
        if self._server is None:
            self._server = HostConfiguration(configuration=self.configuration,
                                               section=ServerEnum.section)
            self.logger.debug(str(self._server))
            self._server.check_rep()
        return self._server
    
    @property
    def other(self):
        """
        Gets the Other Configuration
        """
        if self._other is None:
            self._other = OtherConfiguration(configuration=self.configuration)
            self.logger.debug(str(self._other))
            self._other.check_rep()
        return self._other

    @property
    def traffic(self):
        """
        The Traffic Configuration
        """
        if self._traffic is None:
            self._traffic = IperfConfiguration(configuration=self.configuration)
            # a temporary kludge while I figure out where it should fail
            self._traffic.client_settings.server = "Not set"

            self.logger.debug(str(self._traffic))
            self._traffic.check_rep()
            
            # so it will fail if no one sets it later
            self._traffic.client_settings.server = None
        return self._traffic
    
    def reset(self):
        """
        Resets the attributes to None
        """
        self.attenuation.reset()
        self.dut.reset()
        self.server.reset()
        self.other.reset()
        self.traffic.reset()
        return
# end class RVRConfiguration

class AttenuationConfiguration(BaseConfiguration):
    """
    Configuration for the Attenuation settings
    """
    def __init__(self, *args, **kwargs):
        """
        AttenuationConfiguration constructor

        :param:

         - `configuration`: a loaded configuration adapter
        """
        super(AttenuationConfiguration, self).__init__(*args, **kwargs)
        self._stop = None
        self._name = None
        self._start  = None
        self._control_ip = None
        self._step_sizes = None
        self._step_change_thresholds = False
        self._step_list = None
        self._reversal_limit = None        
        return

    @property
    def example(self):
        """
        An example attenuation section
        """
        if self._example is None:
            self._example = textwrap.dedent("""
            [{section}]
            # if an option is commented out it has the default setting you see

            # 'start' is the attenuation value to use when the testing starts
            
            #start = {start}
            
            # 'stop' is the maximum attenuation to try before stopping
            
            #stop = {stop}

            # 'name' is the name of the attenuator
            # not case-sensitive, but spelling counts
            # valid names : {attenuators}
            
            #name = {name}

            # 'control_ip' is the address of the attenuator
            control_ip = 192.168.10.53

            # 'step_sizes' is a space-separated list of step-sizes
            # (each attenuation increases by the current step-size at each repetition)
            
            #step_sizes = {step_sizes}

            # 'step_change_thresholds' is a space-separated list of thresholds which 
            # when reached trigger a change to the next 'step-size'
            # there should always be one less threshold than step-sizes
            # if you don't want to change, comment out or remove the line
            
            #step_change_thresholds =

            # as an example, the next two lines would cause
            # the attenuation to increase by 1 until 10 is reached
            # then it will increase by 5 until 100 then it will increase by 10
            # until the end of the test
            
            # step_sizes = 1 5 10
            # step_change_thresholds = 10 100

            # `reversal_limit` is the maximum number of times to reverse directions
            # reversal_limit = {reversals}

            # `step_list` a list of attenuations to use instead of calculating a range
            # this overrides step_sizes, start, stop, etc.
            # e.g. to run only attenuations 10, 20, 30,:
            # step_list = 10 20 30 
            # step_list = 
            """.format(section=self.section,
                       start=AttenuationEnum.default_start,
                       attenuators=','.join(attenuation_definitions.keys()),
                stop=AttenuationEnum.default_stop,
                step_sizes = AttenuationEnum.default_step_sizes,
                name=AttenuationEnum.default_attenuator,
                reversals=AttenuationEnum.default_reversal_limit))
        return self._example

    @property
    def section(self):
        """
        The section name in the configuration file [attenuation]
        """
        if self._section is None:
            self._section = AttenuationEnum.section
        return self._section
    
    @property
    def stop(self):
        """
        Gets the maximum attenuation from the config-file

        Instead of returning None, returns sys.maxint so users can use min()
        to compare this and attenuator's given maximum attenuation

        :section: attenuator
        :option: stop
        :return: integer or sys.maxint
        """
        if self._stop is None:
            self._stop = self.configuration.getint(section=self.section,
                                                   option=AttenuationEnum.stop,
                                                   optional=True,
                                                   default=AttenuationEnum.default_stop)
            self.logger.debug(ATTENUATION_LOG_STRING.format('stop', self._stop))
        return self._stop

    @property
    def step_list(self):
        """
        Gets a list of steps to take

        :return: list of ints or None
        """
        if self._step_list is None:
            self._step_list = self.configuration.getlist(section=self.section,
                                                         option=AttenuationEnum.step_list,
                                                         optional=True,
                                                         converter=int)
        return self._step_list

    @property
    def reversal_limit(self):
        """
        number of times to change attenuation direction
        """
        if self._reversal_limit is None:
            self._reversal_limit = self.configuration.getint(section=self.section,
                                                             option=AttenuationEnum.reversal_limit,
                                                             optional=True,
                                                             default=AttenuationEnum.default_reversal_limit)
        return self._reversal_limit
    
    @property
    def name(self):
        """
        Gets the name of the Attenuator for the AttenuatorFactory
        """
        if self._name is None:
            self._name = self.configuration.get(section=self.section,
                                                option=AttenuationEnum.name,
                                                optional=True,
                                                default=AttenuationEnum.default_attenuator)
            self.logger.debug(ATTENUATION_LOG_STRING.format('name', self._name))
        return self._name

    @property
    def control_ip(self):
        """
        The old option was `interface` so it will try that if `control_ip` is missing.

        :return: hostname of the attenuator
        """
        if self._control_ip is None:
            self._control_ip = self.configuration.get(section=self.section,
                                                      option=AttenuationEnum.control_ip,
                                                      optional=True)
            if self._control_ip is None:
                self._control_ip = self.configuration.get(section=self.section,
                                                          option=AttenuationEnum.interface)
            self.logger.debug(ATTENUATION_LOG_STRING.format('control_ip', self._control_ip))
        return self._control_ip

    @property
    def start(self):
        """
        The starting attenuation value
        
        :section: attenuation
        :option: start
        :return: integer attenuation start
        :default: 0
        """
        if self._start is None:
            self._start = self.configuration.getint(section=self.section,
                                                    option=AttenuationEnum.start,
                                                    optional=True,
                                                    default=AttenuationEnum.default_start)
            self.logger.debug(ATTENUATION_LOG_STRING.format('start', self._start))
        return self._start

    @property
    def step_sizes(self):
        """
        The amounts to increase the attenuation with each pass.

        :return: list of integers
        :default: [1]
        """
        if self._step_sizes is None:
            self._step_sizes = self.configuration.getlist(section=self.section,
                                                          option=AttenuationEnum.step_sizes,
                                                          delimiter=AttenuationEnum.delimiter,
                                                          converter=int,
                                                          optional=True)
            # handle the legacy option
            if self._step_sizes is None:
                self._step_sizes = self.configuration.getlist(section=self.section,
                                                              option=AttenuationEnum.step,
                                                              delimiter=AttenuationEnum.delimiter,
                                                              optional=True,
                                                              converter=int,
                                                              default=AttenuationEnum.default_step_sizes)
            self.logger.debug(ATTENUATION_LOG_STRING.format('step_sizes', self._step_sizes))
        return self._step_sizes

    @property
    def step_change_thresholds(self):
        """
        The thresholds which if exceeded triggers a change in step-size

        :return: list of integer thresholds or None (the default)
        """
        # this uses False so it won't query the configuration repeatedly
        if self._step_change_thresholds is False:
            self._step_change_thresholds = self.configuration.getlist(section=self.section,
                                                                      option=AttenuationEnum.step_change_thresholds,
                                                                      delimiter=AttenuationEnum.delimiter,
                                                                      converter=int,
                                                                      optional=True)
            # legacy option
            if self._step_change_thresholds is None:
                self._step_change_thresholds = self.configuration.getlist(section=self.section,
                                                                          option=AttenuationEnum.stepchange,
                                                                          delimiter=AttenuationEnum.delimiter,
                                                                          converter=int,
                                                                          optional=True)
            self.logger.debug(ATTENUATION_LOG_STRING.format( 'step_change_thresholds', self._step_change_thresholds))
        return self._step_change_thresholds

    def reset(self):
        """
        Sets the attributes to None (except step_change_thresholds which is set to False)
        """
        self.logger.debug("Resetting the AttenuationConfiguration")
        self._stop = None
        self._name = None
        self._control_ip = None
        self._start = None
        self._step_sizes = None
        self._step_change_thresholds = False
        self._step_list = None
        self._reversal_limit = None
        return

    def check_rep(self):
        """
        Tries to find inconsistencies in the values

        :raise: AssertionError if value-error is found
        """
        super(AttenuationConfiguration, self).check_rep()
        try:
            # is the name a known attenuator? This seems fragile, but what the hell
            assert self.name.lower() in attenuation_definitions, "Configuration -- Section: [attenuation] Option: name={n}' not a known attenuator".format(n=self.name)
            # is stop greater or equal to start?
            assert self.stop >= self.start, "stop: {stop} not greater than or equal to start: {start}".format(stop=self.stop,
                                                                                                               start=self.start)
        except AssertionError as error:
            self.logger.error(error)
            raise ConfigurationError(error)
        return
# end class AttenuationConfiguration

class OtherConfiguration(BaseConfiguration):
    """
    A holder of leftover parts
    """
    def __init__(self, *args, **kwargs):
        """
        OtherConfiguration constructor

        :param:

         - `configuration`: a loaded configuration-adapter
        """
        super(OtherConfiguration, self).__init__(*args, **kwargs)

        # attributes
        self._result_location = None
        self._test_name = None
        self._repetitions = None
        self._recovery_time = None
        return

    @property
    def example(self):
        """
        An example other-section
        """
        if self._example is None:
            self._example = textwrap.dedent("""
            #[{section}]
            # a sub-folder name to save the output files in
            # also used for the final csv
            # add {{timestamp}}  to get a timestamp            
            # e.g. result_location = rvr_{{timestamp}}
            
            #result_location = {result_location}

            # identifier for the test 
            #test_name = {test_name}

            # to run the same test multiple times
            # repetitions = {repetitions}

            # there is currently a sleep between directions (up and down)
            # use this next setting to change it if it's too long or short
            #recovery_time = {recovery_time}
            """.format(section=self.section,
                       result_location=OtherEnum.default_result_location,
                       test_name=OtherEnum.default_test_name,
                       repetitions=OtherEnum.default_repetitions,
                       recovery_time=OtherEnum.default_recovery_time))
        return self._example

    @property
    def section(self):
        """
        Name of the section in the configuration file
        """
        if self._section is None:
            self._section = OtherEnum.section
        return self._section

    @property
    def result_location(self):
        """
        The name of the output folder (default = 'output_files')
        """
        if self._result_location is None:
            self._result_location = self.configuration.get(section=self.section,
                                                           option=OtherEnum.result_location,
                                                           optional=True,
                                                           default=OtherEnum.default_result_location)
            self.logger.debug("Using Result Location: {0}".format(self._result_location))
        return self._result_location
    
    @property
    def test_name(self):
        """
        The name to use for the test.
        """
        if self._test_name is None:
            self._test_name = self.configuration.get(section=self.section,
                                                     option=OtherEnum.test_name,
                                                     optional=True,
                                                     default=OtherEnum.default_test_name)
            self.logger.debug("Using Test Name: {0}".format(self._test_name))
        return self._test_name

    @property
    def repetitions(self):
        """
        Gets number of times to repeat the same test
        """
        if self._repetitions is None:
            self._repetitions = OtherEnum.default_repetitions
            self._repetitions = self.configuration.getint(section=self.section,
                                                           option=OtherEnum.repetitions,
                                                           optional=True,
                                                           default=OtherEnum.default_repetitions)
        return self._repetitions

    @property
    def recovery_time(self):
        """
        Number of seconds to sleep between test directions
        """
        if self._recovery_time is None:
            self._recovery_time = self.configuration.getint(section=self.section,
                                                            option=OtherEnum.recovery_time,
                                                            optional=True,
                                                            default=OtherEnum.default_recovery_time)
        return self._recovery_time
    
    def reset(self):
        """
        Sets the attributes to None
        """
        self.logger.debug("resetting the attributes to None")
        self._result_location = None
        self._recovery_time = None
        self._test_name = None
        self._ping = None
        self._repetitions = None
        return

    @optionalsection
    def check_rep(self):
        """
        Checks the representation

        :raise: Attenuator Error if something bad found
        """
        super(OtherConfiguration, self).check_rep()
        try:
            assert self.repetitions >= 0
        except AssertionError as error:
            self.logger.error(error)
            raise TestsuiteError("test repetitions must be non-negative, not {0}".format(self.repetitions))
        return
# end class OtherConfiguration
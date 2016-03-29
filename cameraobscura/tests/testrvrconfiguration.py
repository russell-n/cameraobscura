
# python standard library
import unittest
import random
import ConfigParser
import sys
import io
import textwrap

# third-party
from mock import MagicMock, Mock

# this package
from cameraobscura.ratevsrange.rvrconfiguration import BaseConfiguration
from cameraobscura.ratevsrange.rvrconfiguration import RVRConfiguration
from cameraobscura.ratevsrange.rvrconfiguration import AttenuationConfiguration, AttenuationEnum
from cameraobscura.hosts.host import HostConfiguration, HostEnum
from cameraobscura.ratevsrange.rvrconfiguration import OtherConfiguration, OtherEnum

from cameraobscura.tests.helpers import random_string_of_letters
from cameraobscura import CameraobscuraError
from cameraobscura.utilities.configurationadapter import ConfigurationAdapter
from cameraobscura.utilities.configurationadapter import ConfigurationError
from cameraobscura.utilities.query import QueryConfiguration
from cameraobscura.utilities.dump import DumpConfiguration

from cameraobscura.commands.iperf.Iperf import IperfSettings, IperfConfiguration
from cameraobscura.commands.iperf.IperfSettings import IperfClientSettings

from cameraobscura.commands.ping.pingconfiguration import PingConfiguration


class NoSection(BaseConfiguration):
    """
    A Configuration with no section property
    """
    def __init__(self, *args, **kwargs):
        super(NoSection, self).__init__(*args, **kwargs)
        return

    def check_rep(self):
        return

    def reset(self):
        return

class NoCheckRep(BaseConfiguration):
    def __init__(self, *args, **kwargs):
        super(NoCheckRep, self).__init__(*args, **kwargs)
        return

    @property
    def section(self):
        return

    def reset(self):
        return

class NoReset(BaseConfiguration):
    def __init__(self, *args, **kwargs):
        super(NoCheckRep, self).__init__(*args, **kwargs)
        return

    @property
    def section(self):
        return

    def check_rep(self):
        return

class ConcreteConfiguration(BaseConfiguration):
    """
    A Configuration with all properties implemented
    """
    def __init__(self, *args, **kwargs):
        super(ConcreteConfiguration, self).__init__(*args, **kwargs)
        self._apple = None
        self._banana = None
        self._chimpanzee = None
        return

    @property
    def example(self):
        return

    @property
    def apple(self):
        return self._apple

    @property
    def banana(self):
        return self._banana

    @property
    def chimpanzee(self):
        return self._chimpanzee

    @property
    def section(self):
        return 'concrete'

    def check_rep(self):
        return
    
    def reset(self):
        self._unknown_options = None
        return
# end ConcreteConfiguration        
    
class TestBaseConfiguration(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.config_parser = MagicMock()
        self.config_adapter = ConfigurationAdapter(self.config_parser)
        self.configuration = ConcreteConfiguration(configuration=self.config_adapter)
        self.configuration._logger = self.logger
        return
    
    def test_constructor(self):
        """
        Does it build correctly?
        """      
        self.assertEqual(self.configuration.configuration,
                         self.config_adapter)
        return

    def test_section(self):
        """
        Does it raise an exception if section isn't implemented?
        """
        with self.assertRaises(TypeError):
            NoSection(configuration=self.config_adapter)
        return

    def test_exclusions(self):
        """
        Does it have the expected list of attributes to exclude?
        """
        expected = sorted('_section _logger _options _exclusions _example configuration _unknown_options'.split())
        self.assertEqual(expected,
                         self.configuration.exclusions)
        return

    def test_options(self):
        """
        Does it get the relevant options?
        """
        self.config_parser.defaults.return_value = {'uma':'gumma',
                                       'arf':'barf'}
        expected = 'apple banana chimpanzee'.split()
        self.assertEqual(expected, self.configuration.options)
        return

    def test_unknown_options(self):
        """
        Does it return a list of unknown options in the section?
        """
        default_dict =  {'uma':'gumma',
                         'arf':'barf'}       
        self.config_parser.defaults.return_value = default_dict
        known = 'apple banana chimpanzee'.split()
        unknown = 'cow pie'.split()
        self.config_parser.options.return_value = (known +
                                                   default_dict.keys() +
                                                   unknown)

        self.assertEqual(known, self.configuration.options)
        self.assertEqual(unknown, self.configuration.unknown_options)
        self.config_parser.options.assert_called_with(self.configuration.section)
        self.configuration.reset()
        unknown = 'horse fly'.split()
        self.config_parser.options.return_value = (known +
                                                   default_dict.keys() +
                                                   unknown)
        self.assertEqual(unknown, self.configuration.unknown_options)        
        return

    def test_abstract(self):
        """
        Does it raise TypeErrors for unimplemented section, check_rep, and reset?
        """
        with self.assertRaises(TypeError):
            NoSection(self.config_adapter)

        with self.assertRaises(TypeError):
            NoCheckRep(self.config_adapter)

        with self.assertRaises(TypeError):
            NoReset(self.config_adapter)
        return

    def test_string(self):
        """
        Does it create a replica of the configuration?
        """
        self.config_parser.defaults.return_value = {'uma':'gumma',
                                       'arf':'barf'}

        apple = random_string_of_letters()
        banana = random_string_of_letters()
        chimpanzee = random_string_of_letters()
        self.configuration._apple = apple
        self.configuration._banana = banana
        self.configuration._chimpanzee = chimpanzee
        expected="""[concrete]
apple={a}
banana={b}
chimpanzee={c}
""".format(a=apple,
           b=banana,
           c=chimpanzee)

        print self.configuration.options
        
        self.assertEqual(expected, str(self.configuration))
        
# end TestBaseConfiguration    


configuration_ini="""
[attenuation]
steps = 1 2 3
step_sizes = 10 20
interface = 192.168.10.20

[query]
apple = jack

[dut]
username = albert
control_ip = 192.168.10.3
test_ip = 192.168.20.2
operating_system = linux

[server]
username = hammond
test_ip = 192.168.20.3
control_ip = 192.168.10.56
operating_system = cygwin

[other]
repetitions = 5

# more of these should be optional
[iperf]
type = tcp
packet_length = 256K
duration = 10p
arallel = 1
interval = 1
direction = up
tcp_window_size = 153
format = m

[dump]
timeout = 12
dmesg = dmesg
uname = uname -a
os = cat /etc/os-release

[ping]
"""



class TestRVRConfiguration(unittest.TestCase):
    def setUp(self):
        self.config_parser = ConfigParser.SafeConfigParser()
        self.config_parser.readfp(io.BytesIO(configuration_ini))
        self.config_adapter = ConfigurationAdapter(self.config_parser)
        self.configuration = RVRConfiguration(configuration=self.config_adapter)
        return

    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.config_adapter,
                         self.configuration.configuration)
        return


    def test_attenuation(self):
        """
        Does it get build the AttenuationConfiguration? 
        """
        self.assertIsInstance(self.configuration.attenuation,
                              AttenuationConfiguration)
        return

    def test_traffic(self):
        """
        Does it build the Traffic Configuration?
        """
        self.assertIsInstance(self.configuration.traffic,
                              IperfConfiguration)
        return

    def test_dut(self):
        """
        Does it get the dut's configuration?
        """
        self.assertIsInstance(self.configuration.dut,HostConfiguration)
        self.assertEqual('dut', self.configuration.dut.section)
        return

    def test_server(self):
        """
        Does it get the server's configuration?
        """
        self.assertIsInstance(self.configuration.server,
                              HostConfiguration)
        self.assertEqual('server', self.configuration.server.section)
        return

    def test_other(self):
        """
        Does it get the OtherConfiguration?
        """
        self.assertIsInstance(self.configuration.other,
                              OtherConfiguration)
        return

    def test_query(self):
        """
        Does it create the query configuration?
        """
        #query given
        self.assertTrue(self.configuration.configuration.has_section('query'))
        self.assertIsInstance(self.configuration.query,
                              QueryConfiguration)

        self.configuration._query = None
        # query not given
        self.configuration.configuration = MagicMock()
        self.configuration.configuration.has_section.return_value = False
        self.assertIsNone(self.configuration.query)
        return

    def test_dump(self):
        """
        Does it get the dump configuration?
        """
        # dump given
        fields = 'dmesg uname os'.split()
        self.assertEqual(fields, self.configuration.dump.fields)
        self.assertIsInstance(self.configuration.dump, DumpConfiguration)

        # dump not given
        self.configuration._dump = None
        self.configuration.configuration = Mock()
        self.configuration.configuration.has_section.return_value = False
        self.assertIsNone(self.configuration.dump)
        return

    def test_ping(self):
        """
        Does it get the ping configuration?
        """
        self.assertIsInstance(self.configuration.ping, PingConfiguration)
        return
# end class TestRVRConfiguration        


class TestAttenuationConfigurationConfiguration(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.config_parser = MagicMock()
        
        self.config_adapter = ConfigurationAdapter(self.config_parser)
        self.configuration = AttenuationConfiguration(configuration=self.config_adapter)
        self.configuration._logger = self.logger
        return

    def test_constructor(self):
        """
        Does the class build?
        """
        self.assertEqual(self.config_adapter,
                         self.configuration.configuration)
        return

    def test_attenuation_stop(self):
        """
        Does it get the maximum attenuation?
        """
        # user set a value
        value = random.randrange(1000)
        self.config_parser.getint.return_value = value
        self.assertEqual(self.configuration.stop,
                         value)
        self.config_parser.getint.assert_called_with('attenuation',
                                                     'stop')
        self.configuration.reset()
        
        # check the default is the system's maximum integer
        self.config_parser.getint.side_effect = ConfigParser.NoOptionError('stop',
                                                                           'attenuation')
        maxint = sys.maxint
        self.assertEqual(maxint, self.configuration.stop)
        return

    def test_attenuation_name(self):
        """
        Does it get the name of the attenuator?
        """
        expected = 'Herschel'
        self.config_parser.get.return_value = expected
        self.assertEqual(expected, self.configuration.name)
        self.config_parser.get.assert_called_with('attenuation', 'name')

        # none given
        self.configuration.reset()
        self.config_parser.get.side_effect = ConfigParser.NoOptionError("name",
                                                                        "attenuation")
        expected = 'WeinschelP'
        self.assertEqual(expected, self.configuration.name)
        return

    def test_control_ip(self):
        """
        Does it get the hostname of the attenuator?
        """
        # user set it
        expected = '192.168.10.25'
        self.config_parser.get.return_value = expected
        self.assertEqual(expected, self.configuration.control_ip)
        self.config_parser.get.assert_called_with('attenuation',
                                                  'control_ip')

        # user didn't set it
        def side_effect(*args):
            if args == ('attenuation', 'control_ip'):
                raise ConfigParser.NoOptionError('control_ip',
                                                 'attenuation')
            elif args == ('attenuation', 'interface'):
                return "apeman"
            else:
                raise Exception('this test is not set up right')
            
        self.configuration.reset()
        self.config_parser.get.side_effect = side_effect
        self.assertEqual('apeman', self.configuration.control_ip)
        return


    def test_attenuation_start(self):
        """
        Does it get the start value from the attenuation section?
        """
        # user sets it
        value = random.randrange(1000)
        self.config_parser.getint.return_value = value
        self.assertEqual(value, self.configuration.start)
        self.config_parser.getint.assert_called_with('attenuation', 'start')

        # user doesn't set it
        self.configuration.reset()
        self.config_parser.getint.side_effect = ConfigParser.NoOptionError('start',
                                                                           'attenuation')
        self.assertEqual(0, self.configuration.start)
        return

    def test_step_sizes(self):
        """
        Does it get the step-sizes from the attenuation section?
        """
        # user sets it
        expected = [1, 3]
        value = '1 3'
        self.config_parser.get.return_value = value
        self.assertEqual(expected, self.configuration.step_sizes)
        self.config_parser.get.assert_called_with('attenuation', 'step_sizes')
        
        # user didn't set it, use the default
        self.configuration.reset()
        expected = [1]
        self.config_parser.get.side_effect = ConfigParser.NoOptionError('step_sizes',
                                                                        'attenuation')
        self.assertEqual(expected, self.configuration.step_sizes)

        # user set it to the old 'step'
        def side_effect(*args):
            if args == ('attenuation', 'step_sizes'):
                raise ConfigParser.NoOptionError('step_sizes',
                                                'attenuation')
            elif args == ('attenuation', 'step'):
                return '1 1'
        self.config_parser.get.side_effect = side_effect
        self.configuration.reset()
        self.assertEqual([1,1], self.configuration.step_sizes)
        return

    def test_step_change_thresholds(self):
        """
        Does it get the attenuation thresholds which trigger a change in step-size?
        """
        # user sets it
        value = '100 200'
        expected = [100, 200]
        self.config_parser.get.return_value = value
        self.assertEqual(expected, self.configuration.step_change_thresholds)
        self.config_parser.get.assert_called_with('attenuation', 'step_change_thresholds')

        # user uses old 'stepchange' option-name
        self.configuration.reset()
        def side_effect(*args):
            if args == ('attenuation', 'step_change_thresholds'):
                raise ConfigParser.NoOptionError('step_change_thresholds',
                                                 'attenuation')
            elif args == ('attenuation', 'stepchange'):
                return '400'
            else:
                raise Exception("this test is broken")
        expected = [400]
        self.config_parser.get.side_effect = side_effect
        self.assertEqual(expected, self.configuration.step_change_thresholds)

        # neither option was used
        self.configuration.reset()
        self.config_parser.get.side_effect = ConfigParser.NoOptionError('option',
                                                                    'attenuation')
        self.assertIsNone(self.configuration.step_change_thresholds)
        return

    def test_check_rep(self):
        """
        Does it raise assertion errors if there are incorrect representations?
        """
        self.configuration._unknown_options = 'able baker charley'.split()
        self.configuration._name = 'halitosis2000'
        with self.assertRaises(ConfigurationError):
            self.configuration.check_rep()
        self.configuration._name = AttenuationEnum.default_attenuator
        self.configuration.check_rep()
        self.configuration._stop = random.randrange(10)
        self.configuration._start = random.randrange(10, 1000)
        with self.assertRaises(ConfigurationError):
            self.configuration.check_rep()
        return

    def test_reset(self):
        """
        Does it reset the attributes to None?
        """
        self.configuration._stop = 1
        self.assertEqual(self.configuration.stop, 1)
        self.configuration.reset()
        self.assertIsNone(self.configuration._stop)
        self.configuration._name = 'bob'
        self.assertEqual(self.configuration.name, 'bob')
        self.configuration.reset()
        self.assertIsNone(self.configuration._name)
        self.configuration._start = 56
        self.assertEqual(self.configuration.start, 56)
        self.configuration.reset()
        self.assertIsNone(self.configuration._start)
        self.configuration._control_ip = 'albert'
        self.assertEqual(self.configuration.control_ip, 'albert')
        self.configuration.reset()
        self.assertIsNone(self.configuration._control_ip)
        self.configuration._step_sizes = [2,4]
        self.assertEqual(self.configuration.step_sizes, [2,4])
        self.configuration.reset()
        self.assertIsNone(self.configuration._step_sizes)
        self.configuration._step_change_thresholds = [3,6]
        self.assertEqual(self.configuration.step_change_thresholds, [3,6])
        self.configuration.reset()
        self.assertIs(False, self.configuration._step_change_thresholds)
        return
# end TestAttenuationConfiguration


class TestOtherConfiguration(unittest.TestCase):
    def setUp(self):
        self.config_parser = MagicMock()
        self.config_adapter = ConfigurationAdapter(self.config_parser)
        self.section = 'other'
        self.configuration = OtherConfiguration(configuration = self.config_adapter)
        self.configuration._logger = MagicMock()
        return

    def test_constructor(self):
        """
        Does it build the object correctly?
        """
        self.configuration._logger = None
        self.assertEqual(self.config_adapter, self.configuration.configuration)
        return

    def test_result_location(self):
        """
        Does it get the folder name?
        """
        expected = 'unglaublich'
        self.config_parser.get.return_value = expected
        self.assertEqual(expected, self.configuration.result_location)
        self.config_parser.get.assert_called_with(self.section, 'result_location')

        # user didn't give the option, use default
        self.configuration.reset()
        self.config_parser.get.side_effect = ConfigParser.NoOptionError('result_location',
                                                                        self.section)
        self.assertEqual('output_folder', self.configuration.result_location)
        return

    def test_test_name(self):
        """
        Does it get the test_name?
        """
        expected = 'pistolpete'
        option = 'test_name'
        self.config_parser.get.return_value = expected
        self.assertEqual(expected, self.configuration.test_name)
        self.config_parser.get.assert_called_with(self.section,
                                                  option)

        # none given, use the default
        self.configuration.reset()
        self.config_parser.get.side_effect = ConfigParser.NoOptionError(option,
                                                                        self.section)
        self.assertEqual('rate_vs_range', self.configuration.test_name)
        return


    def test_repetitions(self):
        """
        Does it get the repetitions correctly?
        """
        # value given
        value = random.randrange(100)
        self.config_parser.getint.return_value = value
        self.assertEqual(value, self.configuration.repetitions)

        # no value given
        self.configuration.reset()
        self.config_parser.getint.side_effect = ConfigParser.NoOptionError("repetitions",
                                                                           'other')
        self.assertEqual(OtherEnum.default_repetitions,
                         self.configuration.repetitions)
        return

    def test_recovery_time(self):
        """
        Does it set the number of seconds to wait between tests?
        """
        # user sets it        
        value = random.randrange(100)
        self.config_parser.getint.return_value = value
        self. assertEqual(value, self.configuration.recovery_time)

        # user does not set it
        self.configuration.reset()
        self.config_parser.getint.side_effect = ConfigParser.NoOptionError('recovery_time',
                                                                           self.section)
        self.assertEqual(OtherEnum.default_recovery_time, self.configuration.recovery_time)
        return

# end TestOtherConfiguration

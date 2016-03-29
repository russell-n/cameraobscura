
# python standard library
import unittest
import ConfigParser
from ConfigParser import SafeConfigParser
import random
from collections import namedtuple

# third-party
from mock import MagicMock, patch, mock_open

# this package
from cameraobscura.ratevsrange.AutomatedRVR import (Test,
                                                  DIRECTION_MAP,
                                                  AutomatedRVREnum)
from cameraobscura.utilities.configurationadapter import ConfigurationAdapter
from cameraobscura.ratevsrange.rvrconfiguration import RVRConfiguration, AttenuationConfiguration
from cameraobscura.utilities.query import Query
from cameraobscura.attenuators.Attenuator import AttenuatorError
from cameraobscura import CameraobscuraError
from cameraobscura import NoOp


SAMPLE = """[attenuation]
start = 0"""



class TestAutomatedRVRTest(unittest.TestCase):
    def setUp(self):        
        self.parser = MagicMock()
        self.config = ConfigurationAdapter(self.parser)
        self.attenuator = MagicMock()
        self.tester = Test(self.config)
        self.tester._logger = MagicMock()
        self.tester._attenuator = self.attenuator
        return

    def test_constructor(self):
        """
        Does it build and put the ConfigurationAdapter in an RVRConfiguration?
        """
        self.assertIsInstance(self.tester.configuration,
                              RVRConfiguration)
        return

    def test_maximum_attenuation(self):
        """
        Does it use the minimum on the configuration.maximum_attenuation or getAttenMax()
        """
        # user set a small value
        small, large = 65, 9999
        attenuation_configuration = AttenuationConfiguration(self.parser)
        attenuation_configuration._name = "WeinschelP"
        attenuation_configuration._stop = small
        self.tester.configuration._attenuation = attenuation_configuration
        self.attenuator.getAttenMax.return_value = large
        self.assertEqual(small, self.tester.maximum_attenuation)

        # user didn't set a value
        self.tester._maximum_attenuation = None
        attenuation_configuration._stop = large + 1
        self.assertEqual(large, self.tester.maximum_attenuation)
        return

    def test_check_connection(self):
        """
        Does it only ping the server if the option was set?
        """
        ping = MagicMock()
        dut = MagicMock()
        configuration_mock = MagicMock()
        dut.operating_system = 'linux'
        self.tester._dut = dut
        self.tester._server = MagicMock()
        self.tester._server.TestInterface = 'server'

        # check that it doesn't run
        self.parser.has_section.return_value = False
        #self.tester.configuration.ping = None
        outcome = self.tester.connected()
        with self.assertRaises(AssertionError):
            ping.assert_called_with()
        self.assertTrue(outcome)

        # check that it does run
        self.tester._ping = ping
        mock_time = MagicMock()
        times = [500,4,3, 2, 1]
        # pinged
        mock_time.side_effect = lambda: times.pop()
        with patch('time.time', mock_time):
            ping.return_value = True
            outcome = self.tester.connected()
            ping.assert_called_with()
            
        times = [700, 600, 500,400 ,300, 40,30, 20, 10]
        def time_effects():
            output =  times.pop()
            return output
        
        # timed out
        mock_time.side_effect = time_effects
        #mock_time_2 = MagicMock()
        self.tester._result_location = 'cache'
        with patch('time.time', mock_time):
            ping.return_value = False
            outcome = self.tester.connected()
            ping.assert_called_with()
            self.assertFalse(outcome)
        
        # timed out
        times = [700, 600, 100, 10]
        
        mock_time.side_effect = lambda: times.pop()
        # raises exception if asked to
        start = 0
        attenuation = 0
        with self.assertRaises(CameraobscuraError):
            with patch('time.time', mock_time):
                ping.return_value = False
                self.tester.connected(raise_error=start==attenuation)
        return

    def test_attenuations(self):
        """
        Does it set up the attenuations correctly?
        """
        start = 2
        stop = 10
        step_sizes = [1,2]
        step_change_thresholds = [200]
        maximum = 20
        attenuation = 'attenuation'
        int_response = {(attenuation,'start'): start,
                        (attenuation, 'stop'): stop,
                        (attenuation, 'maximum'): maximum}
        get_response = {(attenuation, 'step_sizes'): '1 2',
                        (attenuation, 'step_change_thresholds'): '200',
                        (attenuation, 'name'): 'WeinschelP',
                        (attenuation, 'control_ip'): 'localhost'}
                    
        def get_side_effect(*args):
            return get_response[args]

        def int_side_effects(*args):
            return int_response[args]

        self.parser.get.side_effect = get_side_effect
        self.parser.getint.side_effect = int_side_effects

        iterator = self.tester.attenuations
        self.assertEqual(start, iterator.start)
        self.assertEqual(stop, iterator.stop)
        return

    def test_dut_configuration(self):
        """
        Does the dut's configuration get built and used correctly?
        """
        host_ssh = MagicMock()

        SECTION = 'dut'
        hostname = 'localhost'
        username = 'memyselfi'
        password = 'nunya'
        test_ip = 'eebejeebe'
        serial = False
        prefix = 'PATH=/tmp/bist:$PATH'
        connection_type = 'telnet'
        operating_system = 'amiga'
        timeout = random.randrange(1, 100)

        get_boolean_response = {(SECTION, 'serial'):serial,
                        ('other', 'ping'): False}
        
        get_response = {(SECTION, 'control_ip'): hostname,
                        (SECTION, 'username'): username,
                        (SECTION, 'password'): password,
                        (SECTION, 'test_ip'): test_ip,
                        (SECTION, 'connection_type'): connection_type,
                        (SECTION, 'prefix'):  prefix,
                        (SECTION, 'operating_system'): operating_system,
                        ('other', 'result_location'):'home',
                        ('other', 'test_name'):'bill'}

        get_float = {(SECTION, 'timeout'):timeout}

        get_int = {(SECTION, 'port'):timeout,
                   ('other', 'repetitions'):1}

        def getfloat_side_effect(*args):
            return get_float[args]
            
        def side_effect(*args):
            return get_response[args]

        def getboolean_side_effect(*args):
            return get_boolean_response[args]

        def getint_side_effect(*args):
            return get_int[args]
            

        self.parser.get.side_effect = side_effect
        self.parser.getboolean.side_effect = getboolean_side_effect
        self.parser.getfloat.side_effect = getfloat_side_effect
        self.parser.getint.side_effect = getint_side_effect        
        
        with patch('cameraobscura.hosts.host', host_ssh):
            dut = self.tester.dut
            host_ssh.TheHost.assert_called_with(hostname=hostname,
                                                username=username,
                                                password=password,
                                                test_interface=test_ip,
                                                prefix=prefix,
                                                timeout=timeout,
                                                operating_system=operating_system,
                                                connection_type=connection_type)

        utils_mock = MagicMock()
        return

    def test_server_configuration(self):
        """
        Does it set up and use the server configuration correctly?
        """
        host_ssh = MagicMock()
        SECTION = 'server'
        control = 'localhost'
        username = 'billy'
        password = None
        test_ip = 'here'
        connection_type = 'ssh'
        operating_system = 'beos'
        get_responses = {(SECTION, 'control_ip'): control,
                         (SECTION, 'username'): username,
                         (SECTION, 'password'): password,
                         (SECTION, 'test_ip'): test_ip,
                         (SECTION, 'connection_type'): connection_type,
                         (SECTION, 'prefix'): '',
                         (SECTION, 'operating_system'): operating_system}
        def get_effects(*args):
            return get_responses[args]
        self.parser.get.side_effect = get_effects
        
        with patch('cameraobscura.hosts.host', host_ssh):
            server = self.tester.server

        return

    def test_other_configuration(self):
        """
        Does it properly use the Other Configuration?
        """
        expected = 'aoeusnth'
        strftime = ';qjkwmb'
        self.parser.get.return_value = expected
        time_mock = MagicMock()
        os_patch = MagicMock()
        with patch('time.strftime', time_mock):
            with patch('os.makedirs', os_patch):
                time_mock.return_value = strftime
                self.assertEqual(expected + strftime, self.tester.result_location)
        return

    def test_save_configuration(self):
        """
        Does it have the configuration save a copy of itself?
        """
        configadapter = MagicMock()
        rvrconfiguration = RVRConfiguration(configadapter)
        self.tester._configuration  = rvrconfiguration
        open_mock = mock_open()
        opened_file = MagicMock()
        open_mock.return_value = opened_file
        print __name__
        self.tester._result_location = 'apple_jack'
        with patch('__builtin__.open', open_mock, create=True):
            filename = 'outyor.ini'
            self.tester.save_configuration(filename=filename)
            open_mock.assert_called_with('apple_jack/outyor.ini', 'w')
            configadapter.write.assert_called_with(opened_file.__enter__())
        return

    def test_directon_map(self):
        """
        Does the direction map return the expected directions?
        """
        self.assertEqual((AutomatedRVREnum.upstream,), DIRECTION_MAP['upstream'])
        self.assertEqual((AutomatedRVREnum.upstream, AutomatedRVREnum.downstream),
                         DIRECTION_MAP['both'])
        self.assertEqual((AutomatedRVREnum.downstream,), DIRECTION_MAP['downstream'])
# end TestAutomatedRVRTest    


# python standard library
import unittest
import random
from StringIO import StringIO
import socket
import re
import ConfigParser

# third-party
from mock import MagicMock, patch, Mock

# this package
from cameraobscura.commands.ping.ping import Ping, PingConstants
from cameraobscura.tests.helpers import random_string_of_letters
from cameraobscura import CameraobscuraError

from cameraobscura.commands.ping.pingconfiguration import PingConfiguration
from cameraobscura.utilities.configurationadapter import ConfigurationAdapter


class TestPing(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.target = random_string_of_letters()
        self.timeout = random.randrange(1, 1000)
        self.threshold = random.randrange(1, 100)
        self.operating_system = random.choice('linux cygwin'.split())
        
        self.ping = Ping(connection=self.connection,
                         target=self.target,
                         timeout=self.timeout,
                         threshold=self.threshold,
                         operating_system=self.operating_system)
        return

    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.connection, self.ping.connection)
        self.assertEqual(self.target, self.ping.target)
        self.assertEqual(self.timeout, self.ping.timeout)
        self.assertEqual(self.threshold, self.ping.threshold)
        self.assertEqual(self.operating_system, self.ping.operating_system)
        return

    def test_operating_system(self):
        """
        Does it try to get the operating system if it wasn't given?
        """
        self.ping._operating_system = None
        expected = 'cygwin'
        self.connection.exec_command.return_value = (None, StringIO(expected), "")
        self.assertEqual(expected, self.ping.operating_system)
        self.connection.exec_command.assert_called_with('uname', timeout=1)

        #what if it times out?
        self.connection.exec_command.side_effect = socket.timeout("socket timed out -- why didn't you catch this?")
        with self.assertRaises(CameraobscuraError):
            self.ping._operating_system = None
            self.ping.operating_system

        # what if it returns an error?
        self.connection.exec_command.return_value = (None, StringIO(""), StringIO("'uname' not found"))
        self.connection.exec_command.side_effect = None
        self.ping._operating_system = None
        with self.assertRaises(CameraobscuraError):
            self.ping.operating_system
        return

    def test_call(self):
        """
        Does the call try to ping the device correctly?
        """
        time_mock = MagicMock()
        logger = Mock()
        self.ping._logger = logger

        # case 1 : success
        test_line = '64 bytes from pc-in-f147.1e100.net (74.125.28.147): icmp_req=1 ttl=44 time=13.7 ms'
        self.assertIsNotNone(self.ping.command.data_expression.search(test_line))
        self.connection.exec_command.return_value = None, [test_line], StringIO('')
        
        time_mock.return_value = 0
        with patch('time.time', time_mock):
            self.assertTrue(self.ping())

        ## case 2: failure
        ## this fails sometimes -- the actual path needs to be worked out
        self.connection.exec_command.return_value = None, '', ''
        times = [self.timeout] * 2 + [0] * (self.threshold + 1)
        time_mock.side_effect = lambda: times.pop()
        with patch('time.time', time_mock):
            self.assertFalse(self.ping())

        # case 3: connection problem
        self.connection.exec_command.side_effect = socket.timeout("socket timed out-- catch it")
        with self.assertRaises(CameraobscuraError):
            self.ping()
        return

    def test_command(self):
        """
        Does it construct a valid command?
        """
        self.ping._operating_system = PingConstants.cygwin
        expected = 'ping {1} {0}\n'.format(self.target,
                                         PingConstants.cygwin_one_repetition)
        actual = self.ping.command.command_arguments
        self.assertEqual(expected, actual, "Case 1 (Cygwin): expected {0}, actual {1}".format(expected,
                                                                                              actual))

        self.ping._operating_system = PingConstants.linux
        self.ping._command = None
        self.ping._arguments = None
        self.ping._arguments_target = None
        expected = 'ping {1} {0}\n'.format(self.target, PingConstants.linux_one_repetition)
        actual = self.ping.command.command_arguments
        self.assertEqual(expected, actual, "Case 2 (linux): expected {0}, actual {1}".format(expected,
                                                                                             actual))

        self.ping.reset()
        self.ping._operating_system = PingConstants.linux + random_string_of_letters()
        with self.assertRaises(CameraobscuraError):
            self.ping.command
        return

    def test_expression(self):
        """
        Does it set the appropriate expression?
        """
        test_line = '64 bytes from pc-in-f147.1e100.net (74.125.28.147): icmp_req=1 ttl=44 time=13.7 ms'
        expected = '13.7'
        match = re.compile(self.ping.data_expression).search(test_line)
        self.assertEqual(expected, match.group(PingConstants.round_trip_time))
        return
# end TestPing    


class TestPingConfiguration(unittest.TestCase):
    def setUp(self):
        self.config_parser = Mock()
        self.config_adapter = ConfigurationAdapter(self.config_parser)
        self.configuration = PingConfiguration(configuration=self.config_adapter)
        return

    def test_constructor(self):
        """
        Does it build correctly?
        """
        self.assertEqual(self.configuration.section, 'ping')
        return

    def test_trap_errors(self):
        """
        Does it get the 'trap_errors' value?
        """
        # user gave value
        value = random.choice((True, False))
        self.config_parser.getboolean.return_value = value
        self.assertEqual(self.configuration.trap_errors, value)
        self.config_parser.getboolean.assert_called_with('ping', 'trap_errors')

        # none given, use defaults
        self.configuration.reset()
        self.config_parser.getboolean.side_effect = ConfigParser.NoOptionError('trap_errors',
                                                                               'ping')
        self.assertTrue(self.configuration.trap_errors)
        return

    def test_data_expression(self):
        """
        Does it get the regular expression to match a successful ping?
        """
        # user sets an expression
        value = random_string_of_letters()
        self.config_parser.get.return_value = value
        self.assertEqual(self.configuration.data_expression, value)

        # user didn't set it, return None
        self.configuration.reset()
        self.config_parser.get.side_effect = ConfigParser.NoOptionError('data_expression', 'ping')
        self.assertIsNone(self.configuration.data_expression)
        return

    def test_timeout(self):
        """
        Does it get the readline timeout?
        """
        # user sets a timeout
        value = random.randrange(10, 100)
        self.config_parser.getfloat.return_value = value
        self.assertEqual(self.configuration.timeout, value)
        self.config_parser.getfloat.assert_called_with('ping', 'timeout')

        # user didn't set, use a default
        self.configuration.reset()
        self.config_parser.getfloat.side_effect = ConfigParser.NoOptionError('timeout', 'ping')
        self.assertEqual(self.configuration.timeout, 10)
        return

    def test_operating_system(self):
        """
        Does it get the operating system from the file?
        """
        os = random_string_of_letters(5)
        self.config_parser.get.return_value = os
        self.assertEqual(os, self.configuration.operating_system)
        self.config_parser.get.assert_called_with('ping', 'operating_system')
        
        # user doesn't give it, use the default
        self.configuration.reset()
        self.config_parser.get.side_effect = ConfigParser.NoOptionError('operating_system', 'ping')
        self.assertIsNone(self.configuration.operating_system)
        return

    def test_arguments(self):
        """
        Does it get the argument string from the file?
        """
        arguments = random_string_of_letters()
        self.config_parser.get.return_value = arguments
        self.assertEqual(self.configuration.arguments, arguments)
        self.config_parser.get.assert_called_with('ping', 'arguments')

        # none given, use the defaults
        self.configuration.reset()
        self.config_parser.get.side_effect = ConfigParser.NoOptionError('arguments', 'ping')
        self.assertEqual(self.configuration.arguments, PingConstants.linux_one_repetition)
        return

    def test_threshold(self):
        """
        Does it get the minimum consecuctive pings needed?
        """
        value = random.randrange(1, 100)
        self.config_parser.getint.return_value = value
        self.assertEqual(self.configuration.threshold, value)

        # default
        self.configuration.reset()
        self.config_parser.getint.side_effect = ConfigParser.NoOptionError('threshold', 'ping')
        self.assertEqual(5, self.configuration.threshold)
        return

    def test_time_limit(self):
        """
        Does it get the number of seconds to keep trying to ping?
        """
        value = random.randrange(100)
        self.config_parser.getfloat.return_value = value
        self.assertEqual(self.configuration.time_limit, value)

        # default
        self.configuration.reset()
        self.config_parser.getfloat.side_effect = ConfigParser.NoOptionError('time_limit', 'ping')
        self.assertEqual(300, self.configuration.time_limit)
        return

    def test_target(self):
        """
        Does it get the address (hostname) to ping?
        """
        value = random_string_of_letters()
        self.config_parser.get.return_value = value
        self.assertEqual(value, self.configuration.target)
        self.config_parser.get.assert_called_with('ping', 'target')

        # default
        self.configuration.reset()
        self.config_parser.get.side_effect = ConfigParser.NoOptionError('target', 'ping')
        self.assertIsNone(self.configuration.target)

        # setter
        # since the AutomatedRVR sets the target to the server's TestInterface, this needs to exist
        self.configuration.reset()
        value = random_string_of_letters()
        self.configuration.target = value
        return
# end TestPingConfiguration    

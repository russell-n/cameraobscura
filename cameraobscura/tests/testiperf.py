
# python standard library
import unittest
import os
from cStringIO import StringIO
import random
import ConfigParser
import io

# third-party
from mock import MagicMock, mock_open, patch, call

# this package
from cameraobscura import CameraobscuraError
from cameraobscura.common.errors import ConfigurationError
from cameraobscura.tests.helpers import random_string_of_letters
from cameraobscura.commands.iperf.Iperf import Iperf, IperfConfiguration, IperfEnum
from cameraobscura.commands.iperf.IperfSettings import IperfServerSettings, IperfClientSettings
from cameraobscura.commands.iperf.IperfSettings import IperfConstants

from cameraobscura.utilities.configurationadapter import ConfigurationAdapter


class TestIperf(unittest.TestCase):
    def setUp(self):
        # method mocks
        self.start_server = MagicMock()
        self.run_client = MagicMock()
        
        self.dut_hostname = random_string_of_letters(10)
        self.dut_testInterface = random_string_of_letters(5)
        self.dut = MagicMock(name='dut')
        self.dut.hostname = self.dut_hostname
        self.dut.testInterface = self.dut_testInterface
        
        self.traffic_server_hostname = random_string_of_letters(10)
        self.traffic_server_testInterface = random_string_of_letters(5)
        self.traffic_server = MagicMock(name='traffic_server')
        self.traffic_server.hostname = self.traffic_server_hostname
        self.traffic_server.testInterface = self.traffic_server_testInterface
        self.server_settings = IperfServerSettings()
        self.client_settings = IperfClientSettings()
        self.iperf = Iperf(dut=self.dut,
                           traffic_server=self.traffic_server,
                           server_settings=self.server_settings,
                           client_settings=self.client_settings)
        self.logger = MagicMock()
        self.iperf._logger = self.logger
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.iperf.dut, self.dut)
        self.assertEqual(self.iperf.traffic_server, self.traffic_server)
        self.assertEqual(self.iperf.server_settings, self.server_settings)
        self.assertEqual(self.iperf.client_settings, self.client_settings)
        return

    def test_client_server(self):
        """
        Does it build the client-server dictionary correctly?
        """
        cs = self.iperf.client_server[IperfConstants.down]
        self.assertEqual(cs.client, self.traffic_server)
        self.assertEqual(cs.server, self.dut)

        cs = self.iperf.client_server[IperfConstants.up]
        self.assertEqual(cs.client, self.dut)
        self.assertEqual(cs.server, self.traffic_server)
        return

    def test_udp(self):
        """
        Does it set the udp property correctly?
        """
        self.assertFalse(self.iperf.udp)
        self.iperf._udp = None
        with self.assertRaises(CameraobscuraError):
            self.client_settings.set('udp', True)
            self.iperf.udp

        self.server_settings.set('udp', True)
        self.assertTrue(self.iperf.udp)
        return

    def test_call(self):
        """
        Does the call follow the expected algorithm?
        """
        self.iperf.start_server = self.start_server
        self.iperf.run_client = self.run_client
        filename = random_string_of_letters(5)
        path = random_string_of_letters(5)
        full_path = os.path.join(path, filename)

        # downstream T --> D
        self.iperf(IperfConstants.down, full_path)
        expected_filename = os.path.join(path, IperfConstants.down + "_"+ 'tcp' + '_' +filename)
        self.assertEqual(self.iperf.client_settings.server, self.dut_testInterface)
        self.start_server.assert_called_with(self.dut, expected_filename)
        self.run_client.assert_called_with(self.traffic_server, expected_filename)

        # upstream D --> T
        self.iperf(IperfConstants.up, full_path)
        expected_filename = os.path.join(path, IperfConstants.up + "_" + 'tcp' + '_' + filename)
        self.assertEqual(self.iperf.client_settings.server, self.traffic_server_testInterface)
        self.start_server.assert_called_with(self.traffic_server, expected_filename)
        self.run_client.assert_called_with(self.dut, expected_filename)
        return

    def test_downstream(self):
        """
        Does it run downstream traffic?
        """
        path = random_string_of_letters()
        filename = random_string_of_letters()
        
        self.iperf.start_server = self.start_server
        self.iperf.run_client = self.run_client
        self.iperf.downstream(os.path.join(path, filename))

        expected_filename = os.path.join(path, IperfConstants.down + "_" + 'tcp' + '_' + filename)
        self.start_server.assert_called_with(self.dut, expected_filename)
        self.run_client.assert_called_with(self.traffic_server, expected_filename)
        return

    def test_upstream(self):
        """
        Does it run upstream traffic?
        """
        path = random_string_of_letters()
        filename = random_string_of_letters()
        
        self.iperf.start_server = self.start_server
        self.iperf.run_client = self.run_client
        self.iperf.upstream(os.path.join(path, filename))

        expected_filename = os.path.join(path, IperfConstants.up + "_" + 'tcp'+ '_'+filename)
        # DUT --> TPC
        self.start_server.assert_called_with(self.traffic_server, expected_filename)
        self.run_client.assert_called_with(self.dut, expected_filename)
        return

    def test_run(self):
        """
        Does it run a single direction of traffic?
        """
        host = MagicMock()
        file_writer_definition = MagicMock()
        file_writer_instance = MagicMock()
        file_writer_definition.return_value = file_writer_instance
        stdout = random_string_of_letters(10)
        stderr = random_string_of_letters(5)
        host.exec_command.return_value = None, stdout, stderr
        
        filename = random_string_of_letters()
        file_mock = mock_open()
        opened_file = MagicMock()
        file_mock.return_value = opened_file
        with patch('__builtin__.open', file_mock):
            with patch('cameraobscura.utilities.file_writer.LogWriter', file_writer_definition):
                self.iperf.run(host=host,
                               settings=self.server_settings,
                               filename=filename,
                               verbose=False)
        host.exec_command.assert_called_with('iperf {0}'.format(self.server_settings), timeout=10)
        file_mock.assert_called_with(filename, 'w')

        expected_write_calls = [call(letter) for letter in stdout]
        expected_error_calls = [call(letter) for letter in stderr]
        #print file_writer.mock_calls
        self.assertEqual(file_writer_instance.write.mock_calls, expected_write_calls)
 
        # try the log-writer
        self.logger.reset_mock()
        file_writer_instance.reset_mock()
        with patch('__builtin__.open', file_mock):
            with patch('cameraobscura.utilities.file_writer.LogWriter', file_writer_definition):
                self.iperf.run(host=host,
                               settings=self.server_settings,
                               filename=filename,
                               verbose=True)
        expected_write_calls = [call(letter) for letter in stdout]
        expected_error_calls = [call(letter) for letter in stderr]
        #print file_writer.mock_calls
        self.assertEqual(file_writer_instance.write.mock_calls, expected_write_calls)
        return

    def test_version(self):
        """
        Does it get the version numbers from the client and server?
        """
        stdout = "iperf version 2.0.5 (08 Jul 2010) pthreads"
        self.dut.exec_command.return_value = None, StringIO(stdout), StringIO('')
        output = self.iperf.version(self.dut)
        self.assertEqual(stdout, output)
        self.dut.exec_command.assert_called_with("iperf --version")
        return


class TestIperfConfiguration(unittest.TestCase):
    def setUp(self):
        self.config_parser = MagicMock()
        self.config_adapter = ConfigurationAdapter(self.config_parser)
        self.section = 'traffic'
        self.configuration = IperfConfiguration(configuration = self.config_adapter)
        self.configuration._logger = MagicMock()
        return

    def test_constructor(self):
        """
        Does it build the object correctly?
        """
        self.assertEqual(self.config_adapter, self.configuration.configuration)
        return

    def test_direction(self):
        """
        Does it get the traffic direction?
        """
        # upstream
        value = 'upsy-daisy'
        expected = 'upstream'
        self.config_parser.get.return_value = value
        self.assertEqual(expected, self.configuration.direction)
        self.config_parser.get.assert_called_with('iperf', 'direction')

        # downstream
        self.configuration.reset()
        value = 'down-low'
        expected = 'downstream'
        self.config_parser.get.return_value = value
        self.assertEqual(expected, self.configuration.direction)

        # both
        self.configuration.reset()
        value = 'bi-curious'
        expected = 'both'
        self.config_parser.get.return_value = value
        self.assertEqual(expected, self.configuration.direction)

        # unknown
        with self.assertRaises(CameraobscuraError):
            self.configuration.reset()
            self.config_parser.get.return_value = 'vituperative'
            self.configuration.direction

        # option not given (use default)
        self.configuration.reset()
        self.config_parser.get.side_effect = ConfigParser.NoOptionError("direction",
                                                                        'traffic')
        self.assertEqual(IperfEnum.default_direction, self.configuration.direction)
        return

    def test_client_settings(self):
        """
        Does it build an IperfClientSettings object?
        """
        section = random.choice('iperf traffic'.split())
        client_options = 'time len window parallel'.split()
        options = ['direction'] + client_options
        
        values = ['both', 999, '1470', '256K', 5]
        configuration = "\n".join(["{0}={1}".format(options[index], values[index]) for index in xrange(len(options))])
        configuration = "[{0}]\n{1}".format(section, configuration)
        parameters = dict(zip(options, values))

        parser = ConfigParser.SafeConfigParser()
        parser.readfp(io.BytesIO(configuration))
        
        self.config_adapter.config_parser = parser

        settings = self.configuration.client_settings

        for option in client_options:
            self.assertEqual(parameters[option], settings.get(option))
        return

    def test_server_settings(self):
        """
        Does it build an IperfServerSettings object?
        """
        section = random.choice('iperf traffic'.split())
        server_options = 'daemon udp nodelay'.split()
        options = ['direction'] + server_options
        values = ['down', 'True', 'true', 'false']

        configuration = "\n".join(["{0}={1}".format(options[index], values[index]) for index in xrange(len(options))])
        configuration = "[{0}]\n{1}".format(section, configuration)

        parameters = dict(zip(server_options, ('', '', None)))

        parser = ConfigParser.SafeConfigParser()
        parser.readfp(io.BytesIO(configuration))
        
        self.config_adapter.config_parser = parser
        settings = self.configuration.server_settings

        for option in server_options:
            self.assertEqual(parameters[option], settings.get(option))
        return

# end TestIperfConfiguration    

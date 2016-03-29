
# python standard library
import unittest
from cStringIO import StringIO
import socket
import random
import ConfigParser

# third-party
from mock import Mock, MagicMock, mock_open, patch

# this package
from cameraobscura import CameraobscuraError
from cameraobscura.utilities.configurationadapter import ConfigurationAdapter
from cameraobscura.utilities.dump import TheDump, DumpConstants, DumpConfiguration
from cameraobscura.tests.helpers import random_string_of_letters


class TestDump(unittest.TestCase):
    def setUp(self):
        self.identifier = random_string_of_letters(5)
        self.host = Mock()
        self.command = random_string_of_letters(10)
        self.filename = random_string_of_letters(5)
        self.timeout = random.randrange(1, 100)
        self.dump = TheDump(command=self.command,
                            identifier=self.identifier,
                            connection=self.host,
                            filename=self.filename,
                            timeout=self.timeout)
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        # missing required parameters 
        with self.assertRaises(TypeError):
            TheDump()

        # constructor assigns properties as expected
        self.assertEqual(self.command, self.dump.command)
        self.assertEqual(self.host, self.dump.connection)
        self.assertEqual(self.filename, self.dump.filename)
        self.assertEqual(self.timeout, self.dump.timeout)

        # filename default
        host_string = random_string_of_letters()
        host = MagicMock()
        host.__str__.return_value = host_string
        expected = "{0}_dump_{1}.txt".format(host_string,
                                        self.command)

        dump = TheDump(connection=host, command=self.command)
        self.assertEqual(expected, dump.filename)

        # timeout default
        self.assertEqual(dump.timeout, DumpConstants.default_timeout)
        return

    def test_call(self):
        """
        Does it send the command to the host and save the ouput?
        """
        # setup the mocks
        logger = Mock()
        self.dump._logger = logger
        open_file = mock_open()

        # fake values
        output = random_string_of_letters()
        error = random_string_of_letters()
        timeout = random.randrange(1, 100)
        self.dump.timeout = timeout
        self.host.exec_command.return_value = (None, StringIO(output), StringIO(error))

        # the call
        with patch('__builtin__.open', open_file):
            self.dump()

        # the tests
        open_file.assert_called_with(self.filename, 'w')
        handle = open_file()
        self.host.exec_command.assert_called_with(self.command, timeout=timeout)
        handle.write.assert_called_with(output)
        logger.error.assert_called_with(error)
        return

    def test_timeout(self):
        """
        Does it catch socket timeouts and log the error?
        """
        self.host.exec_command.side_effect = socket.timeout
        open_file = mock_open()
        with patch('__builtin__.open', open_file):
            self.dump()
        return
# end class TestDump


class TestDumpConfiguration(unittest.TestCase):
    def setUp(self):
        self.config_parser = Mock()
        self.config_adapter = ConfigurationAdapter(self.config_parser)
        self.configuration = DumpConfiguration(configuration=self.config_adapter)
        return

    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.configuration.section, DumpConstants.section)
        self.assertEqual(self.configuration.example, DumpConstants.example)
        return

    def test_timeout(self):
        """
        Does it get the timeout correctly?
        """
        expected = random.randrange(1, 100)
        self.config_parser.getfloat.return_value = expected
        self.assertEqual(self.configuration.timeout, expected)

        # bad timeout
        self.configuration.reset()
        self.config_parser.getfloat.return_value = -1
        with self.assertRaises(CameraobscuraError):
            self.configuration.timeout

        # default
        self.configuration.reset()
        self.config_parser.getfloat.side_effect = ConfigParser.NoOptionError('timeout',
                                                                              'dump')
        self.assertEqual(DumpConstants.default_timeout,
                         self.configuration.timeout)
        return

    def test_fields(self):
        """
        Does it get the fields (command identifiers)?
        """
        expected = 'a b c'.split()
        self.config_parser.options.return_value = ['timeout'] + expected
        self.assertEqual(expected, self.configuration.fields)
        return

    def test_commands(self):
        """
        Does it get the commands to send to the device?
        """
        lines = random.randrange(1, 10)
        identifiers = [random_string_of_letters(5) for line in xrange(lines)]
        commands = [random_string_of_letters(5) for line in xrange(lines)]
        self.config_parser.options.return_value = identifiers

        output = dict(zip(identifiers, commands))
        
        def side_effect(*args):
            return output[args[-1]]
        
        self.config_parser.get.side_effect = side_effect
        self.assertEqual(commands, self.configuration.commands)
# end TestDumpConfiguration    

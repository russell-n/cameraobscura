
# python standard library
import unittest
import random
import re
from cStringIO import StringIO
import socket

# third-party
from mock import Mock

# this package
from cameraobscura import CameraobscuraError
from cameraobscura.commands.command.command import TheCommand, CommandConstants
from cameraobscura.tests.helpers import random_string_of_letters


class TestTheCommand(unittest.TestCase):
    def setUp(self):
        self.connection = Mock()
        self.identifier = random_string_of_letters(10)
        self.command_string = random_string_of_letters(10)
        self.arguments = random_string_of_letters(5)
        self.timeout = random.randrange(1, 100)
        self.trap_errors = random.choice((True, False))
        self.data_expression = random_string_of_letters(5)
        self.error_expression = random_string_of_letters(5)
        self.not_available = random_string_of_letters(5)
        
        self.command = TheCommand(connection=self.connection,
                                  command=self.command_string,
                                  arguments=self.arguments,
                                  timeout=self.timeout,
                                  identifier=self.identifier,
                                  trap_errors=self.trap_errors,
                                  data_expression=self.data_expression,
                                  error_expression=self.error_expression,
                                  not_available=self.not_available)
        return

    def test_constructor(self):
        """
        Does it build correctly?
        """
        self.assertEqual(self.connection, self.command.connection)
        self.assertEqual(self.command_string, self.command.command)
        self.assertEqual(self.arguments, self.command.arguments)
        self.assertEqual(self.timeout, self.command.timeout)
        self.assertEqual(self.identifier, self.command.identifier)
        self.assertEqual(self.trap_errors, self.command.trap_errors)
        self.assertEqual(re.compile(self.data_expression), self.command.data_expression)
        self.assertEqual(re.compile(self.error_expression), self.command.error_expression)
        self.assertEqual(self.not_available, self.command.not_available)
        return

    def test_defaults(self):
        """
        Does it set the default constructor arguments as expected?
        """
        command_string = random_string_of_letters(5)
        mixed_command = "{0} {1}".format(command_string,
                                         random_string_of_letters(5))
        command = TheCommand(connection=self.connection,
                             command=mixed_command)
        self.assertIsNone(command.arguments)
        self.assertEqual(command_string, command.identifier)
        self.assertEqual(CommandConstants.default_timeout, command.timeout)
        self.assertTrue(command.trap_errors)
        self.assertEqual(re.compile('(.*)'), command.data_expression)
        self.assertEqual(re.compile(CommandConstants.default_error_expression),
                         command.error_expression)
        self.assertIsNone(command.not_available)
        return

    def test_expressions(self):
        """
        Do the default expressions work?
        """
        # does it match anything
        test = random_string_of_letters()
        self.command.data_expression = None
        match = self.command.data_expression.search(test)
        self.assertEqual(match.groups()[0], test)

        self.command.error_expression = None
        self.assertIsNone(self.command.error_expression.search(test))
        return

    def test_command_arguments(self):
        """
        Does it create a composite command, arguments string?
        """
        # both set by user
        self.assertEqual("{0} {1}\n".format(self.command_string,
                                            self.arguments),
                                            self.command.command_arguments)

        # arguments eliminated
        self.command.arguments = None
        self.assertEqual(self.command_string + '\n',
                         self.command.command_arguments)

        # command changed
        new_command = random_string_of_letters()
        self.command.command = new_command
        self.assertEqual(new_command + '\n',
                         self.command.command_arguments)

        # arguments re-set
        arguments = random_string_of_letters()
        self.command.arguments = arguments
        self.assertEqual("{0} {1}\n".format(new_command,
                                            arguments),
                                            self.command.command_arguments)
        return
    
    def test_call(self):
        """
        Does it work as we expect it to?
        """
        # normal output
        prefix = random_string_of_letters()
        expected = random_string_of_letters()
        expression = "{0}:\s({1})".format(prefix, expected)
        output = "{0}: {1}\n".format(prefix, expected)
        self.command.data_expression = expression
        
        self.connection.exec_command.return_value = None, StringIO(output), StringIO('')
        result = self.command()
        self.connection.exec_command.assert_called_with("{0} {1}\n".format(self.command_string,
                                                                           self.arguments),
                                                                           timeout=self.timeout)
        self.assertEqual(expected, result)

        # no match, no error
        output = random_string_of_letters()
        self.connection.exec_command.return_value = None, output, ''
        self.assertEqual(self.command(), self.not_available)
        return

    def test_bad_data_expression(self):
        """
        Does it raise a CameraobscuraError if the expression matches but there's no group?
        """
        expected = random_string_of_letters()
        expression = expected
        self.command.data_expression = expression
        self.connection.exec_command.return_value = None, StringIO(expected), ''
        with self.assertRaises(CameraobscuraError):
            self.command()
        return

    def test_timeout(self):
        """
        Does it raise a CameraobscuraError if there's a timeout and trap_errors not set?
        """
        # catch the errors
        self.command.trap_errors = True
        self.connection.exec_command.side_effect = socket.timeout
        self.command()

        # don't catch the errors
        self.command.trap_errors = False
        with self.assertRaises(CameraobscuraError):
            self.command()
        return

    def test_error_match(self):
        """
        Does it raise an error if the error_expression matches a line of stderr?
        """
        message = random_string_of_letters()
        prefix = random_string_of_letters()
        expression = "{0}\s*--\s*({1})".format(prefix, message)
        output = "{0} -- {1}\n".format(prefix, message)
        self.command.error_expression = expression
        self.connection.exec_command.return_value  = None, '', StringIO(output)
        with self.assertRaises(CameraobscuraError):
            self.command()
        return

    def test_not_available(self):
        """
        Does it return the right not-available value if the data doesn't match?
        """
        self.connection.exec_command.return_value = None, '', ''
        self.assertEqual(self.not_available, self.command())

        self.connection.exec_command.side_effect = socket.timeout
        self.command.trap_errors = True
        self.assertEqual(self.not_available, self.command())
        return
# end TestTheCommand    

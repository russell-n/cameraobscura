
# python standard library
import re
import socket

# this package
from cameraobscura import CameraobscuraError
from cameraobscura import BaseClass


START_OF_STRING = r'^'
ANYTHING = r'.'
ZERO_OR_MORE = r'*'
GROUP = r'({0})'

EVERYTHING = GROUP.format(ANYTHING + ZERO_OR_MORE)
NOTHING = r'a' + START_OF_STRING
NEWLINE = '\n'

class CommandConstants(object):
    """
    Constants for the Command
    """
    __slots__ = ()
    # defaults
    default_arguments = ''
    default_timeout = 5
    default_trap_errors = True
    default_data_expression = EVERYTHING
    default_error_expression = NOTHING


def socketerrors(method,  *args, **kwargs):
    """
    Traps errors if self.trap_errors is true, raises CameraobscuraErrors otherwise

    also expects that the object has connection,logger, not_available attributes

    :param:

     - `method`: method instance
    """
    def wrapped(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except socket.error as error:
            message = "{e}: Error with connection to {c}".format(c=self.connection,
                                                                 e=type(error))
            self.logger.error(message)
            if not self.trap_errors:
                raise CameraobscuraError("Problem with connection executing '{0}'".format(self.command_arguments))
            return self.not_available
    return wrapped


class TheCommand(BaseClass):
    """
    Command to get output from a device
    """
    def __init__(self, connection, command,
                 data_expression=None,
                 error_expression=None,
                 arguments=None,
                 identifier=None,
                 timeout=CommandConstants.default_timeout,
                 trap_errors=CommandConstants.default_trap_errors,
                 not_available=None):
        """
        The Command constructor

        :param:

         - `identifier`: string to identify this object
         - `connection`: Connection to send command to
         - `command`: string to send to the connection
         - `data_expression` regular expression to get data from command output
         - `error_expression`: regular expression to match fatal errors
         - `arguments`: string of arguments to add to the command
         - `timeout`: seconds to wait for output from device
         - `trap_errors`: if True, log but don't raise socket errors
         - `not_available`: What to return if data not matched in output
        """
        super(TheCommand, self).__init__()
        self.connection = connection
        self._command = None
        self.command = command
        self._arguments = None
        self.arguments = arguments
        self._data_expression = None
        self.data_expression = data_expression
        self._error_expression = None
        self.error_expression = error_expression

        self.timeout = timeout
        self._identifier = identifier
        self.trap_errors = trap_errors
        self._command_arguments = None
        self.not_available = not_available
        return

    @property
    def command(self):
        """
        String to send to the connection
        """
        return self._command

    @command.setter
    def command(self, cmd):
        """
        sets the command, resets the command_arguments
        """
        self._command = cmd
        self._command_arguments = None
        return

    @property
    def arguments(self):
        """
        arguments for the command (separated so they can be updated separately)
        """
        return self._arguments

    @arguments.setter
    def arguments(self, args):
        """
        sets the arguments, resets the command_arguments

        :param:

         - `args`: string of arguments for the command or None
        """
        self._arguments = args
        self._command_arguments = None
        return

    @property
    def command_arguments(self):
        """
        A compilation of command and arguments (with newline appended)
        """
        if self._command_arguments is None:
            suffix = NEWLINE
            if self.arguments is not None:
                suffix = " {0}{1}".format(self.arguments, suffix)
            self._command_arguments = "{0}{1}".format(self.command, suffix)
        return self._command_arguments

    @property
    def data_expression(self):
        """
        compiled regular expression to extract data from the command output
        """
        if self._data_expression is None:
            self._data_expression = re.compile(CommandConstants.default_data_expression)
        return self._data_expression

    @data_expression.setter
    def data_expression(self, regex):
        """
        compiles and sets the regular expression

        :param:

         - `regex`: regular expression to get data from the output
        """
        if regex is not None:
            regex = re.compile(regex)
        self._data_expression = regex
        return

    @property
    def error_expression(self):
        """
        regular expression -- if matched, raise Exception
        """
        if self._error_expression is None:
            self._error_expression = re.compile(CommandConstants.default_error_expression)
        return self._error_expression

    @error_expression.setter
    def error_expression(self, regex):
        """
        Compiles and sets the error_expression

        :param:

         - `regex`: regular expression to find fatal errors
        """
        if regex is not None:
            regex = re.compile(regex)
        self._error_expression = regex
        return

    @property
    def identifier(self):
        """
        A string identifier to distinguish this command

         * Uses the first token in the command-string if not set
        """
        if self._identifier is None:
            self._identifier = self.command.split()[0]
        return self._identifier

    @socketerrors
    def __call__(self):
        """
        Sends the command to the connection and extracts data from the output

        :raise: CameraobscuraError if data matched but no group found
        """
        stdin, stdout, stderr = self.connection.exec_command(self.command_arguments,
                                                             timeout=self.timeout)
        data = self.not_available
        for line in stdout:
            self.logger.debug(line)
            match = self.data_expression.search(line)
            if match:
                try:
                    data = match.groups()[0]
                except IndexError as error:
                    self.logger.error(error)
                    raise CameraobscuraError("Data Expression '{0}' missing group to extract data".format(self.data_expression))
                self.logger.debug("Matched: {0}".format(data))
                break
                
        for line in stderr:
            self.logger.error(line)
            if self.error_expression.search(line):
                raise CameraobscuraError("Fatal Error: '{0}' running command '{1}1".format(line,
                                                                                        self.command_arguments))
        return data
# end class TheCommand

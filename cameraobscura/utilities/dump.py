
# python standard library
import logging
import socket
import textwrap

# third-party
from theape.parts.connections.clientbase import suppresssocketerrors

# this package
from cameraobscura import  CameraobscuraError

from cameraobscura.common.baseconfiguration import BaseConfiguration

WRITEABLE = 'w'

class DumpConstants(object):
    """
    Constants for the Dump
    """
    __slots__ = ()
    # defaults
    default_timeout = 5
    default_delimiter = ','

    # configuration
    section = 'dump'

    # options
    timeout = 'timeout'
    
    example = textwrap.dedent("""
#[{s}]
# the dump takes commands that dump their output and saves
# the output to files. It is mainly intended as a log dump
# comment this section out if you don't want a dump
    
# timeout is how long to wait for output
# timeout = {time}

# for the commands you should use the form:
# <identifier_1> = <command_1>
# <identifier_2> = <command_2>
# ...
# <identifier_n> = <command_n>

# the identifiers can be anything as long as each is unique
# the command should be the actual string you want to send to the device
# as an example for 'dmesg':
# dump = dmesg -k
    """.format(s=section,
               time=default_timeout))
    
# end DumpConstants

class TheDump(object):
    """
    The Dump dumps the output of a command to a file
    """
    def __init__(self, command, connection, identifier=None, filename=None,
                 timeout=DumpConstants.default_timeout):
        """
        TheDump's Constructor

        :param:

         - `command`: the command (string) to send to the device to get output
         - `identifier`: string to identify this object
         - `connection`: connection to the device with an `exec_command` method
         - `filename`: Name for output file
         - `timeout`: Readline timeout (seconds)
        """
        super(TheDump, self).__init__()
        self._logger = None
        self._identifier = identifier
        self.command = command
        self.connection = connection
        self.timeout = timeout
        self._filename = filename
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
    def identifier(self):
        """
        String to identify this dump
        """
        if self._identifier is None:
            self._identifier = 'dump'
        return self._identifier

    @property
    def filename(self):
        """
        Name to use for file to dump command output to

        If not set by user uses '<host-str>_<identifier>_<command 1st token>.txt'

        :rtype: StringType
        :return: filename for output
        """
        if self._filename is None:
            self._filename = "{0}_{1}_{2}.txt".format(self.connection,
                                                      self.identifier,
                                                      self.command.split()[0])
        return self._filename

    @suppresssocketerrors
    def __call__(self):
        """
        runs the command and saves it to the file
        """
        with open(self.filename, WRITEABLE) as output_file:
            stdin, stdout, stderr = self.connection.exec_command(self.command,
                                                                 timeout=self.timeout)
            for line in stdout:
                output_file.write(line)
                
            for line in stderr:
                if line:
                    self.logger.error(line)
        return

    def __str__(self):
        return "{0}: {1}".format(self.identifier, self.command)
# end class TheDump

class DumpConfiguration(BaseConfiguration):
    """
    A configuration for the dump
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor for the DumpConfiguration
        """
        super(DumpConfiguration, self).__init__(*args, **kwargs)
        self._timeout = None
        self._fields = None
        self._commands = None
        return

    @property
    def section(self):
        """
        The expected section name in the configuration file
        """
        if self._section is None:
            self._section = DumpConstants.section
        return self._section

    @property
    def example(self):
        """
        An example string for the user to copy
        """
        if self._example is None:
            self._example = DumpConstants.example
        return self._example

    @property
    def timeout(self):
        """
        The readline-timeout value

        :raise: CameraobscuraError if timeout is <= 0
        """
        if self._timeout is None:
            self._timeout = self.configuration.getfloat(section=self.section,
                                                        option=DumpConstants.timeout,
                                                        optional=True,
                                                        default=DumpConstants.default_timeout)
            if self._timeout <= 0:
                raise CameraobscuraError("timeout must be positive, not {0}".format(self._timeout))
        return self._timeout

    @property
    def fields(self):
        """
        list of identifiers for the commands
        """
        if self._fields is None:
            self._fields = [option for option in self.configuration.options(self.section)
                            if option != DumpConstants.timeout]
        return self._fields

    @property
    def commands(self):
        """
        list of commands to send to the device
        """
        if self._commands is None:
            self._commands = [self.configuration.get(self.section, option) for option in self.fields]
        return self._commands

    def check_rep(self):
        """
        Checks the values for validity
        """
        super(DumpConfiguration, self).check_rep()
        return

    def reset(self):
        """
        Resets the values
        """
        self._timeout = None
        self._commands = None
        self._fields = None
        return
# end class DumpConfiguration

# python Libraries
import telnetlib
import re
from cStringIO import StringIO
import random
import string

# this package
from cameraobscura import CameraobscuraError, BaseClass
from clientbase import BaseClient


NEWLINE = '\n'
EOF = EMPTY_STRING = ''
TIMEOUT = -1
MATCH = 0
OUTPUT_STRING = 2


class TelnetClient(BaseClient):
    """
    A TelnetClient Adapts the telnetlib.Telnet to match the SimpleClient
    """
    def __init__(self, prompt=None, password=None, end_of_line='\r\n',
                 login_prompt="login:", password_prompt='Password:', *args, **kwargs):
        """
        :param:

         - `hostname`: The address of the telnet server
         - `username`: The login username (if needed)
         - `password`: if given tries to login
         - `prompt`: The prompt used on the device (if not given will set a random prompt)
         - `end_of_line`: The end of line string used by the device.
         - `login_prompt`: The prompt to look for when starting a connection.
         - `port`: TCP port (default = 23)
         - `password_prompt`: regular expression to match a prompt for a password
        """
        super(TelnetClient, self).__init__(*args, **kwargs)
        self._prompt = prompt
        self.password = password
        self.end_of_line = end_of_line
        self.password_prompt = password_prompt
        self.login_prompt = login_prompt
        return

    @property
    def prompt(self):
        """
        The prompt -- if not given creates a random string 
        """
        if self._prompt is None:
            characters = xrange(random.randrange(5, 10))
            self._prompt =  "".join((random.choice(string.letters) for character in characters))
        return self._prompt

    @property
    def port(self):
        """
        The TCP Port
        """
        if self._port is None:
            self._port = 23
        return self._port

    @port.setter
    def port(self, new_port):
        """
        Sets the port value

        :param:

         - `new_port`: port number

        :raise: CameraobscuraError if new_port can't be cast to int
        """
        if new_port is not None:
            try:
                self._port = int(new_port)
            except ValueError as error:
                self.logger.error(error)
                raise CameraobscuraError("Invalid port: {0}".format(new_port))
        else:
            self._port = new_port
        return
            
    @property
    def client(self):
        """
        Tries to login before returning.

        :rtype: telnetlib.Telnet
        :return: The telnet client
        :raise: CameraobscuraError if login or password required but not found or unable to match prompt
        """
        if self._client is None:            
            self._client = telnetlib.Telnet(host=self.hostname,
                                            port=self.port,
                                            timeout=self.timeout)
            self.login(self._client)
        return self._client

    def login(self, client):
        """
        Tries to login based on what it sees in the output

        This is actually more of a serial-login (where you don't have new pty's)

        :param:

         - `client`: A Telnet connected to the device

        :postcondition: client is logged in to the device
        :raise: CameraobscuraError if unable to login
        """
        # setup search
        # the ordering is important -- we want to remove already matched strings
        # without changing the index for the remaining
        # this is so that we can avoid false-positives if the client coincidentally
        # emits a string that matches but isn't meant to mean what we think
        # e.g. the banner message 'Last login: <timestamp>' will match our login search
        # but it actually only appears if we've already logged in
        expected = [self.prompt,  self.password_prompt, self.login_prompt]
        PROMPT, PASSWORD, LOGIN = range(len(expected))

        # try to match something
        # output is a tuple:
        # (index of matching expression, matching expression, string read in up to match)
        output = client.expect(expected, timeout=self.timeout)

        if output[MATCH] == LOGIN:
            # we watched the login prompt
            if self.username is None:
                raise CameraobscuraError("Login to {0} required".format(self))
            self.logger.info("Logging in with username: {0}".format(self.username))
            self.logger.debug(output[OUTPUT_STRING])
            
            client.write(self.username + NEWLINE)
            # get rid of the login expression
            # this might not be needed once things get tested more
            expected = expected[:-1]
            # read what comes after the match
            output = client.expect(expected, timeout=self.timeout)

        if output[MATCH] == PASSWORD:
            # password prompt matched
            if self.password is None:
                raise CameraobscuraError("Password required to login to {0}".format(self)) 
            self.logger.info('Logging in with password: {0}'.format(self.password))
            self.logger.debug(output[OUTPUT_STRING])
            client.write(self.password + NEWLINE)
            # get rid of the password-expression
            expected = expected[:-1]
            # read what comes after the password prompt
            output = client.expect(expected, timeout=self.timeout)

        if output[MATCH] == PROMPT:
            # if this was reached the user's prompt must have worked (not a random string)
            self.logger.info("Logged In")
            self.logger.debug(output[OUTPUT_STRING])
                
        elif output[MATCH] == TIMEOUT:
            # even though it's an elif, if the expected expressions only have one value
            # then this should be the only alternative
            # but I'm leaving in the conditional so it's more obvious what this means
            # nothing matched, assume the prompt missed
            self.logger.debug("nothing matched, mangling the prompt")
            self.logger.debug(output[OUTPUT_STRING])
            self.set_prompt(client)
        return
    
    def set_prompt(self, client):
        """
        Tries to set the PS1 environmental variable to the current prompt

        :param:

        - `client`: connected telnet client

        :raise: CameraobscuraError if doesn't seem to have set the prompt
        """
        # expect 2 matches -- one when you set the prompt and one when the next prompt comes up
        matches, expected = 0, 2
        client.write("PS1='{0}'\n".format(self.prompt))
        expressions = [self.prompt]
        for trial in xrange(expected):
            # output is a tuple (index of matching expression, matching expression, string read in before match)
            output = client.expect(expressions, timeout=self.timeout)
            self.logger.debug(output[OUTPUT_STRING])
            matches += output[MATCH]
        # matches is the sum of indices of matching expressions (so 0 if both matched,
        # -1 for each time it timed out)
        if matches < 0:
            raise CameraobscuraError("Unable to set the prompt to '{0}'".format(self.prompt))
        return

    def exec_command(self, command, timeout=None):
        """
        The main interface.

        Since I'm hiding the client from users, this will do a read_very_eager before continuing.
        The read is intended to try and flush the output

        :param:

         - `command`: The command to execute on the device
         - `timeout`: The readline timeout

        :return: TelnetOutput with the this object's as client
        """
        self.client.timeout = timeout
        command = command.rstrip('\n')
        self.logger.debug("Existing output: " + self.client.read_very_eager())
        self.writeline(command)

        # eat up the command itself so it's not in the output

        # this was put here because Host.kill_all is checking for the name of the command in the output
        # I think the kill-all has to be made smarter instead
        # but in the meantime...
        # it looks like there are strange escape codes entering the output so the complete string won't always match
        # I think it happens if the command is too long (as with iperf with a lot of options)
        # Instead I'll assume the command and last option with anything in between should match
        tokens = command.split()
        expression = "{0}.*\r\n".format(tokens[0])
            
        output = self.client.expect([expression, '\r\n'], timeout=timeout)
        self.logger.debug(output)
        return (None, TelnetOutput(client=self.client, prompt=self.prompt,
                                   timeout=timeout, end_of_line=self.end_of_line),
                                   StringIO(''))
                                   
    def writeline(self, message=""):
        """
        :param:

         - `message`: A message to send to the device.
        """
        self.client.write(message + NEWLINE)
        self.logger.debug("'{0}' written to the connection".format(message))
        return
            
    def __del__(self):
        """
        Closes the client (if it exists)
        """
        #self.close()
        return

# end class TelnetClient


MATCH_INDEX = 0
MATCHING_STRING = 2
TIMEOUT_INDEX = -1


class TelnetOutput(BaseClass):
    """
    The TelnetOutput converts the telnet output to a file-like object
    """
    def __init__(self, client, prompt="#", end_of_line='\r\n',timeout=10):
        """
        :param:

         - `client` : a connected telnet client
         - `prompt`: The current prompt on the client
         - `end_of_line`: Then end of line character
         - `timeout`: The readline timeout
        """
        super(TelnetOutput, self).__init__()
        self.client = client
        self.prompt = prompt
        self.end_of_line = end_of_line
        self.timeout = timeout
        self.endings = [end_of_line, prompt]
        self.line_ending_index = 0
        self.prompt_index = 1
        self.finished = False
        return

    def readline(self):
        """
        Reads a single line of output
        
        :param:

         - `timeout`: The readline timeout
         
        :return: The next line of text
        """
        self.logger.debug("calling expect with endings: {0} and timeout: {1}".format(self.endings,
                                                                                         self.timeout))
        try:
            output = self.client.expect(self.endings, self.timeout)
        except AttributeError as error:
            self.logger.debug(error)
            self.logger.debug('client already closed?')
            return EOF

        if output[MATCH_INDEX] == self.prompt_index:
            # matched the prompt, this output is finished
            self.logger.debug("Stopping on : " + output[MATCHING_STRING])
            return EOF
        if output[MATCH_INDEX] == self.line_ending_index:
            self.logger.debug("Matched line ending")
            return output[MATCHING_STRING]
        if output[MATCH_INDEX] == TIMEOUT_INDEX:
            # should this be an end of file?
            self.logger.warning("Output timed out without reaching the prompt")
            return EOF
        else:
            # this should never be reached -- something bad has happened
            self.logger.error(output)
            raise CameraobscuraError("There is a bug in the TelnetOutput. So sad.")
        return 

    def next(self):
        """
        A generator of output lines
        
        :yield: the next line
        """
        line = None
        while line is not EOF:
            line = self.readline()
            yield line
        return

    def readlines(self):
        """
        Reads all the lines
        
        :return: A list of lines
        """
        lines = []
        line = None
        while line is not EOF:
            line = self.readline()
            lines.append(line)
        return lines

    def read(self):
        """
        Same as readlines but joins the lines into a string
        
        :return: String of output
        
        """
        return EMPTY_STRING.join(self.readlines())

    def __iter__(self):
        """
        The main interface, traverses output line by line
        """
        return self.next()
# end class TelnetOutput

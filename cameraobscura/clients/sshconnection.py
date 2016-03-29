
# The MIT License (MIT)
# 
# Copyright (c) 2013 Russell Nakamura
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# python standard library
from collections import namedtuple
import threading

# third party
import paramiko

# this package
from theape import BaseClass
from cameraobscura import CameraobscuraError

SEMICOLON_JOIN = "{0};{1}"
SUDO = "sudo {0}"
ADD_NEWLINE = "{0}\n"
SPACE_JOIN = "{0} {1}"

class SSHConnection(BaseClass):
    def __init__(self, hostname, username, prefix=None, password=None, port=22,
                 compress=False, key_filename=None, timeout=None):
        """
        SSHConnection constructor

        :param:

         - `hostname`: the IP address or resolvable host-name
         - `username`: the login username
         - `password`: the password for the device (optional if public-keys set)
         - `prefix`: string to add as a prefix to the commands
         - `port`: the port for the service
         - `compress`: if True, gzip the connection
         - `key_filename`: file-name or list of file-names for public-keys
         - `timeout`: seconds to wait for login before raising a socket.timeout         
        """
        super(SSHConnection, self).__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.prefix = prefix
        self.port = port
        self.compress = compress
        self.key_filename = key_filename
        self.timeout = timeout
        self._client = None
        self._lock = None
        return

    @property
    def client(self):
        """
        an SSHClient instance

        :raise: ApeError for paramiko and socket exceptions
        :rtype: SSHClient
        :return: SSH Client with the constructor's parameters
        """
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                self._client.connect(hostname=self.hostname,
                                 username=self.username,
                                 port=self.port,
                                 password=self.password,
                                 key_filename=self.key_filename,
                                 compress=self.compress,
                                 timeout=self.timeout)
            except paramiko.PasswordRequiredException as error:
                self.log_error(error)
                raise CameraobscuraError("{u}@{h} Public keys not working".format(u=self.username,
                                                                        h=self.hostname))
            except paramiko.AuthenticationException as error:
                self.log_error(error)
                raise CameraobscuraError("Password: {p} for {u}@{h} not accepted".format(p=self.password,
                                                                               u=self.username,
                                                                               h=self.hostname))
            except paramiko.SSHException as error:
                self.log_error(error)
                raise CameraobscuraError('{u}@{h} with password {p} raised "{e}"'.format(u=self.username,
                                                                               h=self.hostname,
                                                                               p=self.password,
                                                                               e=error))
            except IOError as error:
                self.log_error(error)
                if 'No route to host' in str(error) or 'Network is unreachable' in str(error):
                    raise CameraobscuraError("{h} unreachable from this machine.".format(h=self.hostname))
                if 'Connection refused' in str(error):
                    raise CameraobscuraError("{u}@{h} refused connection (is the ssh-server running?)".format(u=self.username,
                                                                                                     h=self.hostname))
                if 'timed out' in str(error):                    
                    raise CameraobscuraError("Unable to connect to {u}:{h} within {t} seconds (timed out)".format(u=self.username,
                                                                                                        h=self.hostname,
                                                                                                        t=self.timeout))
                raise CameraobscuraError('({e}) connecting to {u}@{h}'.format(e=error,
                                                                     u=self.username,
                                                                     h=self.hostname))

        return self._client

    def sudo(self, command, password, timeout=None):
        """
        A convenience method to hide what's needed to run as root

        :param:

         - `command`: command to run (without the 'sudo' keyword)
         - `password`: the sudoer's password
         - `timeout`: Amount of time to wait for the connection to respond

        :return: InOutError named tuple
        """
        in_out_error = self(SUDO.format(command),
                            get_pty=True)
        in_out_error.input.write(ADD_NEWLINE.format(password))
        return in_out_error


    def __call__(self, command, bufsize=-1, timeout=None, get_pty=False):
        """
        a secondary interface to allow more arbitrary input

        :param:

         - `command`: string with command to send over the ssh-connection
         - `bufsize`: bytes to set for the buffer
         - `timeout`: seconds for channel timeout
         - `get_pty`: needed for interactive things (like sending the sudo password)
        """
        if self.prefix is not None:
            command = SPACE_JOIN.format(self.prefix, command)
        with self.lock:
            stdin, stdout, stderr = self.client.exec_command(command, bufsize=bufsize,
                                                             timeout=timeout,
                                                             get_pty=get_pty)
        return InOutError(input=stdin, output=stdout, error=stderr)

    exec_command = __call__

    def __getattr__(self, command):
        """
        Calls the exec-command

        :param:

         - `command`: command to execute
         - `arguments`: string of arguments to add to the command
         - `bufsize`: buffer size
         - `timeout`: channel timeout
         - `get_pty`: If true sets up the pseudo-terminal
        """
        def procedure_call(arguments='', bufsize=-1, timeout=None, get_pty=False):
            return self(SPACE_JOIN.format(command, arguments), bufsize=bufsize, timeout=timeout, get_pty=get_pty)
        return procedure_call

    @property
    def lock(self):
        """
        A re-entrant lock that threaded users of the connection can use
        """
        if self._lock is None:
            self._lock = threading.RLock()
        return self._lock

    def close(self):
        """
        Closes the connection and sets SSHClient to None
        """
        self.client.close()
        self._client = None
        return
# end class SSHConnection

InOutError = namedtuple('InOutError', 'input output error'.split())
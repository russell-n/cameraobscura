
# python standard library
import socket

# third party
import paramiko

# this package
from cameraobscura.clients.clientbase import BaseClient
from cameraobscura import CameraobscuraError

class ConnectionError(CameraobscuraError):
    """
    A CameraobscuraError child specific to connection errors
    """
# end ConnectionError

PORT = 22
TIMEOUT = 10
NEWLINE = '\n'
SPACE_JOIN = "{prefix} {command}"

class SimpleClient(BaseClient):
    """
    A simple wrapper around paramiko's SSHClient.

    The only intended public interface is exec_command.
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `hostname`: ip address or resolvable hostname.
         - `username`: the login name.
         - `timeout`: Time to give the client to connect
         - `port`: TCP port of the server
         - `args, kwargs`: anything else that the SSHClient.connect can use will be passed in to it
        """
        super(SimpleClient, self).__init__(*args, **kwargs)
        self._client = None
        return

    @property
    def client(self):
        """
        The main reason for this class

        :rtype: paramiko.SSHClient
        :return: An instance of SSHClient connected to remote host.
        :raise: ClientError if the connection fails.
        """
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.load_system_host_keys()
            try:
                self._client.connect(hostname=self.hostname,
                                     username=self.username,
                                     timeout=self.timeout,
                                     port=self.port,
                                     **self.kwargs)

            # these are fatal exceptions, no one but the main program should catch them
            except paramiko.AuthenticationException as error:
                self.logger.error(error)
                raise CameraobscuraError("There is a problem with the ssh-keys or password for \n{0}".format(self))
            
            except paramiko.PasswordRequiredException as error:
                self.logger.error(error)
                self.logger.error("Private Keys Not Set Up, Password Required.")
                raise CameraobscuraError("SSH Key Error :\n {0}".format(self))

            except socket.timeout as error:
                self.logger.error(error)
                raise CameraobscuraError("Paramiko is unable to connect to \n{0}".format(self))
            
            except socket.error as error:
                self.logger.error(error)
                if 'Connection refused' in error: 
                    raise CameraobscuraError("SSH Server Not responding: check setup:\n {0}".format(self))
                raise CameraobscuraError("Problem with connection to:\n {0}".format(self))
        return self._client

    @property
    def port(self):
        """
        The TCP port
        """
        if self._port is None:
            self._port = 22
        return self._port

    @port.setter
    def port(self, new_port):
        """
        Sets the port (I tried putting this in the base but you can't split the setter and property definitions)

        :param:

         - `new_port`: integer port number
        :raise: CameraobscuraError if can't cast to int
        """
        if new_port is not None:
            try:
                self._port = int(new_port)
            except ValueError as error:
                self.logger.error(error)
                raise CameraobscuraError("Unable to set port to : {0}".format(new_port))
        else:
            self._port = new_port
        return

    def exec_command(self, command, timeout=TIMEOUT):
        """
        A pass-through to the SSHClient's exec_command.

        :param:

         - `command`: A string to send to the client.
         - `timeout`: Set non-blocking timeout.

        :rtype: tuple
        :return: stdin, stdout, stderr

        :raise: ConnectionError for paramiko or socket exceptions
        """
        if not command.endswith(NEWLINE):
            command += NEWLINE
        try:
            self.logger.debug("({0}) Sending to paramiko -- '{1}', timeout={2}".format(self,
                                                                                       command,
                                                                                       timeout))
            return self.client.exec_command(command, timeout=timeout)

        except socket.timeout:
            self.logger.debug("socket timed out")
            raise ConnectionError("Timed out -- Command: {0} Timeout: {1}".format(command,
                                                                     timeout))
        # this catches other socket errors so it should go after any other socket exceptions
        except (socket.error, paramiko.SSHException, AttributeError) as error:
            # the AttributeError is raised if no connection was actually made (probably the wrong IP address)
            self._client = None
            self.logger.error(error)
            raise CameraobscuraError("Problem with connection to:\n {0}".format(self))
        return
# end class SimpleClient

if __name__ == '__main__':
    import pudb;pudb.set_trace()
    client = SimpleClient('abc', 'def')
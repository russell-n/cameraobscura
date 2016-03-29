
# python standard library
import unittest
import random
import socket

# third-party
from mock import MagicMock, patch
import paramiko

# this package
from cameraobscura import CameraobscuraError
from cameraobscura.clients.simpleclient import SimpleClient, PORT, TIMEOUT, ConnectionError


class TestSimpleClient(unittest.TestCase):
    def setUp(self):
        self.p_client = MagicMock()
        self.hostname = 'aoeulrcg'
        self.username = 'bububububu'
        self.password = 'klrcheal'
        self.port = random.randrange(1000)
        self.timeout = random.randrange(1000)
        self.client = SimpleClient(hostname=self.hostname,
                                   username=self.username,
                                   password=self.password,
                                   port=self.port,
                                   timeout=self.timeout)
        self.client._client = self.p_client
        return
    
    def test_constructor(self):
        """
        Does it build correctly?
        """
        # hostname is requried (username taken out because of the serial, telnet case)
        #with self.assertRaises(TypeError):
        #    SimpleClient(hostname=self.hostname)
        with self.assertRaises(TypeError):
            SimpleClient(username=self.username)
            
        # defaults
        client = SimpleClient(hostname=self.hostname,
                              username=self.username)
        self.assertEqual(client.hostname, self.hostname)
        self.assertEqual(client.username, self.username)

        self.assertEqual(TIMEOUT, client.timeout)

        # non defaults
        self.assertEqual(self.client.hostname, self.hostname)
        self.assertEqual(self.client.username, self.username)
        self.assertEqual(self.client.kwargs['password'], self.password)
        self.assertEqual(self.client.port, self.port)
        self.assertEqual(self.timeout, self.client.timeout)
        return

    def test_exec_command(self):
        """
        Does it call the exec_command correctly?
        """
        command = 'arrrgh'
        self.client.exec_command(command)
        self.p_client.exec_command.assert_called_with(command + '\n', timeout=TIMEOUT)

        # what if there's an error?
        self.p_client.exec_command.side_effect = paramiko.SSHException("oops")
        with self.assertRaises(CameraobscuraError):
            try:
                self.client.exec_command(command)
            except ConnectionError:
                pass


        self.client._client = self.p_client
        self.p_client.exec_command.side_effect = socket.error("sockettome")
        with self.assertRaises(CameraobscuraError):
            try:
                self.client.exec_command(command)
            except ConnectionError:
                pass

        self.client._client = self.p_client
        self.p_client.exec_command.side_effect = socket.timeout("sockettome")
        with self.assertRaises(ConnectionError):
            self.client.exec_command(command)
        return

    def test_client(self):
        """
        Does it build the paramiko client like we'd expect?
        """
        self.client._client = None
        p_client = MagicMock()
        self.p_client.return_value = p_client
        auto_add_policy = MagicMock()
        auto_add_policy.return_value = 2
        with patch('paramiko.SSHClient', self.p_client):
            with patch('paramiko.AutoAddPolicy', auto_add_policy):
                client = self.client.client
                self.assertEqual(client, p_client)
                client.set_missing_host_key_policy.assert_called_with(2)
                client.load_system_host_keys.assert_called_with()
                client.connect.assert_called_with(hostname=self.hostname,
                                                  port=self.port,
                                                  username=self.username,
                                                  password=self.password,
                                                  timeout=self.timeout)
        # now check for errors
        self.client._client = None
        client_mock = MagicMock()
        self.p_client.return_value = client_mock
        with patch('paramiko.SSHClient', self.p_client):
            client_mock.connect.side_effect = paramiko.PasswordRequiredException("nononono")
            with self.assertRaises(CameraobscuraError):
                self.trap_connection_error(self.client)
                
            client_mock.connect.side_effect = paramiko.AuthenticationException("huh?")
            with self.assertRaises(CameraobscuraError):
                self.trap_connection_error(self.client)

            client_mock.connect.side_effect = socket.timeout('timeout')
            with self.assertRaises(CameraobscuraError):
                self.trap_connection_error(self.client)

            client_mock.connect.side_effect = socket.error('Connection refused')
            with self.assertRaises(CameraobscuraError):
                self.trap_connection_error(self.client)
                
            client_mock.connect.side_effect = socket.error('')
            with self.assertRaises(CameraobscuraError):
                self.trap_connection_error(self.client)
                
        return

    def trap_connection_error(self, simpleclient):
        simpleclient._client = None
        try:
            simpleclient.client
        except ConnectionError:
            pass

    def test_close(self):
        """
        Does it close and delete the client?
        """
        self.client.close()
        self.p_client.close.assert_called_with()
        self.assertIsNone(self.client._client)
        return

    def test_invoke_shell(self):
        """
        Does it call the client's invoke shell?
        """
        self.client.invoke_shell()
        self.p_client.invoke_shell.assert_called_with()
        return
# end TestSimpleClient    

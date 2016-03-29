
# python standard library
import unittest
import random

# third-party
from mock import MagicMock, patch, call, Mock

# this package
from cameraobscura import CameraobscuraError
from cameraobscura.clients.telnetclient import TelnetClient
from cameraobscura.tests.helpers import random_string_of_letters


class TestTelnetClient(unittest.TestCase):
    def setUp(self):
        self.hostname = random_string_of_letters()
        self.username = random_string_of_letters()
        self.timeout = random.randrange(100)
        self.password = random_string_of_letters(5)
        self.port = random.randrange(100)
        self.client = TelnetClient(hostname=self.hostname,
                                   username=self.username,
                                   timeout=self.timeout,
                                   password=self.password,
                                   port=self.port)
        self.telnet = MagicMock()
        self.client._client = self.telnet
        return
    
    def test_constructor(self):
        """
        Does it build correctly?
        """
        self.assertEqual(self.hostname, self.client.hostname)
        self.assertEqual(self.username, self.client.username)
        self.assertEqual(self.timeout, self.client.timeout)
        self.assertEqual(self.password, self.client.password)
        self.assertEqual(self.port, self.client.port)
        return

    def test_exec_command(self):
        """
        Does it implement an `exec_command` that looks like SimpleClient's exec_command?
        """
        # plain vanilla
        command = random_string_of_letters(5)
        stdin, stdout, stderr = self.client.exec_command(command)
        self.assertEqual(stdout.client, self.telnet)
        self.telnet.write.assert_called_with(command + '\n')
        return

    def test_mangle_prompt(self):
        """
        Does it mangle the prompt if not given?
        """
        # default for prompt is None
        self.assertIsNone(self.client._prompt)

        # if set, use the given
        prompt = random_string_of_letters()
        client = TelnetClient(hostname=None, prompt=prompt)
        self.assertEqual(prompt, client.prompt)

        # if not given, set a random prompt       
        randrange_mock = MagicMock()
        randrange_mock.return_value = len(prompt)

        choice_mock = MagicMock()
        prompt_source = list(prompt[:])

        def side_effect(*args): return prompt_source.pop(0)
        choice_mock.side_effect = side_effect
        
        with patch('random.randrange', randrange_mock):
                with patch('random.choice', choice_mock):
                        self.assertEqual(self.client.prompt, prompt)
        return

    def test_set_prompt(self):
        """
        Does it set the prompt on the device?
        """
        client = MagicMock()
        # successful setting of the prompt
        client.expect.return_value = (0, None, "blah")
        self.client.set_prompt(client)
        client.write.assert_called_with("PS1='{0}'\n".format(self.client.prompt))

        # unsuccessful
        client.expect.return_value = (-1, None, '')
        with self.assertRaises(CameraobscuraError):
            self.client.set_prompt(client)

        # unsuccessful case 2 (first match is us setting the variable,
        # second match would be the actual prompt being used        
        outputs = [(-1, None, ''), (0, None, '')]
        def side_effects(*args, **kwargs): return outputs.pop()
        client.expect.side_effect = side_effects
        with self.assertRaises(CameraobscuraError):
            self.client.set_prompt(client)
        return

    def test_login(self):
        """
        Does it follow the crazy login scheme?
        """
        # first case -- no match
        telnut = MagicMock()
        set_prompt = MagicMock()
        logger = MagicMock()
        mocks = (telnut, set_prompt, logger)
        telnut.expect.return_value = (-1, None, '')
        self.client.set_prompt = set_prompt
        self.client._logger = logger

        self.client.login(telnut)
        telnut.expect.assert_called_with([self.client.prompt,
                                          self.client.password_prompt,
                                          self.client.login_prompt],
                                              timeout=self.client.timeout)
        set_prompt.assert_called_with(telnut)

        # second case
        # match the first expression (the prompt)
        # this case doesn't really do anything since there's nothing to do
        for mock in mocks:
            mock.reset_mock()
        telnut.expect.return_value = (0, None, '')
        self.client.login(telnut)
        logger.info.assert_called_with('Logged In')

        # next case: login prompt
        for mock in mocks:
            mock.reset_mock()

        outputs = [(0, None, self.client.prompt), (2, None, 'login:')]
        def side_effects(*args, **kwargs): return outputs.pop()
        telnut.expect.side_effect = side_effects

        self.client.login(telnut)
        telnut.write.assert_called_with(self.client.username + '\n')
        expect_calls = [call([self.client.prompt, self.client.password_prompt, self.client.login_prompt], timeout=self.client.timeout),
                        call([self.client.prompt, self.client.password_prompt], timeout=self.client.timeout)]
        self.assertEqual(expect_calls, telnut.expect.mock_calls)

        # next case -- login and password
        for mock in mocks: mock.reset_mock()
        outputs = [(0, None, self.client.prompt), (1, None, 'Password:'), (2, None, "login:")]
        def side_effects(*args, **kwargs):
            return outputs.pop()
        telnut.expect.side_effect = side_effects
        self.client.login(telnut)
        write_calls = [call(self.client.username + '\n'), call(self.client.password + '\n') ]
        self.assertEqual(telnut.write.mock_calls, write_calls)
        expect_calls = [call([self.client.prompt, self.client.password_prompt, self.client.login_prompt], timeout=self.client.timeout),
                        call([self.client.prompt, self.client.password_prompt], timeout=self.client.timeout),
                        call([self.client.prompt], timeout=self.client.timeout)]
        self.assertEqual(expect_calls, telnut.expect.mock_calls)
        return

    def test_login_errors(self):
        """
        Does it raise errors if the user doesn't set required parameters?
        """
        # login required
        telnet = Mock()
        telnet.expect.return_value = (2, None, "login:")
        self.client.username = None
        with self.assertRaises(CameraobscuraError):
            self.client.login(telnet)

        # password required
        telnet.expect.return_value = (1, None, 'Password:')
        self.client.password = None
        with self.assertRaises(CameraobscuraError):
            self.client.login(telnet)
        return

    def test_client(self):
        """
        Does it build the client and try to login?
        """
        telnetlib = Mock()
        login = Mock()
        self.client.login = login
        self.client._client = None
        with patch('telnetlib.Telnet', telnetlib):
            client = self.client.client
        telnetlib.assert_called_with(host=self.client.hostname,
                                     port=self.client.port,
                                     timeout=self.client.timeout)
        login.assert_called_with(client)
        return

    def test_close(self):
        """
        Does it close the client?
        """
        telnet = Mock()
        self.client._client = telnet
        self.client.close()
        telnet.close.assert_called_with()
        self.assertIsNone(self.client._client)
        return
# end class TestTelnetClient    


# python standard library
import unittest
import random
from types import BooleanType

# this package
from cameraobscura.tests.helpers import random_string_of_letters
from cameraobscura.commands.iperf.IperfSettings import IperfServerSettings, IperfConstants
from cameraobscura.tests.testiperfcommonsettings import common_settings
from cameraobscura import CameraobscuraError


class TestIperfServerSettings(unittest.TestCase):
    def setUp(self):
        self.samples = random.sample(common_settings.keys(),
                                     random.randrange(len(common_settings)))
        self.settings = dict(zip(self.samples, (common_settings[sample] for sample in self.samples)))
        # create the object
        print self.settings
        self.configuration = IperfServerSettings(**self.settings)

        # put the options in the right order
        self.samples = [sample for sample in IperfConstants.general_options if sample in self.samples]

        # change booleans to empty strings
        self.settings = common_settings.copy()
        for setting, value in self.settings.iteritems():
            if type(value) is BooleanType:
                self.settings[setting] = ""

        self.expected_options = "".join((" --{0} {1}".format(sample, self.settings[sample]) for sample in self.samples))
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        # default
        configuration = IperfServerSettings()
        self.assertEqual(' --server', str(configuration))

        # with options
        samples = random.sample(common_settings.keys(),
                               random.randrange(len(common_settings)))
        settings = dict(zip(samples, (common_settings[sample] for sample in samples)))
        configuration = IperfServerSettings(**settings)
        return

    def test_parameters(self):
        """
        Does it accept parameters for the IperfGeneralSettings?
        """
        expected = " --server" + self.expected_options
        self.assertEqual(expected, str(self.configuration))
        return

    def test_setting_options(self):
        """
        Does it allow you to set IperfGeneralSetting options?
        """
        configuration = IperfServerSettings()
        for sample in self.samples:
            configuration.set(sample, common_settings[sample])
            
        expected = " --server" + self.expected_options
        self.assertEqual(expected, str(configuration))

        # bad setting
        with self.assertRaises(CameraobscuraError):
            configuration.set(random_string_of_letters(), random.randrange(100))
        return

    def test_getting_options(self):
        """
        Does it allow you to get IperfGeneralSetting options?
        """
        for sample in self.samples:
            self.assertEqual(self.settings[sample], self.configuration.get(sample))

        # bad attribute
        with self.assertRaises(CameraobscuraError):
            self.configuration.get(random_string_of_letters())
        return

    def test_daemon(self):
        """
        Does it set the daemon flag?
        """
        configuration = IperfServerSettings()
        configuration.daemon = True
        self.assertIsNotNone(getattr(configuration, 'daemon'))
        self.assertEqual(" --server --daemon ", str(configuration))

        # add it to the existing configuration
        self.configuration.daemon = True
        self.assertEqual(" --server --daemon " + self.expected_options, str(self.configuration))
        return

    def test_single_udp(self):
        """
        Does it properly set the flag to run in single-threaded UDP mode?
        """
        configuration = IperfServerSettings()
        configuration.single_udp = True
        self.assertEqual(' --server --single_udp ', str(configuration))

        self.configuration.single_udp = True
        self.assertEqual(" --server --single_udp " + self.expected_options, str(self.configuration))
        return
# end class TestIperfServerSettings    

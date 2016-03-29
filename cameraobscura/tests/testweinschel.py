
# python standard library
import unittest

# this package
from cameraobscura.tests.helpers import random_string_of_letters
from cameraobscura.attenuators.Weinschel import WeinschelP
from cameraobscura.attenuators.AttenuatorFactory import AttenuatorFactory


class TestWeinschel(unittest.TestCase):
    def setUp(self):
        self.hostname = random_string_of_letters()
        self.attenuator = WeinschelP(self.hostname)
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.attenuator.hostname, self.hostname)
        return

    def test_factory(self):
        """
        Does it work with the Attenuator Factory?
        """
        attenuator = AttenuatorFactory.GetAttenuator(self.attenuator.__class__.__name__,
                                                     self.hostname)
        self.assertEqual(self.hostname, attenuator.hostname)
        return
    

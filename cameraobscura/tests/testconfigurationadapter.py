
# python standard library
import unittest
import ConfigParser
import io
import random

# third-party
from mock import MagicMock, call

# this package
from cameraobscura.utilities.configurationadapter import ConfigurationAdapter, ConfigurationError
from cameraobscura import CameraobscuraError
from cameraobscura.tests.helpers import random_string_of_letters


SAMPLE = """[BunnyGrahams]
calories = 120
homocides = 3
name = Bill
cannibal = True

[ApeBananas]
calories = 1145
"""

BOOLEAN_SAMPLE = """[BunnyGrahams]
cannibal = True
tasty = 1
flatulent = yes
lights = on

gangrene = 0
small = False
old = no
brain = off

ummagumma = cow
"""

DEFAULT_SECTION = """[DEFAULT]
ape = banana
goat = grass
bunny = human
"""

FLOAT_SAMPLE = """[BunnyGrahams]
homunculi = 8.98"""

LIST_SAMPLE = """[BunnyGrahams]
mice = able, baker, charley
men = alpha bravo chester
numbers = 0,1,2,3,4
"""

SECTION = 'BunnyGrahams'
SECTIONS = 'BunnyGrahams ApeBananas'.split()
OPTIONS = 'calories homocides name cannibal'.split()
TRUE_OPTIONS = "cannibal tasty flatulent lights".split()
FALSE_OPTIONS = "gangrene small old brain".split()
BUNNY = {'calories': 120,
         'homocides': 3,
         'homunculi': 8.98,
         'name': 'Bill',
         'cannibal':True
         }


class TestConfigurationAdapter(unittest.TestCase):
    def setUp(self):
        self.defaults = {'ape':'banana',
                         'goat': 'grass',
                         'bunny': 'human'}
        self.parser = ConfigParser.SafeConfigParser(defaults=self.defaults)
        self.adapter = ConfigurationAdapter(config_parser=self.parser)
        self.parser.readfp(io.BytesIO(SAMPLE))
        return

    def test_constructor(self):
        """
        Does it take and set the config_parser on construction?
        """
        self.assertEqual(self.parser, self.adapter.config_parser)
        return

    def test_defaults(self):
        """
        Does it return the default-dictionary from the parser?
        """
        self.assertEqual(self.adapter.defaults(), self.defaults)
        return

    def test_sections(self):
        """
        Does it return the list of sections?
        """
        self.assertEqual(self.adapter.sections(), SECTIONS)
        return

    def test_has_section(self):
        """
        Does it return the correct boolean?
        """
        for section in SECTIONS:
            self.assertTrue(self.adapter.has_section(section))
        self.assertFalse(self.adapter.has_section('aosnethu'))
        return

    def test_options(self):
        """
        Does it return the options for a given section (plus the defaults)?
        """
        expected = sorted(OPTIONS + self.defaults.keys())
        self.assertEqual(expected, sorted(self.adapter.options('BunnyGrahams')))
        return

    def test_has_option(self):
        """
        Does it correctly report if the sections has an option?
        """
        options = sorted(OPTIONS + self.defaults.keys())
        for option in options:
            self.assertTrue(self.adapter.has_option('BunnyGrahams', option))

        # return false if section doesn't exist
        self.assertFalse(self.adapter.has_option('aoeu', 'sth'))

        # return false if option doesn't exist
        self.assertFalse(self.adapter.has_option('BunnyGrahams', 'snth'))
        return

    def test_get(self):
        """
        Does it get strings with an optional default?
        """
        section = 'BunnyGrahams'
        expected = BUNNY['name']
        self.assertEqual(expected, self.adapter.get(section, 'name'))
        with self.assertRaises(CameraobscuraError):
            self.adapter.get(section, 'aoeua')
        with self.assertRaises(CameraobscuraError):
            self.adapter.get('aoeu', 'name')

        # does it just return None if optional is False?
        self.assertIsNone(self.adapter.get(section, 'aoeu', optional=True))

        expected = 'coaoeuclt'
        self.assertEqual(expected,
                         self.adapter.get(section, 'aoeu', optional=True, default=expected))
        return

    def test_getfloat(self):
        """
        Does it get values and coerce them to floats?
        """
        # has option an it is castable
        option = 'homunculi'
        expected = BUNNY[option]
        parser = ConfigParser.SafeConfigParser()
        parser.readfp(io.BytesIO(FLOAT_SAMPLE))
        self.adapter.config_parser = parser
        self.assertEqual(expected, self.adapter.getfloat(SECTION,
                                                        option))

        # option not given and it's optional
        self.adapter.config_parser = self.parser
        self.assertIsNone(self.adapter.getfloat(SECTION,
                                                option,
                                                optional=True))

        # option not given, it's optional, and a default was given
        expected = random.uniform(0, 200)
        self.assertEqual(expected, self.adapter.getfloat(SECTION,
                                                         option,
                                                         optional=True,
                                                         default=expected))
        return
    
    def test_getint(self):
        """
        Does it get values and coerce them to integers?
        """
        # has option and it is castable
        OPTION = 'homocides'
        expected = BUNNY[OPTION]
        self.assertEqual(expected,
                         self.adapter.getint(SECTION,
                                             OPTION))
        # has option, but not castable to integer
        with self.assertRaises(CameraobscuraError):
            self.adapter.getint(SECTION, 'name')
            
        # told optional but no defaults given
        self.assertIsNone(self.adapter.getint(SECTION, 'aoeur', optional=True))

        # option not found
        with self.assertRaises(CameraobscuraError):
            self.adapter.getint(SECTION, 'aoeusntg')

        # value not found default is given
        expected = 65
        self.assertEqual(expected,
                         self.adapter.getint(SECTION,
                                             'lrcaogeu',
                                             optional=True,
                                             default=expected))
        return

    def test_getboolean(self):
        """
        Does it get an optional boolean value?
        """
        # has option and is castable
        # True: 1, yes, true, on
        # False: 0, no, false, off
        self.parser.readfp(io.BytesIO(BOOLEAN_SAMPLE))
        for option in TRUE_OPTIONS:
            self.assertTrue(self.adapter.getboolean(SECTION, option))
        for option in FALSE_OPTIONS:
            self.assertFalse(self.adapter.getboolean(SECTION, option))

        # has option, not valid boolean
        with self.assertRaises(CameraobscuraError):
            self.adapter.getboolean(SECTION,
                                    'ummagumma')

        # option not found
        with self.assertRaises(CameraobscuraError):
            self.adapter.getboolean(SECTION, 'aoeusnth')

        # option not found, optional given
        self.assertIsNone(self.adapter.getboolean(SECTION, 'aoeunth',
                                                  optional=True))
        self.assertFalse(self.adapter.getboolean(SECTION, 'aosnethurc',                                                 
                                                  optional=True,
                                                  default=False))
        return

    def test_getlist(self):
        """
        Does it get a delimited list?
        """
        # comma-delimited by default
        self.parser.readfp(io.BytesIO(LIST_SAMPLE))
        expected = "able baker charley".split()
        actual = self.adapter.getlist(SECTION, 'mice')
        self.assertEqual(expected, actual)

        # try space-delimited
        expected = "alpha bravo chester".split()
        actual = self.adapter.getlist(SECTION, 'men', delimiter=' ')
        self.assertEqual(expected, actual)

        # optional
        actual = self.adapter.getlist(SECTION, 'cheese', optional=True)
        self.assertIsNone(actual)

        # optional with default
        expected = 'a b c'.split()
        actual = self.adapter.getlist(SECTION, 'cheese', optional=True,
                                      default = expected)
        self.assertEqual(expected, actual)

        # convert to ints
        expected = range(5)
        actual = self.adapter.getlist(SECTION, 'numbers', converter=int)
        self.assertEqual(expected, actual)
        return


    def test_items(self):
        """
        Does it return a list of name-value pairs
        """
        options = 'ape goat bunny calories homocides name cannibal'.split()
        values = 'banana grass human 120 3 Bill True'.split()
        expected = zip(options, values)
        self.assertEqual(sorted(expected), sorted(self.adapter.items(SECTION)))
        return

    def test_write(self):
        """
        Does it write the configuration to a file?
        """
        open_file = MagicMock()
        for key in self.parser.defaults():
            del(self.parser.defaults()[key])
        calls = [call.write(line + '\n') for line in SAMPLE.split('\n')]
        self.adapter.write(open_file)
        self.assertEqual(calls, open_file.mock_calls)
        return
    
    def test_section_dict(self):
        """
        Does it convert a section to a dictionary?
        """
        section = random_string_of_letters(10)
        rows = random.randrange(1,30)
        options = [random_string_of_letters() for option in xrange(rows)]
        values = [random_string_of_letters() for value in xrange(rows)]
        settings = '\n'.join(["{0}={1}".format(options[index], values[index]) for index in xrange(rows)])
        output = "[{0}]\n".format(section) + settings

        parser = ConfigParser.SafeConfigParser()
        self.adapter.config_parser = parser
        parser.readfp(io.BytesIO(output))

        section_dict = self.adapter.section_dict(section)

        # turns out ConfigParser sets all options to lower case
        lowered_options = [option.lower() for option in options]
        expected = dict(zip(lowered_options, values))
        self.assertDictEqual(expected, section_dict)

        # missing section
        with self.assertRaises(ConfigurationError):
            self.adapter.section_dict(random_string_of_letters(4))
        return

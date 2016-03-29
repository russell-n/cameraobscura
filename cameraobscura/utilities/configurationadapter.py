
# python standard library
import ConfigParser
import logging

# this package
from cameraobscura.common.errors import ConfigurationError

DOT_JOIN = "{0}.{1}"
USING_DEFAULT = "Section: {s}, Option: {o} not found -- using default: {d}"

VALUE_ERROR = "Section: {s} Option: {o} Value: {v} -- couldn't cast value to {t}."

class ConfigurationAdapter(object):
    """
    An adapter to the ConfigParser to add optional-value methods
    """
    def __init__(self, config_parser):
        """
        ConfigurationAdapter constructor

        :param:

         - `config_parser`: An ConfigParser with the configuration already read into it
        """
        self._logger = None
        self.config_parser = config_parser
        return

    @property
    def logger(self):
        """
        A python Logger.
        """
        if self._logger is None:
            self._logger = logging.getLogger(DOT_JOIN.format(self.__module__,
                                                             self.__class__.__name__))
        return self._logger

    def get(self, section, option, optional=False, default=None, method='get'):
        """
        Similar to the ConfigParser.get, but changed so getint and getboolean will match

        :param:

         - `section`: section with option
         - `option`: option in section whose value to return
         - `method`: get-method to call
         - `optional`: if True, returns default for missing options
         - `default`: Value to return if optional and no option found

        :return: value for option as string
        :raise:

         - `NoOptionError`: if option doesn't exist in section or defaults and not optional
         - `NoSectionError`: if section doesn't exist in configuration and not optional
        """
        try:
            return getattr(self.config_parser, method)(section, option)
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as error:
            if optional:
                self.logger.debug(error)
                self.logger.debug(USING_DEFAULT.format(s=section,
                                                      o=option,
                                                      d=default))
                return default
            raise ConfigurationError(error)
        return

    def getint(self, section, option, optional=False, default=None):
        """
        Gets a value from the configuration and tries to cast it to an integer.

        :param:

         - `section`: section in configuration with `option`
         - `option`: option in section with value
         - `optional`: If true, return default when no option found
         - `default`: value to return if optional and option not found (or value found but not castable to int)
         
        :return: value cast to an integer (or default)
        :raises:

         - `ValueError`: If value found but can't cast to integer
         - `ConfigParser.NoSectionError`: If section not found and not optional
         - `ConfigParser.NoOptionError`: If option not found and not optional
        """
        try:
            return self.get(section=section, option=option, method='getint',
                            optional=optional, default=default)
        except ValueError as error:
            self.logger.error(error)
            raise ConfigurationError(VALUE_ERROR.format(s=section,
                                                     o=option,
                                                     v=self.get(section=section,
                                                                option=option),
                                                                t='integer'))

    def getfloat(self, section, option, optional=False, default=None):
        """
        Gets a value from the configuration and tries to cast it to an integer.

        :param:

         - `section`: section in configuration with `option`
         - `option`: option in section with value
         - `optional`: If true, return default when no option found
         - `default`: value to return if optional and option not found (or value found but not castable to int)
         
        :return: value cast to an integer (or default)
        :raises:

         - `ValueError`: If value found but can't cast to integer
         - `ConfigParser.NoSectionError`: If section not found and not optional
         - `ConfigParser.NoOptionError`: If option not found and not optional
        """
        return self.get(section=section, option=option, method='getfloat',
                        optional=optional, default=default)

    def getboolean(self, section, option, optional=False, default=None):
        """
        Gets value and casts to a boolean

        :param:

         - `section`: section in configuration to get option
         - `option`: option in section to get value
         - `optional`: if true, return default if not found
         - `default`: value to return if value not found and optional

        :raises:
         - `ConfigParser.NoSectionError`: if section not found and not optional
         - `ConfigParser.NoOptionError`: if option not found and not optional

        :return: value cast to boolean or default if not found and optional
        """
        try:
            return self.get(section=section, option=option, method='getboolean',
                            optional=optional, default=default)
        except ValueError as error:
            self.logger.error(error)
            raise ConfigurationError(VALUE_ERROR.format(s=section,
                                                     o=option,
                                                     v=self.get(section=section, option=option),
                                                     t='boolean'))
        return

    def getlist(self, section, option, optional=False, default=None,
                delimiter=',', converter=str):
        """
        gets a string and converts it into a list

        :param:
        
         - `section`: section in configuration to get option
         - `option`: option in section to get value
         - `delimiter`: what separates the items in the list

        :return: list of strings
        """
        output = self.get(section=section,
                          option=option,
                          optional=optional,
                          default=default)
        if output == default:
            return default
        return [converter(item.strip()) for item in output.split(delimiter)]

    def section_dict(self, section):
        """
        A convenience function to return the section option=value pairs as option:value dict

        :param:

         - `section`: name of section to convert to dict

        :return: dict of option:value pairs
        :raise: ConfigurationError if the section doesn't exist in the configuration
        """
        try:
            return dict(self.config_parser.items(section))
        except ConfigParser.NoSectionError as error:
            self.logger.error(error)
            raise(ConfigurationError("No Section '{0}' in the configuration".format(section)))
        return

    def __getattr__(self, attribute):
        """
        A pass-through to the config parser for all the methods I don't implement

        :param:

         - `attribute`: An attribute available from the ConfigParser object
        """
        return getattr(self.config_parser, attribute)
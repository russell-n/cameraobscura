Testing The ConfigAdapter
=========================

Although I was hoping to just use the ConfigParser as-is, for some reason `getint` and `getboolean` don't accept defaults the way `get` does (see :ref:`testing-configparser`) so I'm going to create an adapter.

.. currentmodule:: cameraobscura.tests.testconfigadapter
.. autosummary::
   :toctree: api

   TestConfigurationAdapter.test_constructor
   TestConfigurationAdapter.test_defaults
   TestConfigurationAdapter.test_sections
   TestConfigurationAdapter.test_has_section
   TestConfigurationAdapter.test_options
   TestConfigurationAdapter.test_has_option
   TestConfigurationAdapter.test_get
   TestConfigurationAdapter.test_getint
   TestConfigurationAdapter.test_getfloat
   TestConfigurationAdapter.test_getboolean
   TestConfigurationAdapter.test_getlist
   TestConfigurationAdapter.test_items
   TestConfigurationAdapter.test_write
   TestConfigurationAdapter.test_section_dict


The Base Configuration
======================







.. _rvrconfiguration-baseconfiguration:

BaseConfiguration Class
-----------------------

The purpose of this class is to enforce some expected attributes and to provide an `unknown_options` method to children. Additionally, children will get a logger (assuming they initialize this parent class).

.. uml::

   BaseConfiguration o- ConfigurationAdapter
   BaseConfiguration o- logging.Logger
   BaseConfiguration : String section
   BaseConfiguration : String example   
   BaseConfiguration : List options
   BaseConfiguration : List unknown_options
   BaseConfiguration : List exclusions
   BaseConfiguration : __init__(ConfigurationAdapter configuration)
   BaseConfiguration : check_rep()
   BaseConfiguration : reset()

.. currentmodule:: cameraobscura.common.baseconfiguration
.. autosummary::
   :toctree: api

   BaseConfiguration
   BaseConfiguration.section
   BaseConfiguration.options
   BaseConfiguration.example
   BaseConfiguration.unknown_options
   BaseConfiguration.exclusions
   BaseConfiguration.check_rep
   BaseConfiguration.reset




   

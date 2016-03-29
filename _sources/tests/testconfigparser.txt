Testing The ConfigParser
========================

.. _testing-configparser:

I was originally going to create an adapter for the config-parser so that it would take defaults but it kind of looks like ConfigParser already does that (although the `documentation <http://docs.python.org/2/library/configparser.html>`_ doesn't make it obvious that it does). These tests are just to confirm that it works.

.. '

.. currentmodule:: cameraobscura.AutmatedRVR.tests.testconfigparser
.. autosummary::
   :toctree: api

   TestConfigParser.test_defaults
   TestConfigParser.test_no_default
   TestConfigParser.test_vars
   TestConfigParser.test_int_vars
   TestConfigParser.test_bool_vars


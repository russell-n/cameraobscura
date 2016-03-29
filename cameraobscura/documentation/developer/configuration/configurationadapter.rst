The Configuration Adapter
=========================

.. uml:: 

   state "Read Configuration" as RC
   state "Convert to Data" as DS
   state "Convert to Class" as CC

   [*] -> RC : ConfigurationFile
   RC -> DS : ConfigParser
   DS -> CC : Data | Data Structure
   CC -> [*] : Configuration Class

contents:

   * `Read Configuration <developer-configuration-read-configuration>`
   * `Convert to Data <developer-configuration-convert-to-data>`
   * `Convert to Class <developer-configuration-convert-to-class>`

   
.. _developer-configuration-read-configuration:

Read Configuration
------------------

The first part of the requirement is to convert a file into a 'configuration'. This is done in the :ref:`main <rate-vs-range-main>` section by creating a *SafeConfigParser* from a configuration file-name. Since this is part of the standard library it won't be documented.

.. currentmodule:: ConfigParser
.. autosummary::
   :toctree: api

   SafeConfigParser

.. _developer-configuration-convert-to-data:
   
Convert to Data
---------------

An adapter class was created (the :ref:`ConfigurationAdapter <configuration-adapter>`) in order to add two features to the *SafeConfigParser*:

   #. Optional options (and defaults)
   #. Data structures

.. currentmodule:: testsuites.utilities.configurationadapter
.. autosummary::
   :toctree: api

   ConfigurationAdapter

.. _developer-configuration-convert-to-class:

Convert To Class
----------------

The last part of the implementation is difficult to document completely. The idea is that each class that needs a configuration will create a class to map a `<section>:<option>` pair for each parameter it needs -- with `<section>` meaning a section in the configuration file (e.g. `[dut]`) and the `option` meaning the left-hand side of a configuration line (e.g. `hostname=192.168.20.24` would have `hostname` as the option and `192.168.20.24` as the assigned value).


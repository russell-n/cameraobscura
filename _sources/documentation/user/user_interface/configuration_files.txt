The Configuration Files
=======================

.. _user-documentation-configuration-files:

The bulk of the parameters that can be set at run time are passed to the `CameraObscura` program via an `ini-formatted file <http://en.wikipedia.org/wiki/INI_file>`_. We'll walk through each of the sections and try to add enough explanation to the meaning of the options that you will be able to create a configuration that will suit your needs. Many of the settings are optional. If a section in the sample is commented out the whole section is optional. If an option is commented out the example value is the default. See the :ref:`fetch <user-documentation-cli-fetch>` instructions to see a list of the sections and how to get sample configurations. 

Contents:

   * :ref:`The Attenuation Section <user-documentation-configuration-attenuation>`
   * :ref:`The Other Section <user-documentation-configuration-other>`
   * :ref:`The Iperf Section <user-documentation-configuration-iperf>`
   * :ref:`The DUT and Server Sections <user-documentation-configuration-dut-server>`
   * :ref:`The Query Section <user-documentation-configuration-query>`
   * :ref:`The Dump Section <user-documentation-configuration-dump>`
   * :ref:`The Ping Section <user-documentation-configuration-ping>`

.. _user-documentation-configuration-attenuation:

.. include:: configuration_sections/configuration_attenuation.rst

.. _user-documentation-configuration-other:

.. include:: configuration_sections/configuration_other.rst

.. _user-documentation-configuration-iperf:

.. include:: configuration_sections/configuration_iperf.rst

.. _user-documentation-configuration-dut-server:

.. include:: configuration_sections/configuration_dut_server.rst

.. _user-documentation-configuration-query:

.. include:: configuration_sections/configuration_query.rst

.. _user-documentation-configuration-dump:

.. include:: configuration_sections/configuration_dump.rst

.. _user-documentation-configuration-ping:

.. include:: configuration_sections/configuration_ping.rst

Conclusion
----------

Given the number of parameters needed, the configuration file can become an unwieldy thing so I have tried to add as many defaults as I thought possible without accidentally covering up unintended values being used. The main goal of the renovation of this code was to make it so that the last-minute changes that plagued the old code resulting in an explosion of commented out and copied files could be avoided while the functionality was maintained using the configuration file instead. Unfortunately, as is always the case, generalization and optimization are opposing ideas. Hopefully the added flexibility has not come with the price of too much burden placed on the user.


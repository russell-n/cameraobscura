The Iperf
=========


A set of convenience classes and methods for running iperf traffic.







.. _iperf-client-server-namedtuple:

The ClientServer NamedTuple
---------------------------

This is a namedtuple to pass around the client and server  for different directions.


.. code:: python

    ClientServer = namedtuple('ClientServer', 'client server'.split())
    



.. _iperf-class:

The Iperf Class
---------------

.. uml::

   Iperf o- EventTimer
   Iperf o- ClientServer
   Iperf o- HostSSH
   Iperf o- IperfClientSettings
   Iperf o- IperfServerSettings

.. currentmodule:: cameraobscura.commands.iperf.Iperf
.. autosummary::
   :toctree: api

   Iperf
   Iperf.event_timer
   Iperf.client_server
   Iperf.udp
   Iperf.__call__
   Iperf.downstream
   Iperf.upstream
   Iperf.run
   Iperf.start_server
   Iperf.run_client
   Iperf.version
   Iperf.parser





.. _iperf-enum:

Iperf Enum
----------

A holder of constants.




.. _iperf-configuration:

Iperf Configuration
-------------------

A configuration for iperf testing.

.. uml::

   BaseConfiguration <|-- IperfConfiguration
   IperfConfiguration o- ConfigurationAdapter
   IperfConfiguration o- IperfEnum
   IperfConfiguration o- IperfClientSettings
   IperfConfiguration o- IperfServerSettings   

.. module:: cameraobscura.commands.iperf.Iperf
.. autosummary::
   :toctree: api

   IperfConfiguration
   IperfConfiguration.direction
   IperfConfiguration.client_settings
   IperfConfiguration.server_settings
   IperfConfiguration.get_section_dict
   IperfConfiguration.reset
   IperfConfiguration.check_rep
   IperfConfiguration.example
   IperfConfiguration.section
   




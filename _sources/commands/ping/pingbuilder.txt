The Ping Builder
================




This is a module for a builder of pings. At some point it might make sense to put the configuration and builder into the same file as the ping, but since I already have a folder for it...

.. uml::

   PingBuilder o- TheHost
   PingBuilder o- PingConfiguration
   PingBuilder o- Ping

.. currentmodule:: cameraobscura.commands.ping.pingbuilder
.. autosummary::
   :toctree: api

   PingBuilder
   PingBuilder.product





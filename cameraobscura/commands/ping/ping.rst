The Ping
========





.. _ping-ping:

The Ping
--------

This is an adapter to use a different SSHClient that behaves more like the paramiko SSHClient.

.. currentmodule:: cameraobscura.commands.ping.ping
.. autosummary::
   :toctree: api

   Ping
   Ping.operating_system
   Ping.expression
   Ping.command
   Ping.__call__
   Ping.check_rep




.. _ping-ping-constants:

Ping Constants
--------------

A holder of constants for the ping.

.. csv-table:: Ping Constants
   :header: Property, Description

   linux, String to identify the device as having the linux OS
   cygwin, String to identify the device as having the cygwin OS
   known_operating_systems, tuple of string OS identifiers
   cygwin_one_repetition, string argument to ping once only
   linux_one_repetition, string argument to ping once and wait for 1 second
   round_trip_time, string identifier used as the group-name in the regular expression
   rtt_expression, regular expression to match a successful ping






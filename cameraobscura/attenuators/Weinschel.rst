The Weinschel Attenuator
========================

This controls Weinschel attenuators over a telnet connection.


The ports affected by each function are supplied as a list of strings. These strings can be port numbers or predefined port groups.

.. note:: See the route() method for a list of port groups.

By default, operations are done on the first group of two ports.

.. note:: Someone may want to supply default ports from init.

If an error occurs then this throws an :ref:`AttenuatorError <attenuators-attenuator-attenuator-error>` exception.




.. _attenuators-weinschel-handleattenuatorerrors:

An Error-Trapping Decorator
---------------------------

This function was created to make it easier to trap socket errors and EOFErrors and raise AttenuatorErrors instead. The EOFError is raised if the end of a file is reached without any data being read -- they are both telnet-related errors for the connection to the attenuator.

.. currentmodule:: cameraobscura.attenuators.Weinschel
.. autosummary::
   :toctree: api

   handleattenuatorerrors




.. _attenuators-weinschel-constants:

Constants
---------

.. csv-table:: Weinschel Constants
   :header: Constant, Value,Description


   defaultPort,10001,TCP port attenuator's XPort is listening on
   retryWait,5,Seconds before retrying connection



.. _attenuators-weinschel-class:

The WeinschelP Class
--------------------

.. uml::

   Attenuator <|-- WeinschelP
   WeinschelP o- telnetlib.Telnet

.. currentmodule:: cameraobscura.attenuators.Weinschel
.. autosummary::
   :toctree: api

   WeinschelP

Properties
~~~~~~~~~~

.. autosummary::
   :toctree: api

   WeinschelP.connection
   WeinschelP.device_info
   WeinschelP.numChannels
   WeinschelP.maxAttenuation
   WeinschelP.minStepSize
   WeinschelP.routetable

Methods
~~~~~~~

.. autosummary::
   :toctree: api

   WeinschelP.__del__
   WeinschelP.routes
   WeinschelP.setAttenuation
   WeinschelP.getAttenuation
   WeinschelP.getAttenMax

   WeinschelP._portsAffected
   WeinschelP._getDeviceInfo
   WeinschelP._retry_write
   WeinschelP.close




.. _attenuators-weinschel-using-it:

Using the WeinschelP
--------------------

The way this class is currently being used is by having it built with the :ref:`AttenuatorFactory <attenuators-attenuator-factory-class>`. The `AttenuatorFactory` only takes a 


Attenuator Base Class
=====================

A utility that changes the path-loss between two devices.




.. _attenuators-attenuator-base-class:

The Attenuator Class
--------------------


.. currentmodule:: cameraobscura.attenuators.Attenuator
.. autosummary::
   :toctree: api

   Attenuator




.. _attenuators-attenuator-attenuator-error:

AttenuatorError
---------------

An error to raise when predictable errors are detected. This inherits from the CameraobscuraError so that it can be caught by the top-level code without having to catch every possible error raised by all the classes.

.. uml::

   CameraobscuraError <|-- AttenuatorError

.. autosummary::
   :toctree: api

   AttenuatorError




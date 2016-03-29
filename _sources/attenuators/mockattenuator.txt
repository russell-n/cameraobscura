A Mock Attenuator
=================

A Mock for testing. This is meant to test the other code, see the specific mocks for attenuator-specific code.




MockAttenuator Constants
------------------------


.. code:: python

    class MockAttenuatorConstants(object):
        """
        a holder of constants (mostly to make testing easier)
        """
        __slots__ = ()
        # class name
        class_name = 'MockAttenuator'
        # methods
        routes = 'routes'
        getAttenuation = 'getAttenuation'
        setAttenuation = 'setAttenuation'
        getAttenMax = 'getAttenMax'
    
        # arguments
        # there is both a method and common parameter named 'routes'
        value='value'
        route = 'route'
        attenuation_max = 1000
    



The MockAttenuator Class
------------------------

.. uml::

   Attenuator <|-- MockAttenuator
   MockAttenuator.routes
   MockAttenuator.getAttenuation
   MockAttenuator.setAttenuation
   MockAttenuator.getAttenMax

.. currentmodule:: cameraobscura.attenuators.mockattenuator
.. autosummary::
   :toctree: api

   MockAttenuator







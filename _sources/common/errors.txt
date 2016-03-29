A Place for Shared Errors
=========================




.. _configuration-error:

ConfigurationError
------------------

This error is created so that users can trap it if needed.

.. currentmodule:: cameraobscura.common.errors
.. autosummary::
   :toctree: api

   ConfigurationError

.. uml::

   CameraobscuraError <|-- ConfigurationError


.. code:: python

    class ConfigurationError(CameraobscuraError):
        """
        An error to raise if a configuration error is caught
        """
    



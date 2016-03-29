The Client Base
===============

Since the SimpleClient and TelnetClient have started to share so much code I'm going to make an abstract base class to try and create a central place for the non-technology-specific code they need.

.. '







.. _clients-base-client:

The BaseClient
--------------

.. currentmodule:: cameraobscura.clients.clientbase
.. autosummary::
   :toctree: api

   BaseClient




.. _socket-error-decorator:

Socket Decorator
----------------

Since the connections raise socket errors which aren't always easy to interpret, hopefully this will help make it easier to add sensible messages.

.. '

.. autosummary::
   :toctree: api

   handlesocketerrors




.. autosummary::
   :toctree: api

   suppresssocketerrors




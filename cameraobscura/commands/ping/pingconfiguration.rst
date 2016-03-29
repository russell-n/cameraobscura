The Ping Configuration
======================




The ping has been converted to use :ref:`The Command <command-class>` so the configuration it needs is a combination of ping-specific things and what the command needs.

.. currentmodule:: cameraobscura.commands.ping.pingconfiguration
.. autosummary:: 
   :toctree: api

   PingConfiguration
   PingConfiguration.target
   PingConfiguration.time_limit
   PingConfiguration.threshold
   PingConfiguration.arguments
   PingConfiguration.operating_system   
   PingConfiguration.trap_errors
   PingConfiguration.data_expression
   PingConfiguration.timeout




PingConfigurationConstants
--------------------------

This holds the constants for the PingConfiguration and show what's expected in the config-file. 'section' is the section header (e.g. [ping]), the options are the names of the options and the defaults are the values used if the user doesn't fill in the value for that option. The actual strings are what's expected in the configuration file so they can be changed to help clarify their meanings for the user but the variable names shouldn't change since the PingConfiguration class is using them.


.. code:: python

    class PingConfigurationConstants(object):
        """
        Holder of constant values for PingConfiguration
        """
        __slots__ = ()
        section = 'ping'
    
        # options
        data_expression = 'data_expression'
        trap_errors = 'trap_errors'
        timeout = 'timeout'
        operating_system = 'operating_system'
        arguments = 'arguments'
        threshold = 'threshold'
        time_limit = 'time_limit'
        target = 'target'
    
        # defaults
        default_trap_errors = True
        default_timeout = 10
        default_data_expression = None
        default_os = None
        default_threshold = 5
        default_time_limit = 300
    # end PingConfigurationConstants
    



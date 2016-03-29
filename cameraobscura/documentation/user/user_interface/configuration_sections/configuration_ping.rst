Ping Configuration
------------------



The ``ping`` section is an optional section to configure a connectivity-check from the DUT to the traffic server in between testing.

::

    #[ping]
    # target = www.google.com
    # time_limit = 300
    # threshold = 5
    # arguments = -c 1 -W 1
    # operating_system = None
    # timeout = 10
    # data_expression = None
    #trap_errors = True
    
    



None of the options are required, but if the section as a whole is left out, then no pinging will be performed. This was added for a device whose ping implementation was broken.

``target``
~~~~~~~~~~

By default the address to ping will be taken from the ``test_ip`` option in the ``server`` setting. This option allows you to change this.

``time_limit``
~~~~~~~~~~~~~~

This is the total number of seconds to try and ping the target before giving up.

``threshold``
~~~~~~~~~~~~~

This is the number of consecutive pings that constitute 'success'.

``arguments``
~~~~~~~~~~~~~

The command-line arguments being passed to the ping command are being based on the operating system for the DUT. If they are different from what's being used, you can override them here.

``operating_system``
~~~~~~~~~~~~~~~~~~~~

This is redundant with the `dut` `operating_system`, it's only here for completeness, I can't think of a situation where you would need it.

``timeout``
~~~~~~~~~~~

The socket readline timeout.

``data_expression``
~~~~~~~~~~~~~~~~~~~

The `ping` follows the pattern set up by the :ref:`query <user-documentation-configuration-query>` (they share the same code) wherein a regular expression with a group is applied to the output to extract the data. A match will count as a successful ping and a failed match will correspond to a failed ping. If the output of the ping on the device is different than the default expression (there is a surprising amount of variation for ping output across operating systems) change the ``data_expression`` to one that would indicate a successful ping (don't forget to put in group, indicated by parentheses).

``trap_errors``
~~~~~~~~~~~~~~~

This is another parameter shared with the `queries`. By default socket errors are assumed non-fatal (because it has to allow for a point where the attenuation has broken the connection). If you want to troubleshoot or just need it to crash on when socket errors arise, change this to `false`.


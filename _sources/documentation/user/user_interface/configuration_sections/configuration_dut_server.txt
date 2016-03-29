DUT and Server Configuration
----------------------------



The ``dut`` and ``server`` sections are there to set up the connections to the nodes at either end of the ``iperf`` session. Within the program they are being passed to the same code (but with the different settings) so the only difference between the sections is their names -- all the options are the same (kind of -- see the *Everything Else* section at the end).

::

    [dut]
    username = admin
    #password = root
    control_ip = 192.168.10.34
    #connection_type = telnet
    test_ip = 192.168.20.34
    #timeout=10
    #prefix = PATH=/opt:$PATH; adb shell
    # operating_system = cygwin
    # port=52686
    
    [server]
    username = admin
    #password = root
    control_ip = 192.168.10.34
    #connection_type = telnet
    test_ip = 192.168.20.34
    #timeout=10
    #prefix = PATH=/opt:$PATH; adb shell
    # operating_system = cygwin
    # port=52686
    
    



Connection Settings
~~~~~~~~~~~~~~~~~~~

The following are used to connect to and log into the device.

.. csv-table:: Connection Settings
   :header: Option, Meaning

   username, the account username (e.g. *root*)
   password, login password
   control_ip, address to send device commands to
   connection_type, telnet or ssh
   test_ip, address to the interface to use for iperf traffic
   timeout, seconds to try and login

Currently only Telnet and SSH are supported. In the case of SSH, ``hosts`` files and public-keys are checked, so if you have them set up you can leave out the password and use the hostname::

    username = allion
    control_ip = lancetfluke

If for some reason you don't have a separate traffic server then you can use `localhost` as the ``control_ip`` and the Control PC will talk to itself. 

.. note:: For forwarded serial connections, the ``control_ip`` would be for the attached PC that's forwarding the stream

.. note:: For android devices attached to a PC using a USB bridge, the login information would be for the attached PC while the ``test_ip`` would be for the android

``connection_type``
~~~~~~~~~~~~~~~~~~~

As mentioned above, SSH and Telnet are supported. SSH is the default and should be preferred whenever it is available. If you have a device that only has a serial port you can set up a telnet connection to it by attaching a computer to it (via the serial port) and forwarding the connection over the PC's ethernet connection using pyserial's `serial bridge <http://pyserial.sourceforge.net/examples.html#tcp-ip-serial-bridge>`_. Since the serial bridge doesn't create a new PTY every time you connect to it this is much less flexible and possibly won't work for every possible test (serial devices are hard to get so I can't test it fully). As long as you stick to straight-forward TCP testing it should be okay.

``operating_system``
~~~~~~~~~~~~~~~~~~~

The defaults for the commands being used by the program assume that the device is running Linux (and is tested primarily with Ubuntu-based machines). For some things (particularly ping) the different operating systems have slightly different command flags and output. For the known cases you can set the operating system to clue the program into what it should expect. Right now 'cygwin' is the only alternate.

``prefix``
~~~~~~~~~~

Some devices just don't have everything set up in such a way as to allow straight-forward execution of the commands. This particular setting was prompted by three cases that have been encountered before:

    * command not in the non-interactive PATH variable
    * android devices are controlled by an attached PC so they need 'adb shell ' before every command
    * shared library not installed in the standard place

To help with this the ``prefix`` takes a string that will be prepended to every command. For one case, some commands were in a folder called `/opt/wifi` which wasn't in the PATH variable. To fix this you could add it to the PATH using the prefix::

    prefix = PATH=/opt/wifi:$PATH;

Note that the prefix in this case has to end with a semi-colon so the shell will know that the command that follows it is a separate command. It might seem that we could have added the semi-colon in the program, but then the 'adb shell'  prefix would have failed, because it can't have a semi-colon between the prefix and the commands::

    prefix = adb shell

In the case of the shared library, it's similar to the PATH problem::

    prefix = LD_LIBRARY_PATH=/tmp:$LD_LIBRARY_PATH;

Just remember that it's added to every command (with a space in between the prefix and the command).

Everything Else
~~~~~~~~~~~~~~~

The different connection types take different arguments when their code is called so it didn't seem feasible to create a configuration file that works with every possible type (if serial or sub-process connections are added they will have completely different settings) so any arbitrary parameter that the connection libraries take on creation can be passed in. To know what's valid will require looking at the signatures:

    * `Telnet <https://docs.python.org/2/library/telnetlib.html#>`_
    * `SSH <http://www.lag.net/paramiko/docs/paramiko.SSHClient-class.html#connect>`_



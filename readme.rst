The Camera Obscura (Read Me)
============================



This is a renovated form of the 'AutomatedRVR' created to combine three main features:

   * Signal Attenuation via a mechanical attenuator (e.g. a Weinschel attenuator)

   * Iperf Traffic run between two devices in between signal attenuations
   
   * Device state information sampled between attenuations

This assumes that there is a (wireless) `Device Under Test (DUT)` that is connected to a `Wireless Access Point (AP)` which gives the DUT access to a sub-network (test network) used for testing. It is also assumed that there will be a `Traffic Server (TPC)` that is also connected to the sub-network used for testing and that both the DUT and TPC will also be attached to a different sub-network (control network) that will be dedicated to controlling and communicating with the devices. It is further assumed that this code will be run on a third device (`Control PC (CPC)`) and that it will communicate with the devices via the control network.

The Attenuator is also assumed to be attached to the `control network` so that the CPC can communicate with it. Although the assumption is made that there will be an AP and attenuator, the existence of the wireless network is outside the scope of the code. It only communicates with the devices and assumes that the network topology has been set up as desired by whoever runs the code. There's a `MockAttenuator` that could be used to run the traffic without an attenuator, turning it into just an iperf runner.

.. '

Installing the Code
-------------------

The only external requirements for running the code are `theape` and the `iperflexer` (both will be installed by distutils from pypi if they aren't already installed).

.. '

    sudo python setup.py install 

Once installed the command `rvr` will access the code. To test it you can try:

    rvr -h

.. note:: The Camera Obscura is currently using some modules from TheApe so it imports numpy even though it isn't used here. It will also install paramiko (which is used here)

.. '

A Note On The Paramiko Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometime in 2013 (commit `2403504 <https://github.com/paramiko/paramiko/commit/2403504b44de773c3f566e7d647bc0e8661af918#diff-169e8b6af6ef7bee0bb2c9a6a637aa5fR353>`_) a `timeout` parameter was added to the SSHClient.exec_command call. The code within expects that to be available so the installed paramiko version should be v1.13.0 or newer. If an older version of paramiko is required a (relatively) small change needs to be added to the code.

Getting a Sample Configuration
------------------------------

Because there are so many options to the code, `ini formatted <http://en.wikipedia.org/wiki/INI_file>`_ files are used. To get a sample use the ``fetch`` sub-command::

   rvr fetch

.. highlight:: ini   
   

.. code::

    
    [attenuation]
    # if an option is commented out it has the default setting you see
    
    # 'start' is the attenuation value to use when the testing starts
    
    #start = 0
    
    # 'stop' is the maximum attenuation to try before stopping
    
    #stop = 9223372036854775807
    
    # 'name' is the name of the attenuator
    # not case-sensitive, but spelling counts
    # valid names : mockattenuator,weinschelp
    
    #name = WeinschelP
    
    # 'control_ip' is the address of the attenuator
    control_ip = 192.168.10.53
    
    # 'step_sizes' is a space-separated list of step-sizes
    # (each attenuation increases by the current step-size at each repetition)
    
    #step_sizes = [1]
    
    # 'step_change_thresholds' is a space-separated list of thresholds which 
    # when reached trigger a change to the next 'step-size'
    # there should always be one less threshold than step-sizes
    # if you don't want to change, comment out or remove the line
    
    #step_change_thresholds =
    
    # as an example, the next two lines would cause
    # the attenuation to increase by 1 until 10 is reached
    # then it will increase by 5 until 100 then it will increase by 10
    # until the end of the test
    
    # step_sizes = 1 5 10
    # step_change_thresholds = 10 100
    
    # `reversal_limit` is the maximum number of times to reverse directions
    # reversal_limit = 0
    
    # `step_list` a list of attenuations to use instead of calculating a range
    # this overrides step_sizes, start, stop, etc.
    # e.g. to run only attenuations 10, 20, 30,:
    # step_list = 10 20 30 
    # step_list =
    
    [dut]
    # login information (these are required)
    username = admin
    
    # this isn't if your public keys are working
    #password = root
    
    # address of the control-interface 
    control_ip = 192.168.10.34
    
    # this identifies the type (only 'telnet', 'ssh', or 'fake')
    #connection_type = ssh
    
    # address of the interface to test
    test_ip = 192.168.20.34
    
    # connection time-out in seconds
    #timeout = 1
    
    # optional prefix to add to ALL commands (default: None)
    # this will be added with a space (i.e. <prefix> <command>)
    # so if needed, add a semicolon like in the example between the PATH and adb
    
    #prefix = PATH=/opt:$PATH; adb shell
    
    # the operating system for the DUT
    
    # operating_system = linux
    
    # there are too many options for the different connection-types
    # so you can add necessary parameters but make sure the name
    # matches the parameter name
    # e.g. if you need to set the port:
    # port=52686
    
    [server]
    # login information (these are required)
    username = admin
    
    # this isn't if your public keys are working
    #password = root
    
    # address of the control-interface 
    control_ip = 192.168.10.34
    
    # this identifies the type (only 'telnet', 'ssh', or 'fake')
    #connection_type = ssh
    
    # address of the interface to test
    test_ip = 192.168.20.34
    
    # connection time-out in seconds
    #timeout = 1
    
    # optional prefix to add to ALL commands (default: None)
    # this will be added with a space (i.e. <prefix> <command>)
    # so if needed, add a semicolon like in the example between the PATH and adb
    
    #prefix = PATH=/opt:$PATH; adb shell
    
    # the operating system for the DUT
    
    # operating_system = linux
    
    # there are too many options for the different connection-types
    # so you can add necessary parameters but make sure the name
    # matches the parameter name
    # e.g. if you need to set the port:
    # port=52686
    
    [iperf]
    # these are iperf options
    # directions can be upstream, downstream or both (default : both)
    # actually only checks the first letter so could also be ugly, dumb, or bunny too
    direction = upstream
    
    # everything else uses iperf long-option-names
    # to get a list use `iperf -h` or `man iperf`
    # the left-hand-side options are the iperf options without --
    # for example, to set `--parallel 5`:
    #parallel = 5
    
    # if the flag takes no options, use True to set
    #udp = True
    
    # --client <hostname> and server are set automatically don't put them here
    # put all the other settings in, though, and the client vs server stuff will get sorted out
    
    #[ping]
    # 'target' (default: None) is the IP address or name to ping (RVR will use the traffic server if not given)
    # target = www.google.com
    
    # 'time_limit'  is number of seconds to try to ping before giving up
    # time_limit = 300
    
    # 'threshold' is the number of consecutive pings needed for a success
    # threshold = 5
    
    # 'arguments' are the arguments to give the ping command
    # arguments = -c 1 -W 1
    
    # 'operating_system' is used to chose the arguments for the ping
    # operating_system = None
    
    # 'timeout' is the seconds to wait for socket readlines (try to keep above 1 second)
    # timeout = 10
    
    # 'data_expression' is the regular expression to extract the round-trip time (used to check success)
    # data_expression = None
    
    # 'trap_errors'  if False, will raise an error if there is a socket error
    # otherwise it will just log it
    #trap_errors = True
    
    #[query]
    # these are arbitrary commands that will be called in between attenuations
    # it's original use-case is to get RSSI and other monitoring information
    # but since it's free-form you can pass in whatever you like
    # the commands are issued on the DUT, not the traffic-server
    
    # delimiter separating command and expression
    # this is provided so that if the command or expression has a comma in it
    # you can use an alternative
    
    #delimiter =  ,
    
    # if you want to specify a filename set the filename option
    # filename = query.csv
    
    # to change the readline timeout
    # timeout = 10
    
    # to have it crash instead of trap socket errors
    # trap_errors = trap_errors
    
    # everything else is of the format:
    # <column-header> = <command><delimiter><regular expression>
    # the column-header will be used in the csv-file
    # the regular expression has to have a group '()' or it will raise an error
    # the contents of the group is what will be saved to the file
    
    #some examples:
    #rssi = iwconfig wlan0,Signal\slevel=(-\d+\sdBm)
    #noise = wl noise, (.*)
    #bitrate = iwconfig wlan0, Bit\sRate=(\d+\.*\d*\sMb/s)
    #counters = wl counters, (rxcrsglitch [0-9]* )
    #rtt_min/rtt_avg/rtt_max/rtt_mdev = ping -c 2 192.168.103.17,rtt\s+min.*=\s*(.*)\s+ms
    
    #[dump]
    # the dump takes commands that dump their output and saves
    # the output to files. It is mainly intended as a log dump
    # comment this section out if you don't want a dump
    
    # timeout is how long to wait for output
    # timeout = 5
    
    # for the commands you should use the form:
    # <identifier_1> = <command_1>
    # <identifier_2> = <command_2>
    # ...
    # <identifier_n> = <command_n>
    
    # the identifiers can be anything as long as each is unique
    # the command should be the actual string you want to send to the device
    # as an example for 'dmesg':
    # dump = dmesg -k
    
    #[other]
    # a sub-folder name to save the output files in
    # also used for the final csv
    # add {timestamp}  to get a timestamp            
    # e.g. result_location = rvr_{timestamp}
    
    #result_location = output_folder
    
    # identifier for the test 
    #test_name = rate_vs_range
    
    # to run the same test multiple times
    # repetitions = 1
    
    # there is currently a sleep between directions (up and down)
    # use this next setting to change it if it's too long or short
    #recovery_time = 10
    
    



This will dump the sample to standard-out so to use it you need to re-direct it to a file::

   rvr fetch > rvr.ini

I did it this way to prevent accidental over-writes of existing configuration files (originally I was creating the file and users, including myself, sometimes erased one that was meant to be kept). If you are already familiar with the configurations and want to just grab a section you can use the `--section`` option (by `section` I mean the sub-section of the configuration file with the ``[section]`` header). For instance, to append a sample `[dut]` configuration to an existing file called `rvr.ini`::

   rvr fetch --section dut >> rvr.ini

This might also be helpful as a reminder of what goes into each section (just dump it to the screen instead of redirecting it)::

   rvr fetch --section dut

.. highlight:: ini


.. code::

    
    [dut]
    # login information (these are required)
    username = admin
    
    # this isn't if your public keys are working
    #password = root
    
    # address of the control-interface 
    control_ip = 192.168.10.34
    
    # this identifies the type (only 'telnet', 'ssh', or 'fake')
    #connection_type = ssh
    
    # address of the interface to test
    test_ip = 192.168.20.34
    
    # connection time-out in seconds
    #timeout = 1
    
    # optional prefix to add to ALL commands (default: None)
    # this will be added with a space (i.e. <prefix> <command>)
    # so if needed, add a semicolon like in the example between the PATH and adb
    
    #prefix = PATH=/opt:$PATH; adb shell
    
    # the operating system for the DUT
    
    # operating_system = linux
    
    # there are too many options for the different connection-types
    # so you can add necessary parameters but make sure the name
    # matches the parameter name
    # e.g. if you need to set the port:
    # port=52686
    
    
    


   

Getting Help
------------

The Documentation
~~~~~~~~~~~~~~~~~

Here's a dump of the `documentation_requirements.txt` file.


.. code::

    Sphinx==1.2.3
    alabaster==0.6.2
    sphinxcontrib-plantuml==0.5
    
    
    



The source for the main documentation sits at the top level of this package and is built using `make`. Unfortunately there are extra requirements to build it. If you aren't already a sphinx user it might prove problematic. To build it you will need `alabaster`, `sphinx` and `sphinxcontrib-plantuml`::

    pip install alabaster
    pip install sphinx
    pip install sphinxcontrib-plantuml

(you may need to run this as root). `sphinxcontrib-plantuml` requires `plantuml`::

   sudo apt-get plantuml

.. note:: plantuml doesn't always work out of the box for me. Check out the `pypi page for sphinxcontrib-plantuml <https://pypi.python.org/pypi/sphinxcontrib-plantuml>`_ for more information on setting it up.

.. '

You will also need ``graphviz`` for plantuml. On ubuntu you can use::

    sudo apt-get install graphviz

If those have been installed then you can build the documentation by changing into the directory next to the ``Makefile`` and build it (in html) using::

   make html

The output of the `make` command will sit in a folder named `build/<format>` where format is the parameter you passed to `make` -- so if you entered `make html` there will be a folder named `build/html` if everything went as intended.

.. note:: The documentation is also on `the web <http://rallion.bitbucket.org/others/cameraobscura/index.html>`_ I try to push it whenever I make changes but it may be a little behind.

Command-Line Help
~~~~~~~~~~~~~~~~~

Additionally, the command-line help system can prompt you for the options if you can't remember them::

    rvr -h

And you should see something like this.

.. '

.. highlight:: ini


.. code::

    usage: rvr [-h] [-v] [--pudb] [--pdb] [--debug] [--silent] {fetch,run}
    ...
    
    RVR Runner
    
    positional arguments:
      {fetch,run}    RVR Sub-Commands
    
    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  Display the version number and quit
      --pudb         Enable the PUDB debugger default=False.
      --pdb          Enable the python debugger default=False.
      --debug        Enable debugging messages (default=False).
      --silent       Turn off non-error logging messages (default=False).
    
    
    


    

The command should be fairly straight-forward to anyone familiar with unix-like command-options. The one thing that might not be familiar is the use of sub-commands. In the output of the ``rvr -h`` command will be a list in curly braces ``{fetch,run}`` which are sub-commands. They are basically forks in the operation of the code -- choosing ``fetch`` runs one function while choosing ``run`` chooses another. Since they are sub-commands they have their own set of options that you can see with the help command again::

   rvr run -h


.. code::

    usage: rvr run [-h] [configurations [configurations ...]]
    
    positional arguments:
      configurations  Configuration file(s) to use.
                      default=['rvr_configuration.ini']
    
    optional arguments:
      -h, --help      show this help message and exit
    
    
    



Running that last help command should show only the options that can be used with the `run` sub-command (which in case you didn't deduce it, runs the tests).

.. '

Here's the fetch help::

   rvr fetch -h

.. '   


.. code::

    usage: rvr fetch [-h] [-s SECTION]
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SECTION, --section SECTION
                            Section name to retrieve (defaults to all
    sections)
    
    
    



Because configuration files are being used the amount of options being passed in are fairly limited. The top level options are for debugging (and help), the ``fetch`` option is to choose a section to fetch, and the ``run`` option is to pass in a list of configuration file names to use. So, if you had a set of configuration files whose names ended with ``.ini``  you could run them all by using::

   rvr run *.ini

.. '   

.. note:: Since the shell is what's gathering the names the ordering of the tests will follow whatever order the shell uses (I think it's usually lexicographic ordering). If strict ordering is needed it might be better to pass in the file names directly.

Testing the Code
----------------

Here's a dump of the `testing_requirements.txt` file.


.. code::

    PyHamcrest==1.8.1
    behave==1.2.4
    mock==1.0.1
    
    
    



If you want to run the tests you will need `mock <https://pypi.python.org/pypi/mock>`_ it is part of the python 3 standard library but needs to installed for python 2.* versions. There is also no runner for the tests because I use `nose <https://nose.readthedocs.org/en/latest/>`_ to run them.

.. note:: This was true when the updates were first made. Now I use `behave <http://pythonhosted.org/behave/>`_ and `pyhamcrest <http://pyhamcrest.readthedocs.org/en/1.8.0/>`_ instead of nose and the built-in unittest module (I still use mock).

.. code-block:: bash

   pip install behave
   pip install pyhamcrest
   pip install mock

Tangling and Weaving
--------------------

The newer code is written in `pweave <http://mpastell.com/pweave/>`_ format (the ``.pnw`` files are the actual edited sources, the ``.py`` and ``.rst`` files are generated from them). You can edit the ``.py`` or ``.rst`` files directly, but they will be wiped out the next time they are generated (assuming there is a ``pnw`` file, older code was written directly in python files).

To get `pweave`::

   pip install pweave

.. warning:: The latest version of Pweave expects some python 3 syntax so not all the files might be convertible unless you run the older version of pweave. I'll try and make it compatible with the new version, but I'm not going to make an effort to go through all the files and fix things.

To get the older version of Pweave::

  pip install Pweave==0.21

To convert a pnw file to a python file (with the new Pweave, otherwise ``ptangle`` is ``Ptangle`` and ``pweave`` is ``Pweave`` for the older ``pweave``)::

   ptangle somefile.pnw

To convert a pnw file to an rst file::

   pweave somefile.pnw

The ``pweave`` command has a dependency on ``matplotlib`` so even if none of the files use it (which I don't think they do) you have to install it::

   pip install matplotlib   

Or for ubuntu::

   sudo apt-get install python-matplotlib   

If you're using ``pip`` and ``matplotlib`` is having a hard time, you can install the dependencies through ``apt-get`` first::

   sudo apt-get build-dep python-matplotlib

.. note:: I rsync the output of ``make html`` to my web-server directory. This will produce an error at the end of the `make` command (unless you coincidentally have the same folder structure that I do) but that is unrelated to building the documentation.

Plugin Dependencies
-------------------

The ``rvr`` command was built to be standalone, but to open up the possibilities of combining it with other packages, there is currently a plugin for the ``TheApe`` in it (I'll probably put it in its own repository eventually). For it to work (or at least to test it), the APE and its dependencies are required (e.g. `configobj <http://configobj.readthedocs.org/en/latest/>`_), but since ``TheApe`` is itself a dependency they should be installed when this package is installed.

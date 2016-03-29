The Command Line Interface
==========================




.. _user-documentation-cli-introduction:

Introduction
------------

The user runs the program in the shell (e.g. bash) via a command line interface (CLI) that has three main purposes -- to get sample configurations, to run tests, and to help with debugging. It's similar in operation to most unix commands, although it also uses sub-commands which may seem a little odd if you've never used them before, but since most of the settings for the program are done in a configuration file, the CLI is minimal enough that they shouldn't prove difficult to understand. With the exception of getting help, all commands take the form::

    rvr [options] <sub-command> [sub-command options]

The help option helps remind you of what the options are::

    rvr --help

.. '
    
Entering that at the command-line should give you an output that looks something like this:


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
    
    
    



The first line ``usage: ...`` gives the command (``rvr``), its options in square brackets (``-h, -v, --pudb, --debug`` and ``--silent``) and the sub-commands in curly brackets (``fetch`` and ``run``). At the bottom of the output is a brief explanation of the options. We'll cover the options next and then go over the what the two sub-commands are and how to use them.

.. _user-documentation-cli-rvr-options:

The ``rvr`` Options
-------------------

Other than the ``-h`` option,  the options passed to the ``rvr`` command (``version, pudb, debug``, and ``silent``) are primarily meant for debugging problems so hopefully you won't ever need to use them. To get the version you would enter::

    rvr --version

I'm using the date of the most recent change as the version number, but it isn't being dynamically set, so it might not be completely up-to-date. If you have the `python urwid debugger (pudb) <https://pypi.python.org/pypi/pudb>`_ installed and want to step through the code as it runs you can use the option::

    rvr --pudb <subcommand> [<subcommand options>]

The last two options are there so you can change the logging output level. By default all logging goes to the log file `rate_vs_range.log` in the output folder that holds the test-data while only info-level output is sent to the screen. To see all the output you would use something like::

    rvr --debug run rvr_configuration.ini

To turn off all the output except errors::

    rvr --silent run rvr_configuration.ini

I'll cover the ``run rvr_configuration.ini`` part of that command in the next section.

.. _user-documentation-cli-run:

The ``run`` Sub-Command
-----------------------

The ``run`` sub-command is the main sub-command for this code. It tells the program to run the test specified in the configuration file(s) it's given. As a sub-command it also accepts the ``help`` flag::

    rvr run -h

Which should output:


.. code::

    usage: rvr run [-h] [configurations [configurations ...]]
    
    positional arguments:
      configurations  Configuration file(s) to use.
                      default=['rvr_configuration.ini']
    
    optional arguments:
      -h, --help      show this help message and exit
    
    
    



Specifying Files
~~~~~~~~~~~~~~~~

The ``configurations`` option is a positional argument (you don't specify an option name, just give the parameter-values) that expects a space-separated list. There are a few ways you can use it. First, it has as it's default value a list of a single file named `rvr_configuration.ini` so if you give your configuration file the same name as the default you can ignore the parameter::

    rvr run

If you have a single configuration file with a different name you need to specify it at the end::

    rvr run other_configuration.ini

If you want to run multiple configurations you can pass in a space-separated list::

    rvr run config_1.ini config_2.ini config_3.ini

Using Globs
~~~~~~~~~~~

Or, if the configurations are the only ones that have a certain sub-string (in this example we'll assume they all end in `.ini`), then you can use a glob::

    rvr run *ini

.. '    

If there are certain sets of configurations that get run one thing you could do is put tokens in their names that help you filter them using file-globbing. Say you have a folder in your home directory named 'configurations' and within it is set of configurations that you want to run one after the other that all have the token `netgear` in their name, then to run them you could use the following::

    rvr run ~/configurations/*netgear*

Because of the extra setup needed for chamber-related work this may not be a common use-case, but it also illustrates the fact that the `configurations` parameter doesn't have to point to a file in your current working directory. If you have frequently used configurations you can keep them somewhere more convenient and use the full path (or relative path) to point the ``rvr run`` command to them.

.. '

.. _user-documentation-cli-fetch:

The ``fetch`` Subcommand
------------------------

The ``fetch`` sub-command has two main purposes -- to get a sample configuration which you can edit to configure a test and to provide a quick reference to check while editing or creating a configuration. You can check the ``fetch`` options::

    rvr fetch -h


.. code::

    usage: rvr fetch [-h] [-s SECTION]
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SECTION, --section SECTION
                            Section name to retrieve (defaults to all
    sections)
    
    
    



Fetching a Sample Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rather than copying a file over to your current working directory the ``fetch`` prints the sample(s) to the screen. So, if you want to inspect the sample, you can pipe it to less (or grep if there's a specific line you want to see)::

    rvr fetch | less

If you want to have a sample configuration to edit, you should redirect the output to a file::

    rvr fetch > rvr_configuration.ini

.. '

Fetching Sections Within the Sample Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration is composed of sections (denoted by names within square brackets (e.g. ``[attenuation]``)). If you only want to see a specific section you can name it as an option. Using the ``attenuation`` section as an example::

    rvr fetch --section attenuation

This will send only the ``attenuation`` configuration to the screen. This can be used to add any missing sections to an existing configuration file as well. Suppose you got rid of the ``query`` section to make the configuration file cleaner but now want to add it. To add the sample for editing you could use redirection and append it to the end of the file::

    rvr fetch -s query >> rvr_configuration.ini

Grepping the Section Headers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get a list of the sections you can use grep. To get a list of required sections::

    rvr fetch | grep "^\["


.. code::

    [attenuation]
    [dut]
    [server]
    [iperf]
    
    



To get a list of optional sections::

    rvr fetch | grep "^#\["


.. code::

    #[ping]
    #[query]
    #[dump]
    #[other]
    
    



To get all the sections::

    rvr fetch | grep "^#\[\|^\["


.. code::

    [attenuation]
    [dut]
    [server]
    [iperf]
    #[ping]
    #[query]
    #[dump]
    #[other]
    
    



If that last regex is too much trouble to remember just grep for the square brackets ``grep "\["`` and ignore any extra lines that don't look like section headers. Also note that the first section "[QUEMANAGER]" is there for historical reasons and you won't be able to fetch it by itself.

Conclusion
----------

We have covered the main points you need to know about when using the ``rvr`` command. Most of the time you will only be using the ``rvr run`` sub-command, which makes it easy to forget how to set up the configuration files. Using the ``rvr fetch`` will hopefully provide enough of a reminder of the basic configuration-file form so that you can create or edit them whenever you need to. To get a more detailed explanation of what goes into the configuration file, check the :ref:`Configuration Files <user-documentation-configuration-files>` documentation.

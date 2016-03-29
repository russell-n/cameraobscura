The Dump
========

The **Dump** is a module to dump some output from a device. It is similar to the query but differs in that it expects to capture multi-line output and dump it to a file. Think `dmesg`.







.. _the-dump-use-case:

Use Case
--------

.. uml::

   User - (Dump command output to file)

Main Path
~~~~~~~~~

*The Dump* is fairly primitive and acts more as a way to bundle things together.

    #. Open writeable file
    #. Send command to device
    #. Redirect stdout to the file
    #. Redirect stderr to log
    #. Close the file

Alternate Path
~~~~~~~~~~~~~~

I'm not sure how it's going to be used, but I'll assume that socket errors and other connection-related errors should be noted but shouldn't kill the program.

    3.1.1. Socket error is caught
    3.1.2. Error logged
    3.1.3. Quit

.. _the-dump-constants:

Dump Constants
--------------

Some constants put into a class so other modules can get them.


.. code:: python

    class DumpConstants(object):
        """
        Constants for the Dump
        """
        __slots__ = ()
        # defaults
        default_timeout = 5
        default_delimiter = ','
    
        # configuration
        section = 'dump'
    
        # options
        timeout = 'timeout'
    
        example = textwrap.dedent("""
    #[{s}]
    # the dump takes commands that dump their output and saves
    # the output to files. It is mainly intended as a log dump
    # comment this section out if you don't want a dump
    
    # timeout is how long to wait for output
    # timeout = {time}
    
    # for the commands you should use the form:
    # <identifier_1> = <command_1>
    # <identifier_2> = <command_2>
    # ...
    # <identifier_n> = <command_n>
    
    # the identifiers can be anything as long as each is unique
    # the command should be the actual string you want to send to the
    device
    # as an example for 'dmesg':
    # dump = dmesg -k
        """.format(s=section,
                   time=default_timeout))
    
    # end DumpConstants
    


    
.. _the-dump-class:

The Dump Class
--------------

.. currentmodule:: cameraobscura.utilities.dump
.. autosummary::
   :toctree: api

   TheDump
   TheDump.filename
   TheDump.__call__




.. _the-dump-configuration:

Dump Configuration
------------------

A configuration class to make getting values from the config-file maybe a little easier.

.. autosummary::
   :toctree: api

   DumpConfiguration





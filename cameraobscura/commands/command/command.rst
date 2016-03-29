The Command
===========



Contents:

    * :ref:`Introduction <command-introduction>`
    * :ref:`Design <command-design>`
    * :ref:`Command Constants <command-constants>`
    * :ref:`socketerrors Decorator <command-socketerrors-decorator>`
    * :ref:`Command Class <command-class>`

.. _command-introduction:

Introduction
------------

This is a building block to execute non-blocking commands and extracting data from the output. It's probably not the right choice for things like `iperf` where there is a lot of data (although if you aren't using the ``--interval`` flag it might work).

It is based on :ref:`The Query <query-class-implementation>` (and should be what the Query is using). The idea is to allow user's an open-ended way to send commands to the device and get data. It's assumed that this data will then be used in some way -- as opposed to :ref:`The Dump <the-dump-class>` which just dumps the output to a files. To make this possible three things are needed:

   * The command string
   * An argument string for the command
   * A regular expression to search the output

The argument-string is optional (since the command-string can contain all the options). The regular expressions needs to have a group, denoted with parentheses '()' in python's `regular expression syntax <https://docs.python.org/2/library/re.html#regular-expression-syntax>`_. If no group is put into the regular expression it's assumed that an error was made. 

Additionally, the `Command` will check standard error using a regular expression so that known errors can be used to halt operation (if that's a good idea). To make it easier for the end user the default will be to log the errors but not raise an exception (so the user has to purposefully set the expression for it to actually raise an error).

A final element to consider when using `TheCommand` is whether a socket timeout should raise an exception or not. By default it won't (as noted the inspiration was the `Query` class which is assumed to be less important than the main part of the testing and thus tries not to kill the entire program). If it should be fatal than the `trap_errors` should be set to False (despite the name it will only try to catch socket-based errors).

.. _command-design:

Design Elements
---------------

Use Case
~~~~~~~~

.. uml::

   User -> (Requests output from a command)

Main Path
~~~~~~~~~

   #. send command, arguments, and timeout to the connection
   #. traverse the lines in stdout
   #. search each line with a regular expression
   #. return the first match 
   #. traverse the lines in stderr
   #. search each line with a regular expression
   #. raise an error on match

Alternate Path
~~~~~~~~~~~~~~

   2.1.1. Socket time-out

   2.1.2. if the trap-error flag was set, log the error and quit

   2.1.3. if not, raise an exception

.. _command-constants:

Command Constants
-----------------

A holder of constants for TheCommand.

::

    START_OF_STRING = r'^'
    ANYTHING = r'.'
    ZERO_OR_MORE = r'*'
    GROUP = r'({0})'
    
    EVERYTHING = GROUP.format(ANYTHING + ZERO_OR_MORE)
    NOTHING = r'a' + START_OF_STRING
    NEWLINE = '\n'
    
    class CommandConstants(object):
        """
        Constants for the Command
        """
        __slots__ = ()
        # defaults
        default_arguments = ''
        default_timeout = 5
        default_trap_errors = True
        default_data_expression = EVERYTHING
        default_error_expression = NOTHING
    
    



.. _command-socketerrors-decorator:

socketerrors Decorator
----------------------

This is a decorator to handle catching socket errors so the __call__ doesn't get too unwieldy.

.. '

.. currentmodule:: cameraobscura.commands.command.command
.. autosummary::
   :toctree: api

   socketerrors



.. _command-class:

The Command Class
-----------------

.. uml::

   BaseClass <|-- TheCommand
   TheCommand o- TheHost
   TheCommand : String identifier
   TheCommand : String command
   TheCommand : String arguments
   TheCommand : String data_expression
   TheCommand : String error_expression
   TheCommand : Float timeout
   TheCommand : Boolean trap_errors
   TheCommand : String __call__

.. autosummary::
   :toctree: api

   TheCommand
   TheCommand.command
   TheCommand.arguments
   TheCommand.command_arguments
   TheCommand.data_expression
   TheCommand.error_expression
   TheCommand.identifier
   TheCommand.__call__
   

The Command Class is responsible for maintaining a connection, a command and its arguments, and regular expressions to search the output. When called, it sends the command and searches the output, returning matched (group) strings or handles errors depending on how it was configured.

Its main collaborator would be something that looks like one of the clients (hopefully the :ref:`SimpleClient <simpleclient>`) or :ref:`the Host <host-host>` (it will only expect the `exec_command` method).

The Constructor
~~~~~~~~~~~~~~~

The only required arguments are `connection` and `command`. Arguments are optional in the event that the `command` parameter is actual a complete string of `command` + `arguments` (e.g. 'ls -a').

The Call
~~~~~~~~

.. figure:: figures/command_activity.svg
   :align: center

   TheCommand's Activity Diagram

.. '
   

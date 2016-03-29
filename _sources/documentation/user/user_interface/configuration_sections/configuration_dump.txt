Dump Configuration
------------------



The ``dump`` section is an optional section that will call the commands it's given after testing is over and dumps standard out to a file. It is sort of similar to the :ref:`queries <user-documentation-configuration-query>` but is intended more for things like ``logcat`` or ``dmesg`` where you want everything and it doesn't make sense to call them over and over.

::

    #[dump]
    # timeout = 5
    # <identifier_1> = <command_1>
    # <identifier_2> = <command_2>
    # <identifier_n> = <command_n>
    # dump = dmesg -k
    
    



Each command line uses the form::

    <identifier> = <command>

The `<identifier>` will be used as the basename for the output file (with a `.txt` extension) which will be put in a sub-folder named `dump`. So in the above example the output of `dmesg` will be put in a file named `dump.txt`.


``timeout``
~~~~~~~~~~~

This is the socket-timeout value. For some very large output dumps you will need to extend it. Although it's ugly, you could also use this to grab non-terminating output (some logs don't return an end-of-file character) by making it timeout (which it will do eventually anyway).


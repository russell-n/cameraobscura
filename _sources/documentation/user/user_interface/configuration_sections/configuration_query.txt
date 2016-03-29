Query Configuration
-------------------



The ``query`` section is an optional section that allows the user to make arbitrary queries to the device in the chamber (DUT) between tests. It was created because there appeared to be some unused code that did things like retrieve RSSI and similar information. Since it's completely free-form it is simultaneously somewhat restricted -- each command has to be accompanied by a regular expression that will extract the desired data using `groups <https://docs.python.org/2/howto/regex.html#grouping>`_. This is because output is being put into a csv and different commands put out differing lines of output (and much of the interesting data is accessible through non-standard commands (e.g. ``wl`` vs ``iw``...)).

.. note:: The connection being used is being configured by the `dut` section. If you set the ``prefix`` in it, you don't have to use the full path for the command here (if it's not in the PATH). On the other hand, if these commands are in some strange place where only they are (i.e. not the same place as iperf or ping) then you can put the full path here and forget the ``prefix`` in the ``dut`` section. Either (or both) will work, but putting 'adb shell' in both places won't.

::

    #[query]
    #delimiter =  ,
    # filename = query.csv
    # timeout = 10
    # trap_errors = trap_errors
    # <column-header> = <command><delimiter><regular expression>
    #rssi = iwconfig wlan0,Signal\slevel=(-\d+\sdBm)
    #noise = wl noise, (.*)
    #bitrate = iwconfig wlan0, Bit\sRate=(\d+\.\d\sMb/s)
    #counters = wl counters, (rxcrsglitch [0-9]* )
    
    



The basic format for each 'query' you want to make::

    <identifier> = <command>,<regular expression>

.. csv-table:: Query Parts
   :header: Part, Description

   identifier, a string that will be used for the column header in the csv 
   command, a string that will be sent to the device to execute whatever is in it
   regular expression, a regular expression that will extract the data using a group   

As an example, here's how to get RSSI, BitRate, and Link Quality from a device that uses `iwconfig`::

   [query]

   rssi = iwconfig wlan0,Signal level=(-\d+)\s+dBm
   bitrate = iwconfig wlan0,Bit\sRate=(.+)\s[M]?b/s
   link_quality = iwconfig wlan0,Link\sQuality=(\d+/\d+)\s

The program will also add the attenuation and a timestamp to the output file would have something like the following in it:

.. csv-table:: Downstream Query
   :file: downstream_query.csv
   :header-rows: 1

``delimiter``
~~~~~~~~~~~~~

The default configuration expects the `<command>` and `<regular expression>` to be separated by a comma. In the event that either one of them requires a comma, you will need to change the delimiter to something that doesn't conflict. Using the rssi example above (although it doesn't have a comma in it, let's just pretend)::

   [query]
   delimiter = ;

   rssi = iwconfig wlan0;Signal level=(-\d+)\s+dBm

``filename``
~~~~~~~~~~~~

The ``filename`` is the name to use for the output file. In practice I decided it would be better to separate the upstream and downstream files so the ``filename`` acts as a suffix to which a direction prefix is added. Additionally, since there's so many files they all get put into a sub-folder named `queries`.

``timeout``
~~~~~~~~~~~

This is a socket-timeout value (the number of seconds to wait while reading a line before giving up). Since the commands are arbitrary the initial assumption is that they are non-blocking and quick. If the response is too slow and it starts raising errors you can extentd the timeout to try and work around it.

``trap_errors``
~~~~~~~~~~~~~~~

The default behavior of the program is to trap errors raised by calling these commands (most likely socket-timeouts) so that they don't kill the testing. If the data from the commands are critical or you want to troubleshoot failures, set this to 'false' and the program will stop whenever a command fails.


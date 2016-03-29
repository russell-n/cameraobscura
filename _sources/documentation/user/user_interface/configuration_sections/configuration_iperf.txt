Iperf Configuration
-------------------



The ``iperf`` section is where you set the iperf settings.

::

    #[other]
    #result_location = output_folder
    #test_name = rate_vs_range
    # repetitions = 1
    #recovery_time = 10
    
    



``direction``
~~~~~~~~~~~~~

This is the only non-iperf flag. It looks at the first letter of the setting and decides which direction to send traffic. This assumes that traffic is alternating and is oriented to the device sitting in the chamber (called `dut` here).

.. csv-table:: Iperf Directions
   :header: First Letter, Full Name, Meaning

   u, upstream, Traffic is sent from the DUT to the traffic server (simulated upload)
   d, downstream, Traffic is sent to the DUT from the traffic server (simulated download)
   b, both, Traffic alternates between upstream and downstream

So, to run testing only from the DUT to the traffic server::

    direction = up

To run direction only from the traffic server to the DUT::

    directly = down    

Client and Server
~~~~~~~~~~~~~~~~~

Although there are iperf options to determine the direction of the traffic (``-c, --client`` and ``-s, server``) these are set within the program based on the ``direction`` setting and the IP addresses taken from the ``server`` and ``dut`` sections so you shouldn't try and set them (it should crash the program).

.. '

Everything Else
~~~~~~~~~~~~~~~

All the other settings are taken form the long option-names used by iperf::

    iperf -h

::

    Usage: iperf [-s|-c host] [options]
           iperf [-h|--help] [-v|--version]
    
    Client/Server:
      -f, --format    [kmKM]   format to report: Kbits, Mbits, KBytes, MBytes
      -i, --interval  #        seconds between periodic bandwidth reports
      -l, --len       #[KM]    length of buffer to read or write (default 8 KB)
      -m, --print_mss          print TCP maximum segment size (MTU - TCP/IP header)
      -o, --output    <filename> output the report or error message to this specified file
      -p, --port      #        server port to listen on/connect to
      -u, --udp                use UDP rather than TCP
      -w, --window    #[KM]    TCP window size (socket buffer size)
      -B, --bind      <host>   bind to <host>, an interface or multicast address
      -C, --compatibility      for use with older versions does not sent extra msgs
      -M, --mss       #        set TCP maximum segment size (MTU - 40 bytes)
      -N, --nodelay            set TCP no delay, disabling Nagle's Algorithm
      -V, --IPv6Version        Set the domain to IPv6
    
    Server specific:
      -s, --server             run in server mode
      -U, --single_udp         run in single threaded UDP mode
      -D, --daemon             run the server as a daemon
    
    Client specific:
      -b, --bandwidth #[KM]    for UDP, bandwidth to send at in bits/sec
                               (default 1 Mbit/sec, implies -u)
      -c, --client    <host>   run in client mode, connecting to <host>
      -d, --dualtest           Do a bidirectional test simultaneously
      -n, --num       #[KM]    number of bytes to transmit (instead of -t)
      -r, --tradeoff           Do a bidirectional test individually
      -t, --time      #        time in seconds to transmit for (default 10 secs)
      -F, --fileinput <name>   input the data to be transmitted from a file
      -I, --stdin              input the data to be transmitted from stdin
      -L, --listenport #       port to receive bidirectional tests back on
      -P, --parallel  #        number of parallel client threads to run
      -T, --ttl       #        time-to-live, for multicast (default 1)
      -Z, --linux-congestion <algo>  set TCP congestion control algorithm (Linux only)
    
    Miscellaneous:
      -x, --reportexclude [CDMSV]   exclude C(connection) D(data) M(multicast) S(settings) V(server) reports
      -y, --reportstyle C      report as a Comma-Separated Values
      -h, --help               print this message and quit
      -v, --version            print version information and quit
    
    [KM] Indicates options that support a K or M suffix for kilo- or mega-
    
    The TCP window size option can be set by the environment variable
    TCP_WINDOW_SIZE. Most other options can be set by an environment variable
    IPERF_<long option name>, such as IPERF_BANDWIDTH.
    
    Report bugs to <iperf-users@lists.sourceforge.net>
    
    



So, for instance, to set it to run upstream and downstream with 6 parallel threads for 5 minutes, with values output at 1 second intervals and a TCP window-size of 256K you would use::

   [iperf]
   direction = both

   parallel = 6
   interval = 1
   time = 300
   window = 256K

For flags that don't take values (e.g. ``--udp``) set use 'true' as the value::

    udp = true

.. '
    
Special Considerations
~~~~~~~~~~~~~~~~~~~~~~

Here are some miscellaneous things I thought of while re-doing this code.

   * If you use a serial connection (via telnet) the code isn't currently breaking the server-side connection, so if you want TCP you should set the ``--daemon`` flag
   * If you set the ``--daemon`` flag, you won't  get the server-side output so you can get the server's final response (via the client output) but not second by second output
   * The iperf-parser in here is pretty fragile, I crashed it pretty easily, but the raw-iperf files are there in the data folder
   * Iperf seems to have arbitrarily truncated some words -- they use `window` but shortened `length` to `len`... make sure to check what they should be

   

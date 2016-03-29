The Attenuation Section
-----------------------



The ``attenuation`` section is where you set parameters for the Attenuator and how it will be set during the test. The default sample (with comments removed):

::

    [attenuation]
    #start = 0
    #stop = 9223372036854775807
    #name = WeinschelP
    control_ip = 192.168.10.53
    #step_sizes = [1]
    #step_change_thresholds = 
    
    



The options that are commented out have default values so you don't need to specify them if you don't want to (and the defaults work for you). 

``start`` Option
~~~~~~~~~~~~~~~~

This is the attenuation value to use at the start of the testing. It's optional with a default value of 0.


``stop`` Option
~~~~~~~~~~~~~~~

The ``stop`` option is where you set the maximum attenuation you want to try. If you don't set it the value will be retrieved from the attenuator (the program will ask it what the maximum attenuation setting is and take the smaller value of what's set here and what the attenuator allows). The default is the largest integer python allows, which guarantees tha what the attenuator says is its maximum will be less than or equal to the default.

.. note:: the testing will stop if the device in the chamber can't ping the traffic server (if this option is set) or iperf traffic can't be run so this value will in most cases not be reached, assuming it is set high enough.

.. '

``name`` Option
~~~~~~~~~~~~~~~

This is where you set the name of the attenuator that you are using (this isn't case-sensitive). It has to match the name of a class within the program that was created to control the attenuator. It has a default setting (see below) so if that matches the attenuator that you are using, then you can leave this option out.

.. '

The currently available values you can use are:

   * MockAttenuator
   * AdeptNCustomPath
   * WeinschelP
   * AdeptN

The Default Attenuator is **WeinschelP**.



The **MockAttenuator** is a debugging tool. If you want to check other parts of the testing but you don't need the attenuator then set it to that and it will echo the commands it gets to the screen but not do anything else.

.. '

``control_ip``
~~~~~~~~~~~~~~

This is the IP Address to reach the attenuator (or the PC controlling the attenuator).

``step_sizes`` and ``step_change_thresholds``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``step_sizes`` sets the sizes of the attenuation changes. It takes a space-separated list. The default is to increment the attenuations by 1 so if this is what you want, you don't need to define this option. If you want a constant increase between each test that isn't 1, you can set the value and ignore the fact that it expects a list::

   step_sizes = 5

If you want there to be a change in the amount the attenuation is increased as the test progresses, you need to set the ``step_sizes`` to the attenuation increments you want and then set the ``step_change_thresholds`` to a space-separated list of the trigger-values that prompt the change in increments.

Let's say you want the attenuations to initially increment by 1 and then start to increment by 2 once the attenuation has reached 10(or greater). You would set the values to these::

    step_sizes = 1 2
    step_change_thresholds = 10

.. '

There is no logic built in to check the values you set so you can make as many changes as you want, but there always has to be one fewer ``step_change_thresholds`` value than there are ``step_sizes`` values or it will raise an error. This, for instance::

    step_sizes = 1 10 1
    step_change_thresholds = 5 100

Will initially increase by 1 until it reaches 5 then increase by 10 until it reaches 100 at which point it will drop back to increments of 1. This, on the other hand::

    step_sizes = 1 10 5
    step_change_thresholds = 10 2

Will increment by 1, then increment by 10 once and then increment by 5 the rest of the time (because you were already past the final threshold of 2  when the first threshold was reached so it gets triggered as soon as the threshold value is checked again).

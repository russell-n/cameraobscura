DumpConfiguration
=================

.. literalinclude:: ../features/dumpconfiguration.feature
   language: gherkin




Scenario: User creates the default dump configuration
-----------------------------------------------------


.. code:: python

    default_configuration = """
    [dumper]
    #dmesg = dmesg -k
    """.splitlines()




.. code:: python

    @given("a default dump configuration")
    def default_dump(context):
        context.configuration = DumpConfiguration(source=ConfigObj(default_configuration),
                                                  section_name='dumper')
        context.configuration.check_rep()
        return




.. code:: python

    @when("the dump configuration values are checked")
    def check_defaults(context):
        return




.. code:: python

    @then("the dump configuration values are defaults")
    def assert_defaults(context):
        constants = DumpConstants
        config = context.configuration.configuration
        assert_that(config[DumpConstants.timeout],
                    is_(equal_to(DumpConstants.default_timeout)))
        return



Scenario: User configures the dump configuration
------------------------------------------------


.. code:: python

    non_default_configuration = """
    [dumps]
    timeout = 33
    
    dmesg = dmesg -k
    logcat = adb logcat -d
    """.splitlines()




.. code:: python

    @given("a non-default dump configuration")
    def non_default_dump(context):
        context.configuration = DumpConfiguration(source=ConfigObj(non_default_configuration),
                                                  section_name='dumps')
        context.configuration.check_rep()
        return


  

.. code:: python

    @when("the dump configuration values are all checked")
    def check_values(context):
        return




.. code:: python

    @then("the dump configuration will match the settings")
    def match_settings(context):
        config = context.configuration.configuration
        constants = DumpConstants
    
        assert_that(config['dmesg'],
                    is_(equal_to('dmesg -k')))
    
        assert_that(config[constants.timeout],
                    is_(equal_to(33)))
    
        assert_that(config['logcat'],
                    is_(equal_to('adb logcat -d')))
        return







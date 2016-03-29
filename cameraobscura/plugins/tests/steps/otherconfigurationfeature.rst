Other Configuration
===================

.. literalinclude:: ../features/otherconfiguration.feature
   :language: gherkin




Scenario: User creates other configuration
------------------------------------------


.. code:: python

    empty_source = """
    [rvr]
    """.splitlines()




.. code:: python

    @given("an other configuration")
    def other_configuration(context):
        context.configuration = OtherConfiguration(section_name='rvr',
                                                   source=ConfigObj(empty_source))
        #check-rep will fail because it is calling the composed sub-configfurations
        #context.configuration.check_rep()
        return




.. code:: python

    @when("the user checks the other configuration")
    def check_other_configuration(context):
        return




.. code:: python

    @then("the other configuration will have the defaults")
    def assert_defaults(context):
        config = context.configuration.configuration
        assert_that(config['result_location'],
                    is_(equal_to('output_folder')))
    
        assert_that(config['test_name'],
                    is_(equal_to('rate_vs_range')))
    
        assert_that(config['repetitions'],
                    equal_to(1))
        assert_that(config['recovery_time'],
                    is_(equal_to(10)))
        return


    

Scenario: User creates other configuration with non-defaults
------------------------------------------------------------


.. code:: python

    user_values = """
    [arr_vee_arr]
    result_location = over_there
    test_name = rorschach
    repetitions = 357
    recovery_time = 75
    """.splitlines()




.. code:: python

    @given("an other configuration with non-defaults")
    def non_default(context):
        context.configuration = OtherConfiguration(section_name='arr_vee_arr',
                                                   source=ConfigObj(user_values))
        #context.configuration.check_rep()
        return




.. code:: python

    @when("the user checks the other configuration values")
    def check_values(context):
        return




.. code:: python

    @then("the other configuration will have the user-values")
    def assert_user_values(context):
        config = context.configuration.configuration
        options = 'result_location test_name repetitions recovery_time'.split()
        values = 'over_there rorschach'.split()  + [357, 75]
        for key, value in izip(options, values):
            assert_that(config[key],
                        is_(equal_to(value)))
        return



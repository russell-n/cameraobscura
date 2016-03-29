Attenuation Configuration
=========================

.. literealinclude:: ../features/attenuationconfiguration.feature
   :language: gherkin




Scenario: User creates AttenuationPluginConfiguration
-----------------------------------------------------


.. code:: python

    base_configuration = """
    [attenuation]
    control_ip = 192.168.10.32
    """.splitlines()




.. code:: python

    @given("an AttenuationPluginConfiguration")
    def attenuation_configuration(context):
        context.a_configuration = AttenuationPluginConfiguration(source=ConfigObj(base_configuration),
                                                         section_name='attenuation')
        context.a_configuration.check_rep()
        return




.. code:: python

    @when("the AttenuationPluginConfiguration is checked")
    def check_attenuation_configuration(context):
        return




.. code:: python

    @then("it is an ape SubConfiguration")
    def assert_base_configuration(context):
        assert_that(context.a_configuration,
                    is_(instance_of(SubConfiguration)))
        assert_that(context.a_configuration.configuration['control_ip'],
                    is_(equal_to('192.168.10.32')))
        return




.. code:: python

    @then("it has the AttenuationPluginConfiguration defaults")
    def check_defaults(context):
        config = context.a_configuration.configuration
        constants = AttenuationEnum
        assert_that(config[constants.start],
                    is_(equal_to(constants.default_start)))
        assert_that(config[constants.stop],
                    is_(equal_to(constants.default_stop)))
    
        assert_that(config[constants.name],
                    is_(equal_to(constants.default_attenuator)))
    
        assert_that(config[constants.step_sizes],
                    contains(*constants.default_step_sizes))
    
        assert_that(config[constants.step_change_thresholds],
                    is_(None))
        return



Scenario: User sets AttenuationPluginConfiguration values
---------------------------------------------------------


.. code:: python

    attenuation_configuration = """
    [attenuation]
    control_ip = hostname
    start = 100
    stop = 500
    name = MockAttenuator
    step_sizes = 1,5,10
    step_change_thresholds = 5,2
    reversal_limit = 1
    """.splitlines()




.. code:: python

    @given("an AttenuationPluginConfiguration with values")
    def configuration_values(context):
        context.a_configuration = AttenuationPluginConfiguration(source=ConfigObj(attenuation_configuration),
                                                         section_name='attenuation')
        context.a_configuration.check_rep()
        return




.. code:: python

    @when("the AttenuationPluginConfiguration values are checked")
    def check_values(context):
        return




.. code:: python

    @then("the AttenuationPluginConfiguration values are correct")
    def assert_values(context):
        # this doesn't do anything now because I changed the way the class works
        context.a_config = context.a_configuration.attenuation_configuration
    
        return




.. code:: python

    @then("the AttenuationPlugin values are correct")
    def assert_values(context):
        assert_that(context.a_config.control_ip,
                    is_(equal_to('hostname')))
        assert_that(context.a_config.start,
                    is_(equal_to(100)))
        assert_that(context.a_config.stop,
                    is_(equal_to(500)))
        assert_that(context.a_config.step_sizes,
                    contains(1, 5 , 10))
        assert_that(context.a_config.name,
                    is_(equal_to('MockAttenuator')))
        assert_that(context.a_config.step_change_thresholds,
                    contains(5,2))
        assert_that(context.a_config.reversal_limit,
                    is_(equal_to(1)))
        return



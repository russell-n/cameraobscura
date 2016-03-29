Iperf Configuration
===================

.. literalinclude:: ../features/iperfconfiguration.feature
   :language: gherkin




Scenario: Iperf Configuration
-----------------------------


.. code:: python

    section = """
    [action]
    jackson = hole
    """.splitlines()
    
    @given("an iperf configuration with no parameters")
    def default_configuration(context):
        context.configuration = IperfPluginConfiguration(ConfigObj(section),
                                                         section_name='iperf')
        context.configuration.check_rep()
        return




.. code:: python

    @when("the iperf configuration is checked")
    def check_configuration(context):
        try:
            context.iperf_configuration = context.configuration.configuration
        except KeyError:
            pass
        return




.. code:: python

    # this gets called many times
    # so make it simpler
    def assert_equal(expected, actual):
        assert_that(actual,
                    is_(equal_to(expected)),
                    "Actual: {0} Expected: {1}".format(actual,
                                                          expected))
        return
    
    def assert_same(expected, actual):
        assert_that(actual,
                    is_(same_instance(expected)),
                    "Actual: {0} Expected: {1}".format(actual,
                    expected))




.. code:: python

    @then("the iperf configuration has the defaults")
    def assert_defaults(context):
        assert_equal(IperfEnum.default_direction,
                     context.configuration.direction)
        assert_equal(context.configuration.server_settings.prefix,
                     str(context.configuration.server_settings))
    
        # client settings needs a hostname before being used
        # but that's set later in the code
        # so fake it here
        context.configuration.client_settings.server = 'bob'
        expected = '{0} {1}'.format(context.configuration.client_settings.prefix,
                                    'bob')
        assert_equal(context.configuration.client_settings.prefix,
                     str(context.configuration.client_settings))
        return



Scenario: Iperf with some settings
----------------------------------


.. code:: python

    configuration = """
    [traffic]
    direction = up
    parallel = 20
    interval = 1
    bandwidth = 12K
    udp = True
    """.splitlines()




.. code:: python

    @given("an iperf configuration with some parameters")
    def some_parameters(context):
        context.configuration = IperfPluginConfiguration(ConfigObj(configuration),
                                                         section_name='traffic')
        context.configuration.check_rep()
        return



When the iperf configuration is checked


.. code:: python

    @then("the configuration has the iperf parameters")
    def assert_iperf_parameters(context):
        assert_equal(context.configuration.direction,
                     IperfEnum.upstream)
        assert_equal(context.configuration.configuration['parallel'],
                     20)
        expected = ' --server --udp  --interval 1'
        assert_equal(expected,
                     str(context.configuration.server_settings))
    
        context.configuration.client_settings.server = 'ted'
        expected = ' --client ted --udp  --bandwidth 12K --parallel 20 --interval 1'
        assert_equal(expected,
                    str(context.configuration.client_settings))
        return




.. code:: python

    @then("the IperfConfiguration is ready")
    def iperfconfiguration_check(context):
        assert_equal(context.configuration.direction,
                     context.configuration.iperf_configuration.direction)
        assert_same(context.configuration.server_settings,
                    context.configuration.iperf_configuration.server_settings)
    
        assert_same(context.configuration\
                           .client_settings,
                    context.configuration\
                           .iperf_configuration\
                           .client_settings)
    
        return



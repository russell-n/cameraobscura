RVR Plugin
==========

.. literalinclude:: ../features/rvrplugin.feature
   :language: gherkin




Scenario: User builds the RVR Plugin
------------------------------------


.. code:: python

    @given("an instance of the RVR Plugin")
    def rvr_plugin_instance(context):
        context.plugin = RVR()
        return




.. code:: python

    @when("the RVR Plugin is checked")
    def check_plugin(context):
        context.expected = BasePlugin
        return




.. code:: python

    @then("the RVRPlugin is an APE Plugin")
    def assert_ape(context):
        assert_that(context.plugin,
                    is_(instance_of(context.expected)))    
        return



Scenario: User builds the minimal RVR Configuration
---------------------------------------------------


.. code:: python

    base_header = 'default_rvr'
    base_sections = {'attenuation':{'control_ip':'outthere'},
                     'dut':{'username':'root',
                            'control_ip':'www.aoeu.com',
                            'test_ip':'localhost'},
                     'server':{'username':'bama',
                               'control_ip':'here',
                               'test_ip':'there'}}
    base_configuration = {base_header:base_sections}
    
    default_configuration = """
    [rate_vs_range]
    [[attenuation]]
    # 'control_ip' is the address of the attenuator
    control_ip = 192.168.10.53
    
    [[dut]]
    # login information (these are required)
    username = admin
    control_ip = 192.168.10.34
    test_ip = 192.168.20.34
    
    [[server]]
    # login information (these are required)
    username = admin
    control_ip = 192.168.10.34
    test_ip = 192.168.20.34
    
    [[iperf]]
    direction = downstream
    """.splitlines()




.. code:: python

    @given("an instance of the minimal RVRConfiguration")
    def rvr_configuration(context):
        plugin_source = ConfigObj(base_configuration)
        context.configuration = RVRConfiguration(source=plugin_source,
                                                 section_name="default_rvr")
        return




.. code:: python

    @when("the RVRConfiguration is checked")
    def check_rvr_configuration(context):
        section = base_configuration[base_header]['attenuation']
        context.attenuation_control_ip = section['control_ip']
    
        section = base_configuration[base_header]['server']
        context.server_username = section['username']
        #context.server_control = configuration['server']['control_ip']
        #context.server_test = configuration['server']['test_ip']
        #
        section = base_configuration[base_header]['dut']
        context.dut_username = section['username']
        context.dut_control_ip = section['control_ip']
        context.dut_test_ip = section['test_ip']
        return




.. code:: python

    @then("RVRConfiguration is instance of ape's BaseConfiguration")
    def assert_base_configuration(context):
        assert_that(context.configuration,
                    is_(instance_of(BaseConfiguration)))
        return




.. code:: python

    @then("RVRConfiguration has the user values")
    def check_user_values(context):
        context.configuration.check_rep()
        # dut
        assert_that(context.attenuation_control_ip,
                    is_(equal_to(context.configuration.attenuation.control_ip)))
        assert_that(context.dut_username,
                    is_(equal_to(context.configuration.dut.username)))
        assert_that(context.dut_control_ip,
                    is_(equal_to(context.configuration.dut.control_ip)))
        assert_that(context.dut_test_ip,
                    is_(equal_to(context.configuration.dut.test_ip)))
        # server
        assert_that(context.server_username,
                     is_(equal_to(context.configuration.server.username)))
    
        # the check_rep is catching the rest if they're missing anyway
        return




.. code:: python

    @then("RVRConfiguration has the default values")
    def check_default_values(context):
        rvrconfiguration = context.configuration
        assert_that(rvrconfiguration.result_location,
                    is_(equal_to(RVRConstants.default_result_location)))
        assert_that(rvrconfiguration.test_name,
                    is_(equal_to(RVRConstants.default_test_name)))
        assert_that(rvrconfiguration.repetitions,
                    is_(equal_to(RVRConstants.default_repetitions)))
        assert_that(rvrconfiguration.recovery_time,
                    is_(equal_to(RVRConstants.default_recovery_time)))    
    
        section = rvrconfiguration.attenuation
        
        assert_that(section.start,
                    is_(equal_to(AttenuationConstants.default_start)))
        assert_that(section.stop,
                    is_(equal_to(AttenuationConstants.default_stop)))
        assert_that(section.name,
                    is_(equal_to(AttenuationConstants.default_attenuator)))
        
        assert_that(section.step_sizes,
                    contains(*AttenuationConstants.default_step_sizes))
        assert_that(section.step_change_thresholds,
                    is_(None))
            
        section = context.configuration.dut
        assert_that(section.password,
                    is_(None))
        assert_that(section.connection_type,
                    is_(equal_to(HostConstants.default_type)))
        assert_that(section.timeout,
                    is_(equal_to(HostConstants.default_timeout)))
        assert_that(section.prefix,
                    is_(None))
        assert_that(section.operating_system,
                    is_(equal_to(HostConstants.default_operating_system)))
    
        ## iperf
        section = rvrconfiguration.iperf
        assert_that(section.direction,
                    is_(equal_to(TrafficConstants.default_direction)))
        #assert_that(section['parallel'],
        #            is_(None))
    
        return



Scenario: User builds the RVR Configuration with extra iperf values
-------------------------------------------------------------------


.. code:: python

    iperf_configuration = """
    [rate_vs_range]
    [[attenuation]]
    # 'control_ip' is the address of the attenuator
    control_ip = 192.168.10.53
    
    [[dut]]
    # login information (these are required)
    username = admin
    control_ip = 192.168.10.34
    test_ip = 192.168.20.34
    
    [[server]]
    # login information (these are required)
    username = admin
    control_ip = 192.168.10.34
    test_ip = 192.168.20.34
    
    [[iperf]]
    direction = upstream
    parallel = 4
    """.splitlines()
    
    @given("an instance of the RVRConfiguration with extra iperf values")
    def extra_iperf_values(context):
        context.configuration = RVRConfiguration(source=ConfigObj(iperf_configuration),
                                                 section_name="rate_vs_range")
    
        return




.. code:: python

    @when("the RVRConfiguration is checked for extra iperf values")
    def check_extra_iperf(context):
        section = context.configuration.configuration['iperf']
        context.parallel = section['parallel']
        return




.. code:: python

    @then("the RVRConfiguration has the extra iperf values")
    def assert_extra_iperf(context):
        assert_that(context.parallel,
                    is_(equal_to('4')))
        return



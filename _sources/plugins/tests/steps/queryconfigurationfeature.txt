QueryConfiguration
==================

.. literalinclude:: ../features/queryconfiguration.feature
   :language: gherkin




Scenario: User doesn't include query configuration
--------------------------------------------------

.. '


.. code:: python

    empty = """
    """.splitlines()
    
    @given("a configuration without a query section")
    def no_query(context):
        context.configuration = QueryPluginConfiguration(source=ConfigObj,
                                                         section_name='query')
        return




.. code:: python

    @when("the QueryConfiguration is checked")
    def check_query(context):
        return




.. code:: python

    @then("the QueryConfiguration is None")
    def query_is_none(context):
        assert_that(context.configuration.query_configuration,
                    is_(None))
        return



   
Scenario: User creates the default query configuration
------------------------------------------------------





.. code:: python

    @given("a default query configuration")
    def query_default(context):
        context.configuration = QueryPluginConfiguration(source=ConfigObj(query_source),
                                                            section_name='query')
        context.configuration.check_rep()
        return




.. code:: python

    @when("the query configuration values are checked")
    def check_query_values(context):
        config = context.configuration.configuration
        context.filename = config['filename']
        context.timeout = config['timeout']
        context.trap_errors = config['trap_errors']
        return




.. code:: python

    @then("the query configuration values are defaults")
    def assert_defaults(context):
        assert_that(context.filename,
                    is_(equal_to('query.csv')))
        assert_that(context.timeout,
                    is_(equal_to(10)))
        assert_that(context.trap_errors,
                    is_(True))
        return



Scenario: User configures the query configuration
-------------------------------------------------


.. code:: python

    non_default_configuration = """
    [query]
    rssi = iwconfig wlan0, Signal\slevel=(-\d+\sdBm)
    noise = wl noise, (.*)
    bitrate = iwconfig wlan0, Bit\sRate=(\d+\.\d\sMb/s)
    """.splitlines()




.. code:: python

    @given("a non-default query configuration")
    def non_default_query(context):
        context.configuration = QueryPluginConfiguration(source=ConfigObj(non_default_configuration),
                                                   section_name='query')
        context.configuration.check_rep()
        return




.. code:: python

    @when("the query configuration values are all checked")
    def check_non_default(context):
        configuration = context.configuration.configuration
        context.rssi = configuration['rssi']
        context.noise = configuration['noise']
        context.bitrate = configuration['bitrate']
        
        return




.. code:: python

    @then("the query configuration will match the settings")
    def assert_query_configuration(context):
        assert_that(context.rssi,
                    contains('iwconfig wlan0', 'Signal\slevel=(-\d+\sdBm)'))
        assert_that(context.noise,
                    contains('wl noise',
                             '(.*)'))
        assert_that(context.bitrate,
                    contains('iwconfig wlan0',
                             'Bit\sRate=(\d+\.\d\sMb/s)'))
    
        q_configuration = context.configuration.query_configuration
    
        return



Scenario: User makes bad query
------------------------------


.. code:: python

    bad_source = """
    [bad_query]
    okay = ls, (.*)
    missing = ls
    """.splitlines()




.. code:: python

    @given("a Query Configuration that doesn't have command and regex")
    def bad_query(context):
        context.configuration = QueryPluginConfiguration(source=ConfigObj(bad_source),
                                                   section_name='bad_query')
        return




.. code:: python

    @when("the query configuration is checked")
    def check_query(context):
        context.callable = context.configuration.check_rep
        return




.. code:: python

    @then("the Query raises a ConfigurationError")
    def assert_error(context):
        assert_that(calling(context.callable),
                    raises(ConfigurationError))
        return



Scenario: User doesn't use a query
----------------------------------

.. '


.. code:: python

    no_query = """
    """.splitlines()
    
    @given("a configuration with no query section")
    def no_query(context):
        return


When the query configuration is checked


.. code:: python

    @then("the query is None")
    def none_query(context):
        return



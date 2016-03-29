
# third-party
from behave import given, when, then
from hamcrest import assert_that, raises, is_, equal_to
from hamcrest import same_instance
from configobj import ConfigObj

# this plugin
from cameraobscura.plugins.rvrplugin import HostConfiguration, HostConstants

# the ape
from theape import ConfigurationError

source = '''
[missing]
'''.splitlines()

@given("a node configuration with missing required options")
def missing_defaults(context):
    configuration = ConfigObj(source)
    context.configuration=HostConfiguration(configuration,
                                            'missing')
    return

@when("the node configuration is checked")
def check_configuration(context):
    context.callable = context.configuration.check_rep
    return

@then("the node configuration raises an error")
def assert_error(context):
    assert_that(context.callable,
                raises(ConfigurationError))
    return

minimal = """[minimal]
username = bob
control_ip = www.google.com
test_ip = aoeusnth
""".splitlines()

@given("a node configuration with minimal settings")
def minimal_configuration(context):
    configuration = ConfigObj(minimal)
    context.configuration = HostConfiguration(configuration,
                                              'minimal')
    context.configuration.check_rep()
    return

@when("the minimal node configuration options are checked")
def check_options(context):
    context.username = 'bob'
    context.control_ip = 'www.google.com'
    context.test_ip = 'aoeusnth'
    return

@then("the required node configuration is correct")
def assert_correct(context):
    assert_that(context.configuration.username,
                is_(equal_to(context.username)))
    assert_that(context.configuration.password,
                is_(None))
    assert_that(context.control_ip,
                is_(equal_to(context.configuration.control_ip)))

    assert_that(context.configuration.connection_type,
                is_(equal_to(HostConstants.default_type)))
    assert_that(context.test_ip,
                is_(equal_to(context.configuration.test_ip)))
    assert_that(context.configuration.timeout,
                is_(equal_to(HostConstants.default_timeout)))
    assert_that(context.configuration.prefix,
                is_(None))
    assert_that(context.configuration.operating_system,
                is_(equal_to(HostConstants.default_operating_system)))
    return

options = ('username password control_ip test_ip'
           ' connection_type timeout prefix'
           ' operating_system').split()
values = ('bob ummagumma www.google.com aoeusnth telnet'
          ' 4538 sudo planet9').split()
complete = {'complete':dict(zip(options, values))}

@given("a node configuration with full settings")
def full_configuration(context):
    configuration = ConfigObj(complete)
    context.configuration = HostConfiguration(configuration,
                                              'complete')
    context.configuration.check_rep()
    return

@when("the full node configuration options are checked")
def check_options(context):
    section = complete['complete']
    context.username = section['username']
    context.control_ip = section['control_ip']  
    context.test_ip = section['test_ip']  
    context.password = section['password']
    context.connection_type = section['connection_type']
    context.timeout = float(section['timeout'])
    context.prefix = section['prefix']
    context.operating_system = section['operating_system']
    return

@then("the complete node configuration is correct")
def assert_correct(context):
    assert_that(context.configuration.username,
                is_(equal_to(context.username)))
    assert_that(context.configuration.password,
                is_(equal_to(context.password)))
    assert_that(context.control_ip,
                is_(equal_to(context.configuration.control_ip)))
    assert_that(context.connection_type,
                is_(equal_to(context.configuration.connection_type)))
    assert_that(context.test_ip,
                is_(equal_to(context.configuration.test_ip)))
    assert_that(context.timeout,
                is_(equal_to(context.configuration.timeout)))

    assert_that(context.prefix,
                is_(equal_to(context.configuration.prefix)))
    assert_that(context.operating_system,
                is_(equal_to(context.configuration.operating_system)))
    return

options = ('username password control_ip test_ip'
           ' connection_type timeout prefix'
           ' operating_system port').split()
values = ('bob ummagumma www.google.com aoeusnth telnet'
          ' 4538 sudo planet9 52686').split()
overfull = {'complete':dict(zip(options, values))}

@given("a node configuration with extra settings")
def extra_configuration(context):
    configuration = ConfigObj(overfull)
    context.configuration = HostConfiguration(configuration,
                                              'complete')
    context.configuration.check_rep()
    return

@when("the extra node configuration options are checked")
def check_options(context):
    section = overfull['complete']
    context.username = section['username']
    context.control_ip = section['control_ip']  
    context.test_ip = section['test_ip']  
    context.password = section['password']
    context.connection_type = section['connection_type']
    context.timeout = float(section['timeout'])
    context.prefix = section['prefix']
    context.operating_system = section['operating_system']
    context.port = section['port']
    return

@then("the overloaded node configuration is correct")
def assert_correct(context):
    assert_that(context.configuration.username,
                is_(equal_to(context.username)))
    assert_that(context.configuration.password,
                is_(equal_to(context.password)))
    assert_that(context.control_ip,
                is_(equal_to(context.configuration.control_ip)))
    assert_that(context.connection_type,
                is_(equal_to(context.configuration.connection_type)))
    assert_that(context.test_ip,
                is_(equal_to(context.configuration.test_ip)))
    assert_that(context.timeout,
                is_(equal_to(context.configuration.timeout)))

    assert_that(context.prefix,
                is_(equal_to(context.configuration.prefix)))
    assert_that(context.operating_system,
                is_(equal_to(context.configuration.operating_system)))

    assert_that(context.port,
                is_(equal_to(context.configuration.port)))
    return
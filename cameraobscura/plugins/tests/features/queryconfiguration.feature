Feature: QueryConfiguration
 Scenario: User doesn't include query configuration
  Given a configuration without a query section
  When the QueryConfiguration is checked
  Then the QueryConfiguration is None

# Scenario: User configures the query configuration
#  Given a non-default query configuration
#  When the query configuration values are all checked
#  Then the query configuration will match the settings
#
# Scenario: User makes bad query
#   Given a Query Configuration that doesn't have command and regex
#   When the query configuration is checked
#   Then the Query raises a ConfigurationError


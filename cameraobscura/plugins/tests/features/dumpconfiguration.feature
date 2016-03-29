Feature: DumpConfiguration
 Scenario: User creates the default dump configuration
  Given a default dump configuration
  When the dump configuration values are checked
  Then the dump configuration values are defaults

 Scenario: User configures the dump configuration
  Given a non-default dump configuration
  When the dump configuration values are all checked
  Then the dump configuration will match the settings

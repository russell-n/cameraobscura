Feature: OtherConfiguration
 Scenario: User creates other configuration
  Given an other configuration
  When the user checks the other configuration
  Then the other configuration will have the defaults

 Scenario: User creates other configuration with non-defaults
  Given an other configuration with non-defaults
  When the user checks the other configuration values
  Then the other configuration will have the user-values

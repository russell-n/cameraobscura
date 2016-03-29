Feature: Dut Configuration
  Scenario: Missing required options in Node Configuration
    Given a node configuration with missing required options
    When the node configuration is checked
    Then the node configuration raises an error

  Scenario Outline: Node Configurations
    Given a node configuration with <setting> settings
    When the <setting> node configuration options are checked
    Then the <options> node configuration is correct

  Examples: Node Configuration Levels
  | setting | options    |
  | minimal | required   |
  | full    | complete   |
  | extra   | overloaded |


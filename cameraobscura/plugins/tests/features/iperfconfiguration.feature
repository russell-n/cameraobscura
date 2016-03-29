Feature: Iperf Configuration
 Scenario: Iperf default direction
   Given an iperf configuration with no parameters 
   When the iperf configuration is checked
   Then the iperf configuration has the defaults

 Scenario: Iperf with some settings
   Given an iperf configuration with some parameters
   When the iperf configuration is checked
   Then the configuration has the iperf parameters
   And the IperfConfiguration is ready

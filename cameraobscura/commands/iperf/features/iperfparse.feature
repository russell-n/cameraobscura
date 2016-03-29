Feature: Iperf has IperfParser
  Scenario: The default IperfParser is used
    Given no parser
    When the Iperf.parser is checked 
    Then it is the IperfParser

 Scenario: IperfParser parses outcome
   Given An Iperf instance
   When the ``run`` method is called
   Then the output is given to the IperfParser

 Scenario Outline: IperfParser sets summary
   Given an Iperf instance with fake parser
   When the ``run`` method is called and the <role> summary checked
   Then the summary of <role> values is set

   Examples: client and server
   | role   |
   | client |
   | server |

 Scenario: Iperf Settings are unknown
   Given an Iperf instance with fake parser
   When the ``run`` method is called with unknown settings type
   Then a CameraObscura error is raised

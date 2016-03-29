Feature: StepRange compare property
  Scenario Outline:
    Given StepRange `start` is <comparison> `stop`
    When the StepRange `compare` property is checked
    Then the StepRange `compare` is <function name>

 Examples: Starts and Stops
  | comparison   | function name |
  | equal to     | <=            |
  | less than    | <=            |
  | greater than | >=            |




Feature: StepRange Iterator
 Scenario Outline: StepRange Iteration
  Given StepRange start <comparison> stop and <count> step thresholds
  When the StepRange is traversed
  Then the StepRange output is a <type> from start to stop

  Examples: Up Only
  | comparison | count | type          |
  | less than  | no    | range         |
  | less than  | one   | stepped range |

  Examples: Down Only
  | comparison   | count | type             |
  | greater than | no    | descending range |




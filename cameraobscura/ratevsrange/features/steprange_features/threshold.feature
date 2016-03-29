Feature: StepRange threshold property
 Scenario Outline: StepRange threshold properties
   Given a StepRange with <thresholds> step change thresholds and <reversals> reversals
   When the StepRange.threshold is checked
   Then the StepRange.threshold is <threshold>
   And the StepRange.current_change_index is <index>

 Examples: No step change thresholds
 | thresholds | reversals | threshold | index |
 | no         | any       | stop      | zero  |

 Examples: Step Change Thresholds
 | thresholds | reversals | threshold          | index |
 | one        | no        | the threshold      | zero  |
 | two        | no        | the threshold      | one   |
 | two        | one       | previous threshold | zero  |

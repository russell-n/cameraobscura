Feature: StepRange Update Threshold Method
 Scenario Outline: Update threshold
   Given a StepRange where the current_value <compare> threshold
   When the StepRange.update_threshold method is called
   Then the StepRange.threshold value will be <updated>

 Examples: Up
 | compare      | updated        |
 | is less than | the same       |
 | equals       | next threshold |
 | exceeds last | the same       |

 Examples: Down
 | compare         | updated  |
 | is greater than | the same |
 | equals lower    | lower    |

 Scenario: StepRange.step_change_thresholds is None
   Given a StepRange with no step_change_thresholds
   When the StepRange.update_threshold method is called
   Then the StepRange.threshold will be the stop value

Feature: Reverse direction method
 Scenario: reverse called and not reversible
   Given a StepRange that isn't reversible
   When StepRange.reverse is called
   Then the StepRange.current_value is set to stop

 Scenario: reverse called and is reversible
   Given a reversible StepRange
   When StepRange.reverse is called
   Then StepRange.reversals is incremented
   And StepRange start and stop are swapped
   And _threshold is None
   And current_step_index is incremented
   And current_change_index is incremented
   And compare and threshold_compare are swapped
   And direction and list direction are negative


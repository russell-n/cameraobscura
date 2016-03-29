Feature: StepRange step_size property
 Scenario: Step size not set (up)
   Given an upward StepRange with no step_size
   When step_size is retrieved
   Then step_size is first step_size

 Scenario: Step size not set (down)
   Given a downward StepRange with no step_size
   When step_size is retrieved
   Then step_size is first step_size

 Scenario: Current value matches threshold (up)
  Given an upward StepRange with current equal threshold
  When step_size is retrieved
  Then it is the next step size

 Scenario: Current value matches threshold (down)
  Given a downward StepRange with current equal threshold
  When step_size is retrieved
  Then it is the next step size

 Scenario: Current value matches threshold (reverse)
  Given a reversed StepRange with current equal threshold
  When step_size is retrieved
  Then it is the previous step size

 Scenario: Stepsizes are passed in as negative values
   Given a step_sizes list with negative values
   When step_sizes is set
   Then the step_sizes are cast to be positive

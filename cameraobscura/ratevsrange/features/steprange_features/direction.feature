Feature: StepRange direction property
 Scenario: User checks direction when start less than stop
   Given a StepRange with start less than stop
   When the StepRange direction is checked
   Then the direction is 1

 Scenario: User checks direction when stop less than start
  Given a StepRange with stop less than start
  When the StepRange direction is checked
  Then the direction is -1

 Scenario: Stop equals Start
  Given a StepRange with stop equal to start
  When the StepRange direction is checked
  Then the direction is 1

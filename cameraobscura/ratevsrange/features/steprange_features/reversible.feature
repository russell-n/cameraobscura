Feature: StepRange reversible property
 Scenario: User checks reversible when not reversible
  Given StepRange with reversals equal to reversal_limit
  When user checks if StepRange is reversible
  Then StepRange reversible is false

 Scenario: User checks reversible when reversible
  Given StepRange with reversals less than reversal_limit
  When user checks if StepRange is reversible
  Then StepRange reversible is true

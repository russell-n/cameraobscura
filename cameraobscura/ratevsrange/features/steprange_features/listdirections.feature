Feature: StepRange list_directions property
  Scenario: StepRange directions are changed
    Given a StepRange that is reversed multiple times
    When the StepRange list_directions are checked
    Then the StepRange list_directions alternate

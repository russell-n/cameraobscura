Feature: Stop Property
  Scenario: User checks the StepList Stop property
    Given a  configured StepList
    When the StepList stop property is checked
    Then it is the last item in the step list

Feature: StepList __iter__ method
 Scenario Outline:  iterations
   Given a StepList that moves in the <direction> direction
   When the iteration is checked
   Then the values are the expected for the <direction>

 Examples: Directions
 | direction   |
 | upward      |
 | downward    |
 | up and down |


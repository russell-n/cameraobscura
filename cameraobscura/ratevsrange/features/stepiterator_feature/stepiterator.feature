Feature: StepIterator class
  Scenario Outline: A step iterator is built
    Given a  StepIterator with a step-<type>
    When the StepIterator's iterator is checked
    Then the StepIterator's iterator is a  step-<type>

 Examples: Step Types
 | type  |
 | list  |
 | range |


 Scenario Outline: A step iterator is traversed
   Given a StepIterator with a step-<type> to traverse
   When the StepIterator is traversed
   Then the StepIterator given the expected outcome

   Examples: Step iterations
   | type  |
   | list  |
   | range |

 Scenario Outline: A step iterator is traversed and reversed
   Given a StepIterator with a step-<type> to traverse up and down
   When the StepIterator is traversed up and down
   Then the StepIterator gives the expected up and down outcome

   Examples: Step iterations up and down
   | type  |
   | list  |
   | range |

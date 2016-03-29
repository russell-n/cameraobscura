Feature: StepRange increment_index Method
 Scenario Outline: Reversals
  Given StepRange reversals are <odd or even> and <in or out> range
  When the StepRange increment_index is called
  Then StepRange.increment_index returns <increment>

 Examples: In Range
 | odd or even | increment | in or out |
 | odd         | index - 1 | in        |
 | even        | index + 1 | in        |


 Examples: Out of Range
 | odd or even | increment | in or out |
 | odd         | index     | out of    |
 | even        | index     | out of    |




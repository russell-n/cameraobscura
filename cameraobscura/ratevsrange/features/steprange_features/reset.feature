Feature: reset method
 Scenario Outline: after using the StepRange it is reset
 Given a used StepRange
 When the StepRange is reset
 Then the StepRange <variable> will be <expectation>

 Examples: Reset values
   | variable             | expectation     |
   | current_value        | original start  |
   | step_size            | first size      |
   | threshold            | first threshold |
   | current_step_index   | Zero            |
   | current_change_index | Zero            |
   | start                | original start  |
   | stop                 | original stop   |
   | reversals            | Zero            |



 Scenario Outline: after using a reversible StepRange it is reset
   Given a used reversible StepRange
   When the StepRange is reset
   Then the StepRange <variable> will be <expectation>

 Examples: Reset values
   | variable             | expectation     |
   | current_value        | original start  |
   | step_size            | first size      |
   | threshold            | first threshold |
   | current_step_index   | Zero            |
   | current_change_index | Zero            |
   | start                | original start  |
   | stop                 | original stop   |
   | reversals            | Zero            |



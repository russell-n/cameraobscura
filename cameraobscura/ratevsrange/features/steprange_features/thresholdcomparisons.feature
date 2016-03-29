Feature: StepRange threshold_compare property
 Scenario Outline: StepRange threshold_compare
   Given StepRange start is <inequality> stop
   When StepRange.threshold_compare is checked
   Then StepRange.threshold_compare is <comparison>

 Examples: Up and Down
 | inequality   | comparison |
 | equal to     | >=         |
 | less than    | >=         |
 | greater than | <=         |



  
 

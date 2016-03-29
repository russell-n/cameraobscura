StepIterator
============

.. literalinclude:: ../stepiterator.feature
   :language: gherkin



Scenario Outline: A step iterator is built
------------------------------------------

::

    @given("a  StepIterator with a step-list")
    def step_list(context):
        context.step_iterator = StepIterator(step_list=range(10))
        return
    

::

    @when("the StepIterator's iterator is checked")
    def check_step_iterator(context):
        context.iterator = context.step_iterator.iterator
        return
    

::

    @then("the StepIterator's iterator is a  step-list")
    def assert_list(context):
        assert_that(context.iterator,
                    is_(instance_of(StepList)))
        return
    



Scenario Outline: A step iterator range is built
------------------------------------------------

::

    @given("a  StepIterator with a step-range")
    def step_list(context):
        context.step_iterator = StepIterator(start=0, stop=3)
        return
    

::

    @then("the StepIterator's iterator is a  step-range")
    def assert_list(context):
        assert_that(context.iterator,
                    is_(instance_of(StepRange)))
        return
    




Scenario Outline: A step iterator list is traversed
---------------------------------------------------

::

    @given("a StepIterator with a step-list to traverse")
    def step_list(context):
        context.expected = range(35)
        context.iterator = StepIterator(step_list=context.expected)
        return
    

::

    @when("the StepIterator is traversed")
    def step_traversal(context):
        context.outcome = [step for step in context.iterator]
        return
    

::

    @then("the StepIterator given the expected outcome")
    def assert_expected(context):
        assert_that(context.outcome,
                    contains(*context.expected))
        return
    



Scenario Outline: A step iterator range is traversed
----------------------------------------------------

::

    @given("a StepIterator with a step-range to traverse")
    def step_list(context):
        context.expected = range(35)
        context.iterator = StepIterator(start=0,
                                        stop=34)
        return
    




When the StepIterator is traversed

Then the StepIterator given the expected outcome


Scenario Outline: A step iterator is traversed and reversed
-----------------------------------------------------------

::

    @given("a StepIterator with a step-list to traverse up and down")
    def step_list_reversible(context):
        context.iterator = StepIterator(step_list=range(10),
                                        reversal_limit=1)
        return
    

::

    @when("the StepIterator is traversed up and down")
    def traverse_up_down(context):
        context.outcome = []
        context.expected = range(7) + range(5, -1, -1)
        for step in context.iterator:
            context.outcome.append(step)        
            if step == 6:
                context.iterator.reverse()            
        return
    

::

    @then("the StepIterator gives the expected up and down outcome")
    def assert_up_down_outcome(context):
        print context.outcome
        assert_that(context.outcome,
                    contains(*context.expected))
        return
    



Scenario Outline: A step (range) iterator is traversed and reversed
-------------------------------------------------------------------

::

    @given("a StepIterator with a step-range to traverse up and down")
    def step_range_reversible(context):
        context.iterator = StepIterator(start=0,
                                     stop=9,
                                     reversal_limit=1)
        return
    



When the StepIterator is traversed up and down
Then the StepIterator given the expected up and down outcome


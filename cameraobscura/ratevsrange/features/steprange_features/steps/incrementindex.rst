StepRange increment_index Method
================================

.. literalinclude:: ../incrementindex.feature
   :language: gherkin



Scenario: Odd Reversals and list in range
-----------------------------------------

::

    @given("StepRange reversals are odd and in range")
    def odd_reversals(context):
        context.index = 2
        context.container = range(3)
        context.iterator = StepRange(start=0,
                                     stop=10)
        context.iterator.reversals = 3
        return
    

::

    @when("the StepRange increment_index is called")
    def increment_index(context):
        index = context.index
        container = context.container
        context.incremented_index = context.iterator.increment_index(index,
                                                                     container)
        return
    

::

    @then("StepRange.increment_index returns index - 1")
    def less_one(context):
        assert_that(context.incremented_index,
                    is_(equal_to(context.index - 1)))
        return
    



Scenario: Even Reversals and list in range
------------------------------------------

::

    @given("StepRange reversals are even and in range")
    def odd_reversals(context):
        context.index = 1
        context.container = range(3)
        context.iterator = StepRange(start=0, stop=10)
        context.iterator.reversals = 2
        return
    

::

    @then("StepRange.increment_index returns index + 1")
    def add_one(context):
        assert_that(context.incremented_index,
                    is_(equal_to(context.index + 1)))
        return
    



Scenario: Odd Reversals and list out of range
---------------------------------------------

::

    @given("StepRange reversals are odd and out of range")
    def odd_reversals(context):
        context.index = 0
        context.container = range(3)
        context.iterator = StepRange(start=0, stop=10)
        context.iterator.reversals = 5
        return
    

::

    @then("StepRange.increment_index returns index")
    def same_index(context):
        assert_that(context.incremented_index,
                    is_(equal_to(context.index)))
        return
    



Scenario: Even Reversals and list out of range
----------------------------------------------

::

    @given("StepRange reversals are even and out of range")
    def odd_reversals(context):
        context.container = range(randrange(100))
        context.index = len(context.container) - 1
        context.iterator = StepRange(start=0, stop=10)
        context.iterator.reversals = 4
        return
    


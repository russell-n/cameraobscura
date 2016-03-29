Step Size Property
==================

.. literalinclude:: ../stepsize.feature
   :language: gherkin



Scenario: Step size not set (up)
--------------------------------

::

    @given("an upward StepRange with no step_size")
    def no_step_size_up(context):
        context.iterator = StepRange(start=0, stop=100, step_sizes=[35,3])
        return
    

::

    @when("step_size is retrieved")
    def retrieve_step_size(context):
        context.step_size = context.iterator.step_size
        return
    

::

    @then("step_size is first step_size")
    def assert_first(context):
        assert_that(context.step_size,
                    is_(equal_to(context.iterator.step_sizes[0])))
        return
    



Scenario: Step size not set (down)
----------------------------------

::

    @given("a downward StepRange with no step_size")
    def no_step_down(context):
        context.iterator = StepRange(start=12, stop=0,
                                     step_sizes=[1, 42])
        return
    


   When step_size is retrieved


Scenario: Current value matches threshold (up)
----------------------------------------------

::

    @given("an upward StepRange with current equal threshold")
    def threshold_match_up(context):
        context.iterator = StepRange(start=0, stop=75,
                                     step_change_thresholds=[4],
                                     step_sizes = [1, 2])
    
        # the index is pushed to the next size
        # when it's set so step_size has to be retrieved once
        context.iterator.step_size
        context.iterator.current_value = 4
        return
    


  When step_size is retrieved

::

    @then("it is the next step size")
    def assert_next_size(context):    
        assert_that(context.step_size,
                    is_(equal_to(2)))
        return
    



Scenario: Current value matches threshold (down)
------------------------------------------------

::

    @given("a downward StepRange with current equal threshold")
    def current_equal_threshold_down(context):
        context.iterator = StepRange(start=53, stop=9,
                                     step_sizes=[1,2],
                                     step_change_thresholds=[13])
        context.iterator.step_size
        context.iterator.current_value = 13
        return
    


  When step_size is retrieved

::

    @then("it is a negative of the next step size")
    def negative_next(context):
        assert_that(context.step_size,
                    is_(equal_to(-2)))
        return
    



Scenario: Current value matches threshold (reverse)
---------------------------------------------------

::

    @given("a reversed StepRange with current equal threshold")
    def reversed_at_threshold(context):
        context.iterator = StepRange(start=1, stop=753,
                                     step_sizes=[2,4,8],
                                     step_change_thresholds=[22, 30])
        
        context.iterator.current_value = 22
        context.iterator.step_size
        context.iterator.current_value = 30
        context.iterator.step_size
        context.iterator.start, context.iterator.stop = context.iterator.stop, context.iterator.start
        context.iterator.reversals = 1
        context.iterator.current_step_index = context.iterator.increment_index(context.iterator.current_step_index,
                                context.iterator.step_sizes)
        return
    


    
  When step_size is retrieved

::

    @then("it is the previous step size")
    def assert_negative_previous(context):
        it = context.iterator
        assert_that(context.step_size,
                    is_(equal_to(4)))
    
        context.iterator.current_value = 22
        assert_that(context.iterator.step_size,
                    is_(equal_to(2)))
        return
    



Scenario: Stepsizes are passed in as negative values
----------------------------------------------------

::

    @given("a step_sizes list with negative values")
    def negative_steps(context):
        context.step_sizes = [-randrange(1, 100) for size in xrange(10)]
        context.iterator = StepRange(start=0, stop=922,
                                     step_sizes=context.step_sizes)
        return
    

::

    @when("step_sizes is set")
    def set_step_sizes(context):
        return
    

::

    @then("the step_sizes are cast to be positive")
    def cast_step_sizes(context):
        assert_that(context.iterator.step_sizes,
                    contains(*[abs(size) for size in context.step_sizes]))
        return
    


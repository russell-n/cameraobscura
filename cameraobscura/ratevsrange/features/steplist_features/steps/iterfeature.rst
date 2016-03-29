StepList Iterator
=================

.. literalinclude:: ../iter.feature
   :language: gherkin



   
Scenario: Upward iteration
--------------------------


.. code:: python

    @given("a StepList that moves in the upward direction")
    def upward_steplist(context):
        context.expected = range(10)
        context.iterator = StepList(step_list=context.expected)
        return




.. code:: python

    @when("the iteration is checked")
    def check_iteration(context):
        context.steps = [step for step in context.iterator]
        return




.. code:: python

    @then("the values are the expected for the upward")
    def assert_values(context):
        assert_that(context.steps,
                    is_(equal_to(context.expected)))
        return



Scenario: Downward iteration
--------------------------


.. code:: python

    @given("a StepList that moves in the downward direction")
    def upward_steplist(context):
        context.expected = range(10, 0, -1)
        context.iterator = StepList(step_list=context.expected)
        return




.. code:: python

    @then("the values are the expected for the downward")
    def assert_values(context):
        assert_that(context.steps,
                    contains(*context.expected))
        return



Scenario: Upward and Downward iteration
---------------------------------------


.. code:: python

    @given("a StepList that moves in the up and down direction")
    def up_and_down_steplist(context):
        context.range = range(10)
        context.iterator = StepList(step_list=context.range)
        return




.. code:: python

    @then("the values are the expected for the up and down")
    def assert_values(context):
        context.iterator.reset()
        context.iterator.reversal_limit = 1
        expected = range(6) + range(4, -1, -1)
        actual = []
    
        for step in context.iterator:
            actual.append(step)
            if step == 5:
                print "reverse"
                context.iterator.reverse()
        print actual
        assert_that(actual,
                    contains(*expected))
        return

.. code::

    <type 'exceptions.SyntaxError'>
    invalid syntax (chunk, line 12)



StepRange threshold_compare
===========================

.. literalinclude:: ../thresholdcomparisons.feature
   :language: gherkin




Scenario Outline: StepRange threshold_compare equal
---------------------------------------------------


.. code:: python

    @given("StepRange start is equal to stop")
    def start_equal_to_stop(context):
        start = stop = randrange(100)
        context.iterator = StepRange(start=start,
                                     stop=stop)
        return




.. code:: python

    @when("StepRange.threshold_compare is checked")
    def check_threshold_compare(context):
        context.threshold_compare = context.iterator.threshold_compare
        return




.. code:: python

    @then("StepRange.threshold_compare is >=")
    def assert_ge(context):
        assert_that(context.threshold_compare,
                    is_(same_instance(operator.ge)))
        return



Scenario Outline: StepRange threshold_compare start less than stop
------------------------------------------------------------------


.. code:: python

    @given("StepRange start is less than stop")
    def start_less_than_stop(context):
        stop = randrange(100)
        start = stop - randrange(stop)
        context.iterator = StepRange(start=start,
                                     stop=stop)
        return



Scenario Outline: StepRange threshold_compare start greater than stop
---------------------------------------------------------------------


.. code:: python

    @given("StepRange start is greater than stop")
    def start_greater_than_stop(context):
        # randrange will raise a value error if passed 0
        # so start has to be greater than 0
        start = randrange(1, 100)
        stop = start - randrange(start)
        context.iterator = StepRange(start=start,
                                     stop=stop)
        return




.. code:: python

    @then("StepRange.threshold_compare is <=")
    def assert_le(context):
        assert_that(context.threshold_compare,
                    is_(same_instance(operator.le)))
        return




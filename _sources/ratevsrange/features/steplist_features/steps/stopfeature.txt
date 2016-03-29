Stop Property
=============

.. literalinclude::  ../stop.feature
   :language: gherkin





Scenario: User checks the StepList Stop property
------------------------------------------------


.. code:: python

    @given("a  configured StepList")
    def configured_steplist(context):
        context.step_list = range(10)
        context.iterator = StepList(step_list=context.step_list)
        return




.. code:: python

    @when("the StepList stop property is checked")
    def check_stop(context):
        return




.. code:: python

    @then("it is the last item in the step list")
    def assert_last_item(context):
        assert_that(context.iterator.stop,
                    is_(equal_to(context.iterator.step_list[-1])))
        return



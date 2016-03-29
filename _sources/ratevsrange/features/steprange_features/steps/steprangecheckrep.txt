StepRange CheckRep
==================

.. literalinclude:: ../steprangecheckrep.feature
   :language: gherkin




Scenario: User calls check rep
------------------------------

Example: valid step-range
~~~~~~~~~~~~~~~~~~~~~~~~~


.. code:: python

    @given("a StepRange with 1 more step size than step change threshold")
    def valid_step_range(context):
        context.steprange = StepRange()
        return




.. code:: python

    @when("The user calls StepRange.check_rep")
    def call_check_rep(context):
        context.check_rep = context.steprange.check_rep
        return




.. code:: python

    @then("No Error is raised")
    def no_error(context):
        context.check_rep()
        return



Example: Invalid counts
~~~~~~~~~~~~~~~~~~~~~~~


.. code:: python

    @given("a StepRange with not 1 more step size than step change threshold")
    def valid_step_range(context):
        context.steprange = StepRange(step_sizes=[1],
                                      step_change_thresholds=[10],
                                      stop=20)
        return





.. code:: python

    @then("CameraObscuraError is raised")
    def assert_error(context):
        assert_that(calling(context.check_rep),
                    raises(CameraobscuraError))
        return



Example: Invalid count but out of range
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code:: python

    @given("a StepRange with out of range but not 1 more step size than step change threshold")
    def valid_step_range(context):
        context.steprange = StepRange(step_sizes=[1],
                                      step_change_thresholds=[100, 200],
                                      stop=10)
        return



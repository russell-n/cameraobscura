Reversible Property
===================

.. literalinclude:: ../reversible.feature
   :language: gherkin




Scenario: User checks reversible when not reversible
----------------------------------------------------


.. code:: python

    @given("StepRange with reversals equal to reversal_limit")
    def non_reversible(context):
        reversal_limit = random.randrange(-100, 100)
        context.iterator = StepRange(start=0,
                                     stop=10,
                                     reversal_limit=reversal_limit,
                                     step_sizes=[1])
        context.iterator.reversals = reversal_limit
        return




.. code:: python

    @when("user checks if StepRange is reversible")
    def check_reversible(context):
        context.outcome = context.iterator.reversible
        return




.. code:: python

    @then("StepRange reversible is false")
    def assert_false(context):
        assert_that(context.outcome,
                    is_(False))
        return



Scenario: User checks reversible when reversible
------------------------------------------------


.. code:: python

    @given("StepRange with reversals less than reversal_limit")
    def reversible(context):
        limit = random.randrange(100)
        difference = random.randrange(limit)
        context.iterator=StepRange(start=2,
                                   stop=4,
                                   reversal_limit=limit)
        context.iterator.reversals = difference
        return


  When user checks if StepRange is reversible


.. code:: python

    @then("StepRange reversible is true")
    def assert_true(context):
        return



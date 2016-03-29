Direction Property
==================

.. literalinclude:: ../direction.feature
   :language: gherkin


   
Scenario: User checks direction when start less than stop
---------------------------------------------------------

::

    @given("a StepRange with start less than stop")
    def start_less_than_stop(context):
        stop = random.randrange(100)
        start = random.randrange(stop)
        context.iterator = StepRange(start=start,
                                     stop=stop)
        return
    

::

    @when("the StepRange direction is checked")
    def check_direction(context):
        context.direction = context.iterator.direction
        return
    

::

    @then("the direction is 1")
    def assert_1(context):
        assert_that(context.direction,
                    is_(equal_to(1)))
        return
    



Scenario: User checks direction when stop less than start
--------------------------------------------------------

::

    @given("a StepRange with stop less than start")
    def stop_less(context):
        start = random.randrange(100)
        stop = start - random.randrange(start)
        context.iterator = StepRange(start=start,
                                     stop=stop)
        return
    


  When the StepRange direction is checked

::

    @then("the direction is -1")
    def assert_negative_one(context):
        assert_that(context.direction,
                    is_(equal_to(-1)))
        return
    



Scenario: Stop equals Start
---------------------------

::

    @given("a StepRange with stop equal to start")
    def start_equals_stop(context):
        start = stop = random.randrange(-100, 100)
        context.iterator = StepRange(start=start,
                                     stop=stop)
        return
    



  When the StepRange direction is checked
  Then the direction is 1

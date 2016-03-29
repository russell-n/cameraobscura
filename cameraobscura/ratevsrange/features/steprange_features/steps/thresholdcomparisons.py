
# python standard library
from random import randrange
import operator

# third party
from behave import given, when, then
from hamcrest import assert_that, is_, same_instance

# this package
from cameraobscura.ratevsrange.stepiterator import StepRange

@given("StepRange start is equal to stop")
def start_equal_to_stop(context):
    start = stop = randrange(100)
    context.iterator = StepRange(start=start,
                                 stop=stop)
    return

@when("StepRange.threshold_compare is checked")
def check_threshold_compare(context):
    context.threshold_compare = context.iterator.threshold_compare
    return

@then("StepRange.threshold_compare is >=")
def assert_ge(context):
    assert_that(context.threshold_compare,
                is_(same_instance(operator.ge)))
    return

@given("StepRange start is less than stop")
def start_less_than_stop(context):
    stop = randrange(100)
    start = stop - randrange(stop)
    context.iterator = StepRange(start=start,
                                 stop=stop)
    return

@given("StepRange start is greater than stop")
def start_greater_than_stop(context):
    # randrange will raise a value error if passed 0
    # so start has to be greater than 0
    start = randrange(1, 100)
    stop = start - randrange(start)
    context.iterator = StepRange(start=start,
                                 stop=stop)
    return

@then("StepRange.threshold_compare is <=")
def assert_le(context):
    assert_that(context.threshold_compare,
                is_(same_instance(operator.le)))
    return
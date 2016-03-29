
# python standard library
import random

# third-party
from behave import given, when, then
from hamcrest import assert_that, is_, equal_to

# this package
from cameraobscura.ratevsrange.stepiterator import StepRange


@given("a StepRange with start less than stop")
def start_less_than_stop(context):
    stop = random.randrange(100)
    start = random.randrange(stop)
    context.iterator = StepRange(start=start,
                                 stop=stop)
    return


@when("the StepRange direction is checked")
def check_direction(context):
    context.direction = context.iterator.direction
    return


@then("the direction is 1")
def assert_1(context):
    assert_that(context.direction,
                is_(equal_to(1)))
    return


@given("a StepRange with stop less than start")
def stop_less(context):
    start = random.randrange(100)
    stop = start - random.randrange(start)
    context.iterator = StepRange(start=start,
                                 stop=stop)
    return


@then("the direction is -1")
def assert_negative_one(context):
    assert_that(context.direction,
                is_(equal_to(-1)))
    return


@given("a StepRange with stop equal to start")
def start_equals_stop(context):
    start = stop = random.randrange(-100, 100)
    context.iterator = StepRange(start=start,
                                 stop=stop)
    return

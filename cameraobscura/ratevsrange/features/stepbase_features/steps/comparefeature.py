
# python standard library
import random
import operator

# third-party
from behave import then, when, given
from hamcrest import assert_that, is_, same_instance

# this package
from cameraobscura.ratevsrange.stepiterator import StepBase


@given("StepRange `start` is equal to `stop`")
def start_equal_stop(context):
    start = stop = random.randrange(-100, 100)
    context.iterator = StepBase(start=start,
                                 stop=stop)
    return


@when("the StepRange `compare` property is checked")
def check_compare(context):
    context.compare = context.iterator.compare
    return


@then("the StepRange `compare` is <=")
def assert_le(context):
    assert_that(context.compare,
                is_(same_instance(operator.le)))
    return


@given('StepRange `start` is less than `stop`')
def start_less_than_stop(context):
    stop = random.randrange(-100, 100)
    start = stop - random.randrange(abs(stop))
    context.iterator = StepBase(start=start,
                              stop=stop)
    return


@given('StepRange `start` is greater than `stop`')
def start_greater_than_stop(context):
    start = random.randrange(-100, 100)
    stop = start - random.randrange(abs(start))
    context.iterator = StepBase(start=start,
                                stop=stop)
    return


@then('the StepRange `compare` is >=')
def assert_ge(context):
    assert_that(context.compare,
                is_(same_instance(operator.ge)))
    return

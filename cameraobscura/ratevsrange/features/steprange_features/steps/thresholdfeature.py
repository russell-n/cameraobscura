
# third-party
from behave import given, when, then
from hamcrest import assert_that, is_, equal_to

# this package
from cameraobscura.ratevsrange.stepiterator import StepRange

@given("a StepRange with no step change thresholds and any reversals")
def no_thresholds(context):
    context.iterator = StepRange(start=0,
                                 stop=24)
    return

@when("the StepRange.threshold is checked")
def check_threshold(context):
    context.threshold = context.iterator.threshold
    context.current_change_index = context.iterator.current_change_index
    return

@then("the StepRange.threshold is stop")
def threshold_is_stop(context):
    assert_that(context.threshold,
                is_(equal_to(context.iterator.stop)))
    return

@then('the StepRange.current_change_index is zero')
def change_index_zero(context):
    assert_that(context.current_change_index,
                is_(equal_to(0)))

@given("a StepRange with one step change thresholds and no reversals")
def with_thresholds_no_reversals(context):
    context.expected = 3
    context.iterator = StepRange(start=0,
                                 stop=24,
                                 step_change_thresholds=[context.expected])
    return

@then("the StepRange.threshold is the threshold")
def threshold_is_threshold(context):
    assert_that(context.threshold,
                is_(equal_to(context.expected)))
    return

@given("a StepRange with two step change thresholds and no reversals")
def with_two_thresholds_no_reversals(context):
    context.expected = 2
    context.iterator = StepRange(start=0,
                                 stop=24,
                                 step_change_thresholds=[2, 5])
    return

@then("the StepRange.current_change_index is one")
def current_step_index_one(context):
    assert_that(context.iterator.current_change_index,
                is_(equal_to(1)))
    return

@given("a StepRange with two step change thresholds and one reversals")
def with_two_thresholds_one_reversals(context):
    context.expected = 2
    context.iterator = StepRange(start=0,
                                 stop=24,
                                 step_change_thresholds=[2, 5])
    context.iterator.reversals = 1
    return

@then("the StepRange.threshold is previous threshold")
def reverse_threshold(context):    
    context.iterator.current_change_index = 1
    context.iterator._threshold = None

    assert_that(context.iterator.threshold,
                is_(equal_to(5)))

    context.iterator._threshold = None
    assert_that(context.iterator.threshold,
                is_(equal_to(2)))
    return
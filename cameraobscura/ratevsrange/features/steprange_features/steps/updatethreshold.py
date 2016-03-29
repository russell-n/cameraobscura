
# third-party
from hamcrest import assert_that, is_, equal_to, less_than
from behave import when, given, then

# this package
from cameraobscura.ratevsrange.stepiterator import StepRange


@given("a StepRange where the current_value is less than threshold")
def up_current_less(context):
    start = 0
    stop = 32
    context.iterator = StepRange(start=start,
                                 stop=stop,
                                 step_sizes = range(3),
                                 step_change_thresholds=[2,5])
    return


@when("the StepRange.update_threshold method is called")
def update_threshold_call(context):
    context.prior_threshold = context.iterator.threshold
    context.iterator.update_threshold()
    return


@then("the StepRange.threshold value will be the same")
def assert_no_change(context):
    assert_that(context.prior_threshold,
                is_(equal_to(context.iterator.threshold)))
    return


@given('a StepRange where the current_value equals threshold')
def current_equals_threshold(context):
    start = 0
    stop = 75
    context.iterator = StepRange(start=start,
                                 stop=stop,
                                 step_sizes=range(3),
                                 step_change_thresholds=[2,5])
    context.iterator.current_value = 2
    context.next = 5
    return


@then('the StepRange.threshold value will be next threshold')
def next_threshold(context):
    assert_that(context.iterator.threshold,
                is_(equal_to(context.next)))
    return


@given('a StepRange where the current_value exceeds last threshold')
def current_equals_threshold(context):
    start = 0
    stop = 75
    context.iterator = StepRange(start=start,
                                 stop=stop,
                                 step_change_thresholds=[5])
    context.iterator.current_value = 7
    return


@given("a StepRange where the current_value is greater than threshold")
def up_current_less(context):
    start = 35
    stop = 0
    context.iterator = StepRange(start=start,
                                 stop=stop,
                                 step_change_thresholds=[2,5])
    context.iterator.current_value = 8
    return


@given('a StepRange where the current_value equals lower threshold')
def lower_threshold(context):
    start = 55
    stop = 0
    context.iterator = StepRange(start=start,
                                 stop=stop,
                                 step_change_thresholds=[2,5])
    
    return


@then("the StepRange.threshold value will be lower")
def lower_than_threshold(context):
    context.iterator.current_value = 8
    prior_threshold = context.iterator
    context.iterator.current_value = 5
    
    assert_that(context.iterator.threshold,
                is_(less_than(prior_threshold)))
    return


@given("a StepRange with no step_change_thresholds")
def no_step_changes(context):
    start = 0
    stop = 53
    context.iterator = StepRange(start=start, stop=stop)
    return


@then("the StepRange.threshold will be the stop value")
def assert_stop_value(context):
    assert_that(context.iterator.threshold,
                is_(equal_to(context.iterator.stop)))
    return

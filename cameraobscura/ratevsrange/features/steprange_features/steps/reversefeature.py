
# python standard library
import operator

# third-party
from behave import given, when, then
from hamcrest import (assert_that, is_,
                      equal_to, same_instance)

# this package
from cameraobscura.ratevsrange.stepiterator import StepRange


@given("a StepRange that isn't reversible")
def irreversible(context):
    context.iterator = StepRange(start=0, stop=53)
    return


@when("StepRange.reverse is called")
def reverse_call(context):
    context.iterator.reverse()
    return


@then("the StepRange.current_value is set to stop")
def current_is_stop(context):
    assert_that(context.iterator.current_value,
                is_(equal_to(context.iterator.stop)))
    return


@given("a reversible StepRange")
def reversible(context):
    context.start = 9
    context.stop = 71
    context.iterator = StepRange(start=context.start,
                                 stop=context.stop,
                                 step_sizes=[1,2,3],
                                 step_change_thresholds=[10, 30],
                                 
                                 reversal_limit=3)
    context.iterator.step_size
    assert_that(context.iterator.reversals,
                is_(equal_to(0)))
    context.iterator.current_value = 10
    assert_that(context.iterator.step_size,
                is_(equal_to(2)))
    context.iterator.current_value = 30
    context.iterator.step_size
    context.iterator.threshold
    assert_that(context.iterator.current_change_index,
                is_(equal_to(1)))
    return


@then("StepRange.reversals is incremented")
def reversals_incremented(context):
    assert_that(context.iterator.reversals,
                is_(equal_to(1)))
    return


@then("StepRange start and stop are swapped")
def start_stop_swap(context):
    assert_that(context.start,
                is_(equal_to(context.iterator.stop)))

    assert_that(context.stop,
                is_(equal_to(context.iterator.start)))
    return


@then("_threshold is None")
def reset_properties(context):
    assert_that(context.iterator._threshold,
                is_(None))
    return


@then("current_step_index is incremented")
def increment_current_step_index(context):
    assert_that(context.iterator.current_step_index,
                is_(equal_to(1)))
    return


@then("current_change_index is incremented")
def increment_current_change_index(context):
    assert_that(context.iterator.current_change_index,
                is_(equal_to(0)))
    return


@then("compare and threshold_compare are swapped")
def compare_swap(context):
    assert_that(context.iterator.compare,
                is_(same_instance(operator.ge)))

    assert_that(context.iterator.threshold_compare,
                is_(same_instance(operator.le)))
    return


@then("direction and list direction are negative")
def direction_negation(context):
    assert_that(context.iterator.direction,
                is_(equal_to(-1)))
    assert_that(context.iterator.list_direction,
                is_(equal_to(-1)))
    return

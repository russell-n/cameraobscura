
# third-party
from behave import given, when, then
from hamcrest import assert_that, is_, equal_to

# this package
from cameraobscura.ratevsrange.stepiterator import StepRange


@given("a used StepRange")
def used_steprange(context):
    context.start = 4
    context.stop = 42

    context.iterator = StepRange(start=context.start,
                                 step_sizes = [3, 4, 5],
                                 step_change_thresholds = [10, 20], 
                               stop=context.stop)
    for step in context.iterator:
        pass
    return


@when("the StepRange is reset")
def reset_steprange(context):
    context.iterator.reset()
    return


@then("the StepRange current_value will be original start")
def assert_reset(context):
    assert_that(context.iterator.current_value,
                is_(equal_to(context.start)))
    return


@then("the StepRange step_size will be first size")
def assert_step_size_reset(context):
    assert_that(context.iterator.step_size,
                is_(equal_to(context.iterator.step_sizes[0])))
    return


@then("the StepRange threshold will be first threshold")
def assert_step_size_reset(context):
    assert_that(context.iterator.threshold,
                is_(equal_to(context.iterator.step_change_thresholds[0])))
    return


@then("the StepRange current_step_index will be Zero")
def assert_step_size_reset(context):
    assert_that(context.iterator.current_step_index,
                is_(equal_to(0)))
    return


@then("the StepRange current_change_index will be Zero")
def assert_change_index_reset(context):
    assert_that(context.iterator.current_change_index,
                is_(equal_to(0)))
    return


@then("the StepRange start will be original start")
def assert_change_index_reset(context):
    assert_that(context.iterator.start,
                is_(equal_to(context.start)))
    return


@then("the StepRange stop will be original stop")
def assert_change_index_reset(context):
    assert_that(context.iterator.stop,
                is_(equal_to(context.stop)))
    return


@then("the StepRange reversals will be Zero")
def assert_reversals(context):
    assert_that(context.iterator.reversals,
                is_(equal_to(0)))
    return


@given("a used reversible StepRange")
def reversible_steps(context):
    context.start = 2
    context.stop = 24

    context.iterator = StepRange(start=context.start,
                                 step_sizes = [3, 4, 5],
                                 step_change_thresholds = [10, 20],
                                 reversal_limit=3,
                               stop=context.stop)
    for step in context.iterator:
        if step in (2, 9, 12):
            context.iterator.reverse()

    return

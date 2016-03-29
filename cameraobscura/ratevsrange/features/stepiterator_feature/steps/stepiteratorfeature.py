
# third-party
from behave import given, when, then
from hamcrest import assert_that, is_, instance_of, contains

# this package
from cameraobscura.ratevsrange.stepiterator import StepIterator, StepList, StepRange


@given("a  StepIterator with a step-list")
def step_list(context):
    context.step_iterator = StepIterator(step_list=range(10))
    return


@when("the StepIterator's iterator is checked")
def check_step_iterator(context):
    context.iterator = context.step_iterator.iterator
    return


@then("the StepIterator's iterator is a  step-list")
def assert_list(context):
    assert_that(context.iterator,
                is_(instance_of(StepList)))
    return


@given("a  StepIterator with a step-range")
def step_list(context):
    context.step_iterator = StepIterator(start=0, stop=3)
    return


@then("the StepIterator's iterator is a  step-range")
def assert_list(context):
    assert_that(context.iterator,
                is_(instance_of(StepRange)))
    return


@given("a StepIterator with a step-list to traverse")
def step_list(context):
    context.expected = range(35)
    context.iterator = StepIterator(step_list=context.expected)
    return


@when("the StepIterator is traversed")
def step_traversal(context):
    context.outcome = [step for step in context.iterator]
    return


@then("the StepIterator given the expected outcome")
def assert_expected(context):
    assert_that(context.outcome,
                contains(*context.expected))
    return


@given("a StepIterator with a step-range to traverse")
def step_list(context):
    context.expected = range(35)
    context.iterator = StepIterator(start=0,
                                    stop=34)
    return


@given("a StepIterator with a step-list to traverse up and down")
def step_list_reversible(context):
    context.iterator = StepIterator(step_list=range(10),
                                    reversal_limit=1)
    return


@when("the StepIterator is traversed up and down")
def traverse_up_down(context):
    context.outcome = []
    context.expected = range(7) + range(5, -1, -1)
    for step in context.iterator:
        context.outcome.append(step)        
        if step == 6:
            context.iterator.reverse()            
    return


@then("the StepIterator gives the expected up and down outcome")
def assert_up_down_outcome(context):
    print context.outcome
    assert_that(context.outcome,
                contains(*context.expected))
    return


@given("a StepIterator with a step-range to traverse up and down")
def step_range_reversible(context):
    context.iterator = StepIterator(start=0,
                                 stop=9,
                                 reversal_limit=1)
    return

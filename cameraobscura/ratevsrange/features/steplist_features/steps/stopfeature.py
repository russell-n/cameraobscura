
#third-party
from behave import given, when, then
from hamcrest import assert_that, is_, equal_to

# this package
from cameraobscura.ratevsrange.stepiterator import StepList

@given("a  configured StepList")
def configured_steplist(context):
    context.step_list = range(10)
    context.iterator = StepList(step_list=context.step_list)
    return

@when("the StepList stop property is checked")
def check_stop(context):
    return

@then("it is the last item in the step list")
def assert_last_item(context):
    assert_that(context.iterator.stop,
                is_(equal_to(context.iterator.step_list[-1])))
    return
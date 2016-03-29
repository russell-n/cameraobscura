
# third-party
from behave import given, when, then
from hamcrest import assert_that, calling, raises

# this package
from cameraobscura.ratevsrange.stepiterator import StepRange
from cameraobscura import CameraobscuraError

@given("a StepRange with 1 more step size than step change threshold")
def valid_step_range(context):
    context.steprange = StepRange()
    return

@when("The user calls StepRange.check_rep")
def call_check_rep(context):
    context.check_rep = context.steprange.check_rep
    return

@then("No Error is raised")
def no_error(context):
    context.check_rep()
    return

@given("a StepRange with not 1 more step size than step change threshold")
def valid_step_range(context):
    context.steprange = StepRange(step_sizes=[1],
                                  step_change_thresholds=[10],
                                  stop=20)
    return

@then("CameraObscuraError is raised")
def assert_error(context):
    assert_that(calling(context.check_rep),
                raises(CameraobscuraError))
    return

@given("a StepRange with out of range but not 1 more step size than step change threshold")
def valid_step_range(context):
    context.steprange = StepRange(step_sizes=[1],
                                  step_change_thresholds=[100, 200],
                                  stop=10)
    return
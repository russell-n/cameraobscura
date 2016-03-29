from distutils.util import strtobool as _bool
import os

BEHAVE_DEBUG_ON_ERROR = _bool(os.environ.get("BEHAVE_DEBUG_ON_ERROR",
                                             "no"))
def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == 'failed':
        import pudb
        pudb.post_mortem(tb=step.exc_traceback,
                         e_type=None,
                         e_value=None)
    return


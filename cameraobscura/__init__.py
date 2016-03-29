class CameraobscuraError(Exception):
    """
    An error for code in the cameraobscura package to raise
    """
    pass

from theape.infrastructure.indexbuilder import create_toctree
from cameraobscura.utilities.noop import NoOp

BLUE = "\033[34m"
RED  = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0;0m"
BLUE_BOLD_RESET = BLUE + BOLD + "{0}" + RESET

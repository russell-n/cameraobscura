
# this package
from cameraobscura import BaseClass


class TheComposite(BaseClass):
    """
    The Composite aggregates callable objects
    """
    def __init__(self, components):
        """
        Composite constructor

        :param:

         - `components` : list of callable objects
        """
        super(TheComposite, self).__init__()
        self.components = components
        return

    def __call__(self):
        """
        The main interface -- calls all the components
        """
        for component in self.components:
            self.logger.info('Calling Component: {0}'.format(component))
            component()
        return
# end class TheComposite

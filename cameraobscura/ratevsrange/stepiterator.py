
from __future__ import print_function

# python standard library
import operator
import logging

# this package
from cameraobscura import CameraobscuraError

FIRST_ITEM = 0
UP = 1
DOWN = -UP
comparisons = dict(zip((UP, DOWN),
                       (operator.le,
                        operator.ge)))
threshold_comparisons = dict(zip((DOWN, UP),
                       (operator.le,
                        operator.ge)))

class StepBase(object):
    """
    Base-class for the step-iterators
    """
    def __init__(self, start=None, stop=None, reversal_limit=0):
        """
        StepBase Constructor

        :param:

         - ``reversal_limit``: maximum reversals allowed
        """
        super(StepBase, self).__init__()
        self._logger = None
        self.start = start
        self.stop = stop
        self.reversal_limit = reversal_limit
        self.reversals = FIRST_ITEM
        return

    @property
    def logger(self):
        """
        :return: A logging object.
        """
        if self._logger is None:
            self._logger = logging.getLogger("{0}.{1}".format(self.__module__,
                                  self.__class__.__name__))
        return self._logger


    
    @property
    def compare(self):
        """
        comparison function based on direction

        :return: operator le or ge
        """
        return comparisons[self.direction]

    @property
    def direction(self):
        """
        Direction of steps (1 or -1)
        """
        try:
            difference = self.stop - self.start
            return difference/abs(difference)
        except ZeroDivisionError as error:
            self.logger.debug("Start ({0}) equals stop ({1})".format(self.start,
                                                                     self.stop))
        return UP

    @property
    def reversible(self):
        """
        :return: True if still reversible
        """        
        return self.reversals < self.reversal_limit

class StepList(StepBase):
    """
    a list-based attenuation generator
    """
    def __init__(self, step_list, *args, **kwargs):
        """
        StepList constructor

        :param:

         - `step_list`: list of attenuations         
        """
        super(StepList, self).__init__(*args, **kwargs)
        self.start = self.current_value = 0
        self.step_list = step_list
        self._stop = None
        return

    @property
    def stop(self):
        """
        The end-index
        """
        if self._stop is None:
            self._stop = len(self.step_list) - 1
        return self._stop

    @stop.setter
    def stop(self, stopper):
        """
        Sets the stop (needed because the StepBase sets it)
        """
        self._stop = stopper
        return
    

    def __iter__(self):
        """
        The main interface
        """
        while self.compare(self.current_value, self.stop):
            yield self.step_list[self.current_value]
            self.current_value += self.direction
        return

    def reset(self):
        """
        resets the start and stop values
        """
        self.start = self.current_value = 0
        self._stop = None
        self.reversals = 0
        return

    def reverse(self):
        """
        reverse directions

        :precondition: self.stop has been set
        """
        if not self.reversible:
            self.current_value = self.stop
            return False
        self.start, self._stop = self._stop, self.start
        return True

    def check_rep(self):
        """
        Does nothing
        """
        return
# end class StepList

class StepRange(StepBase):
    """
    A stepped-iterator that generates a range of integers
    """
    def __init__(self, step_sizes=None,
                       step_change_thresholds=None,
                       *args, **kwargs):
        """
        StepRange constructor

        :param:

         - `start`: value to start with
         - `stop`: maximum value
         - `step_sizes`: list of step-sizes (in order)
         - `step_change_thresholds`: list of step-thresholds (to trigger change in step-size)
        """
        super(StepRange, self).__init__(*args, **kwargs)
        self._logger = None
        self._step_sizes = None
        self.step_sizes = step_sizes
        self.step_change_thresholds = step_change_thresholds

        # not obvious anymore, but the parent is setting this
        self.current_value = self.start
        
        # properties
        self._threshold = None
        self._step_size = None

        # these are used to keep track of positions in the lists
        # so that they can be reset and the iterator re-used
        self.current_step_index = FIRST_ITEM
        self.current_change_index = FIRST_ITEM

        # count of how many times we've reversed direction
        self.reversals = FIRST_ITEM
        return

    @property
    def list_direction(self):
        """
        Direction to traverse lists (e.g. step_sizes)

        :return: UP or DOWN
        """
        # even means up, odd mean back down
        if self.reversals % 2:
            return DOWN
        return UP

    @property
    def threshold_compare(self):
        """
        comparison function for changing step-size

        :return: operator le or ge
        """
        return threshold_comparisons[self.direction]
    
    @property
    def step_sizes(self):
        """
        List of step-sizes (default of 1)
        """
        if self._step_sizes is None:
            self._step_sizes = [1]
        return self._step_sizes

    @step_sizes.setter
    def step_sizes(self, sizes):
        """
        Casts the sizes to positive and sets step_sizes

        :param:

         - ``sizes``: list of integers for attenuation step-sizes
        """
        if sizes is not None:
            sizes = [abs(size) for size in sizes]
        self._step_sizes = sizes
        return
    
    @property
    def threshold(self):
        """
        The current threshold to test if the step-size should change
        """
        if self._threshold is None:
            if self.step_change_thresholds is not None:
                self._threshold = self.step_change_thresholds[self.current_change_index]
                self.current_change_index = self.increment_index(self.current_change_index,
                                                                 self.step_change_thresholds)
            else:
                self._threshold = self.stop
            self.logger.debug("Initial threshold: {0}".format(self._threshold))
        return self._threshold

    @property
    def step_size(self):
        """
        The amount to increase the current-value with each iteration.

        .. warning:: this checks current_value > threshold and updates accordingly

        :postcondition:

         - step_size set to first step_size
         - or step_size updated
        """
        if self._step_size is None or (self.threshold_compare(self.current_value,
                                                                self.threshold)
                                        and self.threshold != self.stop):
            self._step_size = self.step_sizes[self.current_step_index] 
            self.current_step_index = self.increment_index(self.current_step_index,
                                                           self.step_sizes)
            self.update_threshold()
        return self._step_size

    def update_threshold(self):
        """
        Updates the threshold if it has been exceeded
        """
        if (self.threshold_compare(self.current_value, self.threshold) and
            self.step_change_thresholds is not None):
                self._threshold = self.step_change_thresholds[self.current_change_index]
                self.current_change_index = self.increment_index(self.current_change_index,
                                                                 self.step_change_thresholds)
        return    

    def reset(self):
        """
        Sets the properties back to None
        """
        if self.reversals % 2:
            self.start, self.stop = self.stop, self.start
        self.reversals = FIRST_ITEM
        self.current_value = self.start
        self._step_size = None
        self._threshold = None
        self.current_step_index = FIRST_ITEM
        self.current_change_index = FIRST_ITEM
        return

    def increment_index(self, index, container):
        """
        increments the index for the container

        :param:

         - `index`: current index for the container
         - `container`: container to be indexed

        :return: index incremented, bounded by container size
        """
        index += self.list_direction
        index = min(index, len(container)-1)
        # disallowing wrap-around
        index = max(index, 0)
        return index

    def reverse(self):
        """
        changes the direction of the iteration
        """
        if not self.reversible:
            self.current_value = self.stop
            return False
        
        # reversals, start, and stop are used to check direction
        # so they should be changed first
        self.reversals += 1
        self.start, self.stop = self.stop, self.start
        
        self._threshold = None
        self.current_step_index = self.increment_index(self.current_step_index,
                                                        self.step_sizes)
        if self.step_change_thresholds is not None:
            self.current_change_index = self.increment_index(self.current_change_index,
                                                            self.step_change_thresholds)
        return True

    def check_rep(self):
        """
        Does nothing (to let the user decide what is valid and what is invalid)

        """
        #if self.step_change_thresholds is not None:
        #    try:
        #        assert (len(self.step_sizes) == len(self.step_change_thresholds) + 1 or
        #                min(self.step_change_thresholds) > self.stop)
        #    except AssertionError as error:
        #        self.logger.debug(error)
        #        raise CameraobscuraError(("Need exactly one more step_change_threshold than step_size"
        #                                  "or stop must be less than smallest step_change_threshold")
        return
        

    def __iter__(self):
        """
        Iterates over the values
        """
        while self.compare(self.current_value, self.stop):
            yield self.current_value
            self.current_value += self.step_size * self.direction
        return

    def __str__(self):
        """
        String of constructor parameters
        """
        return "start: {0}, stop: {1}, step_sizes: {2}, step_change_thresholds: {3}".format(self.start,
                                                                                            self.stop,
                                                                                            self.step_sizes,
                                                                                            self.step_change_thresholds)
# end class StepRange

class StepIterator(object):
    """
    An aggregator of step-iterators
    """
    def __init__(self, step_list=None,
                 *args, **kwargs):
        """
        StepIterator constructor

        :param:

         - ``step_list``: collection of steps
         - ``reversal_limit``: number of reversals allowed
        """
        self.args = args
        self.kwargs = kwargs
        self.step_list = step_list
        self._iterator = None
        return

    @property
    def iterator(self):
        """
        StepRange if step_list not set
        """
        if self._iterator is None:
            if self.step_list is not None:
                if 'reversal_limit' in self.kwargs:
                    reversal_limit = self.kwargs['reversal_limit']
                else:
                    reversal_limit = 0
                self._iterator = StepList(step_list=self.step_list,
                                          reversal_limit=reversal_limit)
            else:
                self._iterator = StepRange(*self.args, **self.kwargs)
        return self._iterator

    def __iter__(self):
        """
        traverses the iterator

        :yield: next step
        """
        for step in self.iterator:
            yield step
        return

    def __getattr__(self, name):
        """
        A pass-through to the iterator
        """
        return getattr(self.iterator, name)

if __name__ == "__main__":
    iterator = StepRange(start=0,
                            stop=10,
                            step_sizes=[1,2],
                            step_change_thresholds=[5])
    import pudb
    pudb.set_trace()
    for value in iterator:
        print(value)
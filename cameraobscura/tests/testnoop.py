
# python standard library
import unittest
import random
import string

# this package
from cameraobscura.utilities.noop import NoOp


class TestNoOp(unittest.TestCase):
    def setUp(self):
        self.noop = NoOp(noop_name='NoOp')
        return
    
    def test_constructor(self):
        """
        Does it build?
        """        
        noop = NoOp(noop_name='NoOp',
                    able='alpha')
        NoOp('randrange',
             random.randrange(100))
        return

    def test_call(self):
        """
        Does it do nothing if called?
        """
        self.noop()
        self.noop(3)
        self.noop(pig='wilbur',
                  goat='tom')
        return

    def test_anything(self):
        """
        Can you call most anything?
        """
        name_length = random.randrange(1, 10)
        name = "".join([random.choice(string.letters) for letter in xrange(name_length)])
        args = random.randrange(100)
        getattr(self.noop, name)(args)
        return
        

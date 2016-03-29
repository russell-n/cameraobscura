# Copyright (c) 2012 Russell Nakamura

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
The sumparser parses sums and logs the bandwidth sum
"""

from iperfparser import IperfParser 
from iperfexpressions import HumanExpression, ParserKeys, CsvExpression
import oatbran as bran
from coroutine import coroutine

BITS = 'bits'

class HumanExpressionSum(HumanExpression):
    """
    Changes the thread-column regular expression to match SUMS if needed
    """
    def __init__(self, threads=4):
        """
        :param:

         - `threads`: number of parallel threads
        """
        super(HumanExpressionSum, self).__init__()
        self.threads = threads
        return

    @property
    def thread_column(self):
        """
        :return: expression to match the thread (sum) column
        """
        if self._thread_column is None:
            if self.threads > 1:
                thread = "SUM"
            else:
                thread = bran.OPTIONAL_SPACES + bran.INTEGER
            self._thread_column = bran.L_BRACKET + thread + bran.R_BRACKET
        return self._thread_column
# end class HumanExpressionSum

class CsvExpressionSum(CsvExpression):
    """
    Changes the thread column to look for -1 if needed
    """
    def __init__(self, threads=4):
        """
        :param:

         - `threads`: the number of parallel threads
        """
        super(CsvExpressionSum, self).__init__()
        self.threads = threads
        return

    @property
    def thread_column(self):
        """
        :return: the expression to match the thread (sum) column
        """
        if self._thread_column is None:
            if self.threads > 1:
                thread = "-1"
            else:
                thread = bran.INTEGER
            self._thread_column = bran.NAMED(ParserKeys.thread, thread)
        return self._thread_column

    
class SumParser(IperfParser):
    """
    The SumParser emits bandwidth sum lines
    """
    def __init__(self, *args, **kwargs):
        super(SumParser, self).__init__(*args, **kwargs)
        self.log_format = "({0}) {1} {2}/sec"
        return

    @property
    def regex(self):
        """
        :return: a dictionary of compiled regular expressions
        """
        if self._regex is None:
            self._regex = {ParserKeys.human:HumanExpressionSum(threads=self.threads).regex,
                           ParserKeys.csv:CsvExpressionSum(threads=self.threads).regex}
        return self._regex

    def __call__(self, line):
        """
        :param:

         - `line`: a line of iperf output

        :return: bandwidth or None
        """
        match = self.search(line)
        assert type(match) == dict or match is None, "match: {0}".format(type(match)) 
        bandwidth = None
        if match is not None and self.valid(match):
            
            bandwidth = self.bandwidth(match)
            self.intervals[float(match[ParserKeys.start])] = bandwidth
            self.logger.info(self.log_format.format(match[ParserKeys.start],
                                                    bandwidth,
                                                    self.units))
        return bandwidth

    @coroutine
    def pipe(self, target):
        """
        
        :warnings:

         - For bad connections with threads this might break (as the threads die)
         - Use for good connections or live data only (use `bandwidths` and completed data for greater fidelity)
         
        :parameters:

         - `target`: a target to send matched output to

        :send:

         - bandwidth converted to self.units as a float
        """
        while True:
            line = (yield)
            match = self.search(line)
            if match is not None and self.valid(match):
                # threads is a dict of interval:(thread_count, bandwidths)
                target.send(self.bandwidth(match))
        return
# end class SumParser

"""
Azimuth AdeptN Attenuator.
This is a slightly different implementation of the
AdeptN class. Rather than take AP1 or AP2 as
parameters for the methods, this one assigns a specific
path when constructed.
It's the original way the AdeptN class was designed and
is better suited for a wide range of tests including Rate
vs Range. It allows any port to be used. I created this
class when all of a sudden the ports being used were 2A
and 2B instead of going between COM and 1A or 2A.
"""

TCLSCRIPTDIR = 'C:/AZ_Tests/'
NOROUTE = "Unable to connect to the AdeptN: "

# python standard library
import re

# this package
from Attenuator import Attenuator
from cameraobscura.clients.simpleclient import SimpleClient

class AdeptNCustomPath(Attenuator):
    """
    The attenuation is controlled using tclsh and a tcl script file on the 
    Director PC. 

    This class works just like the AdeptN class but its constructor takes a 
    specifc path for getting and setting the attenuation.
    """

    def __init__(self, host_ip, path, username="allion", password="testlabs"):
        """
        Constructor

        :Parameters:
         - `host_ip`: (str) IP address of the Azimuth Director PC
         - `username and password`: (str) auth data for Director PC
         - `path`: (str) AdpetN attenuation path, e.g. "C1-M2 2A-2B"
        """
        self.path = path
        self.ssh = SimpleClient(host_ip, username ,password)
        self._range_min = None
        self._range_max = None

    @property
    def range_min(self):
        """
        @property - use _getRange to set this as well as range_max
        """
        if self._range_min is None:
            self._range_min, self._range_max = self._getRange()
        return self._range_min

    @property
    def range_max(self):
        """
        @property - use _getRange to set this as well as range_min
        """
        if self._range_max is None:
            self._range_min, self._range_max = self._getRange()
        return self._range_max

    def setAttenuation(self, val):
        """
        :Parameters:
         - `val`: (int) new attenuation value to set (zero-based, must be less 
           than max - see getMax)

        :Returns: (bool,int) Whether value was set correctly, & what value 
         attenuator is at now.
        """
        range_based_val = val + self.range_min
        script_name = 'adeptn_setatten.tcl'
        cmd = 'tclsh {0}'.format(TCLSCRIPTDIR)
        cmd += '{0} {1} {2}'.format(script_name, self.path, range_based_val)

        result = self.ssh.exec_command(cmd)

        newval = self.getAttenuation()[1]
        if val == newval:
            return val
        else:
            raise AttenuatorError("Error setting attenuation ({}) ({})".format(newval,result[-1].readline()))

    def getAttenuation(self):
        """
        :Returns: (bool,int/str) Whether tcl script executed correctly, 
         either the current attenuation value or an error message.
        """
        script_name = 'adeptn_getatten.tcl'
        cmd = 'tclsh {0}'.format(TCLSCRIPTDIR)
        cmd += '{0} {1}'.format(script_name, self.path)

        result = self.ssh.Run(cmd)
        match = re.search(r'INFO\s+(\d+)\s', result.stdout)
        if match:
            return int(match.group(1)) - self.range_min
        else:
            raise AttenuatorError("Error getting attenuation "+result.stderr)

    def _getRange(self):
        """
        Get the minimum and maximum valid values of attenuation.

        :Returns: (int,int) The offset and maximum
        """
        script_name = 'adeptn_getrange.tcl'
        cmd = 'tclsh {0}'.format(TCLSCRIPTDIR)
        cmd += '{0} {1}'.format(script_name, self.path)

        result = self.ssh.exec_command(cmd)
        low = 0
        hi = 0
        match = re.search('\{min\s(\d+)\}\s\{max\s(\d+)', result[1].readline())
        if match:
            low = int(match.group(1))
            hi = int(match.group(2))
            return low,hi
        else:
            raise AttenuatorError("Error getting attenuator range: "+result[-1].readline())

    def getAttenMax(self):
        """
        Get the maximum value the attenuation can be set to.

        :Returns: (int) _getRange specifies the valid range, the 
         zero-based max is just the upper end of that, minus the lower
        """
        return self.range_max - self.range_min + 1

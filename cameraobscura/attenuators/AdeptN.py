#!/usr/bin/env python

"""
Azimuth AdeptN Attenuator
"""

TCLSCRIPTDIR = 'C:/AZ_Tests/'
NOROUTE = "Unable to connect to the AdeptN: "

# python standard library
import re

# This Package
from cameraobscura.clients.simpleclient import SimpleClient
from Attenuator import Attenuator, AttenuatorError



class AdeptN(Attenuator):
    """
    The attenuation is controlled using tclsh and a tcl script file on
    the Director PC.

    For a Rate vs. Range test the methods of this class can be used with
    no arguments passed for AP, since the default value will set the
    attenuation between COM and the 1A port.

    For a Roaming Test the methods can be given an argument specifying which
    AP to change the attenuation of. There is a default value of "AP1".
    Calls to these methods should all use "AP1" or "AP2" to specify
    which attenuation to set. These values will translate to the following:

    :AP Translations:
     - AP1: Chassis C1-M1 Path 1A-COM
     - AP2: Chassis C1-M2 Path 2A-COM

    :Note: If neither of the available paths is correct for the AdeptN
     configuration, take a look at using AdeptNCustom instead.

    Another feature I'd like to implement is disconnecting an AP by simply
    getting or setting the attenuation value for "C1-M1","1C-1A" (I think),
    or "C1-M2","2C-2A" respectively. It needs testing and follow-up.
    """

    def __init__(self, host_ip, username="allion", password="testlabs"):
        """
        :Parameters:
         - `host_ip`: (str) IP address of the Azimuth Director PC
         - `username and password`: (str) auth data for Director PC
        """
        self._range_AP1 = None
        self._range_AP2 = None
        self.ssh = SimpleClient(host_ip, username, password)

    @property
    def range_AP1(self):
        """
        @property method to get/set the pathloss range for AP1
        and only invoke the TCL script once.

        Tuple of 2 Strings.
        """
        if self._range_AP1 is None:
            self._range_AP1 = self._getRange("AP1")
        return self._range_AP1

    @property
    def range_AP2(self):
        """
        @property method to get/set the pathloss range for AP2
        and only invoke the TCL script once.

        Tuple of 2 Strings.
        """
        if self._range_AP2 is None:
            self._range_AP2 = self._getRange("AP2")
        return self._range_AP2

    def setAttenuation(self, val, AP="AP1"):
        """
        :Parameters:
         - `val`: (int) new attenuation value to set (zero-based, must be less
           than max - see getMax)
         - `AP`: (str) specify which attenuation value to set

        :Returns: (bool,int) Whether value was set correctly, & what value
         attenuator is at now.
        """
        chassis, path = self._translateAP(AP)

        try:
            range_based_val = val + self._rangeMin(AP)
        except TypeError as detail:
            raise AttenuatorError("Error setting attenuation: {}".format(detail))
        script_name = 'adeptn_setatten.tcl'
        cmd = 'tclsh {0}'.format(TCLSCRIPTDIR)
        cmd += '{0} {1} {2} {3}'.format(
            script_name, chassis, path, range_based_val)

        result = self.ssh.Run(cmd)

        if val == self.getAttenuation(AP)[1]:
            return val
        else:
            raise AttenuatorError("Error setting attenuation: " + result.stderr)

    def getAttenuation(self, AP="AP1"):
        """
        :Parameters:
         - `AP`: (str) which attenuation value to retrieve

        :Returns: (bool,int/str) Whether tcl script executed correctly, &
         either the current attenuation value or an error message.
        """
        chassis, path = self._translateAP(AP)

        script_name = 'adeptn_getatten.tcl'
        cmd = 'tclsh {0}'.format(TCLSCRIPTDIR)
        cmd += '{0} {1} {2}'.format(script_name, chassis, path)

        result = self.ssh.Run(cmd)

        match = re.search(r'INFO\s+(\d+)\s', result.stdout)
        if match:
            return int(match.group(1)) - self._rangeMin(AP)
        else:
            raise AttenuatorError("Error getting attenuation: " + result.stderr)

    def _getRange(self, AP="AP1"):
        """
        Get the minimum and maximum valid values of attenuation for the
        specified AP.

        :Returns: (int,int) The offset and maximum for this port of the
         attenuator.
        """
        # Should be returned to self._range_AP1 or self._range_AP2
        chassis, path = self._translateAP(AP)

        script_name = 'adeptn_getrange.tcl'
        cmd = 'tclsh {0}'.format(TCLSCRIPTDIR)
        cmd += '{0} {1} {2}'.format(script_name, chassis, path)

        result = self.ssh.Run(cmd)

        low = 0
        hi = 0
        match = re.search('\{min\s(\d+)\}\s\{max\s(\d+)', result.stdout)
        if match:
            low = int(match.group(1))
            hi = int(match.group(2))
            return low, hi
        else:
            raise AttenuatorError("Could not parse range: " + result.stderr)

    def getAttenMax(self, AP="AP1"):
        """
        Get the maximum value the attenuation can be set to.

        :Returns: (int) _getRange specifies the valid range, the
         zero-based max is just the upper end of that, minus the lower
        """
        return self._rangeMax(AP) - self._rangeMin(AP) + 1

    def _translateAP(self, AP):
        """
        Translate "AP1" or "AP2" to the correct
        arguments for the TCL scripts on the Director PC.

        :Parameters:
         - `AP`: (str) "AP1" or "AP2"

        :Returns: (str,str) Chassis and Path for specified AP.
         (Or just Error,Error if not found)
        """
        if AP == "AP1":
            return "C1-M1", "1A-COM"
        elif AP == "AP2":
            return "C1-M2", "2A-COM"
        else:
            raise AttenuatorError("Invalid AP name: " + AP)

    def _rangeMin(self, AP):
        """
        Translate "AP1" and "AP2" to the fields for AP1 and AP2 range.

        :Parameters:
         - `AP`: (str) "AP1" or "AP2"
        """
        if AP == "AP1":
            return self.range_AP1[0]
        elif AP == "AP2":
            return self.range_AP2[0]
        else:
            raise AttenuatorError("Error getting range_min for " + AP)

    def _rangeMax(self, AP):
        """
        Translate "AP1" and "AP2" to the fields for AP1 and AP2 range.

        :Parameters:
         - `AP`: (str) "AP1" or "AP2"
        """
        if AP == "AP1":
            return self.range_AP1[1]
        elif AP == "AP2":
            return self.range_AP2[1]
        else:
            raise AttenuatorError("Error getting range_max for " + AP)

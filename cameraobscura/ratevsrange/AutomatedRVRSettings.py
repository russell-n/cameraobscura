#!/usr/bin/env python

"""
Settings package that uses ConfigParser to build up
all of the options necessary, from a specified config.ini
file. Also has the ability to validate the listed required
options, and can create an empty config file listing those
options.
"""


OPTIONS = [
           "dut,control_ip,192.168.10.x",
           "dut,test_ip,192.168.20.x",
           "dut,username,user",
           "dut,password,pass",
           "server,control_ip,192.168.10.x",
           "server,test_ip,192.168.20.x",
           "server,username,user",
           "server,password,pass",
           "attenuation,name,AdeptN",
           "attenuation,interface_type,LAN",
           "attenuation,interface,192.168.10.27",
           "attenuation,start,0",
           "attenuation,step,2 1",
           "attenuation,stepchange,40",
           "attenuation,path,C1-M2 2A-2B",
           "traffic,type,tcp",
           "traffic,tcp_window_size,256K",
           "traffic,udp_data_rate,200M",
           "traffic,packet_length,1470",
           "traffic,pairs,4",
           "traffic,format,m",
           "traffic,interval,1",
           "traffic,duration,30",
           "traffic,direction,both",
           "other,test_repetitions,1",
           "other,result_location,Results",
           "other,test_name,results",
           "other,dump_device_log,true"
           ]


import ConfigParser

class AutomatedRVRSettings(object):
    def __init__(self, filename):
        """
        Constructor

        :Parameters: filename: *String* name of the config file to parse
        """
        self.config = ConfigParser.ConfigParser()
        self.configfilename = filename
        self.config.read(filename)

    def validate(self):
        """
        For each required option, make sure it is present
        """
        for opt in OPTIONS:
            section,option,defaultval = opt.split(',')
            if not self.config.has_option(section, option):
                return False, "Missing option {0}".format(option)
        return True, "Validated."

    @classmethod
    def generateSampleConfigFile(cls):
        """
        For each required option, add a section to a new ConfigParser
        object if necessary, and add the option. Then write it to a file.
        """
        new_config = ConfigParser.ConfigParser()
        for opt in OPTIONS:
            section,option,defaultval = opt.split(',')
            if not new_config.has_section(section):
                new_config.add_section(section)
            new_config.set(section, option, defaultval)
        with open("rvr_example.ini", 'wb') as newconfigfile:
            new_config.write(newconfigfile)
        print "Generated file: rvr_example.ini"

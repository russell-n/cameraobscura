Configuration Documentation Helpers
===================================

I seem to be using the same code in the different configuration file documentation so this module is a place to gather them all up.

::

    def print_sample(section):
        command = 'rvr fetch -s {0}'.format(section).split()
        output = subprocess.check_output(command).split('\n')
        for line in output:
            if line.startswith('[') or '=' in line:
                print line
        return output
    
    



# python standard library
import subprocess
import re


expression = r"^\[|^#\[|.*=.*"
def print_sample(section):
    command = 'rvr fetch -s {0}'.format(section).split()
    output = subprocess.check_output(command).split('\n')
    for line in output:
        if re.search(expression, line):
            print line
    return output

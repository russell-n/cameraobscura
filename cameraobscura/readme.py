
from __future__ import print_function
# for the new pweave

# python standard library
from subprocess import check_output

print(check_output('rvr fetch'.split()))

print(check_output('rvr fetch --section dut'.split()))

print(open('../documentation_requirements.txt').read())

print(check_output('rvr -h'.split()))

print(check_output('rvr run -h'.split()))

print(check_output('rvr fetch -h'.split()))

print(open('../testing_requirements.txt').read())
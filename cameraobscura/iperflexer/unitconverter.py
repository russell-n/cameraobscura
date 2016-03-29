# Copyright (c) <year> <copyright holders>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
The unit converter is a table to convert Data Rates
"""

class UnitNames(object):
    """
    Unit Names is a namespace to hold units
    """
    __slots__ = ()
    bits = "bits"
    kbits = "K" + bits
    mbits = "M" + bits
    gbits = "G" + bits
    bytes = "Bytes"
    kbytes = "KBytes"
    mbytes = "MBytes"
    gbytes = "GBytes"
# end UnitNames

IDENTITY = 1
ONE = 1.0
KILO = 10**3
TO_KILO = ONE/KILO
MEGA = KILO**2
TO_MEGA = ONE/MEGA
GIGA = KILO * MEGA
TO_GIGA = ONE/GIGA
BYTE = 8
TO_BYTE = ONE/BYTE

to_units = [UnitNames.bits, UnitNames.kbits,UnitNames.mbits , UnitNames.gbits,
             UnitNames.bytes, UnitNames.kbytes, UnitNames.mbytes, UnitNames.gbytes]

bit_row_1 = [IDENTITY, TO_KILO,TO_MEGA , TO_GIGA,]
bit_row_2 = [KILO] + bit_row_1[:-1]
bit_row_3 = [MEGA] + bit_row_2[:-1]
bit_row_4 = [GIGA] + bit_row_3[:-1]

to_byte_row_1 = [TO_BYTE * converter for converter in bit_row_1]
to_byte_row_2 = [KILO * TO_BYTE] + to_byte_row_1[:-1]
to_byte_row_3 = [MEGA * TO_BYTE] + to_byte_row_2[:-1]
to_byte_row_4 = [GIGA * TO_BYTE] + to_byte_row_3[:-1]

byte_row_1 = [BYTE * conversion for conversion in bit_row_1]
byte_row_2 = [KILO * BYTE] + byte_row_1[:-1]
byte_row_3 = [MEGA * BYTE] + byte_row_2[:-1]
byte_row_4 = [GIGA * BYTE] + byte_row_3[:-1]

from_bits = dict(zip(to_units, bit_row_1 + to_byte_row_1))
from_kbits = dict(zip(to_units, bit_row_2 + to_byte_row_2))
from_mbits = dict(zip(to_units, bit_row_3 + to_byte_row_3))
from_gbits = dict(zip(to_units, bit_row_4 + to_byte_row_4))

from_bytes = dict(zip(to_units, byte_row_1 + bit_row_1))
from_kbytes = dict(zip(to_units, byte_row_2 + bit_row_2))
from_mbytes = dict(zip(to_units, byte_row_3 + bit_row_3))
from_gbytes = dict(zip(to_units, byte_row_4 + bit_row_4))

class UnitConverter(dict):
    """
    The UnitConverter is a conversion lookup table.

    Usage::

       converted = old * UnitConverter[old units][new units]

    Use class UnitNames to get valid unit names
    """
    def __init__(self):
        self[UnitNames.bits] = from_bits
        self[UnitNames.kbits] = from_kbits
        self[UnitNames.mbits] = from_mbits
        self[UnitNames.gbits] = from_gbits
    
        self[UnitNames.bytes] = from_bytes
        self[UnitNames.kbytes] = from_kbytes
        self[UnitNames.mbytes] = from_mbytes
        self[UnitNames.gbytes] = from_gbytes
        return
# end class UnitConverter

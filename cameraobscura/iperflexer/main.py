# python
from __future__ import print_function
import sys
import os

# iperflexer
from argumentparser import Arguments
from iperfparser import IperfParser
from sumparser import SumParser
from unitconverter import UnitNames
from finder import find

class ArgumentError(Exception):
    """
    """
# end class ArgumentError

UNITS = {'bits': UnitNames.bits,
         'kbits': UnitNames.kbits,
         'mbits': UnitNames.mbits,
         'gbits': UnitNames.gbits,         
         'bytes': UnitNames.bytes,
         'kbytes': UnitNames.kbytes,
         'mbytes': UnitNames.mbytes,
         'gbytes': UnitNames.gbytes}

WRITEABLE = 'w'
ADD_NEWLINE = "{0}\n"

def enable_debugging():
    try:
        import pudb
        pudb.set_trace()
    except ImportError as error:
        print(error)
        raise ArgumentError("`pudb` argument given but unable to import `pudb`")

def pipe(args, infile=None, outfile=None):
    """
    Reads input from standard in and sends output to standard out.
    """
    if infile is None:
        infile = sys.stdin
    if outfile is None:
        outfile = sys.stdout
    try:
        units = UNITS[args.units.lower()]
    except KeyError:
        raise ArgumentError("Unknown Units: {0}".format(args.units))
        return

    if args.voodoo:
        parser = IperfParser(units=units,
                             maximum=args.maximum,
                             threads=args.threads)
    else:
        parser = SumParser(units=units, maximum=args.maximum,
                           threads=args.threads)
    for line in infile:
        parser(line)
        if args.tee:
            sys.stderr.write(line)
    for bandwidth in parser.bandwidths:
        outfile.write(ADD_NEWLINE.format(bandwidth))
    parser.reset()
    return

def analyze(args):
    """
    Reads data from files and outputs to files
    """
    for name in find(args.glob):
        basename, _ = os.path.splitext(name)
        new_name = basename + "_parsed.csv"
        if args.save:
            output = open(new_name, WRITEABLE)
        else:
            output = None
        pipe(args, open(name), output)
    return

def main():
    args = Arguments().parse_args()
    if args.pudb:
        enable_debugging()
    if args.glob is None:
        pipe(args)
    else:
        analyze(args)
    return

if __name__ == "__main__":
    main()

# python
import sys
import re
import os.path as path
import optparse

import epp_utils as epp

def main(argv):
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args(argv)
    
    data = sys.stdin.read()
    
    fields = re.split('(<.*?>)',data)
    level = 0
    for f in fields:
       if f.strip() == '': continue
       if f[0]=='<' and f[1] != '/':
           epp.print(' '*(level*4) + f)
           level = level + 1
           if f[-2:] == '/>':
               level = level - 1
       elif f[:2]=='</':
           level = level - 1
           epp.print(' '*(level*4) + f)
       else:
           epp.print(' '*(level*4) + f)

if __name__ == "__main__":
    main(sys.argv[1:])
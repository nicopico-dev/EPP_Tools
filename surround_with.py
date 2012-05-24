# python surround_with.py -w "#" | -b "(" -e ")"

import optparse
import os
import sys
import os.path as path
import epp_utils as epp

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-w","--surround_with",action="store",type="string",dest="surround_with",help="String to surround the text with")
    parser.add_option("-b","--begin",action="store",type="string",dest="begin",help="String to add before the text")
    parser.add_option("-e","--end",action="store",type="string",dest="end",help="String to add after the text")
    
    (options, args) = parser.parse_args()
    
    input_text = ''.join(sys.stdin.readlines())
    epp.log("-> %s" % input_text)
    
    if options.surround_with or (options.begin and options.end):
        if options.surround_with:
            begin = options.surround_with
            end = options.surround_with
        else:
            begin = options.begin
            end = options.end
            
        sys.stdout.write(begin + input_text + end)
        
    else: 
        # Provoquer une erreur
        parser.print_help()
        sys.exit(1)
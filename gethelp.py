# python gethelp.py -f "%TEMPFILE%" -c %POS% --keywords "LANGAGE"

DEBUG_FILE = False

import sys
import optparse
import re
import webbrowser

import epp_utils as epp

def get_search(options):
    input_text = epp.readline()

    if len(input_text.strip()) > 0:
        return input_text
    else:
        epp.log(options.filename)
        return epp.getCurrWord(options.filename, options.cursor)

def main(argv):
    parser = optparse.OptionParser()
    parser.add_option("-c","--cursor",action="store",type="int",dest="cursor",help="Cursor position in file (byte)")
    parser.add_option("-f","--filename",action="store",type="string",dest="filename",help="File to parse")
    parser.add_option("--keywords",action="store",type="string",dest="keywords",help="Additionnal keywords that should be sent with the query")
    parser.add_option("-n", action="store",type="string",dest="real_filename")

    parser.set_defaults()
    (options, args) = parser.parse_args(argv)

    if options.filename and options.cursor:
        if not options.real_filename:
            options.real_filename = options.filename
            
        search_term = get_search(options)
        epp.log(search_term)
    
        # Preparation pour google
        tags = epp.getFileTags(options.real_filename)
        if len(tags) > 0:
            epp.log(tags)
            search_term = " ".join(tags) + " " + search_term
        
        if options.keywords:
            search_term = options.keywords + " " + search_term
            
        search_term = re.sub(r"\s+", "+", search_term.strip())
    
        # Lance un navigateur avec une recherche
        url = "http://www.google.com/search?q={0}".format(search_term)
        epp.log("url: " + url)
        
        webbrowser.open_new_tab(url)
        
    else:
        # On provoque une erreur
        if not options.filename:
            parser.error("filename")
        elif not options.cursor:
            parser.error("cursor")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
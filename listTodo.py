# python listTodo.py -p "%PROJECTFILE%" -f "%FILE%" -m "TODO"

# TODO
# - Afficher les chemins relatifs par rapport au projet au lieu des chemins absolus

import sys
import re
import os.path as path
import optparse

import epp_utils as epp

def main(argv):
    parser = optparse.OptionParser()
    parser.add_option("-p","--project",action="store",type="string",dest="project",help="Project file")
    parser.add_option("-f","--file",action="store",type="string",dest="file",help="Current file (if no project are found)")
    parser.add_option("-m","--markers",action="store",type="string",dest="markers",help="Marker to search for, comma separated")
    
    parser.set_defaults(markers='TODO')
    
    (options, args) = parser.parse_args(argv)
    
    epp.log("project file: %s, current file: %s, markers: %s" % (options.project, options.file, options.markers))
    
    # Commentaires gérés : //, /*, #, --, '
    r1 = re.compile(r"(?://|/\*|#|--|')\s*(" + options.markers.replace(',', '|') + r")\s*:?\s+(.*)\s*$", re.IGNORECASE)
    epp.log ("r1 : %s" % r1.pattern)
    
    if options.project or options.file:
        if options.project:
            files = epp.getProjectFiles(options.project)
        else:
            files = (options.file,)
        for f in files:
            epp.log(f)
            if path.exists(f):
                with open(f, 'r') as fileh:
                    l_num = 1
                    for l in fileh:
                        match = r1.search(l)
                        if (match):
                            epp.print(("[%s] %s:%d %s" % ( match.group(1), f, l_num, match.group(2).strip() )))
                        l_num = l_num + 1
    else: 
        # On provoque une erreur
        parser.error('project') 
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
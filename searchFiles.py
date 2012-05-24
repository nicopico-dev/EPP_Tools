# python searchProject.py [-p "%PROJECTFILE%"] [-f "FILE"]

import sys
import os.path as path
import optparse

import epp_utils as epp

def main(argv):
    parser = optparse.OptionParser()
    parser.add_option("-f","--file",action="store",type="string",dest="file",help="File to search")
    parser.add_option("-p","--project",action="store",type="string",dest="project",help="Project file to search")
    parser.add_option("-b","--basedir",action="store",type="string",dest="basedir",help="Base directory to search")
    parser.add_option("-m","--filemask",action="store",type="string",dest="filemask",help="Limit search to file mask")
    parser.add_option("-i","--ignore-case",action="store_true",dest="ignore_case",help="Ignore case")
    parser.add_option("","--interactive",action="store_true",dest="interactive",help="Use dialogs to define search options")
    
    parser.set_defaults(ignore_case=False, interactive=False)
    
    (options, args) = parser.parse_args(argv)
    
    epp.log("project file: %s, file : %s, ignore_case: %s" % (options.project, options.file, options.ignore_case))
    
    input_text = sys.stdin.readline()
    epp.log("-> %s" % input_text)
    
    if options.ignore_case:
        case_flag = re.IGNORECASE 
    else: 
        case_flag = 0
    
    if options.interactive:
        epp.print("test")
    elif (options.project or options.file or options.basedir) and input_text.strip() != '':
        if (options.project):
            files = epp.getProjectFiles(options.project)
        if (options.basedir):
            files = epp.getFilesInTree(options.basedir, options.filemask)
        elif (options.file):
            files = [options.file]
        
        for f in files:
            if path.exists(f):
                try:
                    with open(f, 'r') as fileh:
                        l_num = 1
                        for l in fileh:
                            if l.find(input_text) != -1:
                                epp.print("%s:%d %s" % ( f, l_num, l.strip() ))
                            l_num = l_num + 1
                except UnicodeError:
                    epp.err("Can't read file {0}".format(f))
    else: 
        # Provoque une erreur
        parser.print_help()
        epp.log("-f and -p are mutually exclusive")
        sys.exit(1)

if __name__ == "__main__":
    epp.log(sys.argv)
    main(sys.argv[1:])
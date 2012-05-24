import optparse
import os
import sys
import os.path as path

import epp_utils as epp

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-e","--editor_path",action="store",type="string",dest="editor_path",help="EditPad path")
    parser.add_option("-p","--path",action="store",type="string",dest="path",help="Current file path")
    
    parser.set_defaults()
    (options, args) = parser.parse_args()
    
    input_text = sys.stdin.readline()
    epp.log("-> %s" % input_text)
    
    if len(input_text) == 0:
        epp.log("Selectionner le fichier a ouvrir\n");
    elif options.editor_path and options.path:
        if path.isabs(input_text):
            # Chemin absolu
            file_to_open = path.normpath(input_text)
        else:
            # Chemin relatif
            file_to_open = path.normpath(path.join(options.path, input_text))            
        
        editor_exec = options.editor_path + '\EditPadPro.exe'
        epp.log("exec : %s %s" % (editor_exec, file_to_open))
        
        if exists(file_to_open):
            file_to_open = '"' + file_to_open + '"'
            pid = os.spawnl(os.P_NOWAIT, editor_exec, '/newinstance', file_to_open)
            epp.log("Ok! (%d)" % pid)
        else:
            epp.log("Fichier %s introuvable" % file_to_open)
            sys.exit(2)
    else: 
        # Provoquer une erreur
        parser.print_help()
        sys.exit(1)
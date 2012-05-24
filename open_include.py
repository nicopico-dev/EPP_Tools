# python open_include.py -e "%EPPPATH%" -p "%PATH%" [-d "c:\dev\include"]

import optparse
import os
import sys
import os.path as path
import epp_utils as epp

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-e","--editor_path",action="store",type="string",dest="editor_path",help="EditPad path")
    parser.add_option("-p","--path",action="store",type="string",dest="path",help="Current file path")
    parser.add_option("-d","--default",action="store",type="string",dest="default_path",help="Default path for include")
    
    parser.set_defaults(default_path=".")
    (options, args) = parser.parse_args()
    
    input_text = epp.readline()
    epp.log("-> %s" % input_text)
    
    if options.editor_path and options.path and len(input_text) > 0:
        if not path.isabs(input_text):
            # Chemin relatif
            file_to_open = path.normpath(path.join(options.path, input_text))
            # Nom simple : On teste si l'include existe dans le meme rep
            if not path.exists(file_to_open):
                # Introuvable dans le repertoire courant -> on utilise le repertoire par defaut
                file_to_open = path.normpath(path.join(options.default_path, input_text))
        else:
            file_to_open = path.normpath(input_text)
        
        editor_exec = options.editor_path + "\EditPadPro7.exe"
        epp.log("exec : %s %s" % (editor_exec, file_to_open))
        
        if path.exists(file_to_open):
            file_to_open = '"' + file_to_open + '"'
            pid = os.spawnl(os.P_NOWAIT, editor_exec, '/newinstance', file_to_open)
            epp.log("Ok! (%d)" % pid)
        else:
            epp.err('Fichier "%s" introuvable' % file_to_open)
            sys.exit(2)
        
    else: 
        # Provoquer une erreur
        parser.print_help()
        sys.exit(1)
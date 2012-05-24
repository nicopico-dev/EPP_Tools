# python autocomplete.py -f "%TEMPFILE%" -l %LINE% -w 20 -c %POS% --language LANGAGE

# TODO 
# - Optimiser (suite au dernieres améliorations, le programme est devenu plus lent: 1s-2s d'attente)
# - Simuler une fenêtre modeless ?
# - Dans la liste de mots, si l'utilisateur tape un caractère autre qu'un séparateur, l'ajouter au mot recherché (style téléphone portable)

DEBUG_FILE = False

import sys
import string
import optparse

if DEBUG_FILE:
    import os
    import distutils.file_util
        
import epp_utils as epp
import autocomplete_library as ac

from TkWordsList import TkWordsList

def choix_liste_mots(search, lang_words, file_words):
    form = TkWordsList(None, "AutoComplete", 300, 300)
    form.add_words(sorted(lang_words))
    form.add_words(sorted(file_words), True)
    
    form.select_word('----')
    #form.setAlwaysOnTop(True)
    form.mainloop()
    
    return form.choix
    
def main(argv):
    parser = optparse.OptionParser()
    parser.add_option("-c","--cursor",action="store",type="int",dest="cursor",help="Cursor position in file (byte)")
    parser.add_option("-f","--fileName",action="store",type="string",dest="filename",help="File to parse")
    parser.add_option("-l","--currLine",action="store",type="int",dest="currline",help="Current line in the file")
    parser.add_option("-t","--type",action="store",type="string",dest="type",help="File type (extension without dot)")
    parser.add_option("-w","--width",action="store",type="int",dest="width",help="How many lines to scan above and below the current line. 0 -> whole file (Optional)")
    parser.add_option("--language",action="store",type="string",dest="language",help="The language file to use to get keywords (Optional)")
    
    parser.set_defaults(width=0)
    
    (options, args) = parser.parse_args(argv)
    
    epp.log("cursor:%s, currLine:%s, width:%s" % (options.cursor, options.currline, options.width))
    
    if options.filename and options.currline and options.cursor:
        epp.log(options.filename)
        
        # DEBUG Parfois le programme ne trouve pas le bon terme à chercher...
        if DEBUG_FILE:
            distutils.file_util.copy_file(options.filename, os.path.join(os.environ["TMP"], "EPP_TMP.txt"))
        
        # Check UTF8
        codecName = epp.getFileCodecName(options.filename)
        epp.log("codec detecté: %s" % codecName)
        if codecName == "utf_8":
            options.cursor += 3
        
        with open(options.filename, 'r', encoding=codecName) as fileh:
            # Recuperation des lettres precedants le curseur
            search = ac.get_search(fileh, options.cursor)
            epp.log("Search for %s...\n--------------" % search)
            
            # Taille minimum du mot de recherche
            if len(search) <= 1:
                epp.log("Search term too little, 2 letters minimum")
                sys.exit(1)
                        
            # Scan du fichier pour retrouver les candidats
            file_words = ac.get_file_words(search, fileh, options.currline, options.width)
        
        language = ac.get_language(options.language, options.type)
        if language:
            # Récupération de la liste des mots du langage
            lang_words = ac.get_language_words(search, language)
        else:
            lang_words = set()
        
        # MAJ des mots du fichier étant également des mots du language
        for wordObj in [w for w in file_words if w in lang_words]:
            wordObj.color = "blue"
        
        # on supprime les mots du langage appartenant deja au fichier (pour garder les caracteristiques du mot)
        lang_words = lang_words - file_words
        for wordObj in lang_words:
             wordObj.color = "blue"
        
        nb_words = len(lang_words) + len(file_words)
        
        # Affichage du résultat
        if nb_words == 1:
            # 1 seul candidat -> on l'utilise
            epp.write(ac.get_result(search, (lang_words | file_words).pop()))
        elif nb_words > 1:
            # Plusieurs candidats : Affichage des candidats
            choix = choix_liste_mots(search, lang_words, file_words)
            if choix != None:
                epp.write(ac.get_result(search, choix))
        else:
            # Aucun candidat 
            #import winsound
            #winsound.MessageBeep(winsound.MB_ICONEXCLAMATION);
            epp.log("Aucun candidat trouve")
            # Ajout d'un espace pour montrer que rien n'a été trouvé
            epp.write(' ')
            
        sys.exit()
        
    else: 
        # On provoque une erreur
        if not options.filename:
            parser.error("filename") 
        elif not options.currline:
            parser.error("currline") 
        elif not options.cursor:
            parser.error("cursor") 
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])

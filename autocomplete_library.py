import sys
import re
import itertools
import os.path as path

import epp_utils as epp
import Candidate

def get_regex(search):
    # TODO Problème sur les caractères accentués
    # Echappement des caractères particulier regex 
    search = re.escape(search)
    
    # ((?<=[\W\s])search\w+|^search\w+)
	# 
	# Match the regular expression below and capture its match into backreference number 1 «((?<=[\W\s])search\w+|^search\w+)»
	#    Match either the regular expression below (attempting the next alternative only if this one fails) «(?<=[\W\s])search\w+»
	#       Assert that the regex below can be matched, with the match ending at this position (positive lookbehind) «(?<=[\W\s])»
	#          Match a single character present in the list below «[\W\s]»
	#             Any character that is NOT a word character «\W»
	#             A whitespace character (spaces, tabs, line breaks, etc.) «\s»
	#       Match the characters “search” literally «search»
	#       Match a single character that is a “word character” (letters, digits, etc.) «\w+»
	#          Between one and unlimited times, as many times as possible, giving back as needed (greedy) «+»
	#    Or match regular expression number 2 below (the entire group fails if this one fails to match) «^search\w+»
	#       Assert position at the beginning of the string «^»
	#       Match the characters “search” literally «search»
	#       Match a single character that is a “word character” (letters, digits, etc.) «\w+»
	#          Between one and unlimited times, as many times as possible, giving back as needed (greedy) «+»
    pattern = r"((?<=[\W\s])%(1)s\w+|^%(1)s\w+)" % {"1":search}
    
    return re.compile(pattern)

def get_search(fileh, pos):
    # TODO La methode boggue parfois, et ne renvoie pas toutes les lettres (espaces à la place)...
    # Verification de l'encodage    
    epp.log("pos : %d" % pos)
    
    search = ""
    
    f_tell = fileh.tell
    f_read = fileh.read
    f_seek = fileh.seek
    
    # On recule de 1 caractères par rapport à la position d'origine
    seek_pos = f_seek(pos - 1)
    
    while seek_pos >= 0:
        f_seek(seek_pos)
        char = f_read(1)
        
        epp.log(char)
        if char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$@_":
            search = char + search
            # on recule de 1 caractère
            seek_pos = seek_pos - 1
        else:
            epp.log("!")
            break
    
    return search

def get_language(forced_language, filetype):
    if forced_language != None:
        epp.log("Use options.language: {0}".format(forced_language))
        return forced_language
    else:
        epp.log("Scan filetypes for extensions {0}".format(filetype))
        language = None
        
    config_file = path.join(epp.getcwd(), "language_words", "filetypes.txt")
    
    if filetype != '' and path.exists(config_file):
        r = re.compile(r"^(?:\w+;)*{0}\S*\t(?P<language>\w+)".format(filetype), re.IGNORECASE)
        
        with open(config_file, "r") as f:
            for l in f:
                match = r.search(l)
                if match:
                	language = match.group("language")
                	epp.log("language found: {0}".format(language))
                	break
    return language
        

def get_language_words(search, language):
    # Retourne la liste des mots candidat correspondant au langage
    # Les mots sont stockés dans un fichier de ce type : ./language_words/[language].words
    language_file = path.join(epp.getcwd(), "language_words", language + ".words")
    
    if path.exists(language_file):
        epp.log("language file Ok : %s" % language_file)
        candidates = Candidate.Candidates()
        r1 = get_regex(search)
        
        # Parcours du fichier du langage pour trouver les candidats
        with open(language_file, "r") as fileh:
            for match in [r1.findall(l) for l in fileh]:
                candidates.extend(match, is_language_word=True)
        
        return set(candidates.get_list())
    else:
        return set()

def get_file_words(search, fileh, refline, width):
    # On recherche les mots du fichier commencant par les lettres choisies
    # dans les lignes de fichiers entourant la ligne courante (refline)
    #     "width" lignes au dessus + "width" lignes en dessous
    
    r1 = get_regex(search)
    fileh.seek(0)
    
    # On utilise un set pour n'obtenir qu'une fois chaque candidat
    candidates = Candidate.Candidates(Candidate.ProximitySorted)
    
    if width > 0:
        # Limite la recherche a [width] lignes au dessus et [width] lignes en dessous
        search_lines = itertools.islice(fileh, max([0, refline-width]), refline+width+1)
        distance = max([0, refline-width])
    else:
        search_lines = fileh
        distance = -refline
    
    # distance = curr_ligne - ref_ligne -> negative avant, positive apres
    
    #for match in [r1.findall(l) for l in search_lines]:
    for l in search_lines:
        matches = r1.findall(l)
        candidates.extend(matches, proximity=abs(distance))
        distance += 1
        
    return set(candidates.get_list())
    
def get_result(search, selection):
    # On ne retourne que les caractères manquants (à droite du texte de recherche)
    return getattr(selection, "word", selection)[len(search):]


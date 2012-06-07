import sys
import re
import os
import os.path
import fnmatch
import subprocess

#import pprint
#pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)

# IMPORTANT
# Python 3.0 "plante" sys si on essaye d'ecrire dans un flux qui n'existe pas :
#   Si la sortie d'erreur est désactivée dans EPP et que l'on tente d'ecrire dessus, 
#   les sorties standards ne s'afficheront plus.
# => Test de l'existence du flux avant écriture

def readline():
    if sys.stdin != None:
        return sys.stdin.readline().rstrip('\x1a')
    else:
        return ""

def print(message):
    if sys.stdout != None:
        sys.stdout.write(str(message))
        sys.stdout.write('\n')

def write(message):
    if sys.stdout != None:
        sys.stdout.write(str(message))

def log(message):
    if sys.stderr != None:
        sys.stderr.write('|| ')
        sys.stderr.write(str(message))
        sys.stderr.write('\n')

def err(message):
    if sys.stderr != None:
        sys.stderr.write('## ')
        sys.stderr.write(str(message))
        sys.stderr.write('\n')
    else:
        # TODO Better display alert box (without empty tkinter window)
        from tkinter import messagebox
        messagebox.showwarning("Error", str(message))

def getcwd():
    """
    Retourne le répertoire du script principal
    """
    return sys.path[0]
    
def getProjectFiles(epp_file):
    """
    Parse le fichier epp passé en parametre et retourne la liste des fichiers qu'il contient
    """
    with open(epp_file, 'r') as file:
        return [f.replace('Filename=', '').strip() for f in file if f.startswith('Filename=')]

def getFilesInTree(basedir, fileMask=None):
    """
    Retourne la liste des fichiers contenus dans un répertoire et ses sous-répertoires, en limitant optionnellement par un filemask (expression régulière)
    """
    filesList = []
    for root, dirs, files in os.walk(basedir):
        if ".svn" in dirs:
            dirs.remove(".svn")
        if fileMask == None:
            filesList += [os.path.join(root, f) for f in files]
        else:
            filesList += [os.path.join(root, f) for f in fnmatch.filter(files, fileMask)]
    return filesList

class Struct(object):
    """
    Classe bidon pour faire des structures de données à la volée
    """
    def __init__(self, **attrs):
        if attrs == None:
            attrs = {}
        for (attr, value) in attrs.items():
            setattr(self, attr, value)
            
    def __repr__(self):
        str = ''
        for (item, value) in self.__dict__.items():
            if str != '': str +=', '
            str += "%s='%s'" % (item, value)
        str = '(' + str + ')'
        return str
        
def getFileCodecName(filename):
    """
    Renvoie le nom du codec à utiliser pour lire le fichier
    """
    # Lecture des 4 premiers octets pour déterminer l'encodage
    with open(filename, "rb") as file:
        data = file.read(4)
        
        # From Mark Pilgrim port to Python of Mozilla Universal charset detector by Shy Shalom
        # If the data starts with BOM, we know it is UTF
        # TODO Verifier les noms des codecs pour autre que utf_8
        if data[:3] == b"\xEF\xBB\xBF":
            # EF BB BF  UTF-8 with BOM
            return "utf_8"
        elif data[:4] == b"\xFF\xFE\x00\x00":
            # FF FE 00 00  UTF-32, little-endian BOM
            return "utf_32"
        elif data[:4] == b"\x00\x00\xFE\xFF": 
            # 00 00 FE FF  UTF-32, big-endian BOM
            return "utf_32"
        elif data[:4] == b"\xFE\xFF\x00\x00":
            # FE FF 00 00  UCS-4, unusual octet order BOM (3412)
            return "ucs_4"
        elif data[:4] == b"\x00\x00\xFF\xFE":
            # 00 00 FF FE  UCS-4, unusual octet order BOM (2143)
            return "ucs_4"
        elif data[:2] == b"\xFF\xFE":
            # FF FE  UTF-16, little endian BOM
            return "utf_16"
        elif data[:2] == b"\xFE\xFF":
            # FE FF  UTF-16, big endian BOM
            return "utf_16"
            
        # None : platform dependant -> cp1252 pour windows
        return None
        
def getCurrWord(filename, pos):
    """
    Retourne le mot du fichier filename positionné à l'octet pos (Utile avec EditPad POS variable)
    """
    # Check UTF8
    codecName = getFileCodecName(filename)
    if codecName == "utf_8":
        pos += 3
            
    with open(filename, 'r',encoding=codecName) as f:
        # Recuperation du mot courant
        seek_pos = f.seek(pos - 1)
        
        while seek_pos >= 0:
            char = f.read(1)
            if not re.match(r"\w", char):
                break
            else:
                seek_pos = seek_pos - 1
                f.seek(seek_pos)
                
        m = re.match(r"^(\w+)", f.read())
        
        if m:
            curr_word = m.group(1)
        else:
            curr_word = ""
        
        return curr_word
        
def getFileTags(filename):
    """
    Retourne les tags associés au fichier en fonction de son nom (Exemple: language utilisé, etc.)
    """
    # TODO Utiliser un fichier de regle XML ?
    tags = set()
    log(filename)
    
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in (".cfm", ".cfc"):
        tags.add("coldfusion")
    if ext in (".htm", ".html"):
        tags.add("html")
    if ext in (".py", ".pyw"):
        tags.add("python")
        
    return tags
    
def openWithEPP(filename):
    """
    Ouvre le fichier specifie dans EditPad
    """
    tools_path = os.path.dirname(os.path.realpath(__file__))
    epp_path = os.path.normpath(os.path.join(tools_path, ".."))
    epp_exe = os.path.join(epp_path, "EditPadPro7.exe")
    subprocess.call([epp_exe, filename])

if __name__ == "__main__":
    openWithEPP(r"F:\WORK\CROSS\Stryker_eNews\Maquettes\login.html")
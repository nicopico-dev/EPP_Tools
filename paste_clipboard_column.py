import sys
import win32clipboard as w

import epp_utils as epp

if __name__ == "__main__":
    # TODO Gérer les différents encodage de chaîne
    w.OpenClipboard()
    clipboardText = w.GetClipboardData()
    w.CloseClipboard()
    
    # TODO Prendre en compte le type de saut de ligne
    newLine = '\n'
    
    lines = clipboardText.splitlines()
    
    for l in lines:
        epp.write(l + newLine)
# Tidy SQL
# by Nicolas PICON
# October, 2008

import sys
import re
import optparse

import epp_utils as epp

__version__='0.2'

def getFirstWord(chaine):
    if chaine.strip() != '':
        return chaine.split(None, 1)[0]
    else:
        return ''

def aloner(x):
    return '^' + x + r'\b|\b' + x + r'\b|\b' + x + '$'

def splitter(chaine, separators):
    patternSep = '|'.join([aloner(x) for x in separators if x != ','])
    if ',' in separators:
        patternSep = ',|' + patternSep
    
    preSplit = re.split('(?i)('+patternSep+')', chaine)
    return [x for x in preSplit if x.strip() != '']

def justify(chaine, width):
    return chaine.rjust(width)

def normalizeOperators(chaine):
    # -> DESACTIVEE <-
    # TODO Ne doit pas traiter les operateurs inclus dans une chaine
    # TODO Probleme pour les operateurs composes (exp: != )
    return chaine
    
    operators = ('/', '\+', '\*', '-', '\!=', '=')
    chaineNorm = chaine

    for patternOp in [r'\s*(' + x + r')\s*' for x in operators]:
        chaineNorm = re.sub(patternOp, r' \1 ', chaineNorm)

    return chaineNorm

def normalizeSection(section, NL, MAX_WIDTH):
    firstWord = getFirstWord(section)
    typeSection = firstWord.upper()
    
    # Aligement a utiliser
    def align(chaine): return justify(chaine, len('SELECT'))

    # Separateurs selon le type de section
    if typeSection in ('SELECT', 'GROUP', 'ORDER'):
        sep = (',', 'CASE WHEN', 'THEN', 'ELSE', 'END', 'INTO')
        deindentSub = False
    elif typeSection == 'FROM':
        sep = (',', 'LEFT JOIN', 'LEFT OUTER JOIN', 'RIGHT JOIN', 'INNER JOIN', 'JOIN', 'ON', 'AND', 'OR')
        deindentSub = True
    elif typeSection in ('WHERE', 'HAVING'):
        sep = ('AND', 'OR')
        deindentSub = True
    else:
        return section

    # Recupere les elements (tokens) de la section
    tokens = [x.strip() for x in splitter(section, sep)]
    
    # Alignement du 1er element
    tokens[0] = tokens[0].replace(firstWord, align(firstWord))

    sectionNorm = ''
    currLine = ''
    indentNext = False

    for element in tokens:
        # La virgule est un separateur speciale (sauf pour SELECT où on saute une ligne apres chaque virgule)
        if indentNext or (element.strip() != ',' and (len(currLine) > MAX_WIDTH or element.upper() in sep)):
            indentNext = False
            sectionNorm += currLine + NL
            currLine = ''
            
            if element.upper() in sep and deindentSub:
                if element.count(' ') > 0:
                    # Multi-words
                    element_split = element.split(None, 1)
                    element = align(element_split[0]) + ' ' + element_split[1]
                else:
                    # Mono-word
                    element = align(element)
            else:
                # Tabulation de section
                currLine = align(' ') + ' '
            
            # Ajout d'un espace, sauf pour si le token suivant est la virgule qui doit etre coller
            #if tokens(??).strip() != ',':
            element += ' '
            
        elif element.strip() == ',':
            element = ', '
            if typeSection == 'SELECT':
                indentNext = True
            
        currLine += element
        
    if currLine.strip() != '':
        sectionNorm += currLine
        
    sectionNorm = sectionNorm.replace(' , ', ', ')
    return sectionNorm

def tidySQL(sql, uppercase):
    #TODO Detecter le format
    NL = '\n'
    MAX_WIDTH = 80

    # Suppression des sauts de lignes existants
    sqlNorm = sql.replace(NL, ' ')
    
    # Suppression des espaces en trop
    sqlNorm = re.sub(r"\s{2,}", " ", sqlNorm)

    kwSQL = ('SELECT', 'AS', 'CASE WHEN', 'THEN', 'ELSE', 'END', 'INTO', 'FROM', 'LEFT JOIN', 'RIGHT JOIN', 'JOIN', 'ON', 'WHERE', 'AND', 'OR', 'LIKE', 'GROUP BY', 'HAVING', 'ORDER BY', 'UNION')
    kwNewSection = ('SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY', 'UNION')
    
    for word in kwSQL:
        if uppercase:
            wordNormalized = word.upper()
        else:
            wordNormalized = word.lower()
            
        if word.upper() in kwNewSection:
            wordNormalized = NL + wordNormalized
            
        sqlNorm = re.sub('(?i)' + aloner(word), wordNormalized, sqlNorm)

    epp.log(sqlNorm)
    sqlNorm = normalizeOperators(sqlNorm)
    epp.log ('-----')
    epp.log(sqlNorm)

    sections = sqlNorm.splitlines()
    sectionsNorm = list()

    for section in [e for e in sections if e != '' ]:
        sectionNorm = normalizeSection(section, NL, MAX_WIDTH)
        sectionsNorm.append(sectionNorm)

    return NL.join(sectionsNorm)

if __name__=='__main__':
    parser = optparse.OptionParser()
    parser.add_option("-f","--fileName",action="store",type="string",dest="filename",help="SQL file to beautify")
    parser.add_option("-u","--uppercase",action="store_true",dest="uppercase",default=False,help="Change keyword to uppercase")

    (options, args) = parser.parse_args()

    if options.filename:
        epp.err('not implemented yet')
    else:
        rawSQL = sys.stdin.read()
        epp.write(tidySQL(rawSQL, options.uppercase))
    sys.exit(0)
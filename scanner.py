# http://jason.diamond.name/weblog/2005/04/26/lexical-analysis-python-style

import re

class Tokenizer:

    tokenizerRE = re.compile(r'''
       (?P<SPACE>    \s+            ) |
       (?P<LEFT>     \(             ) |
       (?P<RIGHT>    \)             ) |
       (?P<NUMBER>   \d+            ) |
       (?P<VAR>      \$[_a-zA-Z]\w* ) |
       (?P<OPERATOR> [-+*/]         )
    ''', re.MULTILINE | re.VERBOSE)

    def __init__(self):
        self.source = ''
        self.pos = 0
        self.len = 0

    def scan(self, source):
        self.source = source
        self.pos = 0
        self.len = len(source)
        try:
            while True:
                if self.pos >= self.len:
                    break
                m = self.tokenizerRE.match(self.source, self.pos)
                if m is None:
                    raise Exception('invalid token')
                self.pos = m.end()
                token_type = m.lastgroup
                if token_type != 'SPACE':
                    token = m.group(token_type)
                    if token_type == 'NUMBER':
                        token = int(token)
                    elif token_type == 'VAR':
                        token = token[1:]
                    yield token_type, token
        finally:
            pass
                
                
tokenizer = Tokenizer()
for token in tokenizer.scan("45+23*(56-6*$x)"):
    print(token)

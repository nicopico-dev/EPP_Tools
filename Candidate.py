# TODO Changer l'architecture pour permettre de changer le tri de la liste à la volée
import epp_utils as epp 

class Candidates(object):
    def __init__(self, candidateClass=None):
        self.candidates = {}
        if candidateClass == None:
            candidateClass = _Candidate
        self.candidateClass = candidateClass
        
    def __iter__(self):
        return iter(self.candidates.items())
            
    def __len__(self):
        return len(self.candidates)
        
    def add(self, word, **caracts):
        if word not in self.candidates:
            self.candidates[word] = self.candidateClass(word, **caracts)
        else:
            self.candidates[word].newOccurence(**caracts)
            
    def extend(self, words, **caracts):
        for w in words:
            self.add(w, **caracts)
            
    def get_list(self, orders=None):
        return list(self.candidates.values())
    
class _Candidate(object):
    def __init__(self, word, **caracts):
        self.word = word
        
        # Valeurs par defaut
        self.frequency = 1
        self.proximity = 0
        self.is_language_word = False
        
        # Recuperation des caracteristiques
        if 'proximity' in caracts:
            self.proximity = caracts['proximity']
        if 'is_language_word' in caracts:
            self.is_language_word = caracts['is_language_word']
        
    def __hash__(self):
        return hash(self.word)
        
    def __eq__(self, other):
        if other is None:
            return False
        return self.word == other.word
        
    def __lt__(self, other):
        if other is None:
            return False
        
        if hasattr(other, 'word'): 
            return (self.word < other.word)
        else:
            raise(TypeError)
        
    def __repr__(self):
        return "%s [f:%d, p:%d]" % (self.word, self.frequency, self.proximity)
        
    def __str__(self):
        return self.word
    
    def newOccurence(self, **caracts):
        self.frequency += 1
        
        # MAJ des caracteristiques
        if 'proximity' in caracts:
            self.proximity = min(self.proximity, caracts['proximity'])
            
    @property
    def string(self):
        return self.word
        
    @property
    def infos(self):
        return "f:%d, p:%d" % (self.frequency, self.proximity)

class ProximitySorted(_Candidate):        
    def __lt__(self, other):
        if hasattr(other, 'word') and hasattr(other, 'proximity'):
            if self.word == other.word: 
                return False
            elif self.proximity != other.proximity:
                return (self.proximity < other.proximity)
        return (super(ProximitySorted, self)).__lt__(other)
        
if __name__ == "__main__":
    test = _Candidate('truc', proximity=30)
    epp.print(test)
    
    test = ProximitySorted('truc', proximity=30)
    epp.print(test)

    essai = Candidates(ProximitySorted)
    essai.add('truc', proximity=30)
    essai.add('tast', proximity=50)
    epp.print(repr(essai.get_list()))
    
    essai.add('tast', proximity=20)
    essai.add('tfst', proximity=15)
    epp.print(repr(essai.get_list()))
    epp.print(repr(sorted(set(essai.get_list()))))
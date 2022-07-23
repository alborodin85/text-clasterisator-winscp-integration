import pandas
from nltk.corpus import wordnet
import numpy as np

class Synonymizer:

    def __init__(self):
        self.thesaurus = {}
        self.countReplacements = 0

    def getMainSynonym(self, word: str) -> str:
        for dictItem in self.thesaurus.items():
            if word in dictItem[1]:
                word = dictItem[0]
                self.countReplacements += 1
                return word

        synsets = wordnet.synsets(word)
        lemmas = [synset.lemmas() for synset in synsets]
        sinonyms = [[lemma.name() for lemma in synset] for synset in lemmas]
        sinonymsFlat = []
        for lemmaList in sinonyms:
            for lemmaWord in lemmaList:
                sinonymsFlat.append(lemmaWord)

        self.thesaurus[word] = sinonymsFlat

        return word

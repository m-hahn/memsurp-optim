import os
import random
import sys

header = ["index", "word", "lemma", "posUni", "posFine", "morph", "head", "dep", "_", "_"]


from corpusIterator_V import CorpusIterator_V as CorpusIterator


class CorpusIterator_Adap_V():
   def __init__(self, language, partition="train", storeMorph=False, splitLemmas=False, shuffleData=True):
      self.basis_train =list(CorpusIterator(language, partition="train", storeMorph=storeMorph, splitLemmas=splitLemmas, shuffleData=False, shuffleDataSeed=5, errorWhenEmpty=False).iterator(rejectShortSentences=False))
      self.basis_dev = list(CorpusIterator(language, partition="dev", storeMorph=storeMorph, splitLemmas=splitLemmas, shuffleData=False, shuffleDataSeed=5, errorWhenEmpty=False).iterator(rejectShortSentences=False))
      self.basis_test = list(CorpusIterator(language, partition="test", storeMorph=storeMorph, splitLemmas=splitLemmas, shuffleData=False, shuffleDataSeed=5, errorWhenEmpty=False).iterator(rejectShortSentences=False))
      self.basis = self.basis_train + self.basis_dev + self.basis_test
      random.Random(5).shuffle(self.basis)
      DEV_SIZE = max(100, int(0.05*len(self.basis)))
      if partition == "dev":
          self.basis = self.basis[:DEV_SIZE]
      else:
          self.basis = self.basis[DEV_SIZE:]
   def iterator(self, rejectShortSentences = False):
     for sentence in self.basis:
         yield sentence



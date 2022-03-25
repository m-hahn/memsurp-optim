import os
import random
#import accessISWOCData
#import accessTOROTData
import sys

header = ["index", "word", "lemma", "posUni", "posFine", "morph", "head", "dep", "_", "_"]


def readUDCorpus(language, partition, ignoreCorporaWithoutWords=True):
      assert partition == "together"
      l = language.split("_")
      #language = "_".join(l[:-1])
      #version = l[-1]
      #print(l, language)
      basePath = "/u/scr/mhahn/"
      files = os.listdir(basePath)
      files = list(filter(lambda x:x.startswith("UD_"+language.replace("-Adap", "")), files))
      print >> sys.stderr, ("FILES", files, language)
      data = []
      for name in files:
        if "Sign" in name:
           print >> sys.stderr, ("Skipping "+name)
           continue
        assert ("Sign" not in name)
        if "Chinese-CFL" in name or "English-ESL" in name or "Hindi_English" in name or "French-FQB" in name or "Latin-ITTB" in name or "Latin-LLCT" in name or "English-Pronouns" in name or "English-GUMReddit" in name:
           print >> sys.stderr, ("Skipping "+name)
           continue
        suffix = name[len("UD_"+language):]
        if name == "UD_French-FTB":
            subDirectory = "/u/scr/mhahn/corpus-temp/UD_French-FTB/"
        else:
            subDirectory =basePath+"/"+name
        subDirFiles = os.listdir(subDirectory)
        partitionHere = partition
            
        candidates = list(filter(lambda x:"-ud-" in x and x.endswith(".conllu"), subDirFiles))
#        print >> sys.stderr, ("SUBDIR FILES", subDirFiles)

        print >> sys.stderr, candidates
        assert len(candidates) >= 1, candidates
        for cand in candidates:
           try:
              dataPath = subDirectory+"/"+cand
              with open(dataPath, "r") as inFile:
                 newData = inFile.read().strip().split("\n\n")
                 assert len(newData) > 1
                 data = data + newData
           except IOError:
              print >> sys.stderr, ("Did not find "+dataPath)

      assert len(data) > 0, (language, partition, files)


      print >> sys.stderr, ("Read "+str(len(data))+ " sentences from "+str(len(files))+" "+partition+" datasets. "+str(files)+"   "+basePath)
      return data

class CorpusIterator_V():
   def __init__(self, language, partition="together", storeMorph=False, splitLemmas=False, shuffleData=True, shuffleDataSeed=None, splitWords=False, ignoreCorporaWithoutWords=True):
      print >> sys.stderr, ("LANGUAGE", language)
      if splitLemmas:
           assert language == "Korean"
      self.splitLemmas = splitLemmas
      self.splitWords = splitWords
      assert self.splitWords == (language == "BKTreebank_Vietnamese")

      self.storeMorph = storeMorph
      data = readUDCorpus(language, partition, ignoreCorporaWithoutWords=ignoreCorporaWithoutWords)
      if shuffleData:
       if shuffleDataSeed is None:
         random.shuffle(data)
       else:
         random.Random(shuffleDataSeed).shuffle(data)

      self.data = data
      self.partition = partition
      self.language = language
      assert len(data) > 0, (language, partition)
   def permute(self):
      random.shuffle(self.data)
   def length(self):
      return len(self.data)
   def processSentence(self, sentence):
        sentence = list(map(lambda x:x.split("\t"), sentence.split("\n")))
        result = []
        metadata = {}
        for i in range(len(sentence)):
#           print sentence[i]
           if sentence[i][0].startswith("#"):
              posEq = sentence[i][0].index(" = ")
              key = sentence[i][0][2:posEq]
              value = sentence[i][0][posEq+3:]
              metadata[key] = value
              continue
           if "-" in sentence[i][0]: # if it is NUM-NUM
              continue
           if "." in sentence[i][0]:
              continue
           sentence[i] = dict([(y, sentence[i][x]) for x, y in enumerate(header)])
           sentence[i]["head"] = int(sentence[i]["head"])
           sentence[i]["index"] = int(sentence[i]["index"])
           sentence[i]["word"] = sentence[i]["word"].lower()
           if self.language == "Thai-Adap":
              assert sentence[i]["lemma"] == "_"
              sentence[i]["lemma"] = sentence[i]["word"]
           if "ISWOC" in self.language or "TOROT" in self.language:
              if sentence[i]["head"] == 0:
                  sentence[i]["dep"] = "root"

           if self.splitLemmas:
              sentence[i]["lemmas"] = sentence[i]["lemma"].split("+")

           if self.storeMorph:
              sentence[i]["morph"] = sentence[i]["morph"].split("|")

           if self.splitWords:
              sentence[i]["words"] = sentence[i]["word"].split("_")


           sentence[i]["dep"] = sentence[i]["dep"].lower()
           if self.language == "LDC2012T05" and sentence[i]["dep"] == "hed":
              sentence[i]["dep"] = "root"
           if self.language == "LDC2012T05" and sentence[i]["dep"] == "wp":
              sentence[i]["dep"] = "punct"

           sentence[i]["coarse_dep"] = sentence[i]["dep"].split(":")[0]



           result.append(sentence[i])
 #          print sentence[i]
        return (result, metadata)
   def getSentence(self, index):
      result = self.processSentence(self.data[index])
      return result
   def iterator(self, rejectShortSentences = False):
     for sentence in self.data:
        if len(sentence) < 3 and rejectShortSentences:
           continue
        yield self.processSentence(sentence)



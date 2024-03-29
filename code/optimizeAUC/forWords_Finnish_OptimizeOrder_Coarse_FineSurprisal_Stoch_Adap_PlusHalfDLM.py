# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys
from estimateTradeoffHeldout import calculateMemorySurprisalTradeoff

objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str)
parser.add_argument("--model", dest="model", type=str)
parser.add_argument("--alpha", dest="alpha", type=float, default=1.0)
parser.add_argument("--gamma", dest="gamma", type=int, default=1)
parser.add_argument("--delta", dest="delta", type=float, default=1.0)
parser.add_argument("--cutoff", dest="cutoff", type=int, default=2)
parser.add_argument("--idForProcess", dest="idForProcess", type=int, default=random.randint(0,10000000))



args=parser.parse_args()


myID = random.randint(0,10000000)



posUni = set()
posFine = set() 
deps = ["acl", "acl:relcl", "advcl", "advmod", "amod", "appos", "aux", "auxpass", "case", "cc", "ccomp", "compound", "compound:prt", "conj", "conj:preconj", "cop", "csubj", "csubjpass", "dep", "det", "det:predet", "discourse", "dobj", "expl", "foreign", "goeswith", "iobj", "list", "mark", "mwe", "neg", "nmod", "nmod:npmod", "nmod:poss", "nmod:tmod", "nsubj", "nsubjpass", "nummod", "parataxis", "punct", "remnant", "reparandum", "root", "vocative", "xcomp"] 



from math import log, exp
from random import random, shuffle, choice

from corpusIterator_Adap_V import CorpusIterator_Adap_V as CorpusIterator

originalDistanceWeights = {}


def makeCoarse(x):
   if ":" in x:
      return x[:x.index(":")]
   return x

def initializeOrderTable():
   orderTable = {}
   keys = set()
   vocab = {}
   distanceSum = {}
   distanceCounts = {}
   depsVocab = set()
   for partition in ["train", "dev"]:
     for sentence in CorpusIterator(args.language,partition).iterator():
      for line in sentence:
          vocab[line["word"]] = vocab.get(line["word"], 0) + 1
          line["fine_dep"] = line["dep"]
          depsVocab.add(makeCoarse(line["fine_dep"]))
          posFine.add(line["posFine"])
          posUni.add(line["posUni"])
  
          if line["fine_dep"] == "root":
             continue
          posHere = line["posUni"]
          posHead = sentence[line["head"]-1]["posUni"]
          dep = line["fine_dep"]
          direction = "HD" if line["head"] < line["index"] else "DH"
          key = (posHead, dep, posHere)
          keyWithDir = (dep, direction)
          orderTable[keyWithDir] = orderTable.get(keyWithDir, 0) + 1
          keys.add(key)
          distanceCounts[key] = distanceCounts.get(key,0.0) + 1.0
          distanceSum[key] = distanceSum.get(key,0.0) + abs(line["index"] - line["head"])
   #print orderTable
   dhLogits = {}
   for key in keys:
      hd = orderTable.get((key, "HD"), 0) + 1.0
      dh = orderTable.get((key, "DH"), 0) + 1.0
      dhLogit = log(dh) - log(hd)
      dhLogits[key] = dhLogit
   return dhLogits, vocab, keys, depsVocab

import torch.nn as nn
import torch
from torch.autograd import Variable


# "linearization_logprobability"
def recursivelyLinearize(sentence, position, result, gradients_from_the_left_sum):
   line = position
   # Loop Invariant: these are the gradients relevant at everything starting at the left end of the domain of the current element

   if "children_DH" in line:
      for child in line["children_DH"]:
         recursivelyLinearize(sentence, child, result, None)
   result.append(line)
   if "children_HD" in line:
      for child in line["children_HD"]:
         recursivelyLinearize(sentence, child, result, None)
   return None

import numpy.random

softmax_layer = torch.nn.Softmax()
logsoftmax = torch.nn.LogSoftmax()



def orderChildrenRelative(sentence, remainingChildren, reverseSoftmax):
       childrenLinearized = []
       while len(remainingChildren) > 0:
           logits = torch.cat([distanceWeights[stoi_pure_deps[sentence[x-1]["dependency_key"]]].view(1) for x in remainingChildren])
           softmax = softmax_layer(logits.view(1,-1)).view(-1)
           selected = numpy.random.choice(range(0, len(remainingChildren)), p=softmax.data.numpy())
           log_probability = torch.log(softmax[selected])
           assert "linearization_logprobability" not in sentence[remainingChildren[selected]-1]
           sentence[remainingChildren[selected]-1]["linearization_logprobability"] = log_probability
           childrenLinearized.append(remainingChildren[selected])
           del remainingChildren[selected]
       if reverseSoftmax:
           childrenLinearized = childrenLinearized[::-1]
       return childrenLinearized           



def orderSentence(sentence, weights):
   printThings = (random() < 0.01)
   root = None
   logits = [None]*len(sentence)
   logProbabilityGradient = 0
   for line in sentence:
     line["children_DH"] = []
     line["children_HD"] = []
    
   for line in sentence:
      line["fine_dep"] = line["dep"]
      if line["fine_dep"] == "root":
          root = line["index"]
          continue
      if line["fine_dep"].startswith("punct"):
         continue
      dhLogit = 0
      probability = 0
      dhSampled = 0

      direction = "DH" if weights[line["coarse_dep"]] < weights["HEAD"] else "HD"
#      if printThings: 
 #        print "\t".join(map(str,["ORD", line["index"], (line["word"]+"           ")[:10], (".".join(list(key)) + "         ")[:22], line["head"], dhSampled, direction, weights[line["coarse_dep"]]    ]  ))

      headIndex = line["head"]-1
      sentence[headIndex]["children_"+direction] = (sentence[headIndex].get("children_"+direction, []) + [line])



   for line in sentence:
      if "children_DH" in line:
         line["children_DH"] = sorted(line["children_DH"], key=lambda line:weights[line["coarse_dep"]])
      if "children_HD" in line:
         line["children_HD"] = sorted(line["children_HD"], key=lambda line:weights[line["coarse_dep"]])

   
   linearized = []
   overallLogprobSum = recursivelyLinearize(sentence, sentence[root-1], linearized, Variable(torch.FloatTensor([0.0])))
   fromOriginalToNewIndex = {}
   for i in range(len(linearized)):
      fromOriginalToNewIndex[linearized[i]["index"]] = i
   dependencyLength, wordCount = 0, 0
   for i in range(len(linearized)):
      if linearized[i]["head"] == 0:
         continue
      dependencyLength += abs(i-fromOriginalToNewIndex[linearized[i]["head"]])
      assert dependencyLength > 0
      wordCount += 1
#   print(fromOriginalToNewIndex)
#   print(linearized)
   #if printThings or len(linearized) == 0:
   #  print " ".join(map(lambda x:x["word"], sentence))
   #  print " ".join(map(lambda x:x["word"], linearized))


   return linearized, dependencyLength, wordCount


dhLogits, vocab, vocab_deps, depsVocab = initializeOrderTable()

posUni = list(posUni)
itos_pos_uni = posUni
stoi_pos_uni = dict(zip(posUni, range(len(posUni))))

posFine = list(posFine)
itos_pos_ptb = posFine
stoi_pos_ptb = dict(zip(posFine, range(len(posFine))))



itos_pure_deps = sorted(list(depsVocab)) 
stoi_pure_deps = dict(zip(itos_pure_deps, range(len(itos_pure_deps))))
   


print itos_pure_deps


relevantPath = "/u/scr/mhahn/deps/DLM_MEMORY_OPTIMIZED/locality_optimized_dlm/manual_output_funchead_fine_depl/"

import os
#files = [x for x in os.listdir(relevantPath) if x.startswith(args.language+"_") and __file__ in x]
#posCount = 0
#negCount = 0
#for name in files:
#  with open(relevantPath+name, "r") as inFile:
#    for line in inFile:
#        line = line.split("\t")
#        if line[1] == "obj":
#          dhWeight = float(line[0])
#          if dhWeight < 0:
#             negCount += 1
#          elif dhWeight > 0:
#             posCount += 1
#          break
#
#print(["Neg count", negCount, "Pos count", posCount])
#
#if posCount >= 4 and negCount >= 4:
#   print("Enough models!")
#   quit()
#
dhWeights = Variable(torch.FloatTensor([0.0] * len(itos_pure_deps)), requires_grad=True)
distanceWeights = Variable(torch.FloatTensor([0.0] * len(itos_pure_deps)), requires_grad=True)
for i, key in enumerate(itos_pure_deps):
   dhLogits[key] = 0.0
   if key == "obj": 
       dhLogits[key] = (10.0 if random() > 0.5 else -10.0)

   dhWeights.data[i] = dhLogits[key]

   originalDistanceWeights[key] = 0.0 #random()  
   distanceWeights.data[i] = originalDistanceWeights[key]


data_train = list(CorpusIterator(args.language,"train", storeMorph=True).iterator(rejectShortSentences = False))
data_dev = list(CorpusIterator(args.language,"dev", storeMorph=True).iterator(rejectShortSentences = False))
#print(len(data_train), len(data_dev))
#quit()


words = []

affixFrequency = {}

print(itos_pure_deps)
itos_pure_deps = sorted(list(itos_pure_deps) + ["HEAD"])
stoi_pure_deps = dict(list(zip(itos_pure_deps, range(len(itos_pure_deps)))))

itos_pure_deps_ = itos_pure_deps[::]
shuffle(itos_pure_deps_)
weights = dict(list(zip(itos_pure_deps_, [2*x for x in range(len(itos_pure_deps_))]))) # abstract slot

def calculateTradeoffForWeights(weights):
    # Order the datasets based on the given weights
    train = []
    dev = []
    totalDependencyLength = 0.0
    totalWordCount = 0.0
    for data, processed in [(data_train, train), (data_dev, dev)]:
      for sentence in data:
         linearized, dependencyLength, wordCount = orderSentence(sentence, weights)
         assert dependencyLength+1 >= wordCount, (dependencyLength, wordCount)
         totalDependencyLength += dependencyLength
         totalWordCount += wordCount
         for word in linearized:
            processed.append(word["word"])
#            assert word["word"] != "_", " ".join([x["word"] for x in linearized])
         processed.append("EOS")
         for _ in range(args.cutoff+2):
           processed.append("PAD")
         processed.append("SOS")
 #   print(processed[:100])
#    quit()
    #print(train[:50])
    #print(dev[:50])
    auc, devSurprisalTable = calculateMemorySurprisalTradeoff(train, dev, args)
    print("VALUES", auc, totalDependencyLength/totalWordCount)
    overallObjective = auc + 0.5*totalDependencyLength/totalWordCount
    return overallObjective, devSurprisalTable, totalDependencyLength/totalWordCount
   
bestObjectiveSoFar = 1e100
import os
lastUpdated = 0
for iteration in range(10000):
  # Randomly select a morpheme whose position to update
  coordinate = "root"
  while coordinate == "root":
     coordinate=choice(itos_pure_deps)

  # This will store the minimal Objective found so far and the corresponding position
  mostCorrectValue = weights[coordinate]

  # Iterate over possible new positions
  for newValue in [choice([-1] + [2*x+1 for x in range(len(itos_pure_deps))])]:
     if random() > 0.5:
        continue
     print("Iteration", iteration, newValue, "best Objective so far:", bestObjectiveSoFar, coordinate, args, lastUpdated, __file__)
     # Updated weights, assuming the selected morpheme is moved to the position indicated by `newValue`.
     weights_ = {x : y if x != coordinate else newValue for x, y in weights.items()}

     # Calculate Objective for this updated assignment
     resultingObjective, _, _ = calculateTradeoffForWeights(weights_)

     # Update variables if Objective is smaller than minimum Objective found so far
     if resultingObjective < bestObjectiveSoFar:
        mostCorrectValue = newValue
        bestObjectiveSoFar = resultingObjective
        lastUpdated = iteration
#  assert bestObjectiveSoFar < 1e99
  print(iteration, bestObjectiveSoFar)
  weights[coordinate] = mostCorrectValue
  itos_pure_deps_ = sorted(itos_pure_deps, key=lambda x:weights[x])
  weights = dict(list(zip(itos_pure_deps_, [2*x for x in range(len(itos_pure_deps_))])))
 # print(weights)
  if iteration == lastUpdated:
    for x in itos_pure_deps_:
      print("\t".join([str(y) for y in [x, weights[x]]]))
  if (iteration + 1) % 500 == 0: # and iteration-lastUpdated <= 100:
     _, surprisals, dependencyLength = calculateTradeoffForWeights(weights_)

#     if os.path.exists(TARGET_DIR):
#       pass
#     else:
#       os.makedirs(TARGET_DIR)
     TARGET_DIR = "/u/scr/mhahn/deps/hillclimbing-auc-halfdlm/"
     with open(TARGET_DIR+"/optimized_"+args.language+"_"+__file__+"_"+str(myID)+".tsv", "w") as outFile:
        print >> outFile, (iteration, lastUpdated, bestObjectiveSoFar, str(args), surprisals, dependencyLength)
        for key in itos_pure_deps_:
          print >> outFile, (key+"\t"+str(weights[key]))
     if iteration - lastUpdated > 2000:
        break  




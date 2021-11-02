# based on yWithMorphologySequentialStreamDropoutDev_Ngrams_Log.py

import random
import sys
from estimateTradeoffHeldout import calculateMemorySurprisalTradeoff

objectiveName = "LM"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--language", dest="language", type=str)
parser.add_argument("--group", dest="group", type=str)
parser.add_argument("--model", dest="model", type=str)
parser.add_argument("--alpha", dest="alpha", type=float, default=1.0)
parser.add_argument("--gamma", dest="gamma", type=int, default=1)
parser.add_argument("--delta", dest="delta", type=float, default=1.0)
parser.add_argument("--cutoff", dest="cutoff", type=int, default=2)
parser.add_argument("--idForProcess", dest="idForProcess", type=int, default=random.randint(0,10000000))



args=parser.parse_args()





import glob
if args.group.startswith("DLM_MEMORY_OPTIMIZED"): # == "DLM_MEMORY_OPTIMIZED/locality_optimized_dlm/manual_output_funchead_fine_depl_nopos":
 assert "nopos" in args.group
 with open("output/"+__file__+".tsv", "a") as outFile:
  with open(glob.glob("/u/scr/mhahn/deps/"+args.group+"/*.py_model_"+args.model+".tsv")[0], "r") as inFile:
   header = next(inFile).strip().split("\t")
   assert header == ["DH_Weight", "CoarseDependency", "HeadPOS", "DependentPOS", "DistanceWeight", "Language", "FileName"], header
   for line in inFile:
      line = line.strip().split("\t")
      line = [line[0], line[1], line[4], line[5].strip().replace("_2.6", "_2.8").replace("_2.7", "_2.8"), line[6]]
      print("\t".join([str(q) for q in line]), file=outFile)
else:
 assert False


import os
import sys

#group = sys.argv[1]

group = "DLM_MEMORY_OPTIMIZED/locality_optimized_dlm/manual_output_funchead_fine_depl_size"

PATH = "/u/scr/mhahn/deps/"+group+"/"

files = os.listdir(PATH)

cache = {}

outHeader = set(["Language", "FileName", "Language_", "LanguageBare"])

entries = []

collectedFilesNumber = 0



for filename in files:
   print(filename)
   if "model" in filename:
#      print("READING "+filename )
      part1 = filename.split("_model_")[0]
      if "_" in part1:
        language = part1.split("_opt")[0]
      else:
        assert False
      with open(PATH+filename, "r") as inFile:
          print(filename)
          try:
            header = next(inFile).strip().split("\t")
          except StopIteration:
            print ["EMPTY FILE?",inPath+filename]
            continue
          for x in header:
            outHeader.add(x)
          collectedFilesNumber+= 1
          for line in inFile:
#             print(line)
             line = line.strip().split("\t")
             if len(line) < 2:
                continue
             entry = dict(list(zip(header, line)))
             if "Language" not in entry or True:
                entry["Language"] = language
#             print(filename)
             if not ("_2.6-" in filename):
#               assert False, filename
               collectedFilesNumber-=1
               break
             entry["Language_"] = entry["Language"].replace("_2.6", "")
             entry["LanguageBare"] = language[:language.index("-")]
             if "FileName" not in header:
                entry["FileName"] = filename[filename.rfind("_")+1:-4]
             if entry["CoarseDependency"] not in ["obj", "nsubj"] or entry["HeadPOS"] != "VERB" or entry["DependentPOS"] != "NOUN":
                  continue
  #           if entry["Language"] not in languages:
 #              print("MISSING", entry["Language"])
#               continue
             entries.append(entry)
outHeader = sorted(list(outHeader))
print(outHeader)

print(collectedFilesNumber)
with open(PATH+"auto-summary-lstm_2.6.tsv", "w") as outFile:
  print("\t".join(outHeader) , file=outFile)
  for entry in entries:
    print("\t".join([entry.get(x, "NA") for x in outHeader]), file=outFile)
print("WRITING", PATH+"auto-summary-lstm_2.6.tsv")

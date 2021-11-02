import os
DIR = "/u/scr/mhahn/deps/hillclimbing-auc-fracdlm/"
files = [x for x in sorted(os.listdir(DIR))]
from collections import defaultdict
same = defaultdict(int)

parameters = ["alpha", "cutoff", "delta", "fraction", "gamma", "idForProcess", "language", "model", "script"]

dist_d, dist_n, dist_a = 0, 0, 0
languages = set()
with open(f"output/{__file__}.tsv", "w") as outFile:
 print("\t".join(["idForProcess", "language", "dependency", "weight"]), file=outFile)
 with open(f"output/{__file__}_arguments.tsv", "w") as outFileArgs:
  print("\t".join(parameters), file=outFileArgs)
  for f in sorted(files):
   data = [x.split("\t") for x in open(DIR+"/"+f, "r").read().strip().split("\n")]
   print(data[0][0])
   args = data[0][0][1:-1].split(", ")
   iterations = int(args[0])
   last_change = int(args[1])
   auc = float(args[2])
   args = args[3:]
   args[0] = args[0].replace('"Namespace(', "")
   args[-1] = args[-1].replace(')"', "")
   print(args)
   args = dict([x.split("=") if "=" in x else (x,"NA") for x in args])
   print(set(args))
   args["script"] = f[f.index("forWords"):f.index(".py_")]
   outLineArgs = [args.get(x, "NA").strip("'\")") for x in parameters]
   print("\t".join(outLineArgs), file=outFileArgs)
   assert all([x in parameters or args[x] == "NA" for x in args]), args
   data = dict(data[1:])
   language = args["language"].strip("'").replace("2.6", "2.8").replace("2.7", "2.8")
   for dependency, weight in data.items():
      print("\t".join([args["idForProcess"], language, dependency, weight]), file=outFile)


import os
DIR = "/u/scr/mhahn/deps/hillclimbing-auc-fracdlm/"
files = [x for x in sorted(os.listdir(DIR))]
from collections import defaultdict
same = defaultdict(int)


dist_d, dist_n, dist_a = 0, 0, 0
languages = set()
with open(f"output/{__file__}.tsv", "w") as outFile:
 print("\t".join(["language", "ID", "basic", "np", "Dist_D", "Dist_N", "Dist_A", "Surprisal2", "DepLen"]), file=outFile)
 for f in sorted(files):
   id_ = f[f.rfind("_")+1:-4]
   data = [x.split("\t") for x in open(DIR+"/"+f, "r").read().strip().split("\n")]
   
   _, args, results = data[0][0].split('"')
   print(results)
   surprisals, depLen = results.split("]")
   print("RESULTS", results)
   surprisals = [float(x) for x in [(x.strip().strip(",").strip().strip("[")) for x in surprisals.split(",")] if len(x) > 0]
   if len(depLen.strip()) > 2:
        depLen = float(depLen.strip().strip(")").strip(",").strip())
   else:
        depLen = float("nan")
   data = dict(data[1:])
   language = f[f.index("_")+1:f.index("_for")]
   languages.add(language)
   order = "".join([x[0] for x in sorted([("V", int(data["HEAD"])), ("S", int(data["nsubj"])), ("O", int(data["obj"]))],key= lambda x:x[1])])
   if order.index("S") > order.index("V"):
       order = order[::-1]
   correl = [x for x in ["case", "cop", "mark", "nmod", "obl", "xcomp", "acl", "aux", "amod", "nummod", "nsubj"] if x in data]
   def d(x):
      return int(data[x]) < int(data["HEAD"])

   np = "".join([x[0] for x in sorted([("_", int(data["HEAD"])), ("A", int(data["amod"])), ("N", int(data["nummod"])), ("D", int(data["det"]))],key= lambda x:x[1])])
   if np.index("A") > np.index("_"):
      np = np[::-1]
   dist_d += abs(np.index("D") - np.index("_"))/(len(files)+0.0)
   dist_n += abs(np.index("N") - np.index("_"))/(len(files)+0.0)
   dist_a += abs(np.index("A") - np.index("_"))/(len(files)+0.0)
   print("\t".join([str(x) for x in [language, id_, order, np, abs(np.index("D") - np.index("_")), abs(np.index("N") - np.index("_")), abs(np.index("A") - np.index("_")), round(surprisals[1],3), round(depLen,3)]]), file=outFile)
   print(language, "\t", order, [x for x in correl if d(x) == d("obj")], "\t", [x for x in correl if d(x) != d("obj")], "\t", args[:3], "\t", np)
   for x in correl:
     if d(x) == d("obj"):
         same[x] += 1.0/len(files)
print(same)
print(dist_d, dist_n, dist_a)
print(languages)
print(len(languages))

import os
import subprocess
script = "forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_DLM_RecordAll.py"

#groups = ["hillclimbing-auc"]
groups = ["DLM_MEMORY_OPTIMIZED/locality_optimized_dlm/manual_output_funchead_fine_depl_nopos"]
import random
filesNotDone = []
with open(f"output/{script}.tsv", "w") as outFile:
 print("\t".join(["DH_Weight", "CoarseDependency", "DistanceWeight", "Language", "FileName"]), file=outFile)
for group in groups:
  files = sorted(os.listdir("/u/scr/mhahn/deps/"+group))
  for f in files:
     if "forWord" in f:
       language = f[f.index("_")+1:f.index("_forWord")].replace("2.6", "2.8").replace("2.7", "2.8")
     elif "optimizeDep" in f:
       language = f[:f.index("_optim")].replace("2.6", "2.8").replace("2.7", "2.8")
     else:
       print("NOT DOING THIS FILE", f)
       filesNotDone.append(f)
       continue
     id_ = f[f.rfind("_")+1:-4]
     assert "_2.8" in language
     print(f, language, id_)
     #quit()
     subprocess.call(["/u/nlp/anaconda/main/anaconda3/envs/py37-mhahn/bin/python", script, "--language="+language, "--group="+group, "--model="+id_])
     print(filesNotDone)
     #quit()
print(filesNotDone)

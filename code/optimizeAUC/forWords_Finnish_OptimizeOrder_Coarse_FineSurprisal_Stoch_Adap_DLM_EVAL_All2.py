import glob
import os
import subprocess
import time
script = "forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_DLM_EVAL.py"

groups = ["hillclimbing-auc"]
#groups = ["DLM_MEMORY_OPTIMIZED/locality_optimized_dlm/manual_output_funchead_fine_depl_nopos"]
import random

instance = random.randint(10000, 10000000)

for group in groups:
  files = os.listdir("/u/scr/mhahn/deps/"+group)
  random.shuffle(files)
  for f in files:
     resultsPath = f"/u/scr/mhahn/deps/{group}/{f}"
     if time.time() - os.stat(resultsPath).st_mtime < 3600: # written to within the last hour       
         print("Recent, skip for now")
         continue
     if "forWord" in f:
       language = f[f.index("_")+1:f.index("_forWord")].replace("2.6", "2.8").replace("2.7", "2.8")
     elif "optimizeDep" in f:
       language = f[:f.index("_optim")].replace("2.6", "2.8").replace("2.7", "2.8")
     else:
       print("PROBLEM 21", False, f)
       continue

     assert "_2.8" in language
     if group.startswith("DLM_MEMORY_OPTIMIZED"):
       # The REINFORCE-optimized grammars are optimized on the whole corpora. But for comparability to the hill-climbing grammars, need to evaluate on the restricted corpora
       if "German" in language :
         language = "German-GSD_2.8"
       elif "Czech" in language:
         language = "Czech-PDT_2.8"
       elif "Japanese" in language:
         language = "Japanese-GSD_2.8"

     id_ = f[f.rfind("_")+1:-4]
     relevantLogs = glob.glob("output/forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_DLM_EVAL.py*tsv")
     found = False
     print("Looking for", id_)
     print("LOGs", relevantLogs)
     for log in relevantLogs:
        with open(log, "r") as inFile:
            for line in inFile:
              line = line.strip().split("\t")
        #      print("DONE", int(line[2]), "LOOKING FOR", id_)
              
              if int(line[2]) == int(id_) and line[0] == language:
                
                found = True
                break
        if found:
             break
     if found:
       continue

     print(f, language, id_)
     #quit()
     subprocess.call(["/u/nlp/anaconda/ubuntu_16/envs/py27-mhahn/bin/python2.7", script, "--language="+language, "--group="+group, "--model="+id_, "--instance="+str(instance)])
     #quit()

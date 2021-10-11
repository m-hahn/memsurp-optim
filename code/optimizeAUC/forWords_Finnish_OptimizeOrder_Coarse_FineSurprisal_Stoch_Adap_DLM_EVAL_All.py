import os
import subprocess
script = "forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_DLM_EVAL.py"

groups = ["hillclimbing-auc"]
import random
for group in groups:
  files = os.listdir("/u/scr/mhahn/deps/"+group)
  random.shuffle(files)
  for f in files:
     language = f[f.index("_")+1:f.index("_forWord")].replace("2.6", "2.8").replace("2.7", "2.8")
     id_ = f[f.rfind("_")+1:-4]
     print(f, language, id_)
     subprocess.call(["/u/nlp/anaconda/ubuntu_16/envs/py27-mhahn/bin/python2.7", script, "--language="+language, "--group="+group, "--model="+id_])
     #quit()

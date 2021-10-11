import os
import subprocess
script = "forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_DLM_RecordBasic.py"

#groups = ["hillclimbing-auc"]
groups = ["DLM_MEMORY_OPTIMIZED/locality_optimized_dlm/manual_output_funchead_fine_depl_nopos"]
import random
for group in groups:
  files = os.listdir("/u/scr/mhahn/deps/"+group)
  random.shuffle(files)
  for f in files:
     if "forWord" in f:
       language = f[f.index("_")+1:f.index("_forWord")].replace("2.6", "2.8").replace("2.7", "2.8")
     elif "optimizeDep" in f:
       language = f[:f.index("_optim")].replace("2.6", "2.8").replace("2.7", "2.8")
     else:
       assert False
     id_ = f[f.rfind("_")+1:-4]
     assert "_2.8" in language
     print(f, language, id_)
     #quit()
     subprocess.call(["/u/nlp/anaconda/ubuntu_16/envs/py27-mhahn/bin/python2.7", script, "--language="+language, "--group="+group, "--model="+id_])
     #quit()

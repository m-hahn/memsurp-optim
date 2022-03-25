import random
import sys
from ud_languages_28 import languages
import subprocess
from random import choice
if len(sys.argv) > 1:
   N = int(sys.argv[1])
else:
   N =1000
import glob
BASE = "hillclimbing-auc-fracdlm"
script = "forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_PlusFracDLM.py"
for language in languages:
   print(language, "from 2.6 and 2.8:", len(glob.glob(f"/u/scr/mhahn/deps/{BASE}/optimized_{language}_{script}*tsv")) + len(glob.glob(f"/u/scr/mhahn/deps/{BASE}/optimized_{language.replace('2.8', '2.6')}_{script}*tsv")))
for _ in range(N):
   random.shuffle(languages)
   found = False
   for language in languages:
     if "German" in language:
        language = "German-GSD_2.8"
  #      continue
     elif "Japanese" in language:
        language = "Japanese-GSD_2.8"
     elif "Czech" in language:
        language = "Czech-PDT_2.8"
#        continue
     else:
        continue
     print("Considering", language, "from 2.6 and 2.8:", len(glob.glob(f"/u/scr/mhahn/deps/{BASE}/optimized_{language}_{script}*tsv")) + len(glob.glob(f"/u/scr/mhahn/deps/{BASE}/optimized_{language.replace('2.8', '2.6')}_{script}*tsv")))
     if len(glob.glob(f"/u/scr/mhahn/deps/{BASE}/optimized_{language}_{script}*tsv")) + len(glob.glob(f"/u/scr/mhahn/deps/{BASE}/optimized_{language.replace('2.8', '2.6')}_{script}*tsv")) < 10:
         found = True
         break
   if not found:
     break
   subprocess.call(["/u/nlp/anaconda/ubuntu_16/envs/py27-mhahn/bin/python2.7", script, "--language="+language])

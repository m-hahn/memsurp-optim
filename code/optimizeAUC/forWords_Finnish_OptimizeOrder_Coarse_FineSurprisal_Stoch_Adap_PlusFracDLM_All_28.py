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
   while True:
     language = choice(languages)
     print(language, "from 2.6 and 2.8:", len(glob.glob(f"/u/scr/mhahn/deps/{BASE}/optimized_{language}_{script}*tsv")) + len(glob.glob(f"/u/scr/mhahn/deps/{BASE}/optimized_{language.replace('2.8', '2.6')}_{script}*tsv")))
     if len(glob.glob(f"/u/scr/mhahn/deps/{BASE}/optimized_{language}_{script}*tsv")) + len(glob.glob(f"/u/scr/mhahn/deps/{BASE}/optimized_{language.replace('2.8', '2.6')}_{script}*tsv")) >= 15:
         continue
     break
#     if "German" not in language:
 #    continue
   if "German" in language:
#      language = "German-GSD_2.8"
      pass
   elif "Japanese" in language:
      language = "Japanese-GSD_2.8"
   elif "Czech" in language:
      continue
   subprocess.call(["/u/nlp/anaconda/ubuntu_16/envs/py27-mhahn/bin/python2.7", script, "--language="+language])
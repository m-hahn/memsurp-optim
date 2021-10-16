import sys
from ud_languages_28 import languages
import subprocess
from random import choice
if len(sys.argv) > 1:
   N = int(sys.argv[1])
else:
   N =1000
for _ in range(N):
   language = choice(languages)
   if "German" in language:
     continue
   elif "Japanese" in language:
      language = "Japanese-GSD_2.8"
   elif "Czech" in language:
      continue
   subprocess.call(["/u/nlp/anaconda/ubuntu_16/envs/py27-mhahn/bin/python2.7", "forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap.py", "--language="+language])

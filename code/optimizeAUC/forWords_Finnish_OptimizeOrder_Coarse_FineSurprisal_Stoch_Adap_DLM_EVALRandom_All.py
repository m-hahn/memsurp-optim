import os
import subprocess
script = "forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_DLM_EVALRandom.py"

from ud_languages_28 import languages
import random
random.shuffle(languages)
while True:
     language = random.choice(languages)
     if "German" in language:
       continue
     subprocess.call(["/u/nlp/anaconda/ubuntu_16/envs/py27-mhahn/bin/python2.7", script, "--language="+language])


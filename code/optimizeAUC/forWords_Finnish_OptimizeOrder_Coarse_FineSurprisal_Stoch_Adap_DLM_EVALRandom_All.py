import os
import subprocess
script = "forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_DLM_EVALRandom.py"

from ud_languages_28 import languages
import random

instance = random.randint(10000, 10000000)


random.shuffle(languages)
languages = ["German-GSD_2.8", "Japanese-GSD_2.8", "Czech-PDT_2.8"]
while True:
     language = random.choice(languages)
     if "German" in language:
       language = "German-GSD_2.8"
     elif "Japanese" in language:
       language = "Japanese-GSD_2.8"
     elif "Czech" in language:
       language = "Czech-PDT_2.8"
     subprocess.call(["/u/nlp/anaconda/ubuntu_16/envs/py27-mhahn/bin/python2.7", script, "--language="+language, "--instance="+str(instance)])


import os
import subprocess
script = "forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_DLM_EVALReal_FuncHead.py"

from ud_languages_28 import languages
import random
random.shuffle(languages)
for language in languages:
     if "German" in language:
        language = "German-GSD_2.8"
     elif "Japanese" in language:
        language = "Japanese-GSD_2.8"
     elif "Czech" in language:
        continue
     subprocess.call(["/u/nlp/anaconda/ubuntu_16/envs/py27-mhahn/bin/python2.7", script, "--language="+language])


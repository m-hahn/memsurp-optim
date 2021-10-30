import glob
files = sorted(glob.glob("output/forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_DLM_EVAL_FuncHead.py*tsv"))

with open("output/SUMMARY_forWords_Finnish_OptimizeOrder_Coarse_FineSurprisal_Stoch_Adap_DLM_EVAL_FuncHead.py.tsv", "w") as outFile:
 for f in files:
  with open(f, "r") as inFile:
   for line in inFile:
     print(line.strip(), file=outFile)

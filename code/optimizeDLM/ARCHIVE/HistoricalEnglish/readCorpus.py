BASEPATH = "/u/scr/corpora/YCOE_Old_English_Prose/psd/"

def readFromFile(filename):
 with open(BASEPATH+"/"+filename, "r") as inFile:
  stack = []
#  print(filename)
  for line in inFile:     
#    if len(line) <= 2:
 #       assert len(stack) == 0
    try:
      positionOpen = line.index("(")
      line = line[positionOpen:].strip()
      while True:
         line = line.strip()
#         print(line)
         try:
            positionOpen = line.index("(")
         except ValueError:
            positionOpen = len(line)+1000
         try:
            positionClose = line.index(")")
         except ValueError:
            positionClose = len(line)+1000
         if positionOpen > len(line) and positionClose > len(line):
            break


#         print(line, len(stack))
         if positionOpen < positionClose:
            label = line[:positionOpen]
            if len(label) > 0 and label != " ":
               #print("NextOpen", label)
               #print(line)
               assert stack[-1]["category"] == "UNKNOWN", stack[-1]
               stack[-1]["category"] = label

            line = line[positionOpen+1:]    

            stack.append({"children" : [], "category" : "UNKNOWN"})
            assert "label" not in stack[-1]
         else:
            label = line[:positionClose]
            if len(label) > 0 and stack[-1]["category"] == "UNKNOWN":
               category, word = label.split(" ")
               stack[-1]["category"] = category
               stack[-1]["word"] = word
            elif len(label) > 0:
               stack[-2]["children"].append(stack[-1])
               stack.pop(-1)
               stack.append({"children" : [], "category" : "NOT_GIVEN", "word" : label})
            if len(stack) > 1:
               stack[-2]["children"].append(stack[-1])
            else:
               yield stack[-1]
            stack.pop(-1)
            line = line[positionClose+1:]    

    except ValueError:
         _ = 0
       
#for s in readFromFile("1150.firstgrammar.sci-lin.psd"):
#  print(s)
import os
def texts():
   texts = sorted([x for x in os.listdir(BASEPATH) if x.endswith(".psd")])
   print(texts)
   return texts


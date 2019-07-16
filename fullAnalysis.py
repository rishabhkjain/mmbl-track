
import os
import argparse
import subprocess
from pathlib import Path


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
args = vars(ap.parse_args())
path = Path(args["input"])
outputPath = Path(args["output"])



blurredLst = list()

for root,dirs,files in os.walk(path):
    if not dirs:
        blurredLst.append(Path(root))
cleanLst = list()
resultLst = list()
blurLst = list()
for i in range(len(blurredLst)):
    if "blurred" not in str(blurredLst[i]):
        cleanLst.append(blurredLst[i])
        resultLst.append(cleanLst[-1].parts[-1])
        blurLst.append(Path(str(blurredLst[i]) + "_blurred"))
        blurredLst[i] = "\v"

while "\v" in blurredLst:
    blurredLst.remove("\v")
for i in range (len(blurredLst)):
    print (blurredLst[i])
    print (cleanLst[i])
    print(resultLst[i])
if len(blurredLst) != len(cleanLst):
    print ("Folder Error")
else:
    print ("Running Analysis")
    for i in range (len(blurredLst)):
        print (blurLst[i], cleanLst[i], resultLst[i])
        subprocess.call(['python','main.py',  '--input', str(blurLst[i]), '-c', str(cleanLst[i]), '-o', str(outputPath / resultLst[i]), '-s', '180'], shell = False)
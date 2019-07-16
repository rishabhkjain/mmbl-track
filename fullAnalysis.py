
import os
import argparse
import subprocess
from pathlib import Path


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")
args = vars(ap.parse_args())
path = Path(args["input"])



dirLst = list()

for root,dirs,files in os.walk(path):
    if not dirs:
        dirLst.append(root)
print(dirLst)

for i in range(len(dirLst)):
    if "blurred" not in str(dirLst[i]):
        dirLst[i] = "\v"

while "\v" in dirLst:
    dirLst.remove("\v")

print(dirLst)
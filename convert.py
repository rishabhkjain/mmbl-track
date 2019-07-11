import os
import argparse
import subprocess
from pathlib import Path



def findLatest(s, c):
    strLen = len(s)
    for i in range(strLen-1, -1, -1):
        if s[i] == c:
            return i

    return 0

curLoc = Path(os.getcwd())
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")
args = vars(ap.parse_args())



path = Path(args["input"])

dirLst = os.listdir(path)

for item in dirLst:
    vidDir = curLoc / path / item
    os.chdir(vidDir)
    vidPath = vidDir /  os.listdir()[0]
    print(vidPath)
    subprocess.call(['ffmpeg', '-i', vidPath, '-r', '4', vidDir + "\\outputFile%04d.png"])

print(dirLst)
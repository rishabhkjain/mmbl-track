import os
import argparse
import glob
from pathlib import Path
import copy

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")

args = vars(ap.parse_args())

path = Path(args["input"])


fullList = list(path.glob('**/*.mp4'))

print(fullList)
for j in range (len(fullList)):
    tmpPath = Path((str(fullList[j]).split("."))[0])
    print('tmpPath is ', tmpPath)
    newFilePath = tmpPath / "video.mp4"
    print('newFilePath is ', newFilePath)
    try:
        #os.mkdir(tmpPath)
        Path.mkdir(tmpPath)
    except:
        print("Overwriting Data")
    try:
        #os.rename(fullList[j], newFilePath)
        p = Path(fullList[j])
        p.rename(newFilePath)
    except:
        print("Overwriting Data")
  
    print (fullList[j], tmpPath)


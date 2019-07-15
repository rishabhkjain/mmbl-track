from pathlib import Path
import os
import argparse


ap = argparse.ArgumentParser()

ap.add_argument("-i", "--input", required=True,
	help="directory of videos")

args = vars(ap.parse_args())

path = Path(args["input"])

finLst = []

def findVid(input):
    if Path.is_dir(input):
        tmpList = [x for x in input.iterdir()]
        for i in range (len(tmpList)):
            findVid(tmpList[i])
    else:
        finLst.append(input)
findVid(path)
print(finLst)

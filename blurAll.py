
import os
import argparse
import subprocess
from pathlib import Path


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")
ap.add_argument("-f", "--fast", required=True,
	help="binary for determining if calculating circles")
args = vars(ap.parse_args())

path = Path(args["input"])

flag = int(args["fast"])


dirLst = list()

for root,dirs,files in os.walk(path):
    if not dirs:
        dirLst.append(root)


for item in dirLst:
    print (item)
    subprocess.call(['python', 'blurVideo.py', '--input',  item, '--fast', flag])
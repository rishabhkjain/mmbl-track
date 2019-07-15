
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


for item in dirLst:
    print (item)
    subprocess.call(['python', 'blurVideo.py', '--input',  item])
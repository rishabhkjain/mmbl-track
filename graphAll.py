import os
import argparse
import subprocess
from pathlib import Path


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")

args = vars(ap.parse_args())
path = Path(args["input"])



fileLst = list()

for root,dirs,files in os.walk(path):
    if not dirs:
        tmpPath = Path(root)
        up = tmpPath.parent
        fileLst.append(up)

        

for item in fileLst:
    print(item)
    subprocess.call(['python', 'graph.py', '--input', str(item)])
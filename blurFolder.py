import os
import argparse
import subprocess
from pathlib import Path


curLoc = os.getcwd()
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")
ap.add_argument("-f", "--fast", required=True,
	help="binary for determining if calculating circles")
args = vars(ap.parse_args())
path = Path(args["input"])
flag = int(args["fast"])

dirLst = os.listdir(path)
if flag:
    print ("Fast Analysis")
for item in dirLst:
    subprocess.call(['python', 'blurVideo.py', '--input', path / item], '--fast', flag)
    print item
import os
import argparse
import subprocess
from pathlib import Path


curLoc = os.getcwd()
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")
args = vars(ap.parse_args())
path = Path(args["input"])


dirLst = os.listdir(path)

for item in dirLst:
    subprocess.call(['python', 'blurVideo.py', '--input', path / item])
    print item
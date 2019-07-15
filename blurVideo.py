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

newPath = Path(str(path) + "_blurred")
try:
	os.mkdir(newPath)
except:
	print("Overwriting Data")





dirLst = os.listdir(path)
for item in dirLst:
    if item[-1] == "4":
        continue
    subprocess.call(['python', 'blurPhoto.py', '--input',str( path / item), "--output", str(newPath  / item)])

# print(dirLst)
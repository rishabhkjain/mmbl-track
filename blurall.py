import os
import argparse
import subprocess


curLoc = os.getcwd()
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")
args = vars(ap.parse_args())
path = args["input"] 


dirLst = os.listdir(path)

for item in dirLst:
    subprocess.call(['python', 'batch.py', '--input', path + "\\" + item])
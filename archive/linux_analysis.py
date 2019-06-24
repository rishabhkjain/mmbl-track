import os
import argparse
import glob
import subprocess


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")

args = vars(ap.parse_args())


path = args["input"] 


folderLst = os.listdir(path)
for item in folderLst:
    # print(path  + item)
    subprocess.call(['python','linux_main.py',  '-i', path + item, '-o', 'results//dsdna_s1', '-s', '180'])
    




import os
import argparse
import subprocess


def findLatest(s, c):
    strLen = len(s)
    for i in range(strLen-1, -1, -1):
        if s[i] == c:
            return i

    return 0

curLoc = os.getcwd()
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")
args = vars(ap.parse_args())
path = args["input"] 

newPath = path + "_blurred"
try:
	os.mkdir(newPath)
except:
	print("Overwriting Data")





dirLst = os.listdir(path)
for item in dirLst:
    if item[-1] == "4":
        continue
    print(path + "\\" + item)
    subprocess.call(['python', 'circletest.py', '--input', path + "\\" + item, "--output", newPath + "\\" + item])

# print(dirLst)
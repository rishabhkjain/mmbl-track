import os
import argparse
import glob

def findLatest(s, c):
    strLen = len(s)
    for i in range(strLen-1, -1, -1):
        if s[i] == c:
            return i

    return 0
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="directory of videos")

args = vars(ap.parse_args())


path = args["input"] 

fileLst = (glob.glob(path + "/*.mp4"))


for item in fileLst:
    finish = findLatest(item, ".")
    begin = findLatest(item, "//")
    folderName = item[0: finish]
    newFilePath = folderName + "//" + "video.mp4"
    try:
        os.mkdir(folderName)
    except:
        print("Overwriting Data")
    try:
        os.rename(item, newFilePath)
    except:
        print("Overwriting Data")
  
    # print (item, folderName)


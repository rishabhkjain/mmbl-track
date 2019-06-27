from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import csv
import argparse
import os



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="input path")


args = vars(ap.parse_args())



idLst, deltaLst, frameCount, dirLst, frameLst = [], [], [], [], []
folderPath = Path(args["input"])
folderLst = os.listdir(folderPath / "detailedResults")
with open(folderPath / "compactResults.csv",'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        if len(row) == 0:
            continue
        idLst.append(int(row[0]))
        deltaLst.append(float(row[1]))
        frameCount.append(int(row[2]))
        dirLst.append(row[3])
        frameLst.append(row[4])
        

displacementDistrib = plt.figure()
plt.hist(deltaLst,range=[0, 2000], bins = 20)
plt.xlabel("Frame")
plt.ylabel("Count")
plt.savefig(folderPath / "displacement.png")
try:
    os.mkdir(folderPath / "graphs")
except:
    print("Overwriting data: directory already exists")
for particle in folderLst:
    endID = particle.find("_")
    name = particle[:endID]
    print(name)
    directionLst = []
    f = []
    delta = []
    with open (folderPath / "detailedResults" / particle, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if len(row) == 0:
                continue
            directionLst.append(float(row[4]))
            f.append(int(row[0]))
            delta.append(float(row[3]))
    dirPlot = plt.figure()
    plt.xlim(180, 1500)
    plt.xlabel("Frame")

    plt.plot(f, directionLst)
    dirPlotName = name + "_dir.png"
    plt.savefig(folderPath / "graphs" / dirPlotName)
    totalLst = [0]*len(delta)
    for i in range (len(delta)):
        if i == 0:
            totalLst[i] = delta[i]
        else:
            
            totalLst[i] = delta[i] + totalLst [i-1]
    distPlot = plt.figure()
    plt.plot(f, totalLst)
    plt.xlim(180, 1500)
    plt.xlabel("Frame")
    plt.ylabel("Distance(px)")
    plt.ylim(0, 1500)
    dirPlotName = name + "_movement.png"
    plt.savefig(folderPath / "graphs" / dirPlotName)
    plt.close()

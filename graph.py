from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import csv
import argparse
import os
import string



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="input path")


args = vars(ap.parse_args())


minDist = 10
fps = 4
scalar = 0.27
idLst, deltaLst, frameCount, dirLst, frameLst = [], [], [], [], []
folderPath = Path(args["input"])
folderLst = os.listdir(folderPath / "detailedResults")
testLst = []
with open(folderPath / "compactResults.csv",'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        if len(row) == 0:
            continue
        idLst.append(int(row[0]))
        deltaLst.append(float(row[1])*scalar)
        frameCount.append(int(row[2]))
        dirLst.append((row[3]))
        tmpStr = row[4][1:-1]
        frameLst.append(tmpStr.split(','))

velocityLst = []      
for i in range (len (idLst)):


    numFrames = int(frameLst[i][-1]) - int(frameLst[i][0])
    distance = deltaLst[i]
    

    if numFrames == 0:
        velocity = 0
    else:
        velocity = (distance/numFrames)*fps
    velocityLst.append(velocity)
count = 0
totalVelocity = 0
for i in range (len(velocityLst)):
    if deltaLst[i] < minDist:
        continue
    else:
        count += 1
        totalVelocity += velocityLst[i]
avgVelocity = totalVelocity/count
print(avgVelocity)

with open(folderPath / 'velocity.txt', 'w') as f:
  f.write(str(avgVelocity))
displacementDistrib = plt.figure()
plt.hist(deltaLst,range=[0, 1000], bins = 20)
plt.xlabel("Distance (\u03BCm)")
plt.ylabel("Count")
plt.title("Displacement Distribution for " + str(folderPath.parts[-1]))
plt.savefig(folderPath / "displacement.png")

velocityDistrib = plt.figure()
plt.hist(velocityLst,range=[0, 5], bins = 20)
plt.xlabel("Velocity (\u03BCm/s)")
plt.ylabel("Count")
plt.title("Velocity Distribution for " + str(folderPath.parts[-1]))

plt.savefig(folderPath / "velocity.png")
try:
    os.mkdir(folderPath / "graphs")
except:
    print("Overwriting data: directory already exists")
for particle in folderLst:
    endID = particle.find("_")
    name = particle[:endID]
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
    plt.xlim(180, 1200)
    plt.xlabel("Frame")
    plt.ylabel("Direction (rad)")
    plt.title("Direction of Movement for Particle " + str(name)+ " in " + str(folderPath.parts[-1]))

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
    plt.xlim(180, 1200)
    plt.xlabel("Frame")
    plt.ylabel("Distance (\u03BCm)")
    plt.ylim(0, 1200)
    dirPlotName = name + "_movement.png"
    plt.title("Displacement for Particle " + str(name)+ " in " + str(folderPath.parts[-1]))

    plt.savefig(folderPath / "graphs" / dirPlotName)
    plt.close()

from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
import csv
import argparse
mpl.rc('figure',  figsize=(10, 5))
mpl.rc('image', cmap='gray')
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import os

import pims
import trackpy as tp
mpl.use('Agg')

# change the following to %matplotlib notebook for interactive plotting
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="folder name in media")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
args = vars(ap.parse_args())
# Optionally, tweak styles.


pngStackPath = "media\\" + args["input"] + "\*.png"
frames = pims.ImageSequence(pngStackPath, as_grey = True)
startFrame = 0
endFrame = len(frames)
trajCont = 10
frameCount = endFrame - startFrame




f = tp.batch(frames[startFrame:endFrame],diameter= 19, invert=True, minmass = 3500)
t = tp.link_df(f, 5, memory=5)
compactDict = {}
fullDict = {}
particleLst = set()
t1 = tp.filter_stubs(t, trajCont)
# Compare the number of particles in the unfiltered and filtered data.
print('Before:', t['particle'].nunique())
print('After:', t1['particle'].nunique())

numParticles = t1['particle'].nunique()
for i in range (startFrame,endFrame-1):
    print(i)
    tv = tp.relate_frames(t1, i, i+1)
    for index, row in tv.iterrows():
        tempDX = row['dx']
        tempDY = row['dy']
        tempDT = row['dr']
        tempDir = row['direction']
        if pd.isna(tempDT):
            tempDT = 0
        if pd.isna(tempDir):
            tempDir = 0
        if pd.isna(tempDX):
            tempDX = 0
        if pd.isna(tempDY):
            tempDY = 0
 
        snapshot = (tempDX, tempDY, tempDT, tempDir)


        if index not in compactDict:
            particleLst.add(index)
            dirList = []
            dirList.append(tempDir)
            indexLst = []
            indexLst.append(i)
            totalDist = tempDT
            count = 1
            compactDict[index] = [totalDist, count,dirList, indexLst]
        else:
            compactDict[index][3].append(i)
            compactDict[index][2].append(tempDir)
            compactDict[index][1] += 1
            compactDict[index][0] += tempDT
        if index not in fullDict:
            particleLst.add(index)
            tmpDict = {}
            tmpDict[i] = snapshot
            fullDict[index] = tmpDict
        else:
            tmpDict = fullDict[index]
            tmpDict[i] = snapshot
            fullDict[index] = tmpDict
outputPath = str(args["output"]) +  '\\' + str(args["input"])
os.mkdir(outputPath)
with open(outputPath + '\\compactResults.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in compactDict.items():
        writer.writerow([key, value[0], value[1], value[2], value[3]])

os.mkdir(outputPath + '\\' + "detailedResults")        
for miniDict in fullDict:
    with open(outputPath + '\\' + "detailedResults" + '\\' + str(miniDict) + '_detailedResult.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in fullDict[miniDict].items():
            writer.writerow([key, value[0], value[1],value[2],value[3]])
trajFig = plt.figure()
trajPlot =  tp.plot_traj(t1)
trajFig.savefig(outputPath + '\\' + 'traj.png')

idFig = plt.figure()
idPlot = tp.annotate(t1[t1['frame'] == 0], frames[0])
idFig.savefig(outputPath + '\\' +'id.png')

           

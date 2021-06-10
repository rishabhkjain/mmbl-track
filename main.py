from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import csv
import argparse
mpl.rc('figure',  figsize=(10, 5))
mpl.rc('image', cmap='gray')
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import os
import pickle
import imageio
# import cv2
import glob
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pathlib import Path
import pims
import trackpy as tp
mpl.use('Agg')
from pathlib import Path
import math


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="input path")
ap.add_argument("-c", "--clean", required=True,
	help="path to clean images")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
ap.add_argument("-s", "--start", required=True,
	help="Start frame number")

args = vars(ap.parse_args())

tmpPath = Path(args["input"])
pngStackPath = tmpPath / "*.png" 

#frames = pims.ImageSequence(str(pngStackPath), as_grey = True) #import pngstack into trackpy
print('Importing PNG stack...')
frames = pims.ImageSequence(str(pngStackPath)) # import pngstack into trackpy
tmpCleanPath = Path(args["clean"])
cleanStackPath = tmpCleanPath  / "*.png"
startFrame = int(args["start"])
endFrame = len(frames) 
frameCount = endFrame - startFrame
trajCont = min(int(0.4 * (frameCount)), 240) #minimum number of times the particle's trajectory needs to be identified
#cleanFrames =  pims.ImageSequence(str(cleanStackPath), as_grey = True)
print('Importing clean PNG stack...')
cleanFrames = pims.ImageSequence(str(cleanStackPath))

#f is a dataframe containing all locations particles were located
# diameter & minmass need to be adjusted based on sample
f = tp.batch(frames[startFrame:endFrame],diameter= 19, invert=True, minmass = 3500) 
f2 = tp.locate(frames[startFrame],diameter= 19, invert=True, minmass = 3500)
maxChange = 12
t = tp.link_df(f, maxChange, memory=12)
compactDict = {} #dictionaries for storing relevant data
fullDict = {}
locDict = {}
particleLst = set()
print('Filtering trajectories...')
t1 = tp.filter_stubs(t, trajCont) #filter out the trajectories that do not exist longer than trajCount
# Compare the number of particles in the unfiltered and filtered data.
print('Before:', t['particle'].nunique())
print('After:', t1['particle'].nunique())
def getDistance(index, x2, y2, d):
    x1 = d[index][0]
    y1 = d[index][1]
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    d = math.sqrt(dx*dx + dy*dy)
    return d

numParticles = t1['particle'].nunique()
#main loop which stores the data
for i in range (startFrame,endFrame-1):
    print(i)
    try:
        tv = tp.relate_frames(t1, i, i+1)
    except:
        print ("Velocity Error")
        continue
    for index, row in tv.iterrows():
        #extract the data from the dataframe 
        tempDX = row['dx']
        tempDY = row['dy']
        tempDT = row['dr']
        tempDir = row['direction']
        tempX1 = row['x']
        tempX2 = row['x_b']
        tempY1 = row['y']
        tempY2 = row ['y_b']
        #replace NaN values with 0
        if pd.isna(tempDT):
            tempDT = 0
        if pd.isna(tempDir):
            tempDir = 0
        if pd.isna(tempDX):
            tempDX = 0
        if pd.isna(tempDY):
            tempDY = 0
        if pd.isna(tempX1):
            tempX1 = 0
        if pd.isna(tempX2):
            tempX2 = 0
        if pd.isna(tempY1):
            tempY1 = 0
        if pd.isna(tempY2):
            tempY2 = 0
        snapshot = (tempDX, tempDY, tempDT, tempDir, tempX1, tempY1, tempX2,  tempY2)


        if index not in compactDict:
            particleLst.add(index)
            dirList = []
            dirList.append(tempDir)
            indexLst = []
            indexLst.append(i)
            totalDist = tempDT
            count = 1
            displacement = 0
            locDict[index] = (tempX1, tempY1)
            compactDict[index] = [totalDist, count,dirList, indexLst, displacement]
        else:
            compactDict[index][3].append(i)
            compactDict[index][2].append(tempDir)
            compactDict[index][1] += 1
            compactDict[index][0] += tempDT
            if tempX2 != 0 and tempY2 != 0:
                compactDict[index][4] = getDistance(index, tempX2, tempY2, locDict)
        if index not in fullDict:
            particleLst.add(index)
            tmpDict = {}
            tmpDict[i] = snapshot
            fullDict[index] = tmpDict
        else:
            tmpDict = fullDict[index]
            tmpDict[i] = snapshot
            fullDict[index] = tmpDict
def findLatest(s, c):
    strLen = len(s)
    for i in range(strLen-1, -1, -1):
        if s[i] == c:
            return i

    return 0
begin = findLatest(args["input"], "\\")
print(begin)
#store the data in results
outputPath = Path(args["output"])
print(outputPath)
try:
    #os.mkdir(outputPath)
    Path.mkdir(outputPath)
except:
    print("Overwriting data - directory already exists")
with open('{0}/compactResults.csv'.format(outputPath), 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in compactDict.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], value[4]])
try:
    #os.mkdir(outputPath / "detailedResults") 
    Path.mkdir(outputPath / "detailedResults")
except:
    print("Overwriting data - directory already exists")
       
for miniDict in fullDict:
    #with open(outputPath / "detailedResults"  / (str(miniDict) + '_detailedResult.csv'), 'w') as csv_file:
    with open('{0}/detailedResults/{1}_detailedResult.csv'.format(outputPath, str(miniDict)), 'w') as csv_file: 
        writer = csv.writer(csv_file)
        for key, value in fullDict[miniDict].items():
            writer.writerow([key, value[0], value[1],value[2],value[3], value[4], value[5], value[6], value[7]])
trajFig = plt.figure()
trajPlot =  tp.plot_traj(t1, label = False)
plt.title("Trajectories for " + str(tmpCleanPath.parts[-1]))
#trajFig.savefig(outputPath / 'traj.png')
trajFig.savefig('{0}/traj.png'.format(outputPath))
idFig = plt.figure()
idPlot = tp.annotate(t1[t1['frame'] == startFrame], cleanFrames[startFrame])
plt.title("ID Plot for " + str(tmpCleanPath.parts[-1]))

#idFig.savefig(outputPath  / "id.png")
idFig.savefig('{0}/id.png'.format(outputPath))
t1.to_pickle(outputPath / "traj.pkl")
f.to_pickle(outputPath / "f.pkl")
f2.to_pickle(outputPath / "f2.pkl")

# def cvtFig2Numpy(fig):
#     canvas = FigureCanvas(fig)
#     canvas.draw()
    
#     width, height = fig.get_size_inches() * fig.get_dpi()
#     image = np.fromstring(canvas.tostring_rgb(), dtype='uint8').reshape(height.astype(np.uint32), width.astype(np.uint32), 3)    
#     return image
    
# def makevideoFromArray(movieName, array, fps=25):
#     imageio.mimwrite(movieName, array, fps=fps);

# arr = []
# img = glob.glob(cleanStackPath)
# for i,idx in enumerate(img):
#     if i < startFrame:
#         continue
#     frame = cv2.imread(idx)
#     fig = plt.figure(figsize=(16, 8))
#     plt.imshow(frame)
#     axes = tp.plot_traj(t1.query('frame<={0}'.format(i)))
#     axes.set_yticklabels([])
#     axes.set_xticklabels([])
#     axes.get_xaxis().set_ticks([])
#     axes.get_yaxis().set_ticks([])
#     arr.append(cvtFig2Numpy(fig))
#     plt.close('all')
    

# makevideoFromArray(outputPath / trajvid.mp4", arr, 4)

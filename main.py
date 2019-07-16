from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
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
import cv2
import glob
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pathlib import Path
import pims
import trackpy as tp
mpl.use('Agg')
from pathlib import Path


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

frames = pims.ImageSequence(str(pngStackPath), as_grey = True) #import pngstack into trackpy
tmpCleanPath = Path(args["clean"])
cleanStackPath = tmpCleanPath  / "*.png"
startFrame = int(args["start"])
endFrame = len(frames) 
frameCount = endFrame - startFrame
trajCont = int(0.4 * (frameCount)) #minimum number of times the particle's trajectory needs to be identified
cleanFrames =  pims.ImageSequence(str(cleanStackPath), as_grey = True)

#f is a dataframe containing all locations particles were located
# diameter & minmass need to be adjusted based on sample
f = tp.batch(frames[startFrame:endFrame],diameter= 19, invert=True, minmass = 3500) 
t = tp.link_df(f, 5, memory=5)
compactDict = {} #dictionaries for storing relevant data
fullDict = {}
particleLst = set()
t1 = tp.filter_stubs(t, trajCont) #filter out the trajectories that do not exist longer than trajCount
# Compare the number of particles in the unfiltered and filtered data.
print('Before:', t['particle'].nunique())
print('After:', t1['particle'].nunique())

numParticles = t1['particle'].nunique()
#main loop which stores the data
for i in range (startFrame,endFrame-1):
    tv = tp.relate_frames(t1, i, i+1)
    for index, row in tv.iterrows():
        #extract the data from the dataframe 
        tempDX = row['dx']
        tempDY = row['dy']
        tempDT = row['dr']
        tempDir = row['direction']
        #replace NaN values with 0
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
    os.mkdir(outputPath)
except:
    print("Overwriting data - directory already exists")
with open(outputPath  / 'compactResults.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in compactDict.items():
        writer.writerow([key, value[0], value[1], value[2], value[3]])
try:
    os.mkdir(outputPath / "detailedResults") 
except:
    print("Overwriting data - directory already exists")
       
for miniDict in fullDict:
    with open(outputPath / "detailedResults"  / (str(miniDict) + '_detailedResult.csv'), 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in fullDict[miniDict].items():
            writer.writerow([key, value[0], value[1],value[2],value[3]])
trajFig = plt.figure()
trajPlot =  tp.plot_traj(t1, id = True)
trajFig.savefig(outputPath / 'traj.png')
idFig = plt.figure()
idPlot = tp.annotate(t1[t1['frame'] == startFrame], cleanFrames[startFrame])
idFig.savefig(outputPath  / "id.png")
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

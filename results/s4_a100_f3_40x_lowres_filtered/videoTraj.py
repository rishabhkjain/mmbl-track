from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
import matplotlib.pyplot as plt

# Optionally, tweak styles.
mpl.rc('figure',  figsize=(10, 5))
mpl.rc('image', cmap='gray')

import numpy as np
import pandas as pd
import trackpy as tp
import imageio
import glob
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import cv2


def cvtFig2Numpy(fig):
    canvas = FigureCanvas(fig)
    canvas.draw()
    
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = np.fromstring(canvas.tostring_rgb(), dtype='uint8').reshape(height.astype(np.uint32), width.astype(np.uint32), 3)    
    return image
    
def makevideoFromArray(movieName, array, fps=25):
    imageio.mimwrite(movieName, array, fps=fps);
    
imgs = glob.glob("path\\to\\your\\images\\*.png")
f = pd.read_pickle("path\\to\\your\\features\\features.pkl")
pred = tp.predict.NearestVelocityPredict(span=10)
t = tp.link_df(f, 5, memory=5)

arr = []
for i,idx in enumerate(imgs):
    frame = cv2.imread(idx)
    fig = plt.figure(figsize=(16, 8))
    plt.imshow(frame)
    axes = tp.plot_traj(t1.query('frame<={0}'.format(i)))
    axes.set_yticklabels([])
    axes.set_xticklabels([])
    axes.get_xaxis().set_ticks([])
    axes.get_yaxis().set_ticks([])
    arr.append(cvtFig2Numpy(fig))
    plt.close('all')
    
makevideoFromArray("yourName.mp4", arr, 3)
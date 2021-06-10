
# mmbl-track

Results are stored by name of input folder of the png stack. Compact results has the particle id, total displacement, total number of frames it was tracked across, direction list, frame list of where it was tracked and simple displacement. Total displacement is displacement along the specific path that the particle took (inaccurate sometimes due to oscillation detected back and forth). Simple displacement is the distance between the final and intial point for the swimmer. For each tracked particle, detailed results includes a frame by frame snapshot of the dx, dy, total displacement and change in direction.

## Setup

This repo is written in Python 2. You may need to install pip2.7 to install packages in Python 2 on your machine:  

`$ wget https://bootstrap.pypa.io/pip/2.7/get-pip.py    `     
`$ sudo python2.7 get-pip.py    `     
`$ which pip2.7   `      

If $ which pip2.7 returns a directory, then everything has installed correctly. Now you can use the following steps to set up a virtual environment with the correct packages for this repo. 

1. Create a virtual environment using:

`$ python -m virtualenv ./env    `     
`$ source env/bin/activate     `     

2. Install the required packages at the correct versions using:

`$ pip2.7 install -r requirements.txt    `
 
## Walkthrough 
Sample pipeline for analysis. Assume video files are grouped by amplitude for each sample in a test protocol. We will be analyzing test protocol a for this walkthrough. For example, `media/tpa/s1/a100` has multiple mp4 files inside it. All commands need to be run in the root directory where the scripts are located. 

  

1) `python createFolders.py --input media/tpa`
>This puts all of the videos found recursively in the `media/tpa` folder into their own folders and renames them for later scripts. NOTE: The video files in this directory must be .mp4 format.  
2) `python createPNGStack.py --input media/tpa/a100`
>This converts all of the videos located in `media/tpa/s1/a100` to a png stack. This command needs to be run individuall on all of the amplitude subfolders (ex. `media/tpa/s1/a75`)
3) `python blurAll.py --input media/tpa/ --fast 0`
>For blurring the videos and removing the excess markers. Creates a cloned folder with a png stack in same root directory of original folder containing png stack. For example `media/tpa/s1/a100/s1_a100_f1_v1/` will now have a blurred clone at `media/tpa/s1/a100/s1_a100_f1_v1_blurred`. If fast is set equal to 1, the script runs a lot faster but does not detect the fiducial markers and polystyrene beads (only removes timestamps). 
4) `mkdir results/tpa`
> Make the results directory
5) `python fullAnalysis.py --input media/tpa/ --output results/tpa`
>Run the analysis on the entire test protocol. Note, will put all results folder in `results/tpa` so might be helpful to run fullAnalysis on individual samples ie. `python fullAnalysis.py --input media/tpa/s1/ --output results/tpa/s1` for more organized files
6) `python graphAll.py --input results/tpa`
>Create plots from results and store them in the results directory

##  Items to Modify
### `createPNGStack.py`
1) Line 35, modify fps value (do *not* make higher than sampling fps)
### `fullAnalysis.py`
1) Line 46, startFrame for video analysis. Defaulted to 180 allowing time for setup

### `main.py`
1) Line 53, two key values are diameter and minmass, use getParameters jupyter notebook to calibrate for sample. 
2) Line 56, can modify maxChange and memory to filter velocities
3) Line 170, can turn labels on or off on the trajectory plot




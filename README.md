
# mmbl-track

Results are stored by name of input folder of the png stack. Compact results has the particle id, total displacement, total number of frames it was tracked across, direction list and the frame list of where it was tracked.For each tracked particle, detailed results includes a frame by frame snapshot of the dx, dy, total displacement and change in direction.

  
  

Sample pipeline for analysis. Assume video files are grouped by amplitude for each sample in a test protocol. We will be analyzing test protocol a for this walkthrough. For example, `media/tpa/s1/a100` has multiple mp4 files inside it. All commands need to be run in the root directory where the scripts are located. 

  

1) `python createFolders.py --input media/tpa`
>This puts all of the videos found recursively in the `media/tpa` folder into their own folders and renames them for later scripts. 
2) `python createPNGStack.py --input media/tpa/a100`
>This converts all of the videos located in `media/tpa/a100` to a png stack. This command needs to be run individuall on all of the amplitude subfolders (ex. `media/tpa/a75`)

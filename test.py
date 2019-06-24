
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="input path")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
ap.add_argument("-s", "--start", required=True,
	help="Start frame number")
args = vars(ap.parse_args())
print(args)
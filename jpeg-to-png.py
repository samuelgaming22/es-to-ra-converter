#!/usr/bin/python3

import argparse
import glob
import os
import sys

print("Bulk JPEG to PNG image converter")

parser = argparse.ArgumentParser(description='Convert JPEG images to PNG.')
parser.add_argument('inglobs', metavar='input.jpg', nargs='+', help='names of input files in JPEG format, supports glob syntax')
if len(sys.argv) < 2:
	parser.print_help()
	sys.exit(0)
args = parser.parse_args()

try:
	import PIL, PIL.ImageOps
except:
	print("Please install pillow: pip3 install pillow")
	sys.exit(1)

print("Converting...")
count = 0
skiped = 0

for inglob in args.inglobs:
	for imagefile in glob.glob(inglob):
		pngname = os.path.splitext(imagefile)[0]+'.png'
		if (not os.path.exists(pngname)):
			PIL.ImageOps.exif_transpose(PIL.Image.open(imagefile)).save(pngname)
			count += 1
		else:
			skiped += 1

print("{} image(s) converted, {} image(s) already exist.".format(count, skiped))

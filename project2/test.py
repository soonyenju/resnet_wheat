# coding: utf-8
from pathlib import Path
from spgeo import Raster
from utilities import Cutter

def main():
	path = Path("./data/test")
	for p in path.glob("*.tif"):
		print(p)
		raster = Raster(p.as_posix())
		data, profile = raster.read()
		cutter = Cutter(10)
		segs = cutter.segment(data, profile)
		for seg in segs:
			print(seg.shape)
			# print(profile)


if __name__ == '__main__':
	main()
	print("ok")

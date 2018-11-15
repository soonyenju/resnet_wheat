# coding: utf-8
import rasterio
import rasterio.features
import warnings
from rasterio.transform import Affine
from pathlib import Path
from numba import jit
import numpy as np
import time
from pprint import pprint
import torchvision.transforms as transforms
import torch
from PIL import Image


class Raster(object):
	"""docstring for Raster"""

	def __init__(self, raster_path):
		super(Raster, self).__init__()
		self.path = raster_path

	def __del__(self):
		pass

	def read(self):
		with rasterio.open(self.path) as src:
			data = src.read()
			profile = src.profile
			return data, profile

	def write(self, filedir, data, profile):
		# profile.update(dtype=rasterio.uint8, count=1, compress='lzw')

		with rasterio.open(filedir, 'w', **profile) as dst:
			dst.write(data.astype(rasterio.uint8), 1)

	# @jit
	def segment(self, data, profile, kernel_size=10, filldata=0):
		count  = profile["count"]
		height = profile["height"]
		width  = profile["width"]

		info = {
			"height": [],
			"width" : []
		}
		gen = self.__seg_gen__(height, width, kernel_size)

		for key in ["height", "width"]:
			info[key] = gen.__next__()
			if info[key][1] != 0:
				left = np.ones((count, height, info[key][1])) * profile["nodata"]
				right = np.ones((count, height, info[key][2])) * profile["nodata"]
				data = np.concatenate([left, data], axis=2)
				data = np.concatenate([data, right], axis=2)
		segs = []
		for r in np.arange(int(info["height"][0] - 1)):
			for c in np.arange(int(info["width"][0] - 1)):
				segs.append(data[:, r * kernel_size: (r + 1)*kernel_size,
                                    c * kernel_size: (c + 1)*kernel_size])
		return segs


	def __seg_gen__(self, height, width, kernel_size):
		for los in [height, width]:
			if los % kernel_size == 0:
				seg_num = los/kernel_size
				fill_left = fill_right = 0
				yield [seg_num, fill_left, fill_right]
			else:
				res = kernel_size - (los % kernel_size)
				if res % 2 == 0:
					fill_left = fill_right = res/2
					seg_num = (los + res) / kernel_size
				else:
					fill_left = res//2 + 1
					fill_right = res//2
					seg_num = (los + res) / kernel_size
				yield [seg_num, fill_left, fill_right]

			


def main():
	start = time.time()
	path = Path("./data/test")
	for p in path.glob("*.tif"):
		print(p)
	raster = Raster(p.as_posix())
	data, profile = raster.read()
	print(profile)
	raster.segment(data, profile)


if __name__ == '__main__':
	main()
	print("ok")

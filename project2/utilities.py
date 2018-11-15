# coding: utf-8
from numba import jit
import numpy as np


class Cutter(object):
	"""docstring for Cutter"""

	def __init__(self, kernel_size):
		super(Cutter, self).__init__()
		self.kernel_size = kernel_size
	def __del__(self):
		pass

	# @jit
	def segment(self, data, profile):
		count = profile["count"]
		height = profile["height"]
		width = profile["width"]

		info = {
			"height": [],
			"width": []
		}
		gen = self.__seg_gen__(height, width)

		for key in ["height", "width"]:
			info[key] = gen.__next__()
			if info[key][1] != 0:
				left = np.ones((count, height, info[key][1])) * profile["nodata"] # height?
				right = np.ones((count, height, info[key][2])) * profile["nodata"]
				data = np.concatenate([left, data], axis=2)
				data = np.concatenate([data, right], axis=2)
		segs = []
		profs = []
		for r in np.arange(info["height"][0] - 1):
			for c in np.arange(info["width"][0] - 1):
				segs.append(data[:, r * self.kernel_size: (r + 1)*self.kernel_size,
                                    c * self.kernel_size: (c + 1)*self.kernel_size])
				gt = list(profile["transform"])
				# original
				gt[3] = gt[3] - info["height"][1] * gt[5] # height
				gt[0] = gt[0] - info["width"][1] * gt[1] # width
				# loop
				gt[3] = gt[3] + r * gt[5]  # height
				gt[0] = gt[0] + c * gt[1] # width
				print(gt)
				exit(0)
		return segs

	def __seg_gen__(self, height, width):
		for los in [height, width]:
			if los % self.kernel_size == 0:
				seg_num = los/self.kernel_size
				fill_left = fill_right = 0
				yield [int(seg_num), int(fill_left), int(fill_right)]
			else:
				res = self.kernel_size - (los % self.kernel_size)
				if res % 2 == 0:
					fill_left = fill_right = res/2
					seg_num = (los + res) / self.kernel_size
				else:
					fill_left = res//2 + 1
					fill_right = res//2
					seg_num = (los + res) / self.kernel_size
				yield [int(seg_num), int(fill_left), int(fill_right)]


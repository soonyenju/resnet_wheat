# coding: utf-8
import rasterio
import rasterio.features
import warnings
from rasterio.transform import Affine
import numpy as np


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
			if profile["nodata"] == None:
				most_val = sorted([(np.sum(data == i), i) for i in set(data.flat)])[-1][-1]
				profile.update(nodata=most_val)
			return data, profile

	def write(self, filedir, data, profile):
		"""
		profile.update(dtype=rasterio.uint8, count=1, compress='lzw')
		with rasterio.open(filedir, 'w', **profile) as dst:
			dst.write(data.astype(rasterio.uint8), 1)
		"""
		with rasterio.open(filedir, 'w', **profile) as dst:
			dst.write(data.astype(rasterio.float64), 1)

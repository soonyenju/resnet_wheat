# coding: utf-8
import rasterio
import rasterio.features
import warnings
from rasterio.transform import Affine
from pathlib import Path


class Raster(object):
	"""docstring for Raster"""

	def __init__(self, raster_path):
		super(Raster, self).__init__()
		self.path = raster_path

	def __del__(self):
		pass

	def read(self):
		warnings.filterwarnings("ignore")
		dataset = rasterio.open(self.path)
		c, a, b, f, d, e = dataset.transform
		gt = Affine.from_gdal(c, a, b, f, d, e)
		proj = dataset.crs
		bands = dataset.count
		name = dataset.name
		mode = dataset.mode
		closed = dataset.closed
		width = dataset.width
		height = dataset.height
		bounds = dataset.bounds
		idtypes = {i: dtype for i, dtype in zip(dataset.indexes, dataset.dtypes)}
		# help(rasterio.features.shapes)
		print(dir(dataset))
		print(dataset.meta)
		print(dataset.affine)

	def get_dataset(self):
		pass

	def get_metadata(self):
		pass

def main():
	path = Path("./data/test")
	for p in path.glob("*.tif"):
		print(p)
	raster = Raster(p.as_posix())
	raster.read()


if __name__ == '__main__':
	main()
	print("ok")

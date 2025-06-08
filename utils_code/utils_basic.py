import pathlib
import pyproj

PROJECTED_PATH = r'C:\Users\Wei Zhou\Documents\zhouwei file\Github-Project\VeDa-Public-Transit-Network'
PROJECT_PATH = pathlib.Path(PROJECTED_PATH)

SG_PROJECTED_CRS = pyproj.CRS('EPSG:3414')

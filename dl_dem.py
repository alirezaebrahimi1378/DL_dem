import ee
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import os
import json

service_account = 'geo-test@geotest-317218.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'geotest-privkey.json')
ee.Initialize(credentials)

root = os.getcwd()

file_path = os.path.join(root,'grids_download.json')
with open(file_path, 'r') as file:
    lines = file.readlines()

grid_line = lines[0]
grid_list = json.loads(grid_line)['features']


def turn_image_to_raster(scale ,image, title, coordinate, folder='./data/grids'):
    # download image from google earth engine
    url = image.getDownloadURL(
        params={'name': title, 'scale': scale, 'region': coordinate, 'crs': 'EPSG:4326', 'filePerBand': False})
    zipurl = url
    print(title)
    # unzip tiff image
    if not os.path.isdir(folder):
        os.mkdir(folder)
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(folder)

STRM = ee.Image("USGS/SRTMGL1_003")
Terrain = ee.call('Terrain', STRM)
for item in grid_list:
    serial = item['properties']['serial']
    polygon = item['geometry']['coordinates']
    print('#'*20 , f'downloading grid {serial}' , '#'*20)
    polygon = ee.Geometry.Polygon(polygon)
    Slope = Terrain.select('slope').clip(polygon)
    turn_image_to_raster(scale = 10,image=Slope, title = f'dem_{serial}', coordinate=polygon)

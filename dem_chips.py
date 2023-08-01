import os
import rasterio
from rasterio.windows import Window
from PIL import Image

# Open the tiff image file
root = os.getcwd()
input_path = os.path.join(root , 'data/grids')
output_path = os.path.join(root , 'data/chips')
if not os.path.isdir(output_path):
    os.mkdir(output_path)
os.chdir(input_path)
images = os.listdir()
os.chdir(output_path)

def get_serial(path):
    path = path.replace('_' , ' ')
    path = path.replace('/' , ' ')
    path = path.replace('.' , ' ')
    serial = path.split()[-2]
    return serial

for image in images :
    image_path = os.path.join(input_path , image)
    serial = get_serial(image_path)
    num = 0
    with rasterio.open(image_path) as src:

        # Get the size of the tiff image
        height = src.height
        width = src.width

        # Calculate the number of rows and columns of image chips
        num_rows = height // 512
        num_cols = width // 512

        # Check if there are any remaining pixels in the last row and column
        rem_rows = height % 512
        rem_cols = width % 512

        if rem_rows < 10 :
            height_loop = height - rem_rows
        else:
            width_loop = width
        if rem_cols <10 :
            width_loop = width - rem_cols
        else:
            width_loop = width

        # Iterate over the image chips
        for y in range(0, height_loop , 512):
            for x in range(0, width_loop , 512):
                # Set the window size for the chip
                if x == 2048 and y != 1536:
                    window = Window(x, y, width - x, 512)
                elif x != 2048 and y == 1536 :
                    window = Window(x, y, 512, height - y)
                elif x == 2048 and y == 1536 :
                    window = Window(x, y, width - x, height - y)
                else :
                    window = Window(x, y,512, 512)

                # Read the chip data and metadata
                data = src.read(window=window)
                transform = src.window_transform(window)
                crs = src.crs

                # Create a PIL image from the chip data
                img = Image.fromarray(data.squeeze())

                # Save the chip image with the correct CRS
                num = num + 1
                chip_path = f"dem_{serial}_{num}.tif"
                with rasterio.open(chip_path, 'w', driver='GTiff',
                                   width=window.width, height=window.height,
                                   count=1, dtype=data.dtype,
                                   crs=crs, transform=transform) as dst:
                    dst.write(data)
















































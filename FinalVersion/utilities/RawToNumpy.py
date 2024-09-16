import numpy as np
import os

def RawToNumpy(path,height,width):
    height=int(height)
    width=int(width)


    # Size of the raw image file in bytes
    file_size = os.path.getsize(path)
    print(file_size)

    cut=file_size-(height*width)
    print(cut)


    # Read the raw image data into a NumPy array
    with open(path, 'rb') as f:
        raw_image_data = np.fromfile(f, dtype=np.uint8)

    if cut>=0:
        raw_image_data=raw_image_data[cut:]
    else:
        height=int(file_size/width)
        cut = file_size - (height * width)
        raw_image_data=raw_image_data[:-cut]


    # Reshape the flat array into a 3D array (height, width, channels)
    image_array = raw_image_data.reshape((height, width))
    return image_array







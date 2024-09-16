import cv2
from FinalVersion.utilities.RawToNumpy import RawToNumpy



def ImageProcessor(image,width,height):
    #be careful because the paths have (Secondary) or (Primary) at the end
    if width==0:
        image = cv2.imread(image[:-14], 1)[:,:,0]
    else:
        image =RawToNumpy(image[:-14],height,width)

    return image
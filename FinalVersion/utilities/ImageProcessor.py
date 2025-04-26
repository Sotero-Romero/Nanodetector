import cv2
from FinalVersion.utilities.RawToNumpy import RawToNumpy



def ImageProcessor(image,width,height,addition=14):

    #TODO: check if this remains true:
    #be careful because the paths have (Secondary) or (Primary) at the end
    if addition!=0:
        image=image[:-addition]


    if width==0:
        image = cv2.imread(image, 1)[:,:,0]
    else:
        image =RawToNumpy(image,height,width)

    return image
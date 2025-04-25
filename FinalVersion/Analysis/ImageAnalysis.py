import os
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage as ndi
from skimage import feature
import cv2 as cv
import PIL
import pandas as pd
import pyarrow.feather as feather
from scipy.spatial import KDTree






def AnalyseImage(original_image,canny_minimum, canny_maximum, canny_ksize,canny_sigma,gaussian_fidelity,gaussian_range,pore_cut_off=3):
    #return original_image
    original_image = original_image.copy()
    image_min = original_image.min()
    image_max = original_image.max()
    range_val = image_max - image_min

    if range_val == 0:
        original_image = np.zeros_like(original_image)
    else:
        original_image = ((original_image - image_min) / range_val * 255).astype(np.uint8)

    original_image[original_image == 255] = 254
    original_image = np.pad(original_image, 1, mode='constant', constant_values=255)
    original_image = original_image.astype('uint8')
    raw_image = original_image.copy()

    inner_distance_map = ndi.distance_transform_edt(raw_image != 255)
    inner_distance_map = np.round(inner_distance_map, decimals=2)
    inner_distance_map, raw_image, original_image = inner_distance_map[1:-1, 1:-1], raw_image[1:-1,
                                                                                    1:-1], original_image[1:-1, 1:-1]

    bright_edges = np.full_like(raw_image, 0)
    bright_edges[raw_image > 210] = 200

    raw_image[bright_edges == 200] = np.mean(raw_image)
    bright_distance_map = ndi.distance_transform_edt(raw_image < 200)
    bright_distance_map = np.round(bright_distance_map)
    gaussian_blurred = cv.GaussianBlur(raw_image, (canny_ksize, canny_ksize), canny_sigma)
    edges = cv.Canny(gaussian_blurred, canny_minimum, canny_maximum)
    canny_detection = cv.dilate(edges, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3)), iterations=2)

    gaussian_detection = np.full_like(raw_image, 200)
    gaussian_ranges = [gaussian_range]

    for gaussian_range in gaussian_ranges:
        new_raw = raw_image.copy()
        gaussian_filt = cv.adaptiveThreshold(raw_image, 200, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,
                                             gaussian_range, gaussian_fidelity)
        gaussian_filt[inner_distance_map < gaussian_range] = 200
        gaussian_filt[bright_distance_map < (300 / gaussian_range)] = 200
        gaussian_detection[gaussian_filt == 0] = 0
        new_raw[gaussian_filt == 0] = 255
        del new_raw, gaussian_filt

    del inner_distance_map, bright_distance_map

    combined_detection = np.full_like(raw_image, 200)

    combined_detection[canny_detection == 255] = 0
    combined_detection[gaussian_detection == 0] = 0

    inverted_array = np.where(combined_detection == 200, 0, np.where(combined_detection == 0, 200, combined_detection))
    filled_detection = ndi.binary_fill_holes(inverted_array).astype(int)
    filled_detection = np.where(filled_detection == 200, 0,
                                np.where(filled_detection == 0, 200, filled_detection)).astype(np.uint8)
    filled_detection = cv.dilate(filled_detection, cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)), iterations=3)
    filled_detection[gaussian_detection == 0] = 0
    filled_detection[bright_edges == 200] = 200
    filled_detection[filled_detection == 1] = 0
    del gaussian_detection, canny_detection

    inverted_array = np.where(filled_detection == 200, 0, np.where(filled_detection == 0, 200, filled_detection))
    filled_detection = ndi.binary_fill_holes(inverted_array).astype(int)
    filled_detection = np.where(filled_detection == 200, 0,
                                np.where(filled_detection == 0, 200, filled_detection)).astype(np.uint8)
    filled_detection[filled_detection == 1] = 0
    final_pores = np.full_like(raw_image, 200)
    rows, cols = raw_image.shape
    del raw_image, inverted_array, bright_edges


    for i in range(rows):
        for j in range(cols):
            if filled_detection[i, j] == 0:
                filled_detection[i, j] = 10

                Marked_List = []
                Unmarked_List = [[i, j]]

                List_Boundary = []
                P = 0

                while len(Unmarked_List) > 0:

                    k1, k2 = Unmarked_List[-1]

                    Marked_List.append(Unmarked_List[-1])
                    Unmarked_List.pop(-1)

                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = k1 + dx, k2 + dy
                        if 0 <= nx < rows and 0 <= ny < cols and filled_detection[nx, ny] == 0:
                            filled_detection[nx, ny] = 10
                            Unmarked_List.append([nx, ny])

                        elif (0 <= nx < rows and 0 <= ny < cols) == False:
                            P = P + 1
                            List_Boundary.append([k1, k2])

                        elif filled_detection[nx, ny] == 200:
                            P = P + 1
                            List_Boundary.append([k1, k2])

                A = len(Marked_List)

                try:
                    roundness = 4 * math.pi * A / (P ** 2)
                    pore_value = roundness * A

                    if pore_value >= pore_cut_off and roundness > 0.005:

                        if roundness < 0.3:
                            #Crack
                            for x, y in Marked_List:
                                final_pores[x, y] = 0
                        else:
                            #Pore
                            for x, y in Marked_List:
                                final_pores[x, y] = 0


                except ZeroDivisionError:
                    continue


    return (final_pores)





#TODO: finish the function, maybe make another one just for saving the data
def FullAnalyseImage(original_image,mean_weight=90,mean_range=11,pore_cut_off=3, Fidelity_Base=50):


    # Load and process the original image
    PIL.Image.MAX_IMAGE_PIXELS = None
    original_image[original_image == 255] = 254
    original_image = np.pad(original_image, 1, mode='constant', constant_values=255)
    raw_image = original_image.copy()

    #Skelet 90 is vertical

    # Distance transform
    inner_distance_map = ndi.distance_transform_edt(raw_image != 255)
    inner_distance_map = np.round(inner_distance_map, decimals=2)
    inner_distance_map, raw_image, original_image = inner_distance_map[1:-1, 1:-1], raw_image[1:-1, 1:-1], original_image[1:-1, 1:-1]



    bright_edges=np.full_like(raw_image, 0)
    bright_edges[raw_image>170]=200

    #save_image(bright_edges,'Bright Edges Identified.png')

    raw_image[bright_edges==200]=np.mean(raw_image)

    #save_image(raw_image,'New Raw Image.png')

    # Distance transform
    bright_distance_map = ndi.distance_transform_edt(raw_image < 200)
    bright_distance_map = np.round(bright_distance_map)

    #save_image(bright_distance_map,'Bright Distance Map.png')

    #print(f"Type is {type(bright_distance_map)}\n")
    #print(f"np.unique is {np.unique(bright_distance_map)}\n")

    # Canny edge detection
    mean_kernel = np.ones((mean_range, mean_range)) / mean_weight
    smoothed_image = ndi.convolve(raw_image, mean_kernel, mode='nearest')
    canny_detection = feature.canny(smoothed_image).astype(np.uint8)
    canny_detection = cv.dilate(canny_detection, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3)), iterations=2)


    # Gaussian detection
    gaussian_detection = np.full_like(raw_image, 200)
    gaussian_ranges = [31,151]

    for gaussian_range in gaussian_ranges:
        if gaussian_range==31:
            Fidelity = Fidelity_Base
        if gaussian_range==151:
            Fidelity = Fidelity_Base + 10

        new_raw = raw_image.copy()
        gaussian_filter = cv.adaptiveThreshold(raw_image, 200, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, gaussian_range, Fidelity)
        gaussian_filter[inner_distance_map < gaussian_range] = 200
        gaussian_filter[bright_distance_map < (200/gaussian_range)] = 200
        gaussian_detection[gaussian_filter == 0] = 0
        new_raw[gaussian_filter==0]=255
        del new_raw


    # Combined detection
    combined_detection = np.full_like(raw_image, 200)
    combined_detection[canny_detection == 1] = 0
    combined_detection[gaussian_detection == 0] = 0


    # Fill detected pores
    inverted_array = np.where(combined_detection == 200, 0, np.where(combined_detection == 0, 200, combined_detection))
    filled_detection = ndi.binary_fill_holes(inverted_array).astype(int)
    filled_detection = np.where(filled_detection == 200, 0, np.where(filled_detection == 0, 200, filled_detection)).astype(np.uint8)
    filled_detection = cv.dilate(filled_detection, cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)), iterations=2)
    filled_detection[gaussian_detection == 0] = 0

    #save_image(filled_detection, 'Filled Pores Before Selection and with Bright Edges.png')

    filled_detection[bright_edges==200]=200
    filled_detection[filled_detection==1]=0

    inverted_array = np.where(filled_detection == 200, 0, np.where(filled_detection == 0, 200, filled_detection))
    filled_detection = ndi.binary_fill_holes(inverted_array).astype(int)
    filled_detection = np.where(filled_detection == 200, 0, np.where(filled_detection == 0, 200, filled_detection)).astype(np.uint8)
    filled_detection[filled_detection==1]=0


    # Filter pores based on circularity, area, and smoothness
    final_cracks = np.full_like(raw_image, 200)
    final_gas_pores = np.full_like(raw_image, 200)
    final_lack_of_fusion = np.full_like(raw_image, 200)

    rows, cols = raw_image.shape

    raw_image = original_image.copy()



    # Initialize an empty DataFrame with the required columns--------------------------------
    columns = ['Pore ID', 'Pore Centroid', 'Pixels in Pore', 'Pore Area', 'Pore Perimeter', 'Pore Roundness', 'Pore Orientation', 'Pore Value', 'Pore Identity']
    df = pd.DataFrame(columns=columns)


    feather_path = os.path.join( "BackUp", "backup.feather")

    batch_size = 1000  # Adjust batch size as needed
    batch_data = []

    for i in range(rows):
        for j in range(cols):
            if filled_detection[i, j] == 0:
                filled_detection[i, j] = 10

                Marked_List = []
                Unmarked_List = [[i, j]]

                List_Boundary = []
                P = 0

                while len(Unmarked_List) > 0:
                    k1, k2 = Unmarked_List[-1]

                    Marked_List.append(Unmarked_List[-1])
                    Unmarked_List.pop(-1)

                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = k1 + dx, k2 + dy
                        if 0 <= nx < rows and 0 <= ny < cols and filled_detection[nx, ny] == 0:
                            filled_detection[nx, ny] = 10
                            Unmarked_List.append([nx, ny])
                        elif (0 <= nx < rows and 0 <= ny < cols) == False:
                            P = P + 1
                            List_Boundary.append([k1, k2])
                        elif filled_detection[nx, ny] == 200:
                            P = P + 1
                            List_Boundary.append([k1, k2])

                A = len(Marked_List)
                X_vals = [element[0] for element in Marked_List]
                Y_vals = [element[1] for element in Marked_List]

                try:
                    roundness = 4 * math.pi * A / (P**2)
                    pore_value = roundness * A
                    centroid_point = [sum(X_vals) // A, sum(Y_vals) // A]

                    if pore_value >= pore_cut_off and roundness >= 0.005:
                        List_Boundary = np.array(List_Boundary)

                        if roundness > 0.3:  # ellipse fitting
                            ellipse = cv.fitEllipse(List_Boundary)
                            center, axes, angle = ellipse
                            if angle < 0:
                                angle += 180
                        else:
                            coordinates_array = np.array(List_Boundary)
                            distances = np.linalg.norm(coordinates_array[:, None] - coordinates_array, axis=-1)
                            idx_max = np.unravel_index(np.argmax(distances), distances.shape)
                            point1, point2 = List_Boundary[idx_max[0]], List_Boundary[idx_max[1]]
                            filled_detection[point1[0], point1[1]] = 100
                            filled_detection[point2[0], point2[1]] = 50
                            angle = round(math.atan(float(-(point1[0] - point2[0]) / (point1[1] - point2[1]))) * 180 / math.pi)
                            if angle < 0:
                                angle += 180


                        if roundness < 0.3:
                            for x, y in Marked_List:
                                raw_image[x, y] = 255
                                final_cracks[x, y] = 0
                                category="Crack"
                        else:

                            for x, y in Marked_List:
                                raw_image[x, y] = 255
                                final_gas_pores[x, y] = 0
                                category="Pore"


                        batch_data.append({
                            'Pore ID': f"P_{centroid_point[0]}_{centroid_point[1]}",
                            'Pore Centroid': centroid_point,
                            'Pixels in Pore': Marked_List,
                            'Pore Area': A,
                            'Pore Perimeter': P,
                            'Pore Roundness': roundness,
                            'Pore Orientation': angle,
                            'Pore Value': pore_value,
                            'Pore Identity': category,
                        })

                        if len(batch_data) >= batch_size:
                            batch_df = pd.DataFrame(batch_data)
                            if os.path.exists(feather_path):
                                existing_df = feather.read_feather(feather_path)
                                batch_df = pd.concat([existing_df, batch_df], ignore_index=True)
                            feather.write_feather(batch_df, feather_path)
                            batch_data = []

                except ZeroDivisionError:
                    continue

    # Final save for any remaining data
    if batch_data:
        batch_df = pd.DataFrame(batch_data)
        if os.path.exists(feather_path):
            existing_df = feather.read_feather(feather_path)
            batch_df = pd.concat([existing_df, batch_df], ignore_index=True)
        feather.write_feather(batch_df, feather_path)

    print("Pore Filtering 100% complete")


    return raw_image








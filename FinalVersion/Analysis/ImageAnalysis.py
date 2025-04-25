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
def FullAnalyseImage(original_image,canny_minimum, canny_maximum, canny_ksize,canny_sigma,gaussian_fidelity,gaussian_range,pore_cut_off=3):
    original_image = original_image.copy()
    original_image = (
                (original_image - original_image.min()) / (original_image.max() - original_image.min()) * 255).astype(
        np.uint8)
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

    columns = ['Pore ID', 'Pore Centroid', 'Pixels in Pore', 'Pore Area', 'Pore Perimeter', 'Pore Roundness',
               'Pore Orientation', 'Pore Value', 'Pore Identity']
    df = pd.DataFrame(columns=columns)
    name_of_feather = "backup"
    feather_path = os.path.join("BackUp", f'{name_of_feather}.feather')
    df.to_feather(feather_path)
    batch_size = 1000
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
                    roundness = 4 * math.pi * A / (P ** 2)
                    pore_value = roundness * A
                    centroid_point = [sum(X_vals) // A, sum(Y_vals) // A]

                    if pore_value >= pore_cut_off and roundness > 0.005:

                        List_Boundary = np.array(List_Boundary)

                        if roundness > 0.3 and len(
                                List_Boundary) > 5:
                            ellipse = cv.fitEllipse(List_Boundary)
                            center, axes, angle = ellipse
                            ellipse = ((center[1], center[0]), axes, angle)
                            if angle < 0:
                                angle += 180

                        else:

                            coordinates_array = np.array(List_Boundary).astype(np.uint8)

                            if len(coordinates_array) >= 2:

                                tree = KDTree(coordinates_array)

                                point1_idx, point2_idx = tree.query(coordinates_array, k=2)[1].max(axis=0)

                                point1, point2 = coordinates_array[point1_idx], coordinates_array[point2_idx]

                                filled_detection[point1[0], point1[1]] = 100
                                filled_detection[point2[0], point2[1]] = 50

                                point1 = point1.astype(np.float64)
                                point2 = point2.astype(np.float64)

                                angle = round(
                                    math.atan2(
                                        float(point1[0] - point2[0]),
                                        float(point1[1] - point2[1])
                                    )
                                    * 180 / math.pi
                                )

                                if angle < 0:
                                    angle += 180

                            else:
                                angle = 0

                        new_marked_list = []

                        for element in Marked_List:
                            s = [element[0], element[1]]
                            new_marked_list.append(s)

                        if roundness < 0.3:
                            for x, y in Marked_List:
                                final_pores[x, y] = 0
                                category = "Crack"
                        else:
                            for x, y in Marked_List:
                                final_pores[x, y] = 0
                                category = "Pore"

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

    if batch_data:
        batch_df = pd.DataFrame(batch_data)
        if os.path.exists(feather_path):
            existing_df = feather.read_feather(feather_path)
            batch_df = pd.concat([existing_df, batch_df], ignore_index=True)
        feather.write_feather(batch_df, feather_path)

    return (final_pores)









from PIL import Image
from scipy import ndimage as ndi
from skimage import feature
import cv2 as cv
import PIL
import itertools
import numpy as np
import heapq
from FinalVersion.utilities.ImageProcessor import ImageProcessor
import matplotlib.pyplot as plt

points_inside=[[2500,2500]]
points_outside=[[1,1],[80,2],[80,90]]
boundary_start=[600,20]
boundary_end=[580,7000]

points=[(600,20),(440,1700),(430,2000),(300,4000),(580,7000)]


def Isolate_Boundary(images_paths,points, points_inside, points_outside,mean_weight=350,mean_range=30,width=0,height=0):
    original_image=ImageProcessor(images_paths[0], width, height)
    overall_binary = np.zeros(np.shape(original_image))
    del original_image

    #TODO:change this points
    boundary_start=list(points[0][0][0])
    boundary_end=list(points[0][0][-1])

    for path,boundaries in zip(images_paths,points):
        img= ImageProcessor(path, width, height)
        for boundary in boundaries:
            binary = IsolateBoundary(img, boundary, mean_weight, mean_range)
            del img
            overall_binary[binary == 255] = 255
            del binary

    # plt.imshow(overall_binary)
    # plt.axis('off')
    # plt.rcParams['image.interpolation'] = 'nearest'
    # plt.savefig(rf'C:\Users\Tudor D\OneDrive\Desktop\Overall Binary.png', dpi=5000)
    # plt.close()

    #start_binary=overall_binary[boundary_start[0]-10:boundary_start[0]+10,boundary_start[1]-10:boundary_start[1]+10]

    #plt.imshow(start_binary)
    ## plt.axis('off')
    #plt.rcParams['image.interpolation'] = 'nearest'
    #plt.savefig(rf'C:\Users\Tudor D\OneDrive\Desktop\Start Binary.png')
    #plt.close()

    #end_binary = overall_binary[boundary_end[0] - 10:boundary_end[0] + 10,              boundary_end[1] - 10:boundary_end[1] + 10]

    #plt.imshow(end_binary)
    # plt.axis('off')
    #plt.rcParams['image.interpolation'] = 'nearest'
    #plt.savefig(rf'C:\Users\Tudor D\OneDrive\Desktop\End Binary.png')
    #plt.close()

    print("filling")
    Array = ConnectingBoundaryFilling(overall_binary, boundary_start, boundary_end, points_inside, points_outside)

    #plt.imshow(Array)
    # plt.axis('off')
    #plt.rcParams['image.interpolation'] = 'nearest'
    #plt.savefig(rf'C:\Users\Tudor D\OneDrive\Desktop\Array Image.png', dpi=1000)
    #plt.close()

    #print(f"Np.unique for Array is {np.unique(Array)}")

    original_image = ImageProcessor(images_paths[0], width, height)
    original_image[Array == 1] = 255

    #plt.imshow(original_image)
    # plt.axis('off')
    #plt.rcParams['image.interpolation'] = 'nearest'
    #plt.savefig(rf'C:\Users\Tudor D\OneDrive\Desktop\Filled Image.png', dpi=1000)
    #plt.close()

    return original_image











# Load and process the original image
PIL.Image.MAX_IMAGE_PIXELS = None



def ConnectingBoundaryFilling(binary,boundary_start,boundary_end,points_inside,points_outside):
    # binary must be a binary array of only the boundary. The boundary is drawn with 255 and the background is 0
    # boundary start and end are the first and last points from the boundary detection process
    # points inside is a list of points inside the area that needs to be analysed
    # points outside need to be removed by boundary isolation. AKA the background

    final_boundary_filled = None

    # First try is to see if the boundary is complete as it is and can be just filled

    Initial_boundary=fill_and_reverse(binary)

    if Initial_boundary!=None:
        print("Initial boundary was already complete")
        return Initial_boundary

    # If this doesn't work, we try drawing a straight line between the boundary_start and boundary_end

    connected_line = draw_line(binary, boundary_start, boundary_end)

    dilated_line = cv.dilate(connected_line, cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)), iterations=1)

    filled_boundary = ndi.binary_fill_holes(dilated_line).astype(int)

    if check_points(filled_boundary, points_inside, points_outside) == True:
        final_boundary_filled = filled_boundary

        return final_boundary_filled

    inverted_array = np.where(filled_boundary == 1, 0, np.where(filled_boundary == 0, 1, filled_boundary))

    if check_points(inverted_array, points_inside, points_outside) == True:
        final_boundary_filled = inverted_array

        return final_boundary_filled

    del connected_line
    del dilated_line
    del filled_boundary
    del inverted_array

    # If this doesn't work, we try clipping these points to the 4 boundary walls

    distances = []

    distances.append(f'AU-{boundary_start[0]}')
    distances.append(f'AD-{np.shape(binary)[0] - boundary_start[0]}')
    distances.append(f'AL-{boundary_start[1]}')
    distances.append(f'AR-{np.shape(binary)[1] - boundary_start[1]}')

    distances.append(f'BU-{boundary_end[0]}')
    distances.append(f'BD-{np.shape(binary)[0] - boundary_end[0]}')
    distances.append(f'BL-{boundary_end[1]}')
    distances.append(f'BR-{np.shape(binary)[1] - boundary_end[1]}')

    a_distances = [d for d in distances if d.startswith('A')]
    b_distances = [d for d in distances if d.startswith('B')]

    all_pairs = list(itertools.product(a_distances, b_distances))

    sorted_pairs = sorted(all_pairs, key=get_distance)

    for i in range(len(sorted_pairs)):
        binary_temp = binary.copy()
        pair = sorted_pairs[i]
        direction_1 = list(pair[0])[1]
        direction_2 = list(pair[1])[1]

        if direction_1 == 'U':

            binary_temp[0:boundary_start[0], boundary_start[1]] = 255

            if direction_2 == 'U':
                binary_temp[0:boundary_end[0], boundary_end[1]] = 255
            elif direction_2 == 'D':
                binary_temp[boundary_end[0]:np.shape(binary)[0], boundary_end[1]] = 255
            elif direction_2 == 'L':
                binary_temp[boundary_end[0], 0:boundary_end[1]] = 255
            elif direction_2 == 'R':
                binary_temp[boundary_end[0], boundary_end[1]:np.shape(binary)[1]] = 255

        elif direction_1 == 'D':

            binary_temp[boundary_start[0]:np.shape(binary)[0], boundary_start[1]] = 255

            if direction_2 == 'U':
                binary_temp[0:boundary_end[0], boundary_end[1]] = 255
            elif direction_2 == 'D':
                binary_temp[boundary_end[0]:np.shape(binary)[0], boundary_end[1]] = 255
            elif direction_2 == 'L':
                binary_temp[boundary_end[0], 0:boundary_end[1]] = 255
            elif direction_2 == 'R':
                binary_temp[boundary_end[0], boundary_end[1]:np.shape(binary)[1]] = 255

        elif direction_1 == 'L':

            binary_temp[boundary_start[0], 0:boundary_start[1]] = 255

            if direction_2 == 'U':
                binary_temp[0:boundary_end[0], boundary_end[1]] = 255
            elif direction_2 == 'D':
                binary_temp[boundary_end[0]:np.shape(binary)[0], boundary_end[1]] = 255
            elif direction_2 == 'L':
                binary_temp[boundary_end[0], 0:boundary_end[1]] = 255
            elif direction_2 == 'R':
                binary_temp[boundary_end[0], boundary_end[1]:np.shape(binary)[1]] = 255


        elif direction_1 == 'R':

            binary_temp[boundary_start[0], boundary_start[1]:np.shape(binary)[1]] = 255

            if direction_2 == 'U':
                binary_temp[0:boundary_end[0], boundary_end[1]] = 255
            elif direction_2 == 'D':
                binary_temp[boundary_end[0]:np.shape(binary)[0], boundary_end[1]] = 255
            elif direction_2 == 'L':
                binary_temp[boundary_end[0], 0:boundary_end[1]] = 255
            elif direction_2 == 'R':
                binary_temp[boundary_end[0], boundary_end[1]:np.shape(binary)[1]] = 255

        # print(f"Direction 1 is {direction_1}, Direction 2 is {direction_2}")

        connected_walls = walls_function(binary_temp, '0')
        fill_and_reverse(connected_walls)
        # save_image(connected_walls,f'connected_walls {direction_1},{direction_2}.png')
        connected_walls = walls_function(binary_temp, '1')
        array=fill_and_reverse(connected_walls)

        validity = True

        try:

            for l in range(len(points_inside)):
                point_inside = points_inside[l]

                if array[point_inside[0], point_inside[1]] != 0:
                    # print(f"Failed at point {point_inside} where value is {array[point_inside[0],point_inside[1]]}")
                    validity = False

            for m in range(len(points_outside)):
                point_outside = points_outside[m]

                if array[point_outside[0], point_outside[1]] == 0:
                    # print(f"Failed at point {point_outside} where value is {array[point_outside[0], point_outside[1]]}")
                    validity = False

            if validity == True:
                return array

        except:
            pass

    # Note, this process could fail in which case the retured array is None


    return final_boundary_filled

def draw_line(image, start, end, value=255):

    image=image.copy()

    x0, y0 = start
    x1, y1 = end

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        image[x0, y0] = value
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return image

def check_points(array,points_inside,points_outside):

    validity=True

    for i in range(len(points_inside)):
        point_inside=points_inside[i]

        if array[point_inside[0],point_inside[1]] != 0:
            #print(f"Failed at point {point_inside} where value is {array[point_inside[0],point_inside[1]]}")
            validity=False

    for j in range(len(points_outside)):
        point_outside = points_outside[j]

        if array[point_outside[0], point_outside[1]] == 0:
            #print(f"Failed at point {point_outside} where value is {array[point_outside[0], point_outside[1]]}")
            validity = False

    return validity

# Function to extract the numerical distance from the string
def get_distance(pair):
    a_distance = int(pair[0].split('-')[1])
    b_distance = int(pair[1].split('-')[1])
    return a_distance + b_distance


def help_function(array,start_point,end_point):

    final_boundary_filled=None

    connected_line = draw_line(array, start_point, end_point)
    dilated_line = cv.dilate(connected_line, cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)), iterations=1)
    filled_boundary = ndi.binary_fill_holes(dilated_line).astype(int)

    if check_points(filled_boundary, points_inside, points_outside) == True:
        final_boundary_filled = filled_boundary
    inverted_array = np.where(filled_boundary == 1, 0, np.where(filled_boundary == 0, 1, filled_boundary))
    if check_points(inverted_array, points_inside, points_outside) == True:
        final_boundary_filled = inverted_array

    return final_boundary_filled

def fill_and_reverse(image):
    image=image.copy()
    #print(np.unique(image))
    image[image==255]=1
    filled_boundary = ndi.binary_fill_holes(image).astype(int)

    inverted_array = np.where(filled_boundary == 1, 0, np.where(filled_boundary == 0, 1, filled_boundary)).astype(np.uint8)
    Shrunk_image = cv.dilate(inverted_array, cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)), iterations=1)
    filled_boundary = np.where(Shrunk_image == 200, 0, np.where(Shrunk_image == 0, 200, Shrunk_image))

    final_boundary_filled=None
    if check_points(filled_boundary, points_inside, points_outside) == True:
        final_boundary_filled = filled_boundary
        return final_boundary_filled
    inverted_array = np.where(filled_boundary == 1, 0, np.where(filled_boundary == 0, 1, filled_boundary))
    if check_points(inverted_array, points_inside, points_outside) == True:
        final_boundary_filled = inverted_array
        return final_boundary_filled
    return final_boundary_filled
def walls_function(image,Option):
    image[image==255]=1
    second_image = image.copy()
    second_image[second_image==255]=1
    second_image[:, 0] = 1
    second_image[0, :] = 1
    second_image[np.shape(image)[0] - 1, :] = 1
    second_image[:, np.shape(image)[1] - 1] = 1


    for i in range(np.shape(second_image)[0]):
        for j in range(np.shape(second_image)[1]):
            if image[i, j] == 1:

                if i == 0:
                    if Option == "1":
                        second_image[0, j + 1] = 0
                        return second_image
                    else:
                        second_image[0, j - 1] = 0
                        return second_image

                elif j == 0:
                    if Option == "1":
                        second_image[i + 1, 0] = 0
                        return second_image
                    else:
                        second_image[i - 1, 0] = 0
                        return second_image

                elif i == np.shape(image)[0] - 1:
                    if Option == "1":
                        second_image[i, j + 1] = 0
                        return second_image
                    else:
                        second_image[i, j - 1] = 0
                        return second_image

                elif j == np.shape(image)[1] - 1:
                    if Option == "1":
                        second_image[i + 1, j] = 0
                        return second_image
                    else:
                        second_image[i - 1, j] = 0
                        return second_image

def IsolateBoundary(original_image,points,mean_weight,mean_range):
    #TODO: Changeeeeee arguments "mean"

    raw_image = original_image.copy()

    raw_image[raw_image==255]=254


    mean_kernel = np.ones((mean_range, mean_range)) / mean_weight

    print("raw_image shape:", raw_image.shape)
    print("mean_kernel shape:", mean_kernel.shape)

    smoothed_image = ndi.convolve(raw_image, mean_kernel, mode='nearest')
    canny_detection = feature.canny(smoothed_image).astype(np.uint8)
    canny_detection = cv.dilate(canny_detection, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3)), iterations=1)

    Domain_distance = 1

    for point in range(len(points) - 1):

        point_1 = points[point]
        point_2 = points[point + 1]

        print(point_1)
        print(point_2)

        raw_image[points[point]] = 255

        raw_image[point_1[0],point_1[1]] = 255
        raw_image[point_2[0], point_2[1]] = 255

        Area_of_Interest = raw_image[
                           min(point_1[0], point_2[0]) - Domain_distance:max(point_1[0], point_2[0]) + Domain_distance,
                           min(point_1[1], point_2[1]) - Domain_distance:max(point_1[1], point_2[1]) + Domain_distance]



        new_point_1 = (point_1[0] - (min(point_1[0], point_2[0]) - Domain_distance),
                       point_1[1] - (min(point_1[1], point_2[1]) - Domain_distance))
        new_point_2 = (point_2[0] - (min(point_1[0], point_2[0]) - Domain_distance),
                       point_2[1] - (min(point_1[1], point_2[1]) - Domain_distance))

        mask = canny_detection[
                           min(point_1[0], point_2[0]) - Domain_distance:max(point_1[0], point_2[0]) + Domain_distance,
                           min(point_1[1], point_2[1]) - Domain_distance:max(point_1[1], point_2[1]) + Domain_distance]

        mask_shape = mask.shape

        if new_point_2[1] != new_point_1[1]:

            m = (new_point_2[0] - new_point_1[0]) / (new_point_2[1] - new_point_1[1])

        else:

            m = -100

        c = new_point_1[0] - m * new_point_1[1]

        # Create an array of x and y indices corresponding to each element in the image
        y_indices, x_indices = np.indices(mask_shape)

        # Calculate the distance of each point in the image from the line
        distance = np.abs((m * x_indices - y_indices + c)) / np.sqrt(m ** 2 + 1)

        min_val = np.min(distance)
        max_val = np.max(distance)

        x = max_val / 3 + 300

        # Update the image where the distance exceeds the threshold
        mask[distance > x] = 50

        # Normalize the array in place
        distance -= min_val
        distance *= 255.0 / (max_val - min_val)


        # Initialize distance, visited, and path arrays
        rows, cols = mask.shape
        distance = np.full_like(mask, fill_value=np.inf, dtype=float)
        visited = np.zeros_like(mask, dtype=bool)
        path = np.zeros_like(mask, dtype=bool)

        # Define 4-directional movements (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Priority queue to store nodes and their tentative distances
        pq = []

        # Push the starting node to the priority queue
        heapq.heappush(pq, (0, new_point_1))
        distance[new_point_1[0], new_point_1[1]] = 0


        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if visited[current_node[0], current_node[1]]:
                continue

            visited[current_node[0], current_node[1]] = True

            for direction in directions:
                new_node = (current_node[0] + direction[0], current_node[1] + direction[1])

                # Check if the new position is within bounds and not a pixel to avoid
                if (0 <= new_node[0] < rows and 0 <= new_node[1] < cols and
                        mask[new_node[0], new_node[1]] != 50):  # Avoid pixels with value 10
                    if mask[new_node[0], new_node[1]] == 1:
                        new_dist = current_dist + 1  # Cost of 1 for pixels with value 1
                    elif mask[new_node[0], new_node[1]] == 0:
                        new_dist = current_dist + 50  # Cost of 5 for pixels with value 0

                    if new_dist < distance[new_node[0], new_node[1]]:
                        distance[new_node[0], new_node[1]] = new_dist
                        heapq.heappush(pq, (new_dist, new_node))

        # Backtrack to reconstruct the path
        current_node = new_point_2
        while current_node != new_point_1:
            path[current_node[0], current_node[1]] = 1

            # Find the next node with minimum distance among valid neighbors
            min_distance = np.inf
            next_node = None

            for direction in directions:
                neighbor = (current_node[0] - direction[0], current_node[1] - direction[1])
                if (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and
                        mask[neighbor[0], neighbor[1]] != 50):  # Avoid pixels with value 10
                    if distance[neighbor[0], neighbor[1]] < min_distance:
                        min_distance = distance[neighbor[0], neighbor[1]]
                        next_node = neighbor

            if next_node is None:
                break  # No valid neighbors, terminate the loop

            current_node = next_node

        # print(f"Path number {point + 1} has been found.")

        for i in range(np.shape(path)[0]):
            for j in range(np.shape(path)[1]):
                if path[i, j] == True:
                    raw_image[i + min(point_1[0], point_2[0]) - Domain_distance, j + min(point_1[1], point_2[
                        1]) - Domain_distance] = 255


        point_1 = points[point]
        point_2 = points[point + 1]

        Area_of_Interest = raw_image[
                           min(point_1[0], point_2[0]) - Domain_distance:max(point_1[0], point_2[0]) + Domain_distance,
                           min(point_1[1], point_2[1]) - Domain_distance:max(point_1[1], point_2[1]) + Domain_distance]

        shape = np.shape(Area_of_Interest)

        if len(shape) == 3:
            Area_of_Interest = Area_of_Interest[:, :, 0]

        #save_image(Area_of_Interest,f'Boundary Segment {point+1}.png')

        print(f"Done with segment {point+1} of Boundary Isolation")


    binary=np.full_like(raw_image, 0)

    binary[raw_image==255]=255


    return binary

import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image
from scipy.signal import convolve2d

# Create the main window
root = ctk.CTk()
root.title("Image Processing Parameter Tester")

# Load the original image
image_path = '/Users/Sotero/Downloads/Documentos/Tudor/OneDrive_1_13-1-2024/1 ys - 300 um (stitched)_0.tif'  # Replace with your image path
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
original_image_resized = original_image[500:1000,500:1000]
print(original_image_resized)# Resize for display


# Set the scaling factor
scaling_factor = 1  # For example, 2x the original size

# Calculate new size based on scaling factor
original_height, original_width = original_image_resized.shape
new_width = int(original_width * scaling_factor)
new_height = int(original_height * scaling_factor)

# Resize the original image

# Last used parameters for Canny and Gaussian
last_canny_params = {'lower_thresh': 100, 'upper_thresh': 200}
last_gaussian_params = {'kernel_size': 3, 'sigma': 1.0}

# Convert the original image to a format compatible with CTkImage
def image_to_ctkimage(image_array, width, height):
    pil_image = Image.fromarray(image_array)
    return ctk.CTkImage(pil_image, size=(width, height))

# Function to apply Canny edge detection
def canny_detection(image, lower_thresh, upper_thresh):
    # Apply Canny edge detection
    edges = cv2.Canny(image, lower_thresh, upper_thresh)
    return edges

# Function to apply Gaussian filter
def gaussian_filtering(image, kernel_size, sigma):
    # Create a Gaussian kernel and apply Gaussian blur
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    return blurred

# Function to update the displayed image based on the selected method
def update_image():
    global canny_image_label

    # Get the selected method from the dropdown
    selected_method = method_selector.get()

    if selected_method == "Canny Edge Detection":
        # Get slider values for Canny
        lower_thresh = lower_threshold_slider.get()
        upper_thresh = upper_threshold_slider.get()

        # Save the last used Canny parameters
        last_canny_params['lower_thresh'] = lower_thresh
        last_canny_params['upper_thresh'] = upper_thresh

        # Apply Canny edge detection
        processed_image = canny_detection(original_image_resized, lower_thresh, upper_thresh)

    elif selected_method == "Gaussian Filtering":
        # Get slider values for Gaussian filtering
        kernel_size = int(kernel_size_slider.get()) | 1  # Ensure kernel size is odd
        sigma = sigma_slider.get()

        # Save the last used Gaussian parameters
        last_gaussian_params['kernel_size'] = kernel_size
        last_gaussian_params['sigma'] = sigma

        # Apply Gaussian filtering
        processed_image = gaussian_filtering(original_image_resized, kernel_size, sigma)

    # Update the modified image display
    processed_image_ctk = image_to_ctkimage(processed_image, new_width, new_height)
    canny_image_label.configure(image=processed_image_ctk)
    canny_image_label.image = processed_image_ctk

# Function to switch between parameter sets when a different method is selected
def update_method():
    selected_method = method_selector.get()

    if selected_method == "Canny Edge Detection":
        # Show Canny sliders
        lower_threshold_slider.grid(row=1, column=0, padx=10, pady=10)
        upper_threshold_slider.grid(row=1, column=1, padx=10, pady=10)
        kernel_size_slider.grid_remove()
        sigma_slider.grid_remove()

        # Set the sliders to the last used Canny parameters
        lower_threshold_slider.set(last_canny_params['lower_thresh'])
        upper_threshold_slider.set(last_canny_params['upper_thresh'])

    elif selected_method == "Gaussian Filtering":
        # Show Gaussian sliders
        kernel_size_slider.grid(row=1, column=0, padx=10, pady=10)
        sigma_slider.grid(row=1, column=1, padx=10, pady=10)
        lower_threshold_slider.grid_remove()
        upper_threshold_slider.grid_remove()

        # Set the sliders to the last used Gaussian parameters
        kernel_size_slider.set(last_gaussian_params['kernel_size'])
        sigma_slider.set(last_gaussian_params['sigma'])

    # Update the image based on the new method
    update_image()

# Create image display labels using CTkImage
original_image_ctk = image_to_ctkimage(original_image_resized, new_width, new_height)

original_image_label = ctk.CTkLabel(root, image=original_image_ctk, text="Original Image")
original_image_label.grid(row=0, column=0, padx=10, pady=10)

canny_image_label = ctk.CTkLabel(root, text="Processed Image")
canny_image_label.grid(row=0, column=1, padx=10, pady=10)

# Dropdown menu to select the method
method_selector = ctk.CTkComboBox(root, values=["Canny Edge Detection", "Gaussian Filtering"], command=lambda _: update_method())
method_selector.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
method_selector.set("Canny Edge Detection")  # Set default method

# Sliders for Canny parameters
lower_threshold_slider = ctk.CTkSlider(root, from_=0, to=255, command=lambda val: update_image())
lower_threshold_slider.grid(row=1, column=0, padx=10, pady=10)
lower_threshold_slider.set(last_canny_params['lower_thresh'])  # Initial value

upper_threshold_slider = ctk.CTkSlider(root, from_=0, to=255, command=lambda val: update_image())
upper_threshold_slider.grid(row=1, column=1, padx=10, pady=10)
upper_threshold_slider.set(last_canny_params['upper_thresh'])  # Initial value

# Sliders for Gaussian filter parameters (initially hidden)
kernel_size_slider = ctk.CTkSlider(root, from_=1, to=11, number_of_steps=5, command=lambda val: update_image())
kernel_size_slider.grid_remove()

sigma_slider = ctk.CTkSlider(root, from_=0.1, to=5.0, command=lambda val: update_image())
sigma_slider.grid_remove()

# Initialize the modified image display
update_image()

# Start the main loop
root.mainloop()

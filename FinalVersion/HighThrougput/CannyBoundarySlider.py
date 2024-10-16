import customtkinter as ctk
from PIL import Image
import numpy as np
from scipy.ndimage import convolve as convolve2d
from skimage import feature
from FinalVersion.utilities.ImageProcessor import ImageProcessor
from scipy.ndimage import distance_transform_edt
import cv2

class CannyBoundarySlider(ctk.CTkFrame):
    parameters=(5,50)
    def __init__(self,creator,data):
        super(CannyBoundarySlider, self).__init__(creator)


        path=data["image set 1"]["images"][0]["path"]
        width, height = data["image set 1"]["images"][0]["dimensions"]
        self.original_image=ImageProcessor(path, width, height, 0)
        #TODO:maybe is the other way around
        pointx,pointy=data["image set 1"]["Boundary_points"][0][0][1]
        self.original_image=self.original_image[max(pointx-500,0):max(pointx+500,1000),max(pointy-500,0):max(pointy+500,1000)]
        original_height, original_width = self.original_image.shape
        self.new_width = int(original_width * 0.5)
        self.new_height = int(original_height * 0.5)


        # Create image display labels using CTkImage
        original_image_ctk = self.image_to_ctkimage(self.original_image)

        original_image_label = ctk.CTkLabel(self, image=original_image_ctk, text="")
        original_image_label.grid(row=0, column=0, padx=10, pady=10)

        self.canny_image_label = ctk.CTkLabel(self,text="")
        self.canny_image_label.grid(row=0, column=1, padx=10, pady=10)

        # Create sliders for Canny parameters
        self.lower_threshold_slider = ctk.CTkSlider(self, from_=1, to=100,number_of_steps=99, command=lambda val: self.update_image())
        self.lower_threshold_slider.grid(row=1, column=0, padx=10, pady=10)
        self.lower_threshold_slider.set(50)  # Initial value

        self.label1 = ctk.CTkLabel(self, text="Width: " + str(self.lower_threshold_slider.get()))
        self.label1.grid(row=2, column=0, padx=10, pady=10)



        self.upper_threshold_slider = ctk.CTkSlider(self, from_=2, to=10,number_of_steps=8, command=lambda val: self.update_image())
        self.upper_threshold_slider.grid(row=1, column=1, padx=10, pady=10)
        self.upper_threshold_slider.set(5)  # Initial value

        self.label2 = ctk.CTkLabel(self, text="Range: " + str(self.upper_threshold_slider.get()))
        self.label2.grid(row=2, column=1, padx=10, pady=10)

        # Initialize the modified image display
        self.update_image()

    def image_to_ctkimage(self,image_array):
        pil_image = Image.fromarray(image_array)
        return ctk.CTkImage(pil_image,size=(self.new_width, self.new_height))

    def canny_detection(self,mean_range=5,mean_width=40):

        mean_kernel = np.ones((mean_range, mean_range)) / mean_width
        smoothed_image = convolve2d(self.original_image, mean_kernel, mode='nearest')

        return feature.canny(smoothed_image)

    def update_image(self):
        # Get slider values
        lower_thresh = self.lower_threshold_slider.get()
        upper_thresh = self.upper_threshold_slider.get()

        # Apply Canny edge detection
        edges = self.canny_detection(int(upper_thresh),int(lower_thresh))

        # Update the modified image display
        edges_image_ctk = self.image_to_ctkimage(edges)
        self.canny_image_label.configure(image=edges_image_ctk)
        self.canny_image_label.image = edges_image_ctk

        self.label2.configure(text="Range: " + str((upper_thresh)))
        self.label1.configure(text="Width: " + str((lower_thresh)))

        self.parameters=(int(upper_thresh),int(lower_thresh))





class Multipleslider(ctk.CTkFrame):
    def __init__(self,creator,img):
        super(Multipleslider, self).__init__(creator)

        self.original_image_resized=img
        self.new_width=500
        self.new_height=500

        # Last used parameters for Canny and Gaussian
        self.last_canny_params = {'lower_thresh': 100, 'upper_thresh': 200}
        self.last_gaussian_params = {'kernel_size': 3, 'sigma': 1.0}


        # Create image display labels using CTkImage
        original_image_ctk = self.image_to_ctkimage(self.original_image_resized, self.new_width, self.new_height)

        self.original_image_label = ctk.CTkLabel(self, image=original_image_ctk, text="")
        self.original_image_label.grid(row=0, column=0, padx=10, pady=10)

        self.canny_image_label = ctk.CTkLabel(self, text="")
        self.canny_image_label.grid(row=0, column=1, padx=10, pady=10)

        # Dropdown menu to select the method
        self.method_selector = ctk.CTkComboBox(self, values=["Canny Edge Detection", "Gaussian Filtering"],
                                          command=lambda _: self.update_method())
        self.method_selector.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.method_selector.set("Canny Edge Detection")  # Set default method

        # Sliders for Canny parameters
        self.lower_threshold_slider = ctk.CTkSlider(self, from_=1, to=100,number_of_steps=99, command=lambda val: self.update_image())
        self.lower_threshold_slider.grid(row=1, column=0, padx=10, pady=10)
        self.lower_threshold_slider.set(self.last_canny_params['lower_thresh'])  # Initial value
        self.label1 = ctk.CTkLabel(self, text="Width: " + str(self.lower_threshold_slider.get()))
        self.label1.grid(row=2, column=0, padx=10, pady=10)


        self.upper_threshold_slider = ctk.CTkSlider(self, from_=2, to=10, number_of_steps=8, command=lambda val: self.update_image())
        self.upper_threshold_slider.grid(row=1, column=1, padx=10, pady=10)
        self.upper_threshold_slider.set(self.last_canny_params['upper_thresh'])  # Initial value
        self.label2 = ctk.CTkLabel(self, text="Range: " + str(self.upper_threshold_slider.get()))
        self.label2.grid(row=2, column=1, padx=10, pady=10)



        # Sliders for Gaussian filter parameters (initially hidden)
        self.kernel_size_slider = ctk.CTkSlider(self, from_=35, to=100,number_of_steps=65, command=lambda val: self.update_image())
        self.kernel_size_slider.grid_remove()
        self.label3 = ctk.CTkLabel(self, text="Kernel size: " + str(self.lower_threshold_slider.get()))
        self.label3.grid_remove()

        self.sigma_slider = ctk.CTkSlider(self, from_=0, to=10,number_of_steps=10, command=lambda val: self.update_image())
        self.sigma_slider.grid_remove()
        self.label4 = ctk.CTkLabel(self, text="Fidelity: " + str(self.lower_threshold_slider.get()))
        self.label4.grid_remove()

        # Initialize the modified image display
        self.update_image()




    # Convert the original image to a format compatible with CTkImage
    def image_to_ctkimage(self,image_array, width, height):
        pil_image = Image.fromarray(image_array)
        return ctk.CTkImage(pil_image, size=(width, height))

    # Function to apply Canny edge detection
    def canny_detection(self,image, mean_range=5, mean_width=40):

        mean_kernel = np.ones((mean_range, mean_range)) / mean_width
        smoothed_image = convolve2d(image, mean_kernel, mode='nearest')

        return feature.canny(smoothed_image)

    # Function to apply Gaussian filter
    def gaussian_filtering(self,image, mx, f):

        dt_img = np.pad(image, (mx - 1, mx - 1), "symmetric")
        dt_img = np.pad(dt_img, (1, 1), constant_values=255)

        Inner_Distance_Map = distance_transform_edt(dt_img != 255)

        Inner_Distance_Map = np.round(Inner_Distance_Map, decimals=2)

        Inner_Distance_Map = Inner_Distance_Map[mx:-mx, mx:-mx]

        Gaussian_Detection = np.zeros([image.shape[0], image.shape[1]])

        Gaussian_Detection[Gaussian_Detection == 0] = 200

        Gaussian_Ranges = [i if (i % 2 == 1) else i + 1 for i in range(31, mx, int((mx - 30) / 5))]
        for k in Gaussian_Ranges:
            img = np.pad(image, (k - 1, k - 1), "symmetric")

            Gaussian_Filter = cv2.adaptiveThreshold(img, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                    cv2.THRESH_BINARY, k, f)
            Gaussian_Filter = Gaussian_Filter[k:image.shape[0] + k, k:image.shape[1] + k]

            Gaussian_Detection[Gaussian_Filter == 0] = 0

            Gaussian_Detection[Inner_Distance_Map < k] = 200

        return Gaussian_Detection

    # Function to update the displayed image based on the selected method
    def update_image(self):

        # Get the selected method from the dropdown
        selected_method = self.method_selector.get()

        if selected_method == "Canny Edge Detection":
            # Get slider values for Canny
            lower_thresh = self.lower_threshold_slider.get()
            upper_thresh = self.upper_threshold_slider.get()

            # Save the last used Canny parameters
            self.last_canny_params['lower_thresh'] = lower_thresh
            self.last_canny_params['upper_thresh'] = upper_thresh

            # Apply Canny edge detection
            processed_image = self.canny_detection(self.original_image_resized, int(lower_thresh),int(upper_thresh))

            self.label2.configure(text="Range: " + str((upper_thresh)))
            self.label1.configure(text="Width: " + str((lower_thresh)))

        elif selected_method == "Gaussian Filtering":
            # Get slider values for Gaussian filtering
            kernel_size = int(self.kernel_size_slider.get()) | 1  # Ensure kernel size is odd
            sigma = self.sigma_slider.get()

            # Save the last used Gaussian parameters
            self.last_gaussian_params['kernel_size'] = kernel_size
            self.last_gaussian_params['sigma'] = sigma

            # Apply Gaussian filtering
            processed_image = self.gaussian_filtering(self.original_image_resized, int(kernel_size), int(sigma))

            self.label3.configure(text="Kernel size: " + str((kernel_size)))
            self.label4.configure(text="Fidelity: " + str((sigma)))

        # Update the modified image display
        processed_image_ctk = self.image_to_ctkimage(processed_image, self.new_width, self.new_height)
        self.canny_image_label.configure(image=processed_image_ctk)
        self.canny_image_label.image = processed_image_ctk

    # Function to switch between parameter sets when a different method is selected
    def update_method(self):
        selected_method = self.method_selector.get()

        if selected_method == "Canny Edge Detection":
            # Show Canny sliders
            self.lower_threshold_slider.grid(row=1, column=0, padx=10, pady=10)
            self.upper_threshold_slider.grid(row=1, column=1, padx=10, pady=10)
            self.label1.grid(row=2, column=0, padx=10, pady=10)
            self.label2.grid(row=2, column=1, padx=10, pady=10)
            self.kernel_size_slider.grid_remove()
            self.sigma_slider.grid_remove()
            self.label3.grid_remove()
            self.label4.grid_remove()


            # Set the sliders to the last used Canny parameters
            self.lower_threshold_slider.set(self.last_canny_params['lower_thresh'])
            self.upper_threshold_slider.set(self.last_canny_params['upper_thresh'])

        elif selected_method == "Gaussian Filtering":
            # Show Gaussian sliders
            self.kernel_size_slider.grid(row=1, column=0, padx=10, pady=10)
            self.sigma_slider.grid(row=1, column=1, padx=10, pady=10)
            self.label3.grid(row=2, column=0, padx=10, pady=10)
            self.label4.grid(row=2, column=1, padx=10, pady=10)
            self.lower_threshold_slider.grid_remove()
            self.upper_threshold_slider.grid_remove()
            self.label1.grid_remove()
            self.label2.grid_remove()

            # Set the sliders to the last used Gaussian parameters
            self.kernel_size_slider.set(self.last_gaussian_params['kernel_size'])
            self.sigma_slider.set(self.last_gaussian_params['sigma'])

        # Update the image based on the new method
        self.update_image()






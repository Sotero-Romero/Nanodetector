import customtkinter as ctk
from PIL import Image
import numpy as np
from scipy.ndimage import convolve as convolve2d
from skimage import feature
from FinalVersion.utilities.ImageProcessor import ImageProcessor


class CannyBoundarySlider(ctk.CTkFrame):
    parameters=(5,50)
    def __init__(self,creator,data):
        super(CannyBoundarySlider, self).__init__(creator)


        path=data["image set 1"]["images"][0]["path"]
        width, height = data["image set 1"]["images"][0]["dimensions"]
        self.original_image=ImageProcessor(path, width, height, 0)
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






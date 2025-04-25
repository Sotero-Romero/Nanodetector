import customtkinter
import cv2
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.ndimage import convolve as convolve2d
from skimage import feature
from scipy.ndimage import distance_transform_edt
from FinalVersion.Analysis.ImageAnalysis import AnalyseImage
from scipy import ndimage as ndi



class ManualSelection(customtkinter.CTkFrame):
    def __init__(self,creator,img):
        super(ManualSelection, self).__init__(master=creator)

        self.img_copy = np.copy(img)
        self.canny_var = (100, 200, 5, 25)
        self.gauss_var = (5, 40)

        # original image
        frame_1 = Figure(figsize=(7, 7))
        can = FigureCanvasTkAgg(frame_1,master=self)
        can.get_tk_widget().grid(row=0, column=0, padx=10)
        axs = frame_1.add_subplot()
        plt_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        axs.imshow(plt_image)
        can.draw()

        # modified image
        self.frame_2 = Figure(figsize=(7, 7))
        self.can2 = FigureCanvasTkAgg(self.frame_2,master=self)
        self.can2.get_tk_widget().grid(row=0, column=1, padx=10)
        self.axs2 = self.frame_2.add_subplot()
        plt_image2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.axs2.imshow(plt_image2)
        self.can2.draw()

        frame_2 = customtkinter.CTkFrame(master=self,fg_color="transparent")
        frame_2.grid(row=1, columnspan=2, pady=20, ipadx=300)

        frame_3 = customtkinter.CTkFrame(master=frame_2,fg_color="transparent")
        frame_3.pack(side=customtkinter.LEFT, pady=20)

        combobox = customtkinter.CTkComboBox(master=frame_3, values=["", "Gaussian", "Canny", "Full Analysis"],
                                             command=self.select,state='readonly')
        combobox.pack()

        self.frame_4 = customtkinter.CTkFrame(master=frame_2,fg_color="transparent")
        self.frame_4.pack(fill="x")
        self.frame_4.grid_propagate(False)
        self.frame_4.pack_propagate(False)

        done=customtkinter.CTkButton(master=frame_3,text="Done",
                                        command=lambda : creator.set_premilinary_image(
                                            canny_minimum=self.canny_var[0],
                                            canny_maximum=self.canny_var[1],
                                            canny_ksize=self.canny_var[2],
                                            canny_sigma=self.canny_var[3],
                                            gaussian_fidelity=self.gauss_var[0],
                                            gaussian_range=self.gauss_var[1])
                                     )
        done.pack(pady=30)



    def select(self,choice):
        if choice=="":
            self.empty()
        elif choice=="Gaussian":
            self.empty()
            self.gaussian()
        elif choice=="Canny":
            self.empty()
            self.canny()
        elif choice=="Full Analysis":
            self.empty()
            self.full_analysis()

    def empty(self):
        axs2 = self.frame_2.add_subplot()
        plt_image2 = cv2.cvtColor(self.img_copy, cv2.COLOR_BGR2RGB)
        axs2.imshow(plt_image2)
        self.can2.draw()
        for widget in self.frame_4.winfo_children():
            widget.destroy()

    def canny(self):
        #create sliders

        # First slider (Minimum)
        label = customtkinter.CTkLabel(self.frame_4, text="Minimum:")
        label.grid(row=0, column=0, padx=10, pady=5)
        slider = customtkinter.CTkSlider(self.frame_4, from_=0, to=255,
                                         command=lambda val: evaluate(val, slider2.get(), slider3.get(), slider4.get(),
                                                                      label, label1, label2, label3))
        slider.set(self.canny_var[0])
        slider.grid(row=1, column=0, padx=10, pady=10)

        # Second slider (Maximum)
        label1 = customtkinter.CTkLabel(self.frame_4, text="Maximum:")
        label1.grid(row=0, column=1, padx=10, pady=5)
        slider2 = customtkinter.CTkSlider(self.frame_4, from_=0, to=255,
                                          command=lambda val: evaluate(slider.get(), val, slider3.get(), slider4.get(),
                                                                       label, label1, label2, label3))
        slider2.set(self.canny_var[1])
        slider2.grid(row=1, column=1, padx=10, pady=10)

        # Third slider (K size)
        label2 = customtkinter.CTkLabel(self.frame_4, text="K size:")
        label2.grid(row=0, column=2, padx=10, pady=5)
        slider3 = customtkinter.CTkSlider(self.frame_4, from_=3, to=99, number_of_steps=48,
                                          command=lambda val: evaluate(slider.get(), slider2.get(), val, slider4.get(),
                                                                       label, label1, label2, label3))
        slider3.set(self.canny_var[2])
        slider3.grid(row=1, column=2, padx=10, pady=10)

        # Fourth slider (Sigma)
        label3 = customtkinter.CTkLabel(self.frame_4, text="Sigma:")
        label3.grid(row=0, column=3, padx=10, pady=5)
        slider4 = customtkinter.CTkSlider(self.frame_4, from_=0, to=50, number_of_steps=100,
                                          command=lambda val: evaluate(slider.get(), slider2.get(), slider3.get(), val,
                                                                       label, label1, label2, label3))
        slider4.set(self.canny_var[3])
        slider4.grid(row=1, column=3, padx=10, pady=10)




        def evaluate(canny_minimum,canny_maximum, ksize, canny_sigma,L,L2, L3, L4):
            #change labels
            L.configure(text="Minimum: " + str(int(canny_minimum)))
            L2.configure(text="Maximum: " + str(int(canny_maximum)))
            L3.configure(text="Ksize: " + str(int(ksize)))
            L4.configure(text="Sigma: " + str(int(canny_sigma)))

            self.axs2.remove()
            self.axs2 = self.frame_2.add_subplot()
            plt_image2 = self.canny_detection(canny_minimum,canny_maximum, int(ksize), canny_sigma)
            self.axs2.imshow(plt_image2)
            self.can2.draw()


    def canny_detection(self,canny_minimum=100,canny_maximum=200, ksize=15, canny_sigma=3):

        self.canny_var= (canny_minimum,canny_maximum, ksize, canny_sigma)

        original_image = self.img_copy.copy()
        original_image = (
                (original_image - original_image.min()) / (original_image.max() - original_image.min()) * 255).astype(
            np.uint8)

        gaussian_blurred = cv2.GaussianBlur(original_image, (ksize, ksize), canny_sigma)
        edges = cv2.Canny(gaussian_blurred, canny_minimum, canny_maximum)

        return edges







    def gaussian(self):
        slider = customtkinter.CTkSlider(self.frame_4, from_=3, to=60, number_of_steps=57,
                                         command=lambda val: fid_siz(val,slider2.get(), label, label1))
        slider.set(self.gauss_var[0])
        label = customtkinter.CTkLabel(self.frame_4, text="Fidelity: " + str(slider.get()))
        label.pack(pady=5)
        slider.pack(pady=10)

        slider2 = customtkinter.CTkSlider(self.frame_4, from_=35, to=511, number_of_steps= 238,
                                          command=lambda val: fid_siz(slider.get(), val, label, label1)
                                          )
        slider2.set(self.gauss_var[1])
        label1 = customtkinter.CTkLabel(self.frame_4, text="Range: " + str(slider2.get()))
        label1.pack(pady=5)
        slider2.pack(pady=10)

        def fid_siz(fidelity,max_size,L,L2):

            L.configure(text="Fidelity: " +str(int(fidelity)))
            L2.configure(text="Range: " +str(int(max_size)))
            self.axs2.remove()
            self.axs2 = self.frame_2.add_subplot()
            plt_image2 = self.gauss(int(fidelity), int(max_size))
            self.axs2.imshow(plt_image2)
            self.can2.draw()




    def gauss(self,gaussian_fidelity=5,gaussian_range=40):
        self.gauss_var=(gaussian_fidelity,gaussian_range)

        pad=gaussian_range

        original_image = self.img_copy.copy()
        original_image =  np.pad(original_image, (pad,pad), mode='symmetric')
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
                                                                                        1:-1], original_image[1:-1,
                                                                                               1:-1]

        bright_edges = np.full_like(raw_image, 0)
        bright_edges[raw_image > 210] = 200

        raw_image[bright_edges == 200] = np.mean(raw_image)
        bright_distance_map = ndi.distance_transform_edt(raw_image < 200)
        bright_distance_map = np.round(bright_distance_map)

        gaussian_detection = np.full_like(raw_image, 200)

        gaussian_filt = cv2.adaptiveThreshold(raw_image, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                             gaussian_range, gaussian_fidelity)
        gaussian_filt[inner_distance_map < gaussian_range] = 200
        gaussian_filt[bright_distance_map < (300 / gaussian_range)] = 200
        gaussian_detection[gaussian_filt == 0] = 0

        del gaussian_filt
        del inner_distance_map, bright_distance_map

        return gaussian_detection[pad:-pad,pad:-pad]



    def full_analysis(self):

        def update_analysis():
            self.axs2.remove()
            self.axs2 = self.frame_2.add_subplot()
            plt_image2 = AnalyseImage(
                                      original_image=self.img_copy,
                                      canny_minimum=self.canny_var[0],
                                      canny_maximum=self.canny_var[1],
                                      canny_ksize=self.canny_var[2],
                                      canny_sigma=self.canny_var[3],
                                      gaussian_fidelity=self.gauss_var[0],
                                      gaussian_range=self.gauss_var[1])
            self.axs2.imshow(plt_image2)
            self.can2.draw()

        label=customtkinter.CTkLabel(master=self.frame_4,text="Parameters Selected:")
        label.grid(row=0,column=0,padx=20)

        label_canny = customtkinter.CTkLabel(master=self.frame_4, text="Canny")
        label_canny.grid(row=1, column=1)

        label_gauss = customtkinter.CTkLabel(master=self.frame_4, text="Gauss")
        label_gauss.grid(row=1, column=3)

        label_mean_range = customtkinter.CTkLabel(master=self.frame_4, text="Mean Range: ")
        label_mean_range.grid(row=2, column=1,sticky="w")

        label_mean_width = customtkinter.CTkLabel(master=self.frame_4, text="Mean Width: ")
        label_mean_width.grid(row=3, column=1, sticky="w")

        label_fidelity = customtkinter.CTkLabel(master=self.frame_4, text="Fidelity: ")
        label_fidelity.grid(row=2, column=3, sticky="w")

        label_min_size = customtkinter.CTkLabel(master=self.frame_4, text="Min Size: ")
        label_min_size.grid(row=3, column=3, sticky="w")

        label_mean_range_val = customtkinter.CTkLabel(master=self.frame_4, text=f"{self.canny_var[0]}")
        label_mean_range_val.grid(row=2, column=2, sticky="w")

        label_mean_width_val = customtkinter.CTkLabel(master=self.frame_4, text=f"{self.canny_var[1]}")
        label_mean_width_val.grid(row=3, column=2, sticky="w")

        label_fidelity_var = customtkinter.CTkLabel(master=self.frame_4, text=f"{self.gauss_var[0]}")
        label_fidelity_var.grid(row=2, column=4, sticky="w")

        label_max_size_var = customtkinter.CTkLabel(master=self.frame_4, text=f"{self.gauss_var[1]}")
        label_max_size_var.grid(row=3, column=4, sticky="w")

        analyse_button=customtkinter.CTkButton(master=self.frame_4,text="Analyse",command=update_analysis)
        analyse_button.grid(column=2,row=4,pady=20)





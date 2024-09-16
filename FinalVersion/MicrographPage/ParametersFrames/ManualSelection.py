import customtkinter
import cv2
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.ndimage import convolve as convolve2d
from skimage import feature
from scipy.ndimage import distance_transform_edt
from FinalVersion.Analysis.ImageAnalysis import AnalyseImage


class ManualSelection(customtkinter.CTkFrame):
    def __init__(self,creator,img):
        super(ManualSelection, self).__init__(master=creator)

        self.img_copy = np.copy(img)
        self.canny_var = (5, 40)
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
                                            mean_weight=self.canny_var[1],
                                            mean_range=self.canny_var[0],
                                            pore_cut_off=self.gauss_var[1],
                                            Fidelity_Base=self.gauss_var[0]
                                        )
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



        slider = customtkinter.CTkSlider(self.frame_4, from_=0, to=10,
                                         command=lambda val:mean_range(val,slider2.get(),label,label1))
        slider.set(self.canny_var[0])

        label = customtkinter.CTkLabel(self.frame_4, text="Range: " + str(slider.get()))
        label.pack(pady=5)
        slider.pack(pady=10)



        slider2 = customtkinter.CTkSlider(self.frame_4, from_=0, to=100,
                                          command=lambda val: mean_range(slider.get(), val,label,label1)
                                          )
        slider2.set(self.canny_var[1])
        label1 = customtkinter.CTkLabel(self.frame_4, text="Width: "+str(slider2.get()))
        label1.pack(pady=5)
        slider2.pack(pady=10)




        def mean_range(range,width,L,L2):
            L.configure(text="Range: " + str(int(range)))
            L2.configure(text="Width: " + str(int(width)))
            self.axs2.remove()
            self.axs2 = self.frame_2.add_subplot()
            plt_image2 = self.canny_detection(int(range),int(width))
            self.axs2.imshow(plt_image2)
            self.can2.draw()


    def canny_detection(self,mean_range=5,mean_width=40):
        self.canny_var=(mean_range,mean_width)

        mean_kernel = np.ones((mean_range, mean_range)) / mean_width
        smoothed_image = convolve2d(self.img_copy, mean_kernel, mode='nearest')

        return feature.canny(smoothed_image)







    def gaussian(self):
        slider = customtkinter.CTkSlider(self.frame_4, from_=0, to=10,
                                         command=lambda val: fid_siz(val,slider2.get(), label, label1))
        slider.set(self.gauss_var[0])
        label = customtkinter.CTkLabel(self.frame_4, text="Fidelity: " + str(slider.get()))
        label.pack(pady=5)
        slider.pack(pady=10)

        slider2 = customtkinter.CTkSlider(self.frame_4, from_=35, to=100,
                                          command=lambda val: fid_siz(slider.get(), val, label, label1)
                                          )
        slider2.set(self.gauss_var[1])
        label1 = customtkinter.CTkLabel(self.frame_4, text="Maximum size: " + str(slider2.get()))
        label1.pack(pady=5)
        slider2.pack(pady=10)

        def fid_siz(fidelity,max_size,L,L2):

            L.configure(text="Fidelity: " +str(int(fidelity)))
            L2.configure(text="Maximum size: " +str(int(max_size)))
            self.axs2.remove()
            self.axs2 = self.frame_2.add_subplot()
            plt_image2 = self.gauss(int(fidelity), int(max_size))
            self.axs2.imshow(plt_image2)
            self.can2.draw()




    def gauss(self,f=5,mx=40):
        self.gauss_var=(f,mx)


        dt_img=np.pad(self.img_copy,(mx-1,mx-1), "symmetric")
        dt_img=np.pad(dt_img,(1,1),constant_values=255)

        Inner_Distance_Map = distance_transform_edt(dt_img != 255)

        Inner_Distance_Map = np.round(Inner_Distance_Map, decimals=2)

        Inner_Distance_Map = Inner_Distance_Map[mx:-mx,mx:-mx]

        Gaussian_Detection = np.zeros([self.img_copy.shape[0], self.img_copy.shape[1]])

        Gaussian_Detection[Gaussian_Detection == 0] = 200

        Gaussian_Ranges = [i if (i % 2 == 1) else i + 1 for i in range(31, mx, int((mx - 30) / 5))]
        for k in Gaussian_Ranges:
            img = np.pad(self.img_copy, (k-1, k-1), "symmetric")


            Gaussian_Filter = cv2.adaptiveThreshold(img, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                                    cv2.THRESH_BINARY, k, f)
            Gaussian_Filter=Gaussian_Filter[k:self.img_copy.shape[0]+k,k:self.img_copy.shape[1]+k]

            Gaussian_Detection[Gaussian_Filter == 0] = 0

            Gaussian_Detection[Inner_Distance_Map < k] = 200


        return Gaussian_Detection



    def full_analysis(self):

        def update_analysis():
            self.axs2.remove()
            self.axs2 = self.frame_2.add_subplot()
            plt_image2 = AnalyseImage(self.img_copy,
                                      mean_weight=self.canny_var[1],
                                      mean_range=self.canny_var[0],
                                      pore_cut_off=self.gauss_var[1],
                                      Fidelity_Base=self.gauss_var[0])
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





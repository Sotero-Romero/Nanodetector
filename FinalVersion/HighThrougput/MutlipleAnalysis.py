import os
from tkinter.filedialog import askdirectory

import customtkinter

from FinalVersion.Analysis.BoundaryIsolation import Isolate_Boundary
from FinalVersion.Analysis.ImageAnalysis import FullAnalyseImage
from FinalVersion.utilities.ImageProcessor import ImageProcessor

class MultipleAnalysis(customtkinter.CTkFrame):
    def __init__(self,creator,data):
        super(MultipleAnalysis, self).__init__(creator)

        self.folderPath=""
        self.data=data
        button=customtkinter.CTkButton(self, text="Choose folder to save results", command=self.getFolderPath)
        button.pack()
        self.path_Label=customtkinter.CTkLabel(self,text=self.folderPath)
        self.path_Label.pack()

        download=customtkinter.CTkButton(self, text="Analyse and download results", command=self.analyseDownload)
        download.pack()


    def getFolderPath(self):
        self.folderPath = askdirectory()
        self.path_Label.configure(text=self.folderPath)

    #TODO: make isolate work
    def analyseDownload(self):
        if self.folderPath!="":
            for set_key, set in self.data.items():
                #img=Isolate_Boundary(images_paths, points, points_inside, points_outside, mean_weight=350,mean_range=30, width=0, height=0):

                img=ImageProcessor(set["main_image"]["path"],set["main_image"]["dimensions"][0],
                                   set["main_image"]["dimensions"][1],0)
                canny_params=set["analysis_parameter"]["canny"]
                canny_minimum= canny_params["canny_minimum"]
                canny_maximum= canny_params["canny_maximum"]
                canny_ksize= canny_params["canny_ksize"]
                canny_sigma= canny_params["canny_sigma"]

                gaussian_params=set["analysis_parameter"]["gauss"]
                gaussian_fidelity= gaussian_params["gaussian_fidelity"]
                gaussian_range= gaussian_params["gaussian_range"]

                feather_path=os.path.join(self.folderPath, set_key)

                FullAnalyseImage(img,
                     canny_minimum,
                     canny_maximum,
                     canny_ksize,
                     canny_sigma,
                     gaussian_fidelity,
                     gaussian_range,
                     feather_path,)





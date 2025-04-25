import customtkinter
from FinalVersion.HighThrougput.MultipleImageUploader import MultipleImageUploader
from FinalVersion.HighThrougput.choosing import Choosing,Choosing2
from FinalVersion.HighThrougput.MultipleBoundarySelection import MultipleBoundarySelection,UnitaryBoundarySelection
from FinalVersion.HighThrougput.CannyBoundarySlider import CannyBoundarySlider
from FinalVersion.HighThrougput.SelectParameters import AllParameters,GeneralParameters
from FinalVersion.HighThrougput.MutlipleAnalysis import MultipleAnalysis

class HighThroughFrame(customtkinter.CTkFrame):
    def __init__(self,creator):
        super(HighThroughFrame, self).__init__(creator)
        self.uploadImages()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def uploadImages(self):
        m=MultipleImageUploader(self)
        m.pack()
        button=customtkinter.CTkButton(self,text="Done",command=lambda :self.selectBoundary(m.groups))
        button.pack()

    def selectBoundary(self,images):
        self.images=images
        self.clear_window()
        Choosing(self).pack()

    def set_manualBoundary(self):
        self.clear_window()
        MultipleBoundarySelection(self,self.images).pack()

    #TODO:implement Tudor Script
    def set_automaticBoundary(self):
        self.clear_window()
        UnitaryBoundarySelection(self,self.images).pack()

    def calculate_boundaries(self,data):
        self.clear_window()
        self.images = data
        m=CannyBoundarySlider(self,data)
        m.pack()
        button = customtkinter.CTkButton(self, text="Done", command=lambda: self.matching(m.parameters))
        button.pack()

    def global_parameters(self):
        self.clear_window()
        GeneralParameters(self, self.images).pack()

    def all_paremeters(self):
        self.clear_window()
        AllParameters(self,self.images).pack()

    def matching(self,parameters):
        self.clear_window()
        self.images["boundary_parameters"]=parameters
        Choosing2(self).pack()

    #TODO: Finish script for multiple analysis
    def end_analysis(self,data):
        self.clear_window()
        MultipleAnalysis(self,data).pack()


    #TODO: pre run parameters in 3 images, then confirm to end_anaylis
    def pre_run(self,data):
        self.clear_window()
        #ParameterTest(self,data).pack()


        
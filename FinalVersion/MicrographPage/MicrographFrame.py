import customtkinter
from FinalVersion.MicrographPage import ImagesUploader
from FinalVersion.MicrographPage import RawManager
from FinalVersion.MicrographPage import BoundarySelection
from FinalVersion.MicrographPage import ParameterTesting
from FinalVersion.MicrographPage import FinalAnalysisFrame

class MicrographFrame(customtkinter.CTkFrame):
    Images=""
    creator=""

    def __init__(self,creator):
        super().__init__(master=creator)
        self.creator=creator
        self.set_get_images()



    def back(self):
        self.creator.set_welcomepage()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def set_get_images(self):
        ImagesUploader.ImagesUploader(creator=self).pack()

    def set_raw(self):
        RawManager.RawManager(creator=self).pack(pady=100)

    def set_process_image(self,width=0,height=0):
        self.clear_window()
        BoundarySelection.BoundarySelection(creator=self,images=self.Images,width=width,height=height).pack()

    def set_parameters(self,img):
        self.clear_window()
        ParameterTesting.ParameterTesting(creator=self,img=img).pack()

    def set_final_Analysis(self,img,mean_weight,mean_range,pore_cut_off,Fidelity_Base):
        self.clear_window()
        Final_analysis=FinalAnalysisFrame.FinalAnalysisFrame(self)
        Final_analysis.pack()
        Final_analysis.analyse(img,mean_weight,mean_range,pore_cut_off,Fidelity_Base)





    def set_images(self,paths):
        self.clear_window()
        self.Images=paths
        if ".raw" in paths[0]:
            self.set_raw()
        else:
            self.set_process_image()





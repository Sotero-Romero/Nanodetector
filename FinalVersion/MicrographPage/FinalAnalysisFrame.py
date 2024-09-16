import customtkinter
from FinalVersion.MicrographPage.AnalysisFrames import ProgressFrame
from FinalVersion.Analysis.ImageAnalysis import FullAnalyseImage
from FinalVersion.MicrographPage.SaveFrame import SaveFrame

class FinalAnalysisFrame(customtkinter.CTkFrame):
    def __init__(self,creator):
        super(FinalAnalysisFrame, self).__init__(master=creator)

        ProgressFrame.ProgressFrame(self).pack()


        self.clear_window()





    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


    def analyse(self,img,mean_weight,mean_range,pore_cut_off,Fidelity_Base):
        self.img=FullAnalyseImage(img,mean_weight,mean_range,pore_cut_off,Fidelity_Base)
        self.load_save_frame()

    def load_save_frame(self):
        SaveFrame(self,self.img).pack()



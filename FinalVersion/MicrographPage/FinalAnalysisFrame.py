import customtkinter
from FinalVersion.MicrographPage.AnalysisFrames import ProgressFrame
from FinalVersion.Analysis.ImageAnalysis import FullAnalyseImage
from FinalVersion.MicrographPage.SaveFrame import SaveFrame

class FinalAnalysisFrame(customtkinter.CTkFrame):
    def __init__(self,creator):
        super(FinalAnalysisFrame, self).__init__(master=creator)

        ProgressFrame.ProgressFrame(self).pack()


    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


    def analyse(self,original_image,canny_minimum, canny_maximum, canny_ksize,canny_sigma,gaussian_fidelity,gaussian_range):
        self.img=FullAnalyseImage(original_image,canny_minimum, canny_maximum, canny_ksize,canny_sigma,gaussian_fidelity,gaussian_range)
        self.load_save_frame()

    def load_save_frame(self):
        self.clear_window()
        SaveFrame(self,self.img).pack()



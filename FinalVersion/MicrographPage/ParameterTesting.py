import customtkinter
from FinalVersion.MicrographPage.ParametersFrames.ImageDisplayer import ImageDisplayer
from FinalVersion.MicrographPage.ParametersFrames.ManualSelection import ManualSelection
from FinalVersion.Analysis.ImageAnalysis import AnalyseImage
from FinalVersion.MicrographPage.ParametersFrames.Bayesian import Bayesian
from FinalVersion.utilities.ImageCutter import ImageCutter

class ParameterTesting(customtkinter.CTkFrame):

    def __init__(self,creator,img):
        super(ParameterTesting, self).__init__(master=creator)

        self.img_copy=img
        self.creator=creator


        self.set_ImageCutter()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
    def img_cut_set(self,img):
        self.img_cut=img

    def set_premilinary_image(self,mean_weight=90,mean_range=11,pore_cut_off=3, Fidelity_Base=50):
        self.clear_window()
        img=AnalyseImage(self.img_cut,
                     mean_weight=mean_weight,
                     mean_range=mean_range,
                     pore_cut_off=pore_cut_off,
                     Fidelity_Base=Fidelity_Base
                     )

        ImageDisplayer(creator=self,image=img).pack()

        label=customtkinter.CTkLabel(master=self,text="Is the image good?")
        label.pack(pady=20)

        buttom_holder=customtkinter.CTkFrame(master=self,fg_color="transparent")
        buttom_holder.pack(pady=20)

        back=customtkinter.CTkButton(master=buttom_holder,text="No",command=self.set_parameter_selection)
        back.pack(side="left",padx=25)

        done = customtkinter.CTkButton(master=buttom_holder,text="Yes",command=lambda: self.creator.set_final_Analysis(self.img_copy,mean_weight,mean_range,pore_cut_off,Fidelity_Base))
        done.pack(side="left",padx=25)


    def set_parameter_selection(self):
        self.clear_window()
        label = customtkinter.CTkLabel(master=self, text="How do you want to select the settings?")
        label.pack(pady=20)

        buttom_holder = customtkinter.CTkFrame(master=self, fg_color="transparent")
        buttom_holder.pack(pady=20)

        back = customtkinter.CTkButton(master=buttom_holder, text="Manual",command=self.set_ManualSelection)
        back.pack(side="left", padx=25)

        done = customtkinter.CTkButton(master=buttom_holder, text="Automatic",command=self.set_Bayesian)
        done.pack(side="left", padx=25)

    def set_ManualSelection(self):
        self.clear_window()
        ManualSelection(self,self.img_cut).pack()

    def set_Bayesian(self):
        self.clear_window()
        Bayesian(self,self.img_copy).pack()

    def set_ImageCutter(self):
        self.clear_window()
        ImageCutter(self,self.img_copy).pack()


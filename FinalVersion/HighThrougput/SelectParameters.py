import customtkinter
from FinalVersion.HighThrougput.choosing import Choosing3
from FinalVersion.HighThrougput.Parameters import ManualParameters

class AllParameters(customtkinter.CTkFrame):
    currentImage=1
    def __init__(self,creator,data):
        super(AllParameters, self).__init__(creator)
        self.main_images=data
        Choosing3(self).pack()


    def manual(self):
        self.clear_window()
        image=self.main_images[f"image set {self.currentImage}"]["main_image"]
        ManualParameters(self,image).pack()


    def automatic(self):
        pass

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def saveParameters(self,m):
        self.main_images[f"image set {self.currentImage}"]["analysis_parameter"]={"canny":m.last_canny_params
                                                                                  ,"gauss":m.last_gaussian_params}
        del m
        self.currentImage+=1
        if not self.currentImage==len(self.main_images):
            self.manual()
        else:
            #return to main frame
            pass
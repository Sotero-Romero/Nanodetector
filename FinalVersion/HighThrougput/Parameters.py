import customtkinter
from FinalVersion.utilities.ImageCutter import ImageCutter
from FinalVersion.utilities.ImageProcessor import ImageProcessor
from FinalVersion.HighThrougput.CannyBoundarySlider import Multipleslider

class ManualParameters(customtkinter.CTkFrame):
    def __init__(self,creator,img):
        super(ManualParameters, self).__init__(creator)
        self.creator=creator
        width, height = img["dimensions"]
        image = ImageProcessor(img["path"], width, height, 0)

        ImageCutter(self,image).pack()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def img_cut_set(self,img):
        self.cutted_image=img

    def set_premilinary_image(self):
        self.clear_window()
        m=Multipleslider(self,self.cutted_image)
        m.pack()
        done = customtkinter.CTkButton(self, text="Done", command=lambda: self.creator.saveParameters(m))
        done.pack()

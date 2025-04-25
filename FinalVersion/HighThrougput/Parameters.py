import customtkinter
from FinalVersion.utilities.ImageCutter import ImageCutter
from FinalVersion.utilities.ImageProcessor import ImageProcessor
from FinalVersion.MicrographPage.ParametersFrames.Bayesian import Bayesian
from FinalVersion.MicrographPage.ParametersFrames.ManualSelection import ManualSelection

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
        m=ManualSelection(self,self.cutted_image)
        m.pack()

    def storeParameters(self,canny_minimum, canny_maximum, canny_ksize,canny_sigma,gaussian_fidelity,gaussian_range):
        last_canny_params = {'canny_minimum': canny_minimum, 'canny_maximum': canny_maximum, 'canny_ksize':canny_ksize, 'canny_sigma': canny_sigma}
        last_gaussian_params = {'gaussian_fidelity': gaussian_fidelity, 'gaussian_range': gaussian_range}
        self.creator.saveParametersManual(last_canny_params,last_gaussian_params)


class AutomaticParameters(customtkinter.CTkFrame):
    def __init__(self,creator,img):
        super(AutomaticParameters, self).__init__(creator)
        self.creator=creator
        width, height = img["dimensions"]
        image = ImageProcessor(img["path"], width, height, 0)
        Bayesian(self,image).pack()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


    def set_premilinary_image(self,canny_minimum, canny_maximum, canny_ksize,canny_sigma,gaussian_fidelity,gaussian_range):
        self.clear_window()
        canny_params = {'canny_minimum': canny_minimum, 'canny_maximum': canny_maximum, 'canny_ksize':canny_ksize, 'canny_sigma': canny_sigma}
        gaussian_params = {'gaussian_fidelity': gaussian_fidelity, 'gaussian_range': gaussian_range}
        self.creator.saveParametersAutomatic(canny_params,gaussian_params)


#TODO: Wait for Tudor to confirm how he wants it
class ParameterTest(customtkinter.CTkFrame):
    def __init__(self,creator,data):
        super(ParameterTest, self).__init__(creator)




import customtkinter
from FinalVersion.HighThrougput.choosing import Choosing3
from FinalVersion.HighThrougput.Parameters import ManualParameters,AutomaticParameters

class AllParameters(customtkinter.CTkFrame):
    currentImage=1
    def __init__(self,creator,data):
        super(AllParameters, self).__init__(creator)
        self.creator=creator
        self.main_images=data
        Choosing3(self).pack()


    def manual(self):
        self.clear_window()
        image=self.main_images[f"image set {self.currentImage}"]["main_image"]
        ManualParameters(self,image).pack()


    def automatic(self):
        self.clear_window()
        image = self.main_images[f"image set {self.currentImage}"]["main_image"]
        AutomaticParameters(self, image).pack()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def saveParametersManual(self,last_canny_params,last_gaussian_params ):
        self.main_images[f"image set {self.currentImage}"]["analysis_parameter"]={"canny":last_canny_params
                                                                                  ,"gauss":last_gaussian_params}
        self.currentImage+=1
        if not self.currentImage>=len(self.main_images):
            self.manual()
        else:
            #return to main frame
            self.creator.end_analysis(self.main_images)


    def saveParametersAutomatic(self,last_canny_params,last_gaussian_params):
        self.main_images[f"image set {self.currentImage}"]["analysis_parameter"] = {"canny": last_canny_params
            , "gauss": last_gaussian_params}

        self.currentImage += 1
        if not self.currentImage >= len(self.main_images):
            self.automatic()
        else:
            # return to main frame
            self.creator.end_analysis(self.main_images)


class GeneralParameters(customtkinter.CTkFrame):
    def __init__(self,creator,data):
        super(GeneralParameters, self).__init__(creator)
        self.creator = creator
        self.main_images = data
        Choosing3(self).pack()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def manual(self):
        self.clear_window()
        image=self.main_images[f"image set {1}"]["main_image"]
        ManualParameters(self,image).pack()


    def automatic(self):
        self.clear_window()
        image = self.main_images[f"image set {1}"]["main_image"]
        AutomaticParameters(self, image).pack()

    def saveParametersManual(self,last_canny_params,last_gaussian_params):
        for image_set in self.main_images:
            if image_set == "boundary_parameters": continue
            self.main_images[image_set]["analysis_parameter"]={"canny":last_canny_params,"gauss":last_gaussian_params}
        self.creator.pre_run(self.main_images)


    def saveParametersAutomatic(self,last_canny_params,last_gaussian_params):
        for image_set in self.main_images:
            if image_set == "boundary_parameters": continue
            self.main_images[image_set]["analysis_parameter"] = {"canny": last_canny_params
                , "gauss": last_gaussian_params}
        self.creator.pre_run(self.main_images)




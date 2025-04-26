import customtkinter
from PIL import Image
from FinalVersion.Analysis.ImageAnalysis import AnalyseImage
from FinalVersion.HighThrougput.choosing import Choosing2
from FinalVersion.utilities.ImageCutter import ImageCutter
from FinalVersion.utilities.ImageProcessor import ImageProcessor
from FinalVersion.MicrographPage.ParametersFrames.Bayesian import Bayesian
from FinalVersion.MicrographPage.ParametersFrames.ManualSelection import ManualSelection


class ManualParameters(customtkinter.CTkFrame):
    def __init__(self, creator, img):
        super(ManualParameters, self).__init__(creator)
        self.creator = creator
        width, height = img["dimensions"]
        image = ImageProcessor(img["path"], width, height, 0)

        ImageCutter(self, image).pack()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def img_cut_set(self, img):
        self.cutted_image = img

    def set_premilinary_image(self):
        self.clear_window()
        m = ManualSelection(self, self.cutted_image)
        m.pack()

    def storeParameters(self, canny_minimum, canny_maximum, canny_ksize, canny_sigma, gaussian_fidelity,
                        gaussian_range):
        last_canny_params = {'canny_minimum': canny_minimum, 'canny_maximum': canny_maximum, 'canny_ksize': canny_ksize,
                             'canny_sigma': canny_sigma}
        last_gaussian_params = {'gaussian_fidelity': gaussian_fidelity, 'gaussian_range': gaussian_range}
        self.creator.saveParametersManual(last_canny_params, last_gaussian_params)


class AutomaticParameters(customtkinter.CTkFrame):
    def __init__(self, creator, img):
        super(AutomaticParameters, self).__init__(creator)
        self.creator = creator
        width, height = img["dimensions"]
        image = ImageProcessor(img["path"], width, height, 0)
        Bayesian(self, image).pack()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def set_premilinary_image(self, canny_minimum, canny_maximum, canny_ksize, canny_sigma, gaussian_fidelity,
                              gaussian_range):
        self.clear_window()
        canny_params = {'canny_minimum': canny_minimum, 'canny_maximum': canny_maximum, 'canny_ksize': canny_ksize,
                        'canny_sigma': canny_sigma}
        gaussian_params = {'gaussian_fidelity': gaussian_fidelity, 'gaussian_range': gaussian_range}
        self.creator.saveParametersAutomatic(canny_params, gaussian_params)


class ParameterTest(customtkinter.CTkFrame):
    def __init__(self, creator, data):
        super(ParameterTest, self).__init__(creator)

        iteration = min(3, len(data))

        frame=customtkinter.CTkFrame(self)
        frame.pack()

        label1 = customtkinter.CTkLabel(frame, text="")
        label1.pack(side="left",padx=20, pady=20)
        label2 = customtkinter.CTkLabel(frame, text="")
        label2.pack(side="left",padx=20, pady=20)
        label3 = customtkinter.CTkLabel(frame, text="")
        label3.pack(side="left",padx=20, pady=20)

        for sets,labels in zip(data,[label1,label2,label3]):
            if iteration == 0: break
            if sets == "boundary_parameters": continue

            sets=data[sets]

            img = ImageProcessor(sets["main_image"]["path"], sets["main_image"]["dimensions"][0],
                                 sets["main_image"]["dimensions"][1], 0)

            canny_params = sets["analysis_parameter"]["canny"]
            canny_minimum = canny_params["canny_minimum"]
            canny_maximum = canny_params["canny_maximum"]
            canny_ksize = canny_params["canny_ksize"]
            canny_sigma = canny_params["canny_sigma"]

            gaussian_params = sets["analysis_parameter"]["gauss"]
            gaussian_fidelity = gaussian_params["gaussian_fidelity"]
            gaussian_range = gaussian_params["gaussian_range"]

            img = AnalyseImage(img,
                               canny_minimum,
                               canny_maximum,
                               canny_ksize,
                               canny_sigma,
                               gaussian_fidelity,
                               gaussian_range,
                               )
            img=self.numpy_to_ctkimage(img,(400,400))
            labels.configure(image=img)

            iteration -= 1

        button1=customtkinter.CTkButton(self,text="I like it", command= lambda : creator.end_analysis(data))
        button1.pack()

        button2=customtkinter.CTkButton(self,text="Change parameters", command= lambda : creator.matching(data["boundary_parameters"]))
        button2.pack()


    def numpy_to_ctkimage(self, np_array, size=None):

        # Convert to PIL Image
        pil_image = Image.fromarray(np_array, mode='L')

        # Resize if needed
        if size:
            pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)

        # Create CTkImage
        ctk_image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=size or pil_image.size)
        return ctk_image


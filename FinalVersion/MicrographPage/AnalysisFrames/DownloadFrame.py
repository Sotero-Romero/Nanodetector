import customtkinter
from FinalVersion.MicrographPage.ParametersFrames.ImageDisplayer import ImageDisplayer
from tkinter import filedialog

class DownloadFrame(customtkinter.CTkFrame):
    def __init__(self,creator,img):
        super(DownloadFrame, self).__init__(master=creator)

        self.img = img
        self.creator = creator

        # original image
        self.imageDisplayer = ImageDisplayer(self, self.img, downgrade=True)
        self.imageDisplayer.can.mpl_connect('motion_notify_event', self.hover_event)
        self.imageDisplayer.pack(side=customtkinter.LEFT, padx=20)

        self.imageDisplayerCut = ImageDisplayer(self, self.img, downgrade=True)
        self.imageDisplayerCut.clear()
        self.imageDisplayerCut.pack(side=customtkinter.LEFT, padx=20)

        self.button=customtkinter.CTkButton(self,text="Download",command=self.download)
        self.button.pack(side=customtkinter.BOTTOM, pady=20)

    def hover_event(self, event):
        if event.xdata != None:
            y = round(event.xdata * 10)
            x = round(event.ydata * 10)

            cutted_img = self.img[x - 250:x + 250, y - 250:y + 250]

            self.imageDisplayerCut.update_Image(cutted_img)


    #TODO:investigate how to save as
    def download(self):
        path=filedialog.askdirectory()


import customtkinter
from FinalVersion.MicrographPage.ParametersFrames.ImageDisplayer import ImageDisplayer

class ImageCutter(customtkinter.CTkFrame):
    def __init__(self,creator,img):
        super(ImageCutter, self).__init__(master=creator)

        self.img=img
        self.creator=creator

        # original image
        self.imageDisplayer = ImageDisplayer(self, self.img, downgrade=True)
        self.imageDisplayer.can.mpl_connect('motion_notify_event', self.hover_event)
        self.imageDisplayer.can.mpl_connect('button_press_event', self.click_event)
        self.imageDisplayer.pack(side=customtkinter.LEFT,padx=20)

        self.imageDisplayerCut = ImageDisplayer(self, self.img, downgrade=True)
        self.imageDisplayerCut.clear()
        self.imageDisplayerCut.pack(side=customtkinter.LEFT,padx=20)


    def hover_event(self,event):
        if event.xdata != None:
            y = round(event.xdata*10)
            x = round(event.ydata*10)

            cutted_img=self.img[x - 250:x + 250, y - 250:y + 250]

            self.imageDisplayerCut.update_Image(cutted_img)

    def click_event(self,event):
        if event.button == 3 and event.xdata != None:
            y = round(event.xdata * 10)
            x = round(event.ydata * 10)

            cutted_img = self.img[x - 250:x + 250, y - 250:y + 250]

            self.creator.img_cut_set(cutted_img)
            self.creator.set_premilinary_image()




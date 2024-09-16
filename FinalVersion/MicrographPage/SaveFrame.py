from tkinter.filedialog import asksaveasfilename
import customtkinter
from FinalVersion.MicrographPage.ParametersFrames.ImageDisplayer import ImageDisplayer
import shutil
import os


class SaveFrame(customtkinter.CTkFrame):
    def __init__(self,creator,img):
        super(SaveFrame, self).__init__(master=creator)

        self.img=img

        self.imageDisplayer = ImageDisplayer(self, self.img, downgrade=True)
        self.imageDisplayer.can.mpl_connect('motion_notify_event', self.hover_event)
        self.imageDisplayer.pack(side=customtkinter.LEFT, padx=20)

        self.imageDisplayerSave = ImageDisplayer(self, self.img, downgrade=True)
        self.imageDisplayerSave.clear()
        self.imageDisplayerSave.pack(side=customtkinter.LEFT, padx=20)

        self.download=customtkinter.CTkButton(self,text="Download",command=self.download)
        self.download.pack(side=customtkinter.BOTTOM)

    def hover_event(self,event):
        if event.xdata != None:
            y = round(event.xdata*10)
            x = round(event.ydata*10)

            cutted_img=self.img[x - 250:x + 250, y - 250:y + 250]

            self.imageDisplayerSave.update_Image(cutted_img)
    def download(self):
        feather_path = os.path.join("BackUp", "backup.feather")
        new_file_path = asksaveasfilename(
            defaultextension=".feather",
            filetypes=[("Feather files", "*.feather"), ("All files", "*.*")]
        )
        if new_file_path:
            # Copy and rename the file
            shutil.copy(feather_path, new_file_path)

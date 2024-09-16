import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from cv2 import resize

class ImageDisplayer(customtkinter.CTkFrame):

    def __init__(self,creator,image,extent=None,downgrade=False):
        super(ImageDisplayer, self).__init__(master=creator)

        if downgrade:
            image=self.downgrade(image)

        self.frame_1 = Figure(figsize=(5, 5))
        self.can = FigureCanvasTkAgg(self.frame_1,master=self)
        self.can.get_tk_widget().pack()
        self.axs = self.frame_1.add_subplot()
        self.axs.imshow(image,extent=extent)

        self.toolbar = NavigationToolbar2Tk(self.can, self)
        self.toolbar.update()
        self.can.get_tk_widget().pack()

        self.can.draw()

    def update_Image(self,img,extent=None,downgrade=False):
        if downgrade:
            img=self.downgrade(img)

        self.axs.remove()
        self.axs = self.frame_1.add_subplot()
        self.axs.imshow(img,extent=extent)
        self.can.draw()

    def downgrade(self,img):
        new_width = int(img.shape[1] * 0.1)  # Reduce width by 50%
        new_height = int(img.shape[0] * 0.1)  # Reduce height by 50%
        new_dimensions = (new_width, new_height)
        img2 = resize(img, new_dimensions)
        return img2

    def clear(self):
        self.axs.cla()
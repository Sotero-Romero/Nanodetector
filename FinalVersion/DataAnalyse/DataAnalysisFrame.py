import customtkinter
from FinalVersion.DataAnalyse.Plotter import Plotter
from tkinter import filedialog

class DataAnalysisFrame(customtkinter.CTkFrame):

    def __init__(self,creator):
        super(DataAnalysisFrame, self).__init__(creator)

        path = filedialog.askopenfile(mode='r', filetypes=[('Feather File', '*feather')])
        if path != None:
            path = path.name

            self.selection_frame = customtkinter.CTkFrame(master=self)
            self.selection_frame.pack(side=customtkinter.LEFT)

            self.plots = Plotter(self, path)
            self.plots.pack(side=customtkinter.LEFT)

            histogram = customtkinter.CTkButton(self.selection_frame, text="Histogram", fg_color="transparent",
                                                command=self.plots.histogram_log_area)
            histogram.pack()

            bar = customtkinter.CTkButton(self.selection_frame, text="Bar chart", fg_color="transparent",
                                          command=self.plots.bar_chart)
            bar.pack()

            rose = customtkinter.CTkButton(self.selection_frame, text="Rose Diagram", fg_color="transparent",
                                           command=self.plots.rose_diagram)
            rose.pack()

            bubble = customtkinter.CTkButton(self.selection_frame, text="Bubble Plot", fg_color="transparent",
                                             command=self.plots.bubble_plot)
            bubble.pack()

            line = customtkinter.CTkButton(self.selection_frame, text="Distance Vs Area", fg_color="transparent",
                                           command=self.plots.distanceVSarea)
            line.pack()

        else:
            creator.set_welcomepage()


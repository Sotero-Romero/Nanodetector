import time

import customtkinter
from FinalVersion.MicrographPage.ParametersFrames.ImageDisplayer import ImageDisplayer
from FinalVersion.Analysis.BayesianEvaluation import bayesianEvaluation
import matplotlib.pyplot as plt
from skopt import gp_minimize
from skopt.space import  Integer, Categorical
import threading




class Bayesian(customtkinter.CTkFrame):
    points=[]

    def __init__(self,creator,img):
        super(Bayesian, self).__init__(master=creator)

        self.img=img
        self.creator=creator

        self.imageDisplayer=ImageDisplayer(self,img,downgrade=True)
        self.imageDisplayer.can.mpl_connect('key_press_event',self.click_event_mini)
        self.imageDisplayer.pack()

        self.done=customtkinter.CTkButton(master=self,text="Done",command=self.set_optimice,state="disabled")
        self.done.pack()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def click_event_mini(self,event):
        plt.clf()

        if event.key == "p":
            # avoid finishing if no pont are selected
            self.done.configure(state="normal")

            y = round(event.xdata)
            x = round(event.ydata)
            self.points.append(("pore", self.img[x - 150:x + 150, y - 150:y + 150]))
        elif event.key == "b":
            # avoid finishing if no pont are selected
            self.done.configure(state="normal")

            y = round(event.xdata)
            x = round(event.ydata)
            self.points.append(("background", self.img[x - 150:x + 150, y - 150:y + 150]))

        elif event.key == "z":
            y = round(event.xdata * 10)
            x = round(event.ydata * 10)
            extent = [y - 250, y + 250, x + 250, x - 250]
            # Display the image with the specified extent
            self.imageDisplayer.update_Image(self.img[x - 250:x + 250, y - 250:y + 250],extent)

        elif event.key == "backspace":
            self.imageDisplayer.update_Image(self.img,downgrade=True)

    def set_optimice(self):
        self.clear_window()

        self.max = 0

        self.percentage = customtkinter.CTkLabel(master=self, text="Accuracy: 0%", font=("calibri", 100))
        self.percentage.pack(pady=100)

        self.progress_bar = customtkinter.CTkProgressBar(master=self)
        self.progress_bar.set(0)
        self.progress_bar.pack()

        # Define parameter space
        self.param_space = [
            Integer(0, 255, name='canny_minimum'),
            Integer(0, 255, name='canny_maximum'),
            Categorical(list(range(1, 100, 2)), name="canny_ksize"),
            Integer(0,50,name='canny_sigma'),
            Integer(3,60,name='gaussian_fidelity'),
            Categorical(list(range(35, 512, 2)), name="gaussian_range")
        ]

        self.start_optimization()

    def start_optimization(self):
        optimization_thread = threading.Thread(target=self.run_optimization)
        optimization_thread.start()

    def run_optimization(self):
        def objective_function(params):
            canny_minimum, canny_maximum, canny_ksize,canny_sigma,gaussian_fidelity,gaussian_range   = params
            p = self.points
            # Replace with your actual function to evaluate success rate
            return -bayesianEvaluation(canny_minimum, canny_maximum, canny_ksize,canny_sigma,gaussian_fidelity,gaussian_range, p)

        def callback(result):
            self.progress_bar.set(self.progress_bar.get() + 0.02)

            if -result.fun > self.max:
                self.max = -result.fun
                self.percentage.configure(text=f"Accuracy: {round(self.max*100)}%")

            if -result.fun >= 0.8:  # Convert negative success rate back to positive
                self.progress_bar.set(1)
                time.sleep(2)
                return True

        result = gp_minimize(objective_function, self.param_space, n_calls=50, callback=callback)
        self.after(0, lambda: self.handle_optimization_result(result.x))


    def handle_optimization_result(self,result):

        self.creator.set_premilinary_image(
            canny_minimum=result[0],
            canny_maximum=result[1],
            canny_ksize=result[2],
            canny_sigma=result[3],
            gaussian_fidelity=result[4],
            gaussian_range=result[5]
        )




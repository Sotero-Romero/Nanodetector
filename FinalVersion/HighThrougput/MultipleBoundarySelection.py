import customtkinter
import numpy as np
from FinalVersion.MicrographPage.ParametersFrames.ImageDisplayer import ImageDisplayer
from FinalVersion.utilities.ImageProcessor import ImageProcessor
import itertools


class MultipleBoundarySelection(customtkinter.CTkFrame):
    image_set_counter=1


    def __init__(self,creator, image_set):
        super().__init__(master=creator)

        self.creator=creator
        self.image_set=image_set
        self.colors = itertools.cycle(['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta'])
        self.color=next(self.colors)

        self.set_up()




    def set_up(self):
        self.point_counter = 0
        self.image_counter = 0
        self.boundary_counter = 0
        self.points=[[[]]]


        self.images=self.image_set[f"image set {self.image_set_counter}"]["images"]

        width,height=self.images[self.image_counter]["dimensions"]
        self.current_image=ImageProcessor(self.images[self.image_counter]["path"],width,height,0)



        self.imageDisplayer=ImageDisplayer(self,self.current_image,downgrade=True)
        self.imageDisplayer.can.mpl_connect('button_press_event', self.click_event)
        self.imageDisplayer.can.mpl_connect('key_press_event', self.delete)
        self.imageDisplayer.pack()

        self.label = customtkinter.CTkLabel(master=self, text="Select a point outside the boundary")
        self.label.pack(pady=20)


        self.boundaryButtom=customtkinter.CTkButton(self,text="+ Boundary",command=self.add_boundary,state="disabled")
        self.boundaryButtom.pack()

        self.done=customtkinter.CTkButton(master=self,text="Next Image",command=self.next_image,state="disabled")
        self.done.pack()

        if self.image_counter==len(self.images)-1:
            self.done.configure(text="Done",command=self.next_set)


    def delete(self,event):
        if event.key=="backspace":
            if not self.points[self.image_counter][self.boundary_counter]==[]:
                self.points[self.image_counter][self.boundary_counter].pop()
                self.imageDisplayer.axs.get_lines()[-1].remove()
                self.imageDisplayer.can.draw()


    def click_event(self,event):
        if event.button == 3 and event.xdata != None and self.point_counter<2:
            y = round(event.xdata * 10)
            x = round(event.ydata * 10)
            if self.point_counter==0:
                self.image_set[f"image set {self.image_set_counter}"]["Out_points"]=[[x,y]]
                self.label.configure(text="Select a point inside the boundary")
            else:
                self.image_set[f"image set {self.image_set_counter}"]["In_points"]=[[x,y]]
                self.label.configure(text="Select boundary points")
            self.point_counter+=1


        elif event.button == 3 and event.xdata != None:
            self.done.configure(state="normal")
            self.boundaryButtom.configure(state="normal")


            y = round(event.xdata * 10)
            x = round(event.ydata * 10)

            if x<=self.current_image.shape[1]*0.01:
                x=1
            elif y<=self.current_image.shape[0]*0.01:
                y=1
            elif x>=self.current_image.shape[0]*(1-0.01):
                x=self.current_image.shape[0]-2
            elif y>=self.current_image.shape[1]*(1-0.01):
                y=self.current_image.shape[1]-2
            for element in self.points:
                for boundary in element:
                    for points in boundary:
                        if np.linalg.norm(np.array(points) - np.array((x,y))) < 1700:
                            if not points in self.points[self.image_counter][self.boundary_counter]:
                                print("clip")
                                x,y=points
                            break
            self.imageDisplayer.axs.plot(y//10, x//10, "o", color=self.color)
            self.imageDisplayer.can.draw()

            self.points[self.image_counter][self.boundary_counter].append((x,y))

    def add_boundary(self):
        self.boundary_counter+=1
        self.points[self.image_counter].append([])
        self.color=next(self.colors)

    def next_image(self):
        self.boundary_counter=0
        self.image_counter+=1
        self.points.append([[]])

        width, height = self.images[self.image_counter]["dimensions"]
        self.current_image = ImageProcessor(self.images[self.image_counter]["path"], width, height, 0)

        self.imageDisplayer.update_Image(self.current_image,downgrade=True)

        self.done.configure(state="disabled")
        self.boundaryButtom.configure(state="disabled")

        if self.image_counter==len(self.images)-1:
            self.done.configure(text="Done",command=self.next_set)

        self.colors = itertools.cycle(['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta'])
        self.color=next(self.colors)


    def next_set(self):
        self.clear_window()

        self.image_set[f"image set {self.image_set_counter}"]["Boundary_points"] = self.points
        if self.image_set_counter>=len(self.image_set):
            self.creator.calculate_boundaries(self.image_set)
        else:
            self.image_set_counter+=1
            self.set_up()


    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()




class UnitaryBoundarySelection(customtkinter.CTkFrame):
    def __init__(self,creator,image_set):
        super(UnitaryBoundarySelection, self).__init__(creator)

        self.creator = creator
        self.image_set = image_set
        self.colors = itertools.cycle(['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta'])
        self.color = next(self.colors)

        self.set_up()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


    def set_up(self):
        self.point_counter = 0
        self.boundary_counter = 0
        self.points = [[]]

        self.image = self.image_set[f"image set 0"]["main_image"]

        width, height = self.image["dimensions"]
        self.current_image = ImageProcessor(self.image["path"], width, height, 0)

        self.imageDisplayer = ImageDisplayer(self, self.current_image, downgrade=True)
        self.imageDisplayer.can.mpl_connect('button_press_event', self.click_event)
        self.imageDisplayer.can.mpl_connect('key_press_event', self.delete)
        self.imageDisplayer.pack()

        self.label = customtkinter.CTkLabel(master=self, text="Select a point outside the boundary")
        self.label.pack(pady=20)

        self.boundaryButtom = customtkinter.CTkButton(self, text="+ Boundary", command=self.add_boundary,
                                                      state="disabled")
        self.boundaryButtom.pack()

        self.done = customtkinter.CTkButton(master=self, text="Done", command=self.next_image, state="disabled")
        self.done.pack()

    def delete(self, event):
        if event.key == "backspace":
            if not self.points[self.boundary_counter] == []:
                self.points[self.boundary_counter].pop()
                self.imageDisplayer.axs.get_lines()[-1].remove()
                self.imageDisplayer.can.draw()

    def click_event(self, event):
        if event.button == 3 and event.xdata != None and self.point_counter < 2:
            y = round(event.xdata * 10)
            x = round(event.ydata * 10)
            if self.point_counter == 0:
                self.OutPoints = [[x, y]]
                self.label.configure(text="Select a point inside the boundary")
            else:
                self.InPoints = [[x, y]]
                self.label.configure(text="Select boundary points")
            self.point_counter += 1


        elif event.button == 3 and event.xdata != None:
            self.done.configure(state="normal")
            self.boundaryButtom.configure(state="normal")

            y = round(event.xdata * 10)
            x = round(event.ydata * 10)

            if x <= self.current_image.shape[1] * 0.01:
                x = 1
            elif y <= self.current_image.shape[0] * 0.01:
                y = 1
            elif x >= self.current_image.shape[0] * (1 - 0.01):
                x = self.current_image.shape[0] - 2
            elif y >= self.current_image.shape[1] * (1 - 0.01):
                y = self.current_image.shape[1] - 2
            for element in self.points:
                for boundary in element:
                    for points in boundary:
                        if np.linalg.norm(np.array(points) - np.array((x, y))) < 1700:
                            if not points in self.points[self.boundary_counter]:
                                x, y = points
                            break
            self.imageDisplayer.axs.plot(y // 10, x // 10, "o", color=self.color)
            self.imageDisplayer.can.draw()

            self.points[self.boundary_counter].append((x, y))


    def add_boundary(self):
        self.boundary_counter+=1
        self.points.append([])
        self.color=next(self.colors)

    #TODO: finish this
    def done(self):
        pass







import customtkinter
import numpy as np
from FinalVersion.Analysis.BoundaryIsolation import Isolate_Boundary
from FinalVersion.MicrographPage.ParametersFrames.ImageDisplayer import ImageDisplayer
from FinalVersion.utilities.ImageProcessor import ImageProcessor
import itertools


class BoundarySelection(customtkinter.CTkFrame):
    points=[[[]]]
    points_inside=[]
    points_outside=[]
    point_counter=0
    image_counter=0
    boundary_counter=0

    def __init__(self,creator, images,width,height):
        super().__init__(master=creator)

        self.creator=creator
        self.images=images
        self.width=width
        self.height=height
        self.colors = itertools.cycle(['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta'])
        self.color=next(self.colors)


        self.current_image=ImageProcessor(self.images[self.image_counter],width,height,14)

        self.label=customtkinter.CTkLabel(master=self,text="Select a point outside the boundary")
        self.label.pack(pady=20)


        self.imageDisplayer=ImageDisplayer(creator,self.current_image,downgrade=True)
        self.imageDisplayer.can.mpl_connect('button_press_event', self.click_event)
        self.imageDisplayer.can.mpl_connect('key_press_event', self.delete)
        self.imageDisplayer.pack()


        self.boundaryButtom=customtkinter.CTkButton(self,text="+ Boundary",command=self.add_boundary,state="disabled")
        self.boundaryButtom.pack()

        self.done=customtkinter.CTkButton(master=self,text="Next Image",command=self.next_image,state="disabled")
        self.done.pack()

        if self.image_counter==len(self.images)-1:
            self.done.configure(text="Done",command=self.isolate)


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
                self.points_outside.append([x,y])
                self.label.configure(text="Select a point inside the boundary")
            else:
                self.points_inside.append([x,y])
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
        self.current_image=ImageProcessor(self.images[self.image_counter],self.width,self.height)
        self.imageDisplayer.update_Image(self.current_image,downgrade=True)

        self.done.configure(state="disabled")
        self.boundaryButtom.configure(state="disabled")

        if self.image_counter==len(self.images)-1:
            self.done.configure(text="Done",command=self.isolate)

        self.colors = itertools.cycle(['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta'])
        self.color=next(self.colors)




    #TODO: make it work
    def isolate(self):
        del self.current_image
        #img=Isolate_Boundary(self.images,self.points,self.points_inside,self.points_outside,width=self.width,height=self.height)
        self.creator.set_parameters(ImageProcessor(self.images[0],self.width,self.height))
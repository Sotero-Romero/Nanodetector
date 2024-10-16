import customtkinter

class Choosing(customtkinter.CTkFrame):
    def __init__(self,creator):
        super(Choosing, self).__init__(creator)

        label=customtkinter.CTkLabel(self,text="Manual or Automatic Boundary Selection?")
        label.pack()

        holder=customtkinter.CTkFrame(self)
        holder.pack()

        button1=customtkinter.CTkButton(holder,text="Manual",command=creator.set_manualBoundary)
        button1.pack(side=customtkinter.LEFT)

        button2=customtkinter.CTkButton(holder,text="Automatic",command=creator.set_automaticBoundary)
        button2.pack(side=customtkinter.LEFT)


class Choosing2(customtkinter.CTkFrame):
    def __init__(self, creator):
        super(Choosing2, self).__init__(creator)

        label = customtkinter.CTkLabel(self, text="Do you want to select parameters for each image?")
        label.pack()

        holder = customtkinter.CTkFrame(self)
        holder.pack()

        button1 = customtkinter.CTkButton(holder, text="Yes", command=creator.all_paremeters)
        button1.pack(side=customtkinter.LEFT)

        button2 = customtkinter.CTkButton(holder, text="No", command=creator.global_parameters)
        button2.pack(side=customtkinter.LEFT)

class Choosing3(customtkinter.CTkFrame):
    def __init__(self, creator):
        super(Choosing3, self).__init__(creator)

        label = customtkinter.CTkLabel(self, text="How do you want to select the parameters?")
        label.pack()

        holder = customtkinter.CTkFrame(self)
        holder.pack()

        button1 = customtkinter.CTkButton(holder, text="Manual", command=creator.manual)
        button1.pack(side=customtkinter.LEFT)

        button2 = customtkinter.CTkButton(holder, text="Automatic", command=creator.automatic)
        button2.pack(side=customtkinter.LEFT)


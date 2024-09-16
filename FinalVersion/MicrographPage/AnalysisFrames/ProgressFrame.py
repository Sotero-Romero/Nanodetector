import customtkinter


class ProgressFrame(customtkinter.CTkFrame):
    def __init__(self,creator):
        super(ProgressFrame, self).__init__(master=creator)

        label=customtkinter.CTkLabel(self,text="Analysing")
        label.pack(pady=200)


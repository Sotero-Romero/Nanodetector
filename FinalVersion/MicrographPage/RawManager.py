import customtkinter

class RawManager(customtkinter.CTkFrame):

    def __init__(self,creator):
        super().__init__(master=creator)

        title_height=customtkinter.CTkLabel(master=self,text="HEIGHT",font=("futura",30))
        title_height.pack(pady=20)

        height=customtkinter.CTkEntry(master=self,placeholder_text="Height",width=420,height=84,font=("futura", 30))
        height.pack(padx=50)

        title_width = customtkinter.CTkLabel(master=self, text="WIDTH", font=("futura", 30))
        title_width.pack(pady=20)

        width=customtkinter.CTkEntry(master=self,placeholder_text="Width",width=420,height=84,font=("futura", 30))
        width.pack(padx=50)

        done=customtkinter.CTkButton(master=self,text="Done",command=lambda : creator.set_process_image(width.get(),height.get()))
        done.pack(pady=25)





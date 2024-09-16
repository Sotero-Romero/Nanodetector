import customtkinter

class ButtonFrame(customtkinter.CTkFrame):
    def __init__(self,creator,window):
        super().__init__(master=creator)

        button1=customtkinter.CTkButton(master=self,text="Analyse Micrograph")
        button1.configure(command=window.set_analysis)
        button1.pack(padx=10,pady=10)

        button2 = customtkinter.CTkButton(master=self, text="Analyse Stack")
        button2.configure(command=window.set_analysis_stack)
        button2.pack(padx=10, pady=10)

        button3 = customtkinter.CTkButton(master=self, text="Load Data")
        button3.configure(command=window.set_analyse_load)
        button3.pack(padx=10, pady=10)

        button4 = customtkinter.CTkButton(master=self, text="Settings")
        button4.configure(command=window.set_settings)
        button4.pack(padx=10, pady=10)

        button5 = customtkinter.CTkButton(master=self, text="Credits")
        button5.configure(command=window.set_credits)
        button5.pack(padx=10, pady=10)






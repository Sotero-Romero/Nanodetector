import customtkinter
from FinalVersion.WelcomePage.ButtonFrame import ButtonFrame


class WelcomeFrame(customtkinter.CTkFrame):

    def __init__(self,creator):
        #initializaton of CTK window
        super().__init__(master=creator)


        #adding label
        title=customtkinter.CTkLabel(master=self,text="NanoDetector",font=("futura",50))
        title.pack(padx=50,pady=50)

        #adding buttons
        buttonframe=ButtonFrame(self,creator)
        buttonframe.pack(padx=50,pady=50)








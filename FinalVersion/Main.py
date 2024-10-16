import customtkinter
from FinalVersion.WelcomePage import WelcomeFrame
from FinalVersion.MicrographPage import MicrographFrame
from FinalVersion.DataAnalyse.DataAnalysisFrame import DataAnalysisFrame
from FinalVersion.HighThrougput.HighThroughFrame import HighThroughFrame


class window(customtkinter.CTk):
    def __init__(self):
        # initializaton of CTK window
        super().__init__()


        # window configuration
        self.title("NanoDetector")
        self.state('zoomed')
        self.attributes('-fullscreen', True)

        self.set_welcomepage()



    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def set_welcomepage(self):
        self.clear_window()
        WelcomeFrame.WelcomeFrame(creator=self).pack(fill="both", expand=True)


    def set_analysis(self):
        self.clear_window()
        MicrographFrame.MicrographFrame(creator=self).pack(fill="both", expand=True)

    def set_analysis_stack(self):
        self.clear_window()
        HighThroughFrame(self).pack()

    def set_analyse_load(self):
        self.clear_window()
        DataAnalysisFrame(self).pack()


    def set_credits(self):
        pass

    def set_settings(self):
        pass





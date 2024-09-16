import customtkinter
from tkinter import filedialog



class ImagesUploader(customtkinter.CTkFrame):
    file_frame="Scrollable Frame"
    switch="switch"
    file_button="button"
    maxImages=0
    Paths=[]

    def __init__(self,creator,max=-1):
        super().__init__(master=creator)
        self.maxImages=max
        self.file_frame=customtkinter.CTkScrollableFrame(master=self,width=800,height=200)
        self.file_frame.pack(pady=50,padx=50)


        self.file_button = customtkinter.CTkButton(
            master=self,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            text="Add file",
            command=lambda: self.get_file()
        )
        self.file_button.pack(pady=50,padx=50)


        self.switch = customtkinter.CTkCheckBox(self, text="Secondary Image", corner_radius=20)
        self.switch.pack(pady=20)

        # Frame for Buttons 2 and 3 (below)
        self.button_frame = customtkinter.CTkFrame(self,fg_color="transparent")
        self.button_frame.pack(side="top", pady=10)

        # Button 2 (left)
        self.back = customtkinter.CTkButton(self.button_frame, text="Back", command=creator.back)
        self.back.pack(side="left", padx=10)

        # Button 3 (right)
        self.done = customtkinter.CTkButton(self.button_frame, text="Done",command=lambda :creator.set_images(self.Paths))
        self.done.pack(side="left", padx=10)


    def get_file(self):
        #TODO: change from (bse) to original and secondary
        file_path = filedialog.askopenfile(mode='r', filetypes=[('Tif File', '*tif'), ('Raw File', '*raw')]).name

        if self.switch.get():
            file_path+= " ( Secondary )"
            self.switch.deselect()
            self.switch.configure(state="disabled")
            self.Paths.append(file_path)
        else:
            file_path+= "  ( Primary ) "
            self.switch.select()
            self.switch.configure(state="disabled")
            self.Paths.insert(0,file_path)



        self.display_items()


    def display_items(self):
        # Clear previous items
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        # Display each item with a delete button
        for index, item in enumerate(self.Paths):
            label = customtkinter.CTkLabel(self.file_frame, text=item)
            label.grid(row=index, column=0, sticky="W")

            delete_button = customtkinter.CTkButton(self.file_frame, text="X",fg_color="transparent", command=lambda idx=index: self.delete_item(idx))
            delete_button.grid(row=index, column=1, sticky="E")

        if len(self.Paths)==self.maxImages:
            self.file_button.configure(state="disabled")
        else:
            self.file_button.configure(state="normal")

    def delete_item(self, index):
        if " ( Secondary )" in self.Paths[index]:
            self.switch.configure(state="normal")

        # Delete item from list
        del self.Paths[index]
        # Update the display
        self.display_items()









import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import os


class MultipleImageUploader(ctk.CTkFrame):
    def __init__(self,creator):
        super().__init__(creator)


        self.groups = {}
        self.group_count = 0  # Track the number of groups created
        self.current_group = None  # Track the current group for adding images

        # Frame to hold the dropdown and the two buttons
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=10, fill="x")

        # Upload Image button (on the left of the dropdown)
        self.upload_button = ctk.CTkButton(self.top_frame, text="Upload Image",
                                           command=self.add_images_to_current_group)
        self.upload_button.pack(side="left", padx=10)

        # Dropdown (Combobox) for selecting groups (in the middle)
        self.group_selector = ttk.Combobox(self.top_frame, state="readonly", values=[],
                                           postcommand=self.update_group_selector)
        self.group_selector.pack(side="left", fill="x", expand=True, padx=10)
        self.group_selector.bind("<<ComboboxSelected>>", self.on_group_select)

        # Create New Group button (on the right of the dropdown)
        self.new_group_button = ctk.CTkButton(self.top_frame, text="Create New Group",
                                              command=self.upload_image_to_new_group)
        self.new_group_button.pack(side="left", padx=10)

        # Define the Treeview with two columns: one for image names, one for the "x"
        self.treeview = ttk.Treeview(self, columns=("Image", "Remove"), show="headings", height=10)
        self.treeview.heading("Image", text="Images")
        self.treeview.heading("Remove", text="Remove")

        # Set column width
        self.treeview.column("Image", anchor="w", width=400)
        self.treeview.column("Remove", anchor="center", width=50)

        self.treeview.pack(pady=10, fill="both", expand=True)

        # Bind the "x" column to be clickable, and images to be selectable
        self.treeview.bind("<Button-1>", self.on_click)

    def update_group_selector(self):
        """Update the dropdown with the current group names."""
        self.group_selector["values"] = list(self.groups.keys())

    def on_group_select(self, event):
        """Update the treeview when a new group is selected from the dropdown."""
        selected_group = self.group_selector.get()
        if selected_group in self.groups:
            self.current_group = selected_group
            self.update_treeview(selected_group)

    def upload_image_to_new_group(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.tif *.raw")])
        if file_paths:
            # Automatically create a new group with an incrementing name
            self.group_count += 1
            group_name = f"image set {self.group_count}"
            self.groups[group_name] = {'images': [], 'main_image': None, 'raw_dimensions': None}
            self.current_group = group_name  # Set the new group as the current group
            self.update_group_selector()  # Update the group dropdown with the new group

            # Automatically select the new group in the dropdown
            self.group_selector.set(group_name)
            self.add_images_to_group(file_paths, group_name)

    def add_images_to_current_group(self):
        if self.current_group is None:
            messagebox.showerror("Error", "No group selected. Create or select a group first.")
            return

        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.tif *.raw")])
        if file_paths:
            self.add_images_to_group(file_paths, self.current_group)

    def add_images_to_group(self, file_paths, group_name):
        """Add images to the given group and handle .raw files with dimension input."""
        group = self.groups[group_name]

        for file_path in file_paths:
            image_info = {'path': file_path}

            # Check if the image is a .raw file
            if file_path.lower().endswith('.raw'):
                # If this is the first .raw file for the group or all .raw files were deleted
                if group['raw_dimensions'] is None:
                    # Open a CustomTkinter popup to ask for dimensions once
                    popup = RawDimensionsPopup(self)
                    self.wait_window(popup)  # Wait for popup to close
                    dimensions = popup.get_dimensions()

                    if dimensions:
                        group['raw_dimensions'] = dimensions  # Store dimensions at the group level
                    else:
                        messagebox.showerror("Error", "Invalid dimensions entered. Skipping file.")
                        continue  # Skip this file if dimensions are invalid

                # Add the dimensions to the image info (for display purposes)
                image_info['dimensions'] = group['raw_dimensions']
            else:
                image_info['dimensions']=(0,0)

            group['images'].append(image_info)

            # Set the first uploaded image as the main image if none exists
            if group['main_image'] is None:
                group['main_image'] = image_info

        self.update_treeview(group_name)

    def update_treeview(self, group_name):
        """Update the TreeView to display all images in the group."""
        # Clear the treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        group = self.groups[group_name]

        # Add images to the treeview with an "x" button and mark the main image
        for img_info in group['images']:
            image_name = os.path.basename(img_info['path'])
            if img_info == group['main_image']:
                image_name += " [MAIN]"  # Indicate the main image

            # Show dimensions if the file is a .raw file
            if 'dimensions' in img_info and img_info['dimensions'][0]!=0:
                image_name += f" (RAW {img_info['dimensions'][0]}x{img_info['dimensions'][1]})"

            # Insert the image name in the first column, and the "❌" in the second
            self.treeview.insert("", "end", values=(image_name, "X"))

    def on_click(self, event):
        """Handle clicks on the TreeView. Detect if user clicked 'x' to remove or on image path to set main."""
        region = self.treeview.identify_region(event.x, event.y)
        column = self.treeview.identify_column(event.x)
        item = self.treeview.identify_row(event.y)

        if region == "cell":
            if column == "#2":  # This corresponds to the second column (the "x")
                values = self.treeview.item(item, "values")
                image_name = values[0].split(" [MAIN]")[0]  # Remove the [MAIN] tag if present
                self.remove_image(image_name)
            elif column == "#1":  # Clicking on the image name to make it the main image
                values = self.treeview.item(item, "values")
                image_name = values[0].split(" [MAIN]")[0]  # Remove the [MAIN] tag if present
                self.set_main_image(image_name)

    def set_main_image(self, image_name):
        """Set the clicked image as the main image in the current group."""
        group = self.groups[self.current_group]

        # Find the image by name and set it as the main image
        for img_info in group['images']:
            if os.path.basename(img_info['path']) in image_name:
                group['main_image'] = img_info
                self.update_treeview(self.current_group)  # Refresh the treeview with the new main image
                return

    def remove_image(self, image_name):
        """Remove the image from the current group and handle .raw-specific logic."""
        if self.current_group:
            group = self.groups[self.current_group]
            group_images = group['images']

            # Find the image and remove it
            for img_info in group_images:
                img_base_name = os.path.basename(img_info['path'])
                if img_base_name in image_name:
                    group_images.remove(img_info)

                    # If the removed image was the main image, reset the main image
                    if img_info == group['main_image']:
                        group['main_image'] = group_images[0] if group_images else None

                    # Check if the deleted image was the last .raw image in the group
                    if img_info['path'].lower().endswith('.raw') and not any(
                            img['path'].lower().endswith('.raw') for img in group_images):
                        group['raw_dimensions'] = None  # Reset raw dimensions if no .raw images remain

                    self.update_treeview(self.current_group)  # Update the treeview after removing the image
                    return


class RawDimensionsPopup(ctk.CTkToplevel):
    """Popup to ask for .raw image dimensions"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Enter RAW Image Dimensions")
        self.geometry("300x300")

        self.label_width = ctk.CTkLabel(self, text="Width:")
        self.label_width.pack(pady=10)
        self.entry_width = ctk.CTkEntry(self)
        self.entry_width.pack(pady=10)

        self.label_height = ctk.CTkLabel(self, text="Height:")
        self.label_height.pack(pady=10)

        self.entry_height = ctk.CTkEntry(self)
        self.entry_height.pack(pady=10)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=20)

        self.dimensions = None

    def on_submit(self):
        """Retrieve and validate the dimensions."""
        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            self.dimensions = (width, height)
            self.destroy()  # Close the popup
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for dimensions.")

    def get_dimensions(self):
        """Return the dimensions entered by the user."""
        return self.dimensions


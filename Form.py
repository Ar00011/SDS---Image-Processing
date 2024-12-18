from customtkinter import *
import tkinter as tk #imports tkinter for the Graphical User Interface                   
from tkinter import messagebox, filedialog #allows the user to enter an input, allows the user to select a file
from PIL import Image, ImageTk   #PIL allows image handling
import cv2
import numpy as np


class ImageProcessingApp: #A class for Image Processing containing infomration about the window.
    def __init__(self,root): 
        self.root = root 
        self.root.geometry('700x1000')  
        self.root.title('Image Processing') 

        self.current_view = None
        self.setup_form_view()


    def setup_form_view(self):
        if self.current_view:
            self.current_view.destroy()

        self.current_view = CTkFrame(self.root)
        self.current_view.pack(pady = 22, padx = 22, fill= "both", expand = True)

        CTkLabel(self.current_view, text = "Photo Submission Form", font=("Calibri", 18, "bold")).pack(pady=10)

        CTkLabel(self.current_view, text= "Name of the photo: ").pack(pady= 6)
        Name_photo_entry = CTkEntry(self.current_view, width= 450)
        Name_photo_entry.pack()

        CTkLabel(self.current_view, text = "Date Photo Captured" ).pack(pady = 6)
        Date_photo_captured_entry = CTkEntry(self.current_view ,width= 450)
        Date_photo_captured_entry.pack()

        CTkLabel(self.current_view,text="Date of submission").pack(pady=6)
        Date_of_submission_entry = CTkEntry(self.current_view, width= 450)
        Date_of_submission_entry.pack()

        CTkLabel(self.current_view, text=" Photographer:").pack(pady= 6)
        photographer_entry = CTkEntry(self.current_view, width= 450)
        photographer_entry.pack()

        submit_button = CTkButton(self.current_view ,text="Submit Form", command= self.submit_form)
        submit_button.pack(pady=25)

    def submit_form(self):

        self.setup_image_view()




    def setup_image_view(self):
        if self.current_view:
            self.current_view.destroy()

        # Main frame
        self.current_view = CTkFrame(self.root)
        self.current_view.pack(pady=22, padx=22, fill="both", expand=True)

        # Header label
        CTkLabel(self.current_view, text="Image Processing", font=("Calibri", 14, "bold")).pack(pady=10)

        # Frame for buttons (uses grid layout)
        buttons_frame = CTkFrame(self.current_view)  # Buttons placed inside this frame
        buttons_frame.pack(pady=10, anchor='w', padx=10)

        # Define buttons
        buttons = [
            ("Upload", self.upload_image),
            ("Grayscale", self.convert_to_grayscale),
            ("Image Blurring", self.image_blurring),
            ("Detect Edges", self.detect_edges),
        ]

        # Add buttons horizontally using grid
        for idx, (text, command) in enumerate(buttons):
            CTkButton(
                buttons_frame, text=text, width=120, height=32, command=command
            ).grid(row=0, column=idx, padx=10)  # Place in grid layout

        # Image label (uses pack layout)
        self.img_label = tk.Label(self.current_view)  # A label for images
        self.img_label.pack(pady=20)

    
    def upload_image(self): #Allows the user to upload the image 
        file_path = filedialog.askopenfilename( 
            title = "Choose an image", 
            filetypes=[("Image files", "*.jpeg;*.jpg;*.png;*.bmp")] 
        )
        if not file_path: 
            return # Exits
        try: 
            self.image = Image.open(file_path) #Opens the image file
            self.display_image(self.image) 
        except Exception as e: 
            messagebox.showerror("Error", f"Could not load the image: {e}") 

    def display_image(self, img): #Places the image inside the label
        self.tkImg = ImageTk.PhotoImage(img) 
        self.img_label.config(image=self.tkImg)  
    
    def convert_to_grayscale(self): # Converts into grayscale
        if self.image: 
            gray_image = self.image.convert("L") 
            self.update_image(gray_image) 
        else:
            messagebox.showerror("Error", "No image uploaded") 

    def update_image(self,new_image): # Function, allows to update the current image on display
        self.image = new_image 
        self.display_image(new_image) 

    def image_blurring(self): # Function, applies Gaussian blur to loaded image using Pillow
        if self.image: 
            opencv_picture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR) 
            blurred_img = cv2.GaussianBlur(opencv_picture, (15,15),0) 
            blurred_img_pil = Image.fromarray(cv2.cvtColor(blurred_img, cv2.COLOR_BGR2RGB)) 
            self.update_image(blurred_img_pil) 
        else:
            messagebox.showerror("Error", "No image loaded") 


    def detect_edges(self): #Function, detects edges in loaded image
        if self.image: 
            opencv_picture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR) 
            edge_detection = cv2.Canny(opencv_picture, 100,200) 
            edges_pil = Image.fromarray(edge_detection) 
            self.update_image(edges_pil) 
        else:
            messagebox.showerror("Error", "No image loaded")




if __name__ == '__main__':
    root = tk.Tk() 
    application = ImageProcessingApp(root)
    root.mainloop() 


        


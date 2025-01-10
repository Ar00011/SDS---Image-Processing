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

        self.active_frame = None
        self.original_image = None
        self.image = None

        self.setup_form_view()


    def setup_form_view(self):
        if self.active_frame:
            self.active_frame.destroy()

        self.active_frame = CTkFrame(self.root)
        self.active_frame.pack(pady = 22, padx = 22, fill= "both", expand = True)

        CTkLabel(self.active_frame, text = "Photo Submission Form", font=("Calibri", 18, "bold")).pack(pady=10)

        CTkLabel(self.active_frame, text= "Name of the photo: ").pack(pady= 6)
        self.Name_photo_entry = CTkEntry(self.active_frame, width= 450, justify = "center")
        self.Name_photo_entry.pack()

        CTkLabel(self.active_frame, text = "Date Photo Captured" ).pack(pady = 6)
        self.Date_photo_captured_entry = CTkEntry(self.active_frame ,width= 450, justify = "center")
        self.Date_photo_captured_entry.pack()

        CTkLabel(self.active_frame,text="Date of submission").pack(pady=6)
        self.Date_of_submission_entry = CTkEntry(self.active_frame, width= 450, justify = "center")
        self.Date_of_submission_entry.pack()

        CTkLabel(self.active_frame, text=" Photographer:").pack(pady= 6)
        self.photographer_entry = CTkEntry(self.active_frame, width= 450, justify = "center")
        self.photographer_entry.pack()

        CTkLabel(self.active_frame,text= "Description of image:").pack(pady=6)
        self.Description_of_image_entry = CTkEntry(self.active_frame, width = 450, height = 300, justify = "center")
        self.Description_of_image_entry.pack()

        submit_button = CTkButton(self.active_frame ,text="Submit Form", command= self.submit_form)
        submit_button.pack(pady=25)

    def submit_form(self):  # Inputs are validated, errors displayed and if success then     proceeded
        errors = self.check_input()
        if errors:
            messagebox.showerror("Form Error", errors[0])
        else:
            self.setup_image_view()

    def check_input(self):  # Form inputs are verified
        errors = []
        if not self.Name_photo_entry.get().strip():
            errors.append("Please enter the name of the photo")
        if not self.Date_photo_captured_entry.get().strip():
            errors.append("Please enter the date the photo was captured")
        if not self.Date_of_submission_entry.get().strip():
            errors.append("Please enter the date of submission")
        if not self.photographer_entry.get().strip():
            errors.append("Please enter the name of the photographer")
        if not self.Description_of_image_entry.get().strip():
            errors.append("Please enter a description for your image")
        return errors

    def setup_image_view(self):

        if self.active_frame:
            self.active_frame.destroy()

        self.active_frame = CTkFrame(self.root)
        self.active_frame.pack(pady= 22, padx= 22, fill="both", expand=True)

        CTkLabel(self.active_frame, text = "Image Processing",  font =("Calibri", 14, "bold")).pack(pady=10)
     
        buttons_frame = CTkFrame(self.active_frame)  # Frame which holds the buttons
        buttons_frame.pack(pady=10, anchor='w', padx=10)  

        buttons = [ # Text, #Button
        ("Upload", self.upload_image),
        ("Grayscale", self.convert_to_grayscale),
        ("Image Blurring", self.image_blurring),
        ("Detect Edges", self.detect_edges),
        ("Reset", self.reset_image),
        ]

        for index, (text, command) in enumerate (buttons): 
            tk.Button(buttons_frame, text = text, width = 10, height=2, command=command).grid(row= 0, column=index, padx= 120) 

    
        self.img_label = tk.Label(self.active_frame) # A label for images in main menu
        self.img_label.pack(pady=20) 

    def reset_image(self):
        if self.original_image:
            self.update_image(self.original_image)
        else:
            messagebox.showerror("Error", "No image loaded")
    
    
    def upload_image(self): #Uploads an image
        file_path = filedialog.askopenfilename( 
            title = "Choose an image", 
            filetypes=[("Image files", "*.jpeg;*.jpg;*.png;*.bmp")] 
        )
        if not file_path: 
            return # Exits
        try: 
            self.original_image = Image.open(file_path) #Opens the image file
            self.image = self.original_image.copy()
            self.display_image(self.image) 
        except Exception as e: 
            messagebox.showerror("Error", f"Could not load the image: {e}") 

    def display_image(self, img): #Places the image inside the label
        self.tkImg = ImageTk.PhotoImage(img) 
        self.img_label.config(image=self.tkImg)  
    
    def convert_to_grayscale(self): # Converts into grayscale
        if self.original_image: 
            gray_image = self.image.convert("L") 
            self.update_image(gray_image) 
        else:
            messagebox.showerror("Error", "No image uploaded") 

    def update_image(self,new_image): # Function, allows to update the current image on display
        self.image = new_image 
        self.display_image(new_image) 

    def image_blurring(self): # Function, applies Gaussian blur to loaded image using Pillow
        if self.original_image: 
            opencv_picture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR) 
            blurred_img = cv2.GaussianBlur(opencv_picture, (15,15),0) 
            blurred_img_pil = Image.fromarray(cv2.cvtColor(blurred_img, cv2.COLOR_BGR2RGB)) 
            self.update_image(blurred_img_pil) 
        else:
            messagebox.showerror("Error", "No image loaded") 


    def detect_edges(self): #Function, detects edges in loaded image
        if self.original_image: 
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


        

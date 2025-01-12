
#Importsa essential libraries for the GUI

from customtkinter import *
import tkinter as tk                  
from tkinter import messagebox, filedialog #Alerts and dialogs
from PIL import Image, ImageTk   #PIL allows image handling with TKinter
import cv2 #Applied in image processing features such as image blurring and edge detection.
import numpy as np # Custom widgets for modern UI


class ImageProcessingApp: #A class for Image Processing containing infomration about the window.
    def __init__(self,root): 
        self.root = root 
        self.root.geometry('700x800')  
        self.root.title('Image Processing') 
        #Placeholde for essential properties
        self.active_frame = None
        self.original_image = None
        self.image = None

        self.filter_applied = False # Boolean initialised, tracking filters.

        self.setup_form_view()

    #Form screen setup
    def setup_form_view(self):
        #if a old frame exists, clear it
        if self.active_frame:
            self.active_frame.destroy()

        #Creates a new frame
        self.active_frame = CTkFrame(self.root)
        self.active_frame.pack(pady = 22, padx = 22, fill= "both", expand = True)

        #Form title
        CTkLabel(self.active_frame, text = "Photo Submission Form", font=("Calibri", 18, "bold")).pack(pady=10)


        #Input fields created with their labels
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

    
    
    
    def submit_form(self):  # Inputs are validated, errors displayed and if successful then proceed
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

    #Form screen initialisation
    def setup_image_view(self):
        #if older frame exists, delete it
        if self.active_frame:
            self.active_frame.destroy()
        
        #Creates a new frame
        self.active_frame = CTkFrame(self.root)
        self.active_frame.pack(pady= 22, padx= 22, fill="both", expand=True)

        #Titlte and font set through a label
        CTkLabel(self.active_frame, text = "Image Processing",  font =("Calibri", 14, "bold")).pack(pady=10)

        # Frame which holds the buttons
        buttons_frame = CTkFrame(self.active_frame)  
        buttons_frame.pack(pady=10, padx=10, anchor='center')  
        
        #Frame positioned lower to initial, for reset and save buttons
        bottom_buttons_frame = CTkFrame(self.active_frame) 
        bottom_buttons_frame.pack(pady=10)

        #Reset button personalised
        reset_button = CTkButton(bottom_buttons_frame, text="Reset", command=self.reset_image,fg_color="#FF0000", text_color="white")
        reset_button.pack(side="left", padx=10)
        
        #Save button personalised
        save_button = CTkButton(bottom_buttons_frame, text="Save", command=self.save_image, fg_color="#4CAF50", text_color="white")
        save_button.pack(side="left", padx=10)



         # Text and Functions for the buttons
        buttons = [
        ("Upload", self.upload_image),
        ("Grayscale", self.convert_to_grayscale),
        ("Image Blurring", self.image_blurring),
        ("Detect Edges", self.detect_edges),
        ]

        for index, (text, command) in enumerate (buttons): 
            CTkButton(buttons_frame, text = text, width = 120, height=40, command=command).grid(row= 0, column=index, padx= 120) 

        #Label to display the picture
        self.img_label = tk.Label(self.active_frame) # A label for images in main menu
        self.img_label.pack(pady=20) 
    
    def save_image(self):
        #Current picture can get saved by the user
        if self.image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                self.image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
        else:
            messagebox.showerror("Error", "No image to save")


    def reset_image(self):
        if not self.original_image:
            messagebox.showerror("Error", "No image attached. Please upload an image first")
            return

        if self.filter_applied:
            self.update_image(self.original_image)
            self.filter_applied = False
            messagebox.showinfo("Success", "Picture has been reset to original")
        else:
            messagebox.showinfo("Info", "No filters to reset, it is already original")
                
    #Allows certain types of images to be uploaded
    def upload_image(self): 
        #Gives the user a choice to pick an image to upload
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

    #Places the image inside the label
    def display_image(self, img): 
        self.tkImg = ImageTk.PhotoImage(img) 
        self.img_label.config(image=self.tkImg)  
    
    def convert_to_grayscale(self): # Converts into grayscale
        if self.original_image: 
            gray_image = self.image.convert("L") 
            self.update_image(gray_image) 
            self.filter_applied = True # Mark filter as applied
        else:
            messagebox.showerror("Error", "No image uploaded") 

    # Updates the current image on display
    def update_image(self,new_image): 
        self.image = new_image 
        self.display_image(new_image) 

    # Applies Gaussian blur to loaded image using Pillow
    def image_blurring(self): 
        if self.original_image: 
            opencv_picture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR) 
            blurred_img = cv2.GaussianBlur(opencv_picture, (15,15),0) 
            blurred_img_pil = Image.fromarray(cv2.cvtColor(blurred_img, cv2.COLOR_BGR2RGB)) 
            self.update_image(blurred_img_pil) 
            self.filter_applied = True # Mark filter as applied
        else:
            messagebox.showerror("Error", "No image loaded") 

    #Detects edges in loaded image
    def detect_edges(self): 
        if self.original_image: 
            opencv_picture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR) 
            edge_detection = cv2.Canny(opencv_picture, 100,200) 
            edges_pil = Image.fromarray(edge_detection) 
            self.update_image(edges_pil) 
            self.filter_applied = True # Mark filter as applied
        else:
            messagebox.showerror("Error", "No image loaded")




if __name__ == '__main__':
    root = tk.Tk() 
    application = ImageProcessingApp(root)
    root.mainloop() 


        

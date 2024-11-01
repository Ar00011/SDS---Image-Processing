import tkinter as tk #imports tkinter for the Graphical User Interface                   
from tkinter import messagebox, filedialog #allows the user to enter an input, allows the user to select a file
from PIL import Image, ImageTk   #PIL allows image handling
import cv2
import numpy as np

class ImageProcessingApp: #A class for Image Processing
    def __init__(self,root): #initialize the class with the root Tkinter Window
        self.root = root #Stores the main window, used for future reference
        self.root.geometry('700x1000')  #Sets windows size 
        self.root.title('Image Processing') #Sets the title of the root window
        self.setup_ui() #Initilises the function


        self.image=None # initialises the variable to store the current picture
 

    def setup_ui(self): #Contains buttons which are displayed in the GUI
        buttons = [("Upload", self.upload_image),("Grayscale", self.convert_to_grayscale,),("Image Blurring", self.image_blurring),("Detect Edges", self.detect_edges)]# Text, #Button
        for text, command in buttons: #Loops through the buttons in the list and creates them
            tk.Button(self.root, text = text, width = 15, height=2, command=command).pack(pady= 10) # Create and pack the buttons in that format
    
        self.img_label = tk.Label(self.root) #Label to display the image
        self.img_label.pack() #Packs the label inside the window
    

    def upload_image(self): #Function to upload the image 
        file_path = filedialog.askopenfilename( #Opens the file explorer for the user to select an image
            title = "Choose an image", # sets the title of the file dialog
            filetypes=[("Image files", "*.jpeg;*.jpg;*.png;*.bmp")] # Filters the accepted formats
        )
        if not file_path: # If there is no file selected
            return # Exits
        try: 
            self.image = Image.open(file_path) #Opens the image file
            self.display_image(self.image) # Function is called to display the image 
        except Exception as e: # Will display any exceptions/errors during image loading
            messagebox.showerror("Error", f"Could not load the image: {e}") # Displays error with title, message format

    def display_image(self, img): # Function which allows to an image to be placed in the label
        self.tkImg = ImageTk.PhotoImage(img) #Converts the picture to a compatible Tkinter format
        self.img_label.config(image=self.tkImg)  #Updates the label to show most recent/up to date image
    
    def convert_to_grayscale(self): # Function to convert into grayscale
        if self.image: # Verify if an image uploaded
            gray_image = self.image.convert("L") # Converts image to grayscale mode
            self.update_image(gray_image) # Calls the function which displays the new grayscale image
        else:
            messagebox.showerror("Error", "No image uploaded") # Displays error with title, message format

    def update_image(self,new_image): # Function, allows to update the current image on display
        self.image = new_image # updates the image to the new image
        self.display_image(new_image) #Calls the function to display the updated image

    def image_blurring(self): # Function, applies Gaussian blur to loaded image
        if self.image: # Referers to the picture uploaded
            opencv_picture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR) # Uses numpy array to convert image from RGB to BGR
            blurred_img = cv2.GaussianBlur(opencv_picture, (15,15),0) # Applies the Gaussian Blur
            blurred_img_pil = Image.fromarray(cv2.cvtColor(blurred_img, cv2.COLOR_BGR2RGB)) # Converts the blurred image back to RGB
            self.update_image(blurred_img_pil) # Updates the image
        else:
            messagebox.showerror("Error", "No image loaded") # Displays error with title, message format


    def detect_edges(self): #Function, detects edges in loaded image
        if self.image: # Verifies if an image is uploaded 
            opencv_picture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR) # Transforms PIL image to Numpy array, then RGB to BGR for OpenCV valid format
            edge_detection = cv2.Canny(opencv_picture, 100,200) # Applies canny detection , using those parameters for edge detection
            edges_pil = Image.fromarray(edge_detection) # Converts edge detected image to PIL format
            self.update_image(edges_pil) # Calls the function to updated and show the edge detected image
        else:
            messagebox.showerror("Error", "No image loaded")


if __name__ == '__main__':
    root = tk.Tk() # Creates the window using Tkinter
    application = ImageProcessingApp(root) # Instantiates the class with root window
    root.mainloop() # Starts TKinter main event loop to run app


        



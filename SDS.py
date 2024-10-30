import tkinter as tk #imports tkinter for the Graphical User Interface                   
from tkinter import messagebox, filedialog #allows the user to enter an input, allows the user to select a file
from PIL import Image, ImageTk   #PIL allows image handling
import cv2

class ImageProcessingApp: #A class for Image Processing
    def __init__(self,root): #initialize the class with the root Tkinter Window
        self.root = root  #Will create and store the main window for reference to it later
        self.root.geometry('700x1000') #sets the apps's windows size
        self.root.title('Image Processing')
        self.layout_gui() #Will initalize  GUI buttons for me


        self.picture=None # Will initialize the variable to store the current picture
 

    def layout_gui(self):
        upload_button = tk.Button(self.root, text= "Upload",width=15, height =2, command=self.upload_image)
        upload_button.pack(pady=10)
        
        grayscale_button = tk.Button(self.root, text="Grayscale",width=15, height = 2, command=self.convert_to_grayscale)
        grayscale_button.pack(pady= 10)

        imageBlurring_button = tk.Button(self.root,text = "Image Blurring", width=15, height=2, command= self.image_blurring )
        imageBlurring_button.pack(pady=10) #Displays the image in the  - Label

        self.picture_label = tk.Label(self.root)
        self.picture_label.pack() #Adds the label to the window

    

    

    def upload_image(self):
        # Allows the user to choose a file from the file manager
        selected_file = filedialog.askopenfilename(title= "Choose an Image", filetypes=[("Supported Image Formats","*.jpeg;*.jpg;*.png;*.bmp")])
        if not selected_file:
            return
        try:
            # uses PIL to load the image and gives it a variable
            self.picture = Image.open(selected_file)
            # Renders the uploaded image
            self.show_image(self.picture)
        except Exception as error: 
            messagebox.showerror("Image loading error", f"Unable to laod the chosen image: {error}")   

    def show_image(self, picture):

        self.tkImg = ImageTk.PhotoImage(picture) #Converts the picture to a compatible Tkinter format
        self.picture_label.config(image=self.tkImg) #Displays the picture in the label
        self.picture_label.image = self.tkImg #will use the image as reference so that it doesn't accumulate other garbage
    
    def convert_to_grayscale(self):
        if self.picture:
            gray_picture = self.picture.convert("L")
            self.reform_picture(gray_picture)
        else:
            messagebox.showerror("Error", "No image uploaded")

    def reform_picture(self,new_picture):
        self.picture = new_picture
        self.show_image(new_picture)

    def image_blurring(self):
        pass


    # def display_image(self):

if __name__ == '__main__':
    root = tk.Tk()

    application = ImageProcessingApp(root)

    root.mainloop()


        



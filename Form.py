# Imports essential libraries for the GUI and image processing

#GUI
from customtkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog  # Alerts and dialogs
from PIL import Image, ImageTk  # PIL allows image handling with TKinter

import cv2  # Applied in image processing features such as image blurring and edge detection.

import numpy as np  #Array manipulation and OpenCV



class ImageProcessingApp:  # A class for Image Processing containing information about the window.
    def __init__(self, root):
        # Main window is initialised
        self.root = root
        self.root.geometry('950x950')
        self.root.title('Cool Image Processing')
        # Placeholders for image processing
        self.activeFrame = None
        self.originalImage = None
        self.image = None
        self.filterApplied = False  # Flag, tracks if filter applied to an image.

        # Starts the form view
        self.setupFormView()

    def setupFormView(self):
        # If an old frame exists, clear it
        if self.activeFrame:
            self.activeFrame.destroy()

        # Creates a new frame for the form
        self.activeFrame = CTkFrame(self.root)
        self.activeFrame.pack(pady=22, padx=22, fill="both", expand=True)

        # Form title
        CTkLabel(self.activeFrame, text="Photo Submission Form", font=("Calibri", 18, "bold")).pack(pady=10)

        # Input fields created with their labels
        CTkLabel(self.activeFrame, text="Name of the photo: ").pack(pady=6)
        self.namePhotoEntry = CTkEntry(self.activeFrame, width=450, justify="center")
        self.namePhotoEntry.pack()

        CTkLabel(self.activeFrame, text="Date Photo Captured - DD/MM/YYYY ").pack(pady=6)
        self.datePhotoCapturedEntry = CTkEntry(self.activeFrame, width=450, justify="center")
        self.datePhotoCapturedEntry.bind("<KeyRelease>", lambda event: self.checkDateInput(event.char, self.datePhotoCapturedEntry))
        self.datePhotoCapturedEntry.pack()

        CTkLabel(self.activeFrame, text="Date of submission - DD/MM/YYYY").pack(pady=6)
        self.dateOfSubmissionEntry = CTkEntry(self.activeFrame, width=450, justify="center")
        self.dateOfSubmissionEntry.bind("<KeyRelease>", lambda event: self.checkDateInput(event.char, self.dateOfSubmissionEntry))
        self.dateOfSubmissionEntry.pack()

        CTkLabel(self.activeFrame, text="Photographer:").pack(pady=6)
        self.photographerEntry = CTkEntry(self.activeFrame, width=450, justify="center")
        self.photographerEntry.pack()

        CTkLabel(self.activeFrame, text="Description of image:").pack(pady=6)
        self.descriptionOfImageEntry = CTkTextbox(self.activeFrame, width=450, height=300, fg_color="#333333", border_color="#444444", border_width=5)
        self.descriptionOfImageEntry.pack()

        self.wordCountLabel = CTkLabel(self.activeFrame, text="Word count: 0/250", font=("Calibri", 15))
        self.wordCountLabel.pack(pady=2)

        # As keys are pressed, the word count is increased
        self.descriptionOfImageEntry.bind("<KeyRelease>", self.updateWordCount)

        # Selection box for categories
        CTkLabel(self.activeFrame, text="Image Category", font=("Calibri", 16)).pack(pady=6)
        self.categoriesOptions = ["Urban", "Nature", "Landscape", "Portrait", "Abstract", "Wildlife"] #Options in the selection box
        self.categoryMenu = CTkOptionMenu(self.activeFrame, values=self.categoriesOptions) #Selection box
        self.categoryMenu.pack(pady=6)

        submitButton = CTkButton(self.activeFrame, text="Submit Form", command=self.submitForm)
        submitButton.pack(pady=25)

    def checkDateInput(self, char, entryWidget):
        if not (char.isdigit() or char == '/'):  # Limited to only / and digits
            currentText = entryWidget.get()
            entryWidget.delete(len(currentText) - 1, len(currentText))
            return False

        currentText = entryWidget.get() # Get text inputted again from the entry
        try:
            if len(currentText) == 10: # Checks input when there is full date length available
                from datetime import datetime
                inputedDate = datetime.strptime(currentText, "%d/%m/%Y")

                if inputedDate > datetime.now(): 
                    entryWidget.delete(0, 'end') # Deletes all of the characters
                    messagebox.showerror("", "Date cannot be in the future")

        except ValueError:
            entryWidget.delete(0, 'end')
            messagebox.showerror("Error","Invalid date format, Please enter in format DD/MM/YYYY")
        return True

    def countWords(self, text):
        return len(text.split())  # Returns number of words in the input text

    def updateWordCount(self, event=None):
        # Text from description_box is updated
        descriptionText = self.descriptionOfImageEntry.get("1.0", "end").strip()
        wordCount = self.countWords(descriptionText)

        # Word count label is updated
        self.wordCountLabel.configure(text=f"Word count: {wordCount}/250")

        # Checks if word count > 250
        if wordCount > 250:
            # Removes last input after 250 was reached
            self.descriptionOfImageEntry.delete("end-2c", "end")

            self.wordCountLabel.configure(text="Word count: 250/250 (Limit Reached)")

            messagebox.showerror("Error", "Max limit of 250 words is reached")
            return

    def submitForm(self):  # Inputs are validated, errors displayed and if successful then proceed
        errors = self.checkInput()
        if errors:
            messagebox.showerror("Form Error", errors[0])
        else:
            self.setupImageView()

    def checkInput(self):  # Checks if a field is left empty
        errors = []
        if not self.namePhotoEntry.get().strip():
            errors.append("Please enter the name of the photo")
        if not self.datePhotoCapturedEntry.get().strip():
            errors.append("Please enter the date the photo was captured")
        if not self.dateOfSubmissionEntry.get().strip():
            errors.append("Please enter the date of submission")
        if not self.photographerEntry.get().strip():
            errors.append("Please enter the name of the photographer")
        if not self.descriptionOfImageEntry.get("1.0", "end").strip():
            errors.append("Please enter a description for your image")
        return errors

    # Form screen initialisation
    def setupImageView(self):
        # If older frame exists, delete it
        if self.activeFrame:
            self.activeFrame.destroy()

        # Creates a new frame
        self.activeFrame = CTkFrame(self.root)
        self.activeFrame.pack(pady=22, padx=22, fill="both", expand=True)

        # Title and font set through a label
        CTkLabel(self.activeFrame, text="Image Processing", font=("Calibri", 14, "bold")).pack(pady=10)

        # Frame which holds the top buttons
        buttonsFrame = CTkFrame(self.activeFrame)
        buttonsFrame.pack(pady=10, padx=10, anchor='center')

        # Frame positioned lower, for reset and save buttons
        bottomButtonsFrame = CTkFrame(self.activeFrame)
        bottomButtonsFrame.pack(pady=10)
        
        resetButton = CTkButton(bottomButtonsFrame, text="Reset", command=self.resetImage, fg_color="#FF0000", text_color="white")
        resetButton.pack(side="left", padx=10)
        
        saveButton = CTkButton(bottomButtonsFrame, text="Save", command=self.saveImage, fg_color="#4CAF50", text_color="white")
        saveButton.pack(side="left", padx=10)

        # Text and Functions for the buttons
        buttons = [
            ("Upload", self.uploadImage),
            ("Grayscale", self.convertToGrayscale),
            ("Image Blurring", self.imageBlurring),
            ("Detect Edges", self.detectEdges),
        ]
        #Loop through each button's text and command, whilst tracking the index
        for index, (text, command) in enumerate(buttons):
            CTkButton(buttonsFrame, text=text, width=120, height=40, command=command).grid(row=0, column=index, padx=120)

        # Displays the transformed image in the label 
        self.imgLabel = tk.Label(self.activeFrame)  # A label for images in main menu
        self.imgLabel.pack(pady=20)

    def saveImage(self):
        # Current picture can get saved by the user
        if self.image:
            filePath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if filePath:
                self.image.save(filePath)
                messagebox.showinfo("Success", "Image saved successfully!")
        else:
            messagebox.showerror("Error", "No image to save. Please upload an image.")

    def resetImage(self):
        # If no image attached, then display error
        if not self.originalImage:
            messagebox.showerror("Error", "No image attached. Please upload an image first")
            return
        # Resets back the original image and resets filter
        if self.filterApplied:
            self.updateImage(self.originalImage)
            self.filterApplied = False
            messagebox.showinfo("Success", "Picture has been reset to original")
        else:
            messagebox.showinfo("Info", "No filters to reset, it is already original")

    # Allows certain types of formats of images to be uploaded
    def uploadImage(self):
        filePath = filedialog.askopenfilename(
            title="Choose an image", 
            filetypes=[("Image files", "*.jpeg;*.jpg;*.png;*.bmp")] #Supported image formats
        )
        if not filePath:
            return  # Exits
        try:
            self.originalImage = Image.open(filePath)  # Opens the image file
            self.image = self.originalImage.copy()
            self.displayImage(self.image)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load the image: {e}")

    # Places the image inside the label
    def displayImage(self, img):
        self.tkImg = ImageTk.PhotoImage(img)
        self.imgLabel.config(image=self.tkImg)

  
    def convertToGrayscale(self):
        if self.originalImage:
            grayImage = self.image.convert("L") # Applies grayscale into current image
            self.updateImage(grayImage) 
            self.filterApplied = True  # Mark filter as applied
        else:
            messagebox.showerror("Error", "No image uploaded")

    # Updates the current image on display
    def updateImage(self, newImage):
        self.image = newImage
        self.displayImage(newImage)

    # Applies Gaussian blur to loaded image using OpenCV and Pillow
    def imageBlurring(self):
        if self.originalImage:
            opencvPicture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR) #Converts the Image from Pillow to OpenCV
            blurredImg = cv2.GaussianBlur(opencvPicture, (15, 15), 0) # Applies Gaussian Blur
            blurredImgPil = Image.fromarray(cv2.cvtColor(blurredImg, cv2.COLOR_BGR2RGB)) #Convert back to Pillow format
            self.updateImage(blurredImgPil)
            self.filterApplied = True  # Mark filter as applied
        else:
            messagebox.showerror("Error", "No image loaded")

    # Detects edges in the loaded image
    def detectEdges(self):
        if self.originalImage:
            opencvPicture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            edgeDetection = cv2.Canny(opencvPicture, 100, 200)
            edgesPil = Image.fromarray(edgeDetection)
            self.updateImage(edgesPil)
            self.filterApplied = True  # Mark filter as applied
        else:
            messagebox.showerror("Error", "No image loaded")


if __name__ == '__main__':
    root = tk.Tk()
    application = ImageProcessingApp(root)
    root.mainloop()

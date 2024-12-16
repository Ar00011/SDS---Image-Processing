from customtkinter import *
import tkinter as tk  # Import tkinter with alias 'tk'
from tkinter import messagebox, filedialog  # Additional imports for dialogs and alerts
from PIL import Image, ImageTk  # For image handling
import cv2
import numpy as np
import datetime


class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x800")
        self.root.title("Photo Submission and Image Processing")

        self.current_view = None  # Track the current view
        self.setup_form_view()  # Start with the form view

    def setup_form_view(self):
        """Display the form view."""
        if self.current_view:
            self.current_view.destroy()  # Clear the current view

        self.current_view = CTkFrame(self.root)
        self.current_view.pack(pady=20, padx=20, fill="both", expand=True)

        CTkLabel(self.current_view, text="Photo Submission Form", font=("Arial", 16, "bold")).pack(pady=10)

        # Form Fields
        CTkLabel(self.current_view, text="Name of the photo: ").pack(pady=6)
        self.name_entry = CTkEntry(self.current_view, width=450)
        self.name_entry.pack()

        CTkLabel(self.current_view, text="Date Photo Captured (YYYY-MM-DD):").pack(pady=6)
        self.date_captured_entry = CTkEntry(self.current_view, width=450)
        self.date_captured_entry.pack()

        CTkLabel(self.current_view, text="Date of Submission (YYYY-MM-DD):").pack(pady=6)
        self.date_submission_entry = CTkEntry(self.current_view, width=450)
        self.date_submission_entry.pack()

        CTkLabel(self.current_view, text="Photographer:").pack(pady=6)
        self.photographer_entry = CTkEntry(self.current_view, width=450)
        self.photographer_entry.pack()

        # Submit Button
        CTkButton(self.current_view, text="Submit Form", command=self.validate_form).pack(pady=10)

    def validate_form(self):
        """Validate form inputs and transition to image processing view if valid."""
        errors = []

        # Validate Name of the photo
        if not self.name_entry.get().strip():
            errors.append("Please enter the name of the photo.")

        # Validate Date Photo Captured
        try:
            datetime.datetime.strptime(self.date_captured_entry.get().strip(), "%Y-%m-%d")
        except ValueError:
            errors.append("Enter the date the photo was taken in YYYY-MM-DD format.")

        # Validate Date of Submission
        try:
            datetime.datetime.strptime(self.date_submission_entry.get().strip(), "%Y-%m-%d")
        except ValueError:
            errors.append("Enter the date of submission in YYYY-MM-DD format.")

        # Validate Photographer
        if not self.photographer_entry.get().strip():
            errors.append("Please enter the name of the photographer.")

        # Show errors or transition
        if errors:
            messagebox.showerror("Form Validation Errors", "\n".join(errors))
        else:
            messagebox.showinfo("Success", "Form submitted successfully!")
            self.setup_image_processing_view()

    def setup_image_processing_view(self):
        """Display the image processing view."""
        if self.current_view:
            self.current_view.destroy()  # Clear the current view

        self.current_view = tk.Frame(self.root)
        self.current_view.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(self.current_view, text="Image Processing", font=("Arial", 16, "bold")).pack(pady=10)

        # Image Processing Buttons
        buttons = [
            ("Upload", self.upload_image),
            ("Grayscale", self.convert_to_grayscale),
            ("Image Blurring", self.image_blurring),
            ("Detect Edges", self.detect_edges),
        ]
        self.image_processing_buttons = []
        for text, command in buttons:
            button = tk.Button(self.current_view, text=text, width=15, height=2, command=command)
            button.pack(pady=10)
            self.image_processing_buttons.append(button)

        self.img_label = tk.Label(self.current_view, relief="solid")
        self.img_label.pack(pady=10)

    def upload_image(self):
        """Upload an image for processing."""
        file_path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[("Image files", "*.jpeg;*.jpg;*.png;*.bmp")],
        )
        if not file_path:
            return
        try:
            self.image = Image.open(file_path)
            self.display_image(self.image)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load the image: {e}")

    def display_image(self, img):
        """Display the current image."""
        self.tkImg = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.tkImg)

    def convert_to_grayscale(self):
        """Convert the uploaded image to grayscale."""
        if hasattr(self, "image") and self.image:
            gray_image = self.image.convert("L")
            self.update_image(gray_image)
        else:
            messagebox.showerror("Error", "No image uploaded")

    def update_image(self, new_image):
        """Update the displayed image."""
        self.image = new_image
        self.display_image(new_image)

    def image_blurring(self):
        """Apply Gaussian blur to the uploaded image."""
        if hasattr(self, "image") and self.image:
            opencv_picture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            blurred_img = cv2.GaussianBlur(opencv_picture, (15, 15), 0)
            blurred_img_pil = Image.fromarray(cv2.cvtColor(blurred_img, cv2.COLOR_BGR2RGB))
            self.update_image(blurred_img_pil)
        else:
            messagebox.showerror("Error", "No image loaded")

    def detect_edges(self):
        """Detect edges in the uploaded image."""
        if hasattr(self, "image") and self.image:
            opencv_picture = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            edge_detection = cv2.Canny(opencv_picture, 100, 200)
            edges_pil = Image.fromarray(edge_detection)
            self.update_image(edges_pil)
        else:
            messagebox.showerror("Error", "No image loaded")


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

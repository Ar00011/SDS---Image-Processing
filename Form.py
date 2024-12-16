from customtkinter import *

app = CTk()

app.geometry("600x600")
app.title("Upload Photo Image")
app.resizable(True,True)

CTkLabel(app, text= "Name of the photo: ").pack(pady= 6)
Name_photo_entry = CTkEntry(app, width= 450)
Name_photo_entry.pack()

CTkLabel(app, text = "Date Photo Captured" ).pack(pady = 6)
Date_photo_captured_entry = CTkEntry(app,width= 450)
Date_photo_captured_entry.pack()

CTkLabel(app,text="Date of submission").pack(pady=6)
Date_of_submission_entry = CTkEntry(app, width= 450)
Date_of_submission_entry.pack()


CTkLabel(app, text=" Photographer:").pack(pady= 6)
photographer_entry = CTkEntry(app, width= 450)
photographer_entry.pack()

submit_button = CTkButton(app,text="Submit Form")
submit_button.pack(pady=25)





app.mainloop()
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import numpy as np
from tkinter import messagebox
import os
import subprocess

def selection(event):
    if variable.get() == "New Material":
        nameLabel.pack()
        nameEntry.pack()
        speedLabel.pack()
        speedEntry.pack()
        powerLabel.pack()
        powerEntry.pack()
        confirmButton.pack_forget()  # Unpack the "Confirm" button
    else:
        nameLabel.pack_forget()
        nameEntry.pack_forget()
        speedLabel.pack_forget()
        speedEntry.pack_forget()
        powerLabel.pack_forget()
        powerEntry.pack_forget()
        confirmButton.pack()  # Pack the "Confirm" button


def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def start_spectroscopy_system():
    material_name = nameEntry.get()  # Get the material name from the Entry widget
    subprocess.run(["python", "SpectroscopySystemOpenCV.py", material_name])

def start_spectroscopy_system_existing():
    subprocess.run(["python", "SpectroscopySystemExistingMaterial.py"])

def confirm():
    exec(open("array1DComparison.py").read(), globals(), locals())

root = tk.Tk()
root.geometry("1000x500")
root.title("APALES")

# Create the "Laser Parameters" directory if it doesn't exist
laser_parameters_dir = "laser_parameters"
os.makedirs(laser_parameters_dir, exist_ok=True)

def save():
    # Get the material data
    name = nameEntry.get()
    speed = speedEntry.get()
    power = powerEntry.get()

    # Write the data to a file in the "Laser Parameters" directory
    with open(os.path.join(laser_parameters_dir, f'{name}_Parameters.txt'), 'w') as file:
        file.write(f'F{speed}\n')
        file.write(f'S{power}\n')

# Display "Saved!" in the same window
    savedLabel.config(text="Saved!", font=("Arial", 12))
    savedLabel.pack()

# Create the "Saved!" label
savedLabel = tk.Label(root, text="")

# Create the "Save" button
saveButton = tk.Button(root, text="Save", command=save)


def selection(event):
    if variable.get() == "New Material":
        nameLabel.pack()
        nameEntry.pack()
        speedLabel.pack()
        speedEntry.pack()
        powerLabel.pack()
        powerEntry.pack()
        saveButton.pack()  # Pack the "Save" button
        startLabel.pack()  # Pack the "Start Spectroscopy System" label
        startButton.pack()  # Pack the "Start" button
        startLabelExisting.pack_forget()  # Unpack the "Start Spectroscopy System Existing" label
        startButtonExisting.pack_forget()  # Unpack the "Start Existing" button
        confirmButton.pack_forget()  # Unpack the "Confirm" button
    else:
        nameLabel.pack_forget()
        nameEntry.pack_forget()
        speedLabel.pack_forget()
        speedEntry.pack_forget()
        powerLabel.pack_forget()
        powerEntry.pack_forget()
        saveButton.pack_forget()  # Unpack the "Save" button
        startLabel.pack_forget()  # Unpack the "Start Spectroscopy System" label
        startButton.pack_forget()  # Unpack the "Start" button
        startLabelExisting.pack()  # Pack the "Start Spectroscopy System Existing" label
        startButtonExisting.pack()  # Pack the "Start Existing" button
        confirmButton.pack()  # Pack the "Confirm" button

heading = tk.Label(root, text="APALES Material Selection", font=("Arial", 32))
heading.pack()

heading = tk.Label(root, text="Please select an option:", font=("Arial", 16))
heading.pack()

image = Image.open("APALES Logo.png")  # replace with your logo file
image = image.resize((100, 100), Image.BICUBIC)
logo = ImageTk.PhotoImage(image)
logoLabel = tk.Label(root, image=logo)
logoLabel.pack()

variable = tk.StringVar(root)
variable.set("Pick an option:")  # default value

options = ["New Material", "Existing Material"]
dropdown = tk.OptionMenu(root, variable, *options, command=selection)
dropdown.config(bg='lightblue', fg='black', activebackground='blue', activeforeground='white')
dropdown.pack()

nameLabel = tk.Label(root, text="Name of the material:")
nameEntry = tk.Entry(root)
speedLabel = tk.Label(root, text="Laser speed (mm/min):")
speedEntry = tk.Entry(root)
powerLabel = tk.Label(root, text="Laser power (0-1000):")
powerEntry = tk.Entry(root)


# Create the "Start" button
startButton = tk.Button(root, text="Start", command=start_spectroscopy_system)

# Create a label for the button
startLabel = tk.Label(root, text="Start Spectroscopy System", font=("Arial", 12))

confirmButton = tk.Button(root, text="Confirm", command=confirm)

# Create the "Start Existing" button
startButtonExisting = tk.Button(root, text="Start Existing", command=start_spectroscopy_system_existing)

# Create a label for the button
startLabelExisting = tk.Label(root, text="Start Spectroscopy System Existing", font=("Arial", 12))

root.mainloop()
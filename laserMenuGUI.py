# Senior Design 2 Spring 2024 Group 5: APALES
# Authors: Kavinaash Jesurajah, Nolan McGinley
# laserMenuGUI.py

""" 
Description: Python module to do ...
UPDATE THIS COMMENT, KAV
"""



import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import subprocess
import numpy as np

import os
import queue
import threading
import time

start_time = 0

def selection(event):
    if variable.get() == "New Material":
        nameLabel.pack()
        nameEntry.pack()
        speedLabel.pack()
        speedEntry.pack()
        pwmLabel.pack()
        pwmEntry.pack()
        confirmButton.pack_forget()  # Unpack the "Confirm" button
    else:
        nameLabel.pack_forget()
        nameEntry.pack_forget()
        speedLabel.pack_forget()
        speedEntry.pack_forget()
        pwmLabel.pack_forget()
        pwmEntry.pack_forget()
        confirmButton.pack()  # Pack the "Confirm" button


def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def start_spectroscopy_system():
    material_name = nameEntry.get()  # Get the material name from the Entry widget
    subprocess.run(["python", "SpectroscopySystemOpenCV.py", material_name])

def start_spectroscopy_system_existing():
    global start_time
    start_time = time.time()
    subprocess.run(["python", "SpectroscopySystemExistingMaterial.py"])
    print("--- %s seconds ---" % (time.time() - start_time))

def confirm():
    # Run the array1DComparison.py script and capture its output
    process = subprocess.Popen(["python", "array1DComparison.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)

    # Function to read the output line by line and display it in the output box
    def read_output():
        for line in iter(process.stdout.readline, ''):
            output_box.insert(tk.END, line)
            output_box.see(tk.END)

    # Start a new thread to read the output
    threading.Thread(target=read_output).start()
    
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
    pwm = pwmEntry.get()

    # Write the data to a file in the "Laser Parameters" directory
    with open(os.path.join(laser_parameters_dir, f'{name}_Parameters.txt'), 'w') as file:
        file.write(f'F{speed}\n')
        file.write(f'S{int(float(pwm)*10)}\n')

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
        pwmLabel.pack()
        pwmEntry.pack()
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
        pwmLabel.pack_forget()
        pwmEntry.pack_forget()
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
pwmLabel = tk.Label(root, text="S-Max (G-code parameter):")
pwmEntry = tk.Entry(root)


# Create the "Start" button
startButton = tk.Button(root, text="Start", command=start_spectroscopy_system)

# Create a label for the button
startLabel = tk.Label(root, text="Start Spectroscopy System", font=("Arial", 12))

confirmButton = tk.Button(root, text="Confirm", command=confirm)

# Create the "Start Existing" button
startButtonExisting = tk.Button(root, text="Start Existing", command=start_spectroscopy_system_existing)

# Create a label for the button
startLabelExisting = tk.Label(root, text="Start Spectroscopy System Existing", font=("Arial", 12))
# Variable to keep track of the laser pulse state
laser_pulse_on = False

# Directory for the laser pulse files
laser_pulse_dir = "Laser Pulse"
os.makedirs(laser_pulse_dir, exist_ok=True)

# Function to handle the laser pulse button click
def toggle_laser_pulse():
    global laser_pulse_on

    # Toggle the laser pulse state
    laser_pulse_on = not laser_pulse_on

    # Update the laser pulse button text
    if laser_pulse_on:
        laser_pulse_button.config(text="Laser Pulse: ON")
        # Add your code to turn on the laser pulse here
    else:
        laser_pulse_button.config(text="Laser Pulse: OFF")
        # Add your code to turn off the laser pulse here

    # Write the current state of the laser pulse to a file
    with open(os.path.join(laser_pulse_dir, 'LaserPulseState.txt'), 'w') as file:
        file.write("ON" if laser_pulse_on else "OFF")

# Create a Button widget for the laser pulse
laser_pulse_button = tk.Button(root, text="Laser Pulse: OFF", command=toggle_laser_pulse)
laser_pulse_button.pack()

# Create a new window
root = tk.Tk()

# Create a ScrolledText widget for displaying the output
output_box = scrolledtext.ScrolledText(root, width=50, height=10)
output_box.pack()

# Create an Entry widget for user input
input_box = tk.Entry(root)
input_box.pack()

# Create a queue for user input
input_queue = queue.Queue()

# Function to handle the user's input
def handle_input(event=None):
    # Get the user's input
    user_input = input_box.get()

    # Clear the input box
    input_box.delete(0, tk.END)

    # Add the user's input to the queue
    input_queue.put(user_input + '\n')

    # Handle the user's input
    if user_input.lower() == "y":
        output_box.insert(tk.END, "Proceeding to the engraving process.\n")
        # Add your engraving process code here
    elif user_input.lower() == "n":
        output_box.insert(tk.END, "Please input the data manually as a 'New Material' in the GUI.\n")
        # Add your code to handle this situation here
    else:
        output_box.insert(tk.END, "Invalid input. Please enter 'Yes' or 'No'.\n")

    # Scroll the output box to the end
    output_box.see(tk.END)

# Bind the Return key to the handle_input function
root.bind("<Return>", handle_input)

# Create a "Submit" button
submit_button = tk.Button(root, text="Submit", command=handle_input)
submit_button.pack()

def confirm():
    # Run the array1DComparison.py script and capture its output
    process = subprocess.Popen(["python", "array1DComparison.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)

    # Function to write the user's input to the process
    def write_input():
        while True:
            # Get the user's input from the queue
            user_input = input_queue.get()

            # Write the user's input to the process
            process.stdin.write(user_input)
            process.stdin.flush()

    # Start a new thread to write the user's input
    threading.Thread(target=write_input).start()


root.mainloop()
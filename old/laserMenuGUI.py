# Senior Design 2 Spring 2024 Group 5: APALES
# Authors: Kavinaash Jesurajah, Nolan McGinley
# laserMenuGUI.py

""" 
Description: GUI for the user to select a material and its parameters.
"""


import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import subprocess
import numpy as np
import tkinter.messagebox as messagebox
import os
import queue
import threading
import time
import serial.tools.list_ports



def selection(event): # Function to select the material
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
        startComparison.pack_forget()  # Unpack the "Comparison" label
        confirmButton.pack_forget()  # Unpack the "Confirm" button
        gcode_dropdown_label.pack_forget() # Unpack the g-code dropdown label
        gcode_file_dropdown.pack_forget() # Unpack the g-code file dropdown menu
        run_file_button.pack_forget() # Unpack the "Run File" button

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
        startLabelExisting.pack()  # Pack the "Comparison" label
        startButtonExisting.pack()  # Pack the "Start Existing" button
        startComparison.pack()  # Pack the Comparison" label
        confirmButton.pack()  # Pack the "Confirm" button
        gcode_dropdown_label.pack() # Pack the g-code dropdown label
        gcode_file_dropdown.pack() # Pack the g-code file dropdown menu
        run_file_button.pack() # Pack the "Run File" button


#def euclidean_distance(a, b):
 #   return np.sqrt(np.sum((a - b) ** 2))

def start_spectroscopy_system():
    material_name = nameEntry.get()  # Get the material name from the Entry widget
    subprocess.run(["python", "SpectroscopySystemOpenCV.py", material_name])
    # Display a popup message when the script finishes running
    messagebox.showinfo("Success", "Image area sliced, converted to grayscale, and 1D array written to text file successfully!")

def start_spectroscopy_system_existing():

    start_time = time.time()
    subprocess.run(["python", "SpectroscopySystemExistingMaterial.py"])
    time_elapsed = f'{(time.time() - start_time):.3f}'
    
    messagebox.showinfo(f"Success", "Image area sliced, converted to grayscale, and 1D array written to text file successfully!\n\n"
                         + "Time Elapsed: " + time_elapsed + " seconds" )
    

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
    
root = tk.Tk() # Create the main window
root.geometry("1000x500") # Size of the window
root.title("APALES") # Title of the window

# Create a StringVar for the COM port dropdown
com_port_var = tk.StringVar(root)

# Get a list of available COM ports
com_ports = [comport.device for comport in serial.tools.list_ports.comports()]

# If no COM ports are available, set the default value to "No COM ports"
if not com_ports:
    com_ports = ["No COM ports"]
        
    # Set the default value to the first COM port
    com_port_var.set(com_ports[0])

# Create the COM port dropdown menu
com_port_dropdown = tk.OptionMenu(root, com_port_var, *com_ports)
com_port_dropdown.pack(side='right')



# Create the "Laser Parameters" directory if it doesn't exist
laser_parameters_dir = "laser_parameters"
os.makedirs(laser_parameters_dir, exist_ok=True)

def save(): # Function to save the material data
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

confirmButton = tk.Button(root, text="Compare", command=confirm)

# Create a StringVar to hold the selected g-code file
gcode_file_var = tk.StringVar()

# Create the g-code file dropdown menu
gcode_file_dropdown = tk.OptionMenu(root, gcode_file_var, [])
gcode_file_dropdown.pack()

# Specify the relative path to the "gcode_examples" folder
gcode_examples = os.path.relpath("gcode_examples")

# Function to populate the g-code files list and update the OptionMenu widget
def update_gcode_files():
    # Get a list of all .gc files in the "gcode_examples" folder
    gcode_files = [f for f in os.listdir(gcode_examples) if f.endswith(".nc")]

    # Set the default value to the first g-code file
    if gcode_files:
        gcode_file_var.set(gcode_files[0])
    else:
        gcode_files = ["No g-code files"]
        gcode_file_var.set(gcode_files[0])

    # Update the OptionMenu widget
    gcode_file_dropdown["menu"].delete(0, "end")
    for gcode_file in gcode_files:
        gcode_file_dropdown["menu"].add_command(label=gcode_file, command=tk._setit(gcode_file_var, gcode_file))

# Function to run the selected g-code file
def run_file():
    selected_file = gcode_file_var.get()
    if selected_file == "No g-code files":
        print("No g-code file selected")
    else:
        # Run the selected g-code file
        print(f"Running {selected_file}")
        # Add your code to run the g-code file here

# Create the "Run File" button
run_file_button = tk.Button(root, text="Run File", command=run_file)
run_file_button.pack()

# Call the update_gcode_files function once the GUI is idle
root.after_idle(update_gcode_files)

# Create the "Start Existing" button
startButtonExisting = tk.Button(root, text="Start Existing", command=start_spectroscopy_system_existing)

# Create a label for the confirm button
startComparison = tk.Label(root, text="Start Comparison", font=("Arial", 12))

# Create a label for the g-code dropdown
gcode_dropdown_label = tk.Label(root, text="G-Code File Search", font=("Arial", 12))

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

"""
FOR USER INPUT AREA WINDOW IN GUI (TERMINAL-LIKE INTERFACE)
"""
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
    if user_input.lower() == "Yes" or "yes":
        output_box.insert(tk.END, "Proceeding to the engraving process.\n")
        # Add your engraving process code here
    elif user_input.lower() == "No" or "no":
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
submit_button.pack() # Pack the "Submit" button

def confirmUserInput():
    # Run the array1DComparison.py script and capture its output
    process = subprocess.Popen(["python", "array1DComparison.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)

    # Function to write the user's input to the process
    def write_input():
        while True:
            # Get the user's input from the queue
            user_input = input_queue.get()

            # Write the user's input to the process
            process.stdin.write(user_input) # Write the user's input to the process
            process.stdin.flush() # Flush the input buffer

    # Start a new thread to write the user's input
    threading.Thread(target=write_input).start()


root.mainloop()
# Senior Design 2 Spring 2024 Group 5: APALES
# Authors: Kavinaash Jesurajah, Aly Megahed, Nolan McGinley
# menu.py

""" 
Description: GUI for the user to select a material and its parameters.
"""


import tkinter as tk
from tkinter import scrolledtext, ttk
from PIL import Image, ImageTk
import subprocess
import numpy as np
import tkinter.messagebox as messagebox
import os
import queue
import threading
import time
import serial.tools.list_ports

import spectroscopy
import gcodeParameter
import gcodeSender

# Contains base gcode files with S-MAX set to 1000
# Parameteriser scales this value down and updates F Parameters (feed rate)
gcode_folder = "gcode_examples"

# Contians laser parameters for each material added
laser_parameters_folder = "laser_parameters"
os.makedirs(laser_parameters_folder, exist_ok=True)

# Show or hide widgets based on option selection
def option_select():

    option = radio_var.get()

    if option == "New Material":
        info_frame.grid(row=2, column=1)
        info.config(text = "Place the material on the bed.\nInput material and start spectroscopy system.")
        info.grid(row=2, column=1)
        nameLabel.grid(row = 3, column= 1)
        nameEntry.grid(row=4, column =1)
        speedLabel.grid(row=5, column =1)
        speedEntry.grid(row = 6, column= 1)
        pwmLabel.grid(row = 7, column= 1)
        pwmEntry.grid(row = 8, column= 1)
        saveButton.grid(row=9, column =1, pady=10)  
        startButton.grid_forget()
        
        
    else:
        info_frame.grid(row=2, column=1)
        info.config(text = "Place the material on the bed.\nStart spectroscopy and classification of material.")
        info.grid()
        startButton.grid(row = 3, column= 1, pady=10)         
        nameLabel.grid_forget()
        nameEntry.grid_forget()
        speedLabel.grid_forget()
        speedEntry.grid_forget()
        pwmLabel.grid_forget()
        pwmEntry.grid_forget()
        saveButton.grid_forget() 
        


def new_material():

    # Get  values from textboxes
    material_name = nameEntry.get()  
    speed = speedEntry.get()
    pwm = pwmEntry.get()

    start_time = time.time()
    spectroscopy.new_spectroscopy(material_name)
    end_time = (time.time() - start_time)

    # Write the data to a file in the "Laser Parameters" directory
    with open(os.path.join(laser_parameters_folder, f'{material_name}_parameters.txt'), 'w') as file:
        file.write(f'F{speed}\n')
        file.write(f'S{pwm}')

    # Display a popup message with time elapsed
    messagebox.showinfo(f"Success! Time Elapsed: {(end_time):.3f} seconds.", f"New material array and parameters saved:\n{material_name}")


def existing_material():

    start_time = time.time()
    classified_material = spectroscopy.existing_spectroscopy()
    end_time = (time.time() - start_time)
    # Display a popup message with time elapsed
    
    question = messagebox.askquestion(f"Success! Time Elapsed: {(end_time):.3f} seconds.", f"Material captured and classified! \nClassified material: {classified_material} \n Is this correct?")

    # Get currently selected COM
    current_com =  com_port_var.get()
    if question == 'yes':
        current_gcode = gcode_file_var.get()
        parameteriser = gcodeParameter.Parameteriser(param_file=f'{classified_material}_parameters.txt', gcode_file=current_gcode)
        parameteriser.read_parameter()
        parameteriser.update_parameter()
        messagebox.showinfo("Ready to engrave.", f"{current_gcode} is ready to be engraved on {classified_material}\nClick ok to begin job")
       
        if current_com == "No COM":
            messagebox.showerror("No available COM Ports!!!", "Please connect laser CNC controller.")
            return

        sender = gcodeSender.Sender(port=current_com)
        sender.connect()
        sender.send_job()
        print(current_com)

    else:
        messagebox.showinfo("Sorry about that.", "Please select 'New Material' and enter the information.")

# Function to populate the g-code files list and update the OptionMenu widget
def update_gcode_files(folder):

    # Specify the relative path to the "gcode_examples" folder
    gcode_examples = os.path.relpath(folder)
    # Get a list of all .nc files in the "gcode_examples" folder
    gcode_files = [f for f in os.listdir(gcode_examples) if f.endswith(".nc")]

    # Set the default value to the first g-code file
    if gcode_files:
        gcode_file_var.set(gcode_files[0])
    else:
        gcode_files = ["No files found"]
        gcode_file_var.set(gcode_files[0])

    # Update the OptionMenu widget
    gcode_file_dropdown["menu"].delete(0, "end")
    for gcode_file in gcode_files:
        gcode_file_dropdown["menu"].add_command(label=gcode_file, command=tk._setit(gcode_file_var, gcode_file))

def update_preview():
    print('something')

# Main Tkinter window
app = tk.Tk()  
app.geometry("800x500")
app.title("APALES")
app.resizable(width=False, height=False)

# Top frame with lavender background
topFrame = tk.Frame(app, bg='lavender', width=800, height=100, relief="raised")
topFrame.grid(row=0, column=0, columnspan=3, sticky='w')

# APALES heading and option select subheading
heading = tk.Label(app, text="APALES App", font=("Arial", 22), bg='lavender')
heading.grid(row=0, column=1, pady= 10, sticky= 'nswe')

subheading = tk.Label(app, text="Please select an option", font=("Arial", 14), bg= 'lavender') 
subheading.grid(row=0,column=1, sticky= 's')

# APALES LOGO
logo_image = Image.open("APALES Logo.png")  # replace with your logo file
logo_image = logo_image.resize((100, 100), Image.BICUBIC)
logo = ImageTk.PhotoImage(logo_image)
logoLabel = tk.Label(app, image=logo, bg='lavender')
logoLabel.grid(row=0, column=0, sticky= 'w', padx=15)



# Radio buttons, existing material or new material
radio_var = tk.StringVar()
radio_var.set('')
radio_frame = tk.Frame(app)
radio_frame.grid(row=1,column=1)

radio_button1 = tk.Radiobutton(radio_frame, text="New Material", variable=radio_var, value="New Material", command=option_select)
radio_button2 = tk.Radiobutton(radio_frame, text="Existing Material", variable=radio_var, value="Existing Material", command=option_select)
# radio_button3 = tk.Radiobutton(radio_frame, text="Manual User Input", variable=radio_var, value="", command=option_select)

radio_button1.grid(sticky="w")
radio_button2.grid(stick="e")

radio_var.set(' ')

# Info widgets to explain either option (new or existing)
info_frame = tk.Frame(app, width=200, height=100, bg="")
info = tk.Label(info_frame, text="", font=("Arial", 10), bg= 'lightblue')

# New Material widgets
nameLabel = tk.Label(app, text="New Material Name:")
nameEntry = tk.Entry(app)
speedLabel = tk.Label(app, text="Feed Rate (mm/min):")
speedEntry = tk.Entry(app)
pwmLabel = tk.Label(app, text="S-Max (G-code parameter):")
pwmEntry = tk.Entry(app)
saveButton = tk.Button(app, text="Save", font=("Arial",14), bg= "lightyellow", command=new_material)

# Existing material widgets
startButton = tk.Button(app, text="Start", font=("Arial",14), bg= "lightgreen", command=existing_material)


# Create a StringVar for the COM port dropdown
com_port_var = tk.StringVar(app)

# Get a list of available COM ports
com_ports = [comport.device for comport in serial.tools.list_ports.comports()]

# If no COM ports are available, set the default value to "No COM ports"
if not com_ports:
    com_ports = ["No COM"]
        
    # Set the default value to the first COM port
    com_port_var.set(com_ports[0])


com_frame = tk.Frame(app, bg='lavender')
com_frame.grid(row=0, column=2,sticky= 'ne', padx=5,pady=5)

# Create the COM port dropdown menu
com_port_dropdown = tk.OptionMenu(com_frame, com_port_var, *com_ports)
com_port_dropdown.config(bg='lightblue', fg='black', activebackground='blue', activeforeground='white')

com_port_label = tk.Label(com_frame, text="COM Port:", font=("Arial", 12), bg='lavender')
com_port_label.grid(row=0, sticky='nw')
com_port_dropdown.grid(row=1, sticky= 'ne')


# Create a StringVar to hold the selected g-code file
gcode_file_var = tk.StringVar()

# Create the g-code file dropdown menu
gcode_label = tk.Label(app, text="Select Example:", font=("Arial", 12))
gcode_label.grid(row=1,column=0, sticky= 'sw', padx=15)

gcode_file_dropdown = tk.OptionMenu(app, gcode_file_var, [], command=update_preview)
gcode_file_dropdown.config(bg='lightblue', fg='black', activebackground='blue', activeforeground='white')
gcode_file_dropdown.grid(row=2, column=0, sticky= 'nw', padx=15)

# Image preview
# APALES LOGO
preview_image = Image.open("gcode_examples\star.png")  # replace with your logo file
preview_image = preview_image.resize((150, 150), Image.BICUBIC)
preview = ImageTk.PhotoImage(preview_image)
previewFrame = tk.Frame(width= 150, height = 150, padx=15, pady=10, relief='sunken')
previewFrame.grid(row=3, column=0, rowspan=10, sticky='w')

previewLabel = tk.Label(previewFrame, image=preview)
previewLabel.grid(sticky='nw')



# Call the update_gcode_files function once the GUI is idle
app.after_idle(update_gcode_files, gcode_folder)

app.mainloop()


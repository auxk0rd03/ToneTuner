import tkinter as tk
from tkinter import StringVar, filedialog
from pygame import mixer
import os

#TODO MAke play,pause and select song menu show up on the pop up-----Status-[COMPLETE]
#TODO IN ORDER TO RUN THIS APP YOU NEED PYGAME INSTALLED
#you can initalize the pop up by just pressing the stop button 

"""          !!!!!!!!!!!ISSUES!!!!!!!!!!!!!!!!!!!!!!!!!!
#Whenever you press stop within the popup, it will create another pop-up from the popup||||| Status-[In-Progress]

"""

# Initialize Pygame mixer
mixer.init()

# Dictionary to store MP3 files format--> (Name of Song: local file location)
mp3_files = {
    "Bad_at_coding.mp3": "Songs/Bad_at_coding.mp3",
    "Shitty_programmer.mp3": "Songs/Shitty_programmer.mp3"
}

# Function to play the selected music file
def play_music():
    selected_file = mp3_files[file_var.get()]  # Get the file path from mp3_files dictionary
    mixer.music.load(selected_file)  # Load the selected file
    mixer.music.play()
    check_if_finished()  # Start checking if the song has finished

def stop_music():
    mixer.music.stop()

# Function to add a new MP3 file
def add_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        file_name = os.path.basename(file_path)  # Get just the file name from the path
        mp3_files[file_name] = file_path         # Add to dictionary with file name as key
        file_var.set(file_name)                  # Set as current selection

        # Update the dropdown menu with the new file
        dropdown["menu"].add_command(label=file_name, command=tk._setit(file_var, file_name))

# Function to check if the song has finished
def check_if_finished():
    if not mixer.music.get_busy():  # If the music is not playing
        open_popup()  # Show the popup window
    else:
        win.after(1000, check_if_finished)  # Check again in 1 second

# Function to open the popup window
def open_popup():
    popup = tk.Toplevel(win)
    popup.title("Song Finished")
    popup.geometry("500x250")
    popup.config(background="wheat2")

    label = tk.Label(popup, text="song ended")
    label.pack(pady=20)
    #BUTTONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!TODO:May be buggy(Update...it is buggy :] )
    # Play button
    play_button = tk.Button(popup, text="Play", command=play_music)
    play_button.pack(pady=10)
    play_button.config(background="SeaGreen1")
    #Stop button!!!!!!!!!!!!!!!!
    stop_button = tk.Button(popup, text="Stop", command=stop_music)
    stop_button.pack(pady=10)
    stop_button.config(background="firebrick1")
    # Add File button!!!!!!!!!!!!!!!!
    add_button = tk.Button(popup, text="Add MP3", command=add_file)
    add_button.pack(pady=10)
    add_button.config(background="cyan2")
    # Dropdown menu for selecting MP3 files!!!!!!!!!!!!!!!!
    file_var = StringVar(win)
    file_var.set("Select a file")  # Default value for the dropdown

    # Dropdown menu for file selection
    dropdown = tk.OptionMenu(popup, file_var, *mp3_files.keys())
    dropdown.pack(pady=10)
    dropdown.config(background="coral")


    #close button that closes the application
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)

# Create the main Tkinter window
win = tk.Tk()
win.title("Tone Tuner")
win.geometry("750x400")
win.config(background="gray23")

# Dropdown menu for selecting MP3 files
file_var = StringVar(win)
file_var.set("Select a file")  # Default value for the dropdown

# Dropdown menu for file selection
dropdown = tk.OptionMenu(win, file_var, *mp3_files.keys())
dropdown.pack(pady=10)
dropdown.config(background="coral")

# Play button
play_button = tk.Button(win, text="Play", command=play_music)
play_button.pack(pady=10)
play_button.config(background="SeaGreen1")

# Stop button
stop_button = tk.Button(win, text="Stop", command=stop_music)
stop_button.pack(pady=10)
stop_button.config(background="firebrick1")

# Add File button
add_button = tk.Button(win, text="Add MP3", command=add_file)
add_button.pack(pady=10)
add_button.config(background="cyan2")

# Run the Tkinter main loop
win.mainloop()

